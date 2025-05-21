# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may
# obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio

from google.adk.agents import PersonalAssistantAgent
from google.adk.run_agent_locally import run_agent_locally
from google.genai import types

async def main():
  """Runs the personal assistant agent with some sample queries."""
  print("Initializing Personal Assistant Agent...")
  assistant_agent = PersonalAssistantAgent(
      # Using default name, description, model, and instructions
      # as defined in PersonalAssistantAgent and TaskManagerAgent
  )

  print("\n--- Running Agent with Sample Interactions ---")
  print("User: Hello there!")
  async for event in run_agent_locally(
      agent=assistant_agent,
      user_input="Hello there!",
      stream_events=False # Get final response directly for simplicity here
  ):
    if event.content:
      print(f"Assistant: {event.content.parts[0].text}")

  print("\nUser: Can you add a task to buy groceries?")
  async for event in run_agent_locally(
      agent=assistant_agent,
      user_input="Can you add a task to buy groceries?",
      stream_events=False
  ):
    if event.content:
      print(f"Assistant: {event.content.parts[0].text}")
  
  # It's good practice to see the task ID from the previous response.
  # For this example, we'll assume the LLM correctly extracts it or user provides it.
  # If the LLM response includes the ID, we could parse it. Here, we'll just list.

  print("\nUser: What are my pending tasks?")
  async for event in run_agent_locally(
      agent=assistant_agent,
      user_input="What are my pending tasks?",
      stream_events=False
  ):
    if event.content:
      # The list_tasks tool returns a list of dicts.
      # The TaskManagerAgent's LLM should format this into a readable string.
      print(f"Assistant: {event.content.parts[0].text}")

  print("\nUser: Add another task: 'Call John at 5 PM'.")
  async for event in run_agent_locally(
      agent=assistant_agent,
      user_input="Add another task: 'Call John at 5 PM'.",
      stream_events=False
  ):
    if event.content:
      print(f"Assistant: {event.content.parts[0].text}")

  print("\nUser: Show me all my tasks again.")
  async for event in run_agent_locally(
      agent=assistant_agent,
      user_input="Show me all my tasks again.",
      stream_events=False
  ):
    if event.content:
      print(f"Assistant: {event.content.parts[0].text}")

  # Example of trying to mark a task complete.
  # This requires knowing a task ID. The assistant should guide the user
  # or the user should specify it based on the list_tasks output.
  # For this simple script, we'll assume the first task added was ID 1.
  print("\nUser: Mark task 1 as complete.")
  async for event in run_agent_locally(
      agent=assistant_agent,
      user_input="Mark task 1 as complete.",
      stream_events=False
  ):
    if event.content:
      print(f"Assistant: {event.content.parts[0].text}")

  print("\nUser: List my completed tasks.")
  async for event in run_agent_locally(
      agent=assistant_agent,
      user_input="List my completed tasks.",
      stream_events=False
  ):
    if event.content:
      print(f"Assistant: {event.content.parts[0].text}")
      
  print("\n--- Example run finished ---")

if __name__ == "__main__":
  try:
    asyncio.run(main())
  except RuntimeError as e:
    if "asyncio.run() cannot be called from a running event loop" in str(e):
      # This handles environments like Jupyter notebooks where an event loop is already running.
      loop = asyncio.get_event_loop()
      if loop.is_running():
        print("Asyncio loop already running, creating task.")
        loop.create_task(main())
      else:
        # Should not happen if the error is the one we checked for, but as a fallback:
        print("Starting new event loop for main.")
        asyncio.run(main()) # Or handle differently if this state is unexpected
    else:
      raise # Re-raise other RuntimeError exceptions
