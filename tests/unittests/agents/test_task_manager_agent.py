# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import unittest
import asyncio

# Adjust the import path based on where the TaskManagerAgent and its tools are located
# Assuming they are accessible via google.adk.agents.task_manager_agent
from google.adk.agents.task_manager_agent import (
    add_task,
    list_tasks,
    mark_task_complete,
    clear_all_tasks,
    TaskManagerAgent,
    _tasks as task_manager_tasks,  # For direct inspection/reset
    _next_task_id as task_manager_next_id, # For reset
)
from google.adk.run_agent_locally import run_agent_locally
from google.genai import types

class TestTaskManagerTools(unittest.TestCase):
    """Tests for the standalone tool functions of TaskManagerAgent."""

    def setUp(self):
        # Reset tasks before each test
        clear_all_tasks()

    def tearDown(self):
        # Clean up tasks after each test
        clear_all_tasks()

    def test_add_task(self):
        result = add_task("Test task 1")
        self.assertIn("Task added with ID: 1", result)
        self.assertEqual(len(task_manager_tasks), 1)
        self.assertEqual(task_manager_tasks[0]["description"], "Test task 1")
        self.assertFalse(task_manager_tasks[0]["completed"])

        result = add_task("Test task 2")
        self.assertIn("Task added with ID: 2", result)
        self.assertEqual(len(task_manager_tasks), 2)

    def test_list_tasks(self):
        add_task("Task A")
        add_task("Task B")
        
        all_tasks = list_tasks()
        self.assertEqual(len(all_tasks), 2)
        self.assertEqual(all_tasks[0]["description"], "Task A")
        self.assertEqual(all_tasks[1]["description"], "Task B")

        pending_tasks = list_tasks(filter_status="pending")
        self.assertEqual(len(pending_tasks), 2)

        completed_tasks = list_tasks(filter_status="completed")
        self.assertEqual(len(completed_tasks), 0)

    def test_mark_task_complete(self):
        add_task("Task C") # ID will be 1
        result = mark_task_complete(1)
        self.assertEqual(result, "Task 1 marked as complete.")
        self.assertTrue(task_manager_tasks[0]["completed"])

        # Test marking already completed task
        result = mark_task_complete(1)
        self.assertEqual(result, "Task 1 was already marked as complete.")

        # Test marking non-existent task
        result = mark_task_complete(99)
        self.assertEqual(result, "Error: Task with ID 99 not found.")
        
    def test_list_tasks_with_completed(self):
        add_task("Task D") # ID 1
        add_task("Task E") # ID 2
        mark_task_complete(1)

        all_tasks = list_tasks()
        self.assertEqual(len(all_tasks), 2)
        
        pending_tasks = list_tasks(filter_status="pending")
        self.assertEqual(len(pending_tasks), 1)
        self.assertEqual(pending_tasks[0]["description"], "Task E")

        completed_tasks = list_tasks(filter_status="completed")
        self.assertEqual(len(completed_tasks), 1)
        self.assertEqual(completed_tasks[0]["description"], "Task D")

    def test_clear_all_tasks(self):
        add_task("Task F")
        add_task("Task G")
        self.assertEqual(len(task_manager_tasks), 2)
        result = clear_all_tasks()
        self.assertEqual(result, "All tasks have been cleared.")
        self.assertEqual(len(task_manager_tasks), 0)
        # Check if next_task_id is reset (implementation detail, but good to check)
        # This requires accessing the global _next_task_id from the module,
        # which we've imported as task_manager_next_id for this purpose if needed.
        # For this test, ensuring task_manager_tasks is empty is the primary check.
        # If we add a new task, its ID should be 1.
        add_task("New task after clear")
        self.assertEqual(task_manager_tasks[0]["id"], 1)


class TestTaskManagerAgent(unittest.IsolatedAsyncioTestCase):
    """Tests for the TaskManagerAgent itself, using run_agent_locally."""

    async def asyncSetUp(self):
        # Reset tasks before each agent test
        clear_all_tasks()
        self.agent = TaskManagerAgent()

    async def asyncTearDown(self):
        clear_all_tasks()

    async def run_agent_query(self, query: str) -> str:
        """Helper to run a query against the agent and get the text response."""
        response_text = ""
        async for event in run_agent_locally(
            agent=self.agent, user_input=query, stream_events=False
        ):
            if event.content and event.content.parts:
                response_text += event.content.parts[0].text
        return response_text.strip()

    async def test_agent_add_task(self):
        response = await self.run_agent_query("Please add a task: 'Buy milk'")
        self.assertIn("Task added with ID: 1", response)
        self.assertIn("Buy milk", response)
        self.assertEqual(len(task_manager_tasks), 1)
        self.assertEqual(task_manager_tasks[0]["description"], "Buy milk")

    async def test_agent_list_tasks(self):
        await self.run_agent_query("Add task: 'Walk the dog'")
        await self.run_agent_query("Add task: 'Water plants'")
        
        response = await self.run_agent_query("Show me my tasks")
        # The LLM will format the list. We check for key elements.
        self.assertIn("Walk the dog", response)
        self.assertIn("Water plants", response)
        self.assertIn("ID: 1", response) # Assuming LLM includes IDs
        self.assertIn("ID: 2", response)

    async def test_agent_mark_task_complete(self):
        await self.run_agent_query("Add task: 'Charge phone'") # ID 1
        
        response = await self.run_agent_query("Mark task 1 as complete")
        self.assertIn("Task 1 marked as complete", response)
        self.assertTrue(task_manager_tasks[0]["completed"])

        response = await self.run_agent_query("What are my completed tasks?")
        self.assertIn("Charge phone", response)
        self.assertIn("ID: 1", response)
        
        response = await self.run_agent_query("What are my pending tasks?")
        self.assertNotIn("Charge phone", response) # Should not be in pending

    async def test_agent_list_empty(self):
        response = await self.run_agent_query("List my tasks")
        # Exact response depends on LLM, but should indicate no tasks
        self.assertTrue(
            "no tasks" in response.lower() or 
            "don't have any tasks" in response.lower() or
            "task list is empty" in response.lower() or
            "[]" in response # If LLM just returns empty list string
        )

    async def test_agent_mark_non_existent_task(self):
        response = await self.run_agent_query("Mark task 99 as done")
        self.assertIn("Task with ID 99 not found", response)

if __name__ == "__main__":
    unittest.main()
