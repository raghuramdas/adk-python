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

from google.adk.agents import Agent
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from .task_manager_agent import TaskManagerAgent # Added import

class PersonalAssistantAgent(Agent):
  """A personal assistant agent that helps users with productivity tasks."""

  def __init__(self, **kwargs):
    # Pop 'sub_agents' from kwargs to handle it separately.
    sub_agents = kwargs.pop('sub_agents', [])
    
    # Check if a TaskManagerAgent instance already exists.
    # This avoids adding it multiple times if sub_agents are passed in kwargs.
    if not any(isinstance(agent, TaskManagerAgent) for agent in sub_agents):
        sub_agents.append(TaskManagerAgent()) # Add TaskManagerAgent if not present

    super().__init__(
        name=kwargs.pop('name', "personal_assistant"),
        description=kwargs.pop('description', "A helpful AI personal assistant that can delegate task management."),
        instruction=kwargs.pop('instruction', """
You are a helpful personal assistant.
You have a sub-agent called 'task_manager' that is specialized in managing tasks.
If the user asks you to add a task, list tasks, or mark a task as complete, delegate this to the 'task_manager' agent.
For other requests, like general conversation, handle them yourself.
Be friendly and proactive.
        """),
        model=kwargs.pop('model', "gemini-1.5-flash"),
        sub_agents=sub_agents, # Pass the potentially modified sub_agents list
        **kwargs # Pass any remaining kwargs to the parent
    )
    
    # Initialize memory service for the root agent if it's not already set.
    # This ensures a single memory service instance for the entire agent hierarchy if this is the root.
    if hasattr(self.root_agent, 'memory_service'):
      if self.root_agent.memory_service is None:
        self.root_agent.memory_service = InMemoryMemoryService()
    else:
      # If root_agent doesn't have memory_service attribute at all (e.g., if it's a very basic custom root)
      # or if this PersonalAssistantAgent IS the root_agent.
      setattr(self.root_agent, 'memory_service', InMemoryMemoryService())
