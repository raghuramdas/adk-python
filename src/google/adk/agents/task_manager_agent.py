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

from typing import List, Dict, Any
from google.adk.agents import Agent

# In-memory task storage for simplicity
_tasks: List[Dict[str, Any]] = []
_next_task_id = 1

def add_task(task_description: str) -> str:
  """Adds a new task to the task list.

  Args:
    task_description: The description of the task.

  Returns:
    A confirmation message with the new task's ID.
  """
  global _tasks, _next_task_id
  task = {"id": _next_task_id, "description": task_description, "completed": False}
  _tasks.append(task)
  _next_task_id += 1
  return f"Task added with ID: {task['id']}. Description: {task_description}"

def list_tasks(filter_status: str = "all") -> List[Dict[str, Any]]:
  """Lists all tasks, or filters by status.

  Args:
    filter_status: "all", "pending", or "completed".

  Returns:
    A list of task dictionaries.
  """
  if filter_status == "pending":
    return [task for task in _tasks if not task["completed"]]
  elif filter_status == "completed":
    return [task for task in _tasks if task["completed"]]
  return _tasks

def mark_task_complete(task_id: int) -> str:
  """Marks a specific task as complete.

  Args:
    task_id: The ID of the task to mark as complete.

  Returns:
    A confirmation message or an error if the task is not found.
  """
  global _tasks
  for task in _tasks:
    if task["id"] == task_id:
      if task["completed"]:
        return f"Task {task_id} was already marked as complete."
      task["completed"] = True
      return f"Task {task_id} marked as complete."
  return f"Error: Task with ID {task_id} not found."

def clear_all_tasks() -> str:
  """Clears all tasks from the list. For testing or reset purposes."""
  global _tasks, _next_task_id
  _tasks = []
  _next_task_id = 1
  return "All tasks have been cleared."

class TaskManagerAgent(Agent):
  """An agent specialized in managing tasks."""

  def __init__(self, **kwargs):
    super().__init__(
        name="task_manager",
        description="Manages tasks, including adding, listing, and marking tasks as complete.",
        instruction="""
          You are a task management assistant.
          Use the available tools to manage the user's tasks.
          - To add a task, use the `add_task` tool with the task description.
          - To list tasks, use the `list_tasks` tool. You can filter by "all", "pending", or "completed".
          - To mark a task as complete, use the `mark_task_complete` tool with the task ID.
          - You can also clear all tasks using `clear_all_tasks` if specifically requested for a reset.
          Always confirm the action taken or provide the requested list of tasks.
        """,
        tools=[add_task, list_tasks, mark_task_complete, clear_all_tasks],
        model="gemini-1.5-flash", # Or any suitable model
        **kwargs
    )
