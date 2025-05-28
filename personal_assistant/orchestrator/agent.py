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

# Import sub-agents
from personal_assistant.agents.superbase_agent import superbase_agent
from personal_assistant.agents.notion_agent import notion_agent
from personal_assistant.agents.weather_agent import weather_agent
from personal_assistant.agents.search_agent import search_agent

# Define the Orchestrator Agent
orchestrator_agent = Agent(
    model="gemini-1.5-pro-latest", # Using Gemini 1.5 Pro as 2.5 is not generally available
    name="orchestrator_agent",
    instruction="""
You are the main orchestrator for a helpful personal assistant.
Your primary role is to understand user requests and delegate them to the appropriate sub-agent.
You have the following sub-agents available:
- Superbase Agent (superbase_agent): For managing to-do lists, notes, and reminders.
- Notion Agent (notion_agent): For interacting with Google Mail and Google Calendar.
- Weather Agent (weather_agent): For fetching weather information.
- Search Agent (search_agent): For performing internet web searches.

Based on the user's query, determine which agent is best suited to handle the request and delegate the task accordingly by calling the appropriate agent with its name.
For example, if the user asks to create a to-do, delegate to 'superbase_agent'.
If the user asks to check their email, delegate to 'notion_agent'.
If the user asks for the weather, delegate to 'weather_agent'.
If the user asks to search for something online, delegate to 'search_agent'.

If the user's request is ambiguous, ask for clarification before delegating.
Provide a final response to the user based on the information from the sub-agents.
""",
    sub_agents=[
        superbase_agent,
        notion_agent,
        weather_agent,
        search_agent,
    ],
    # tools list can be populated if the orchestrator needs its own tools
    tools=[],
)

if __name__ == '__main__':
    # This is a placeholder for testing the agent individually if needed.
    # For actual execution, this agent will be part of a larger application.
    print("Orchestrator agent defined and sub-agents linked.")
    # To run and test this agent (example):
    # from google.adk.runners import run_agent_loop
    # from google.adk.sessions import Session
    # session = Session()
    # response = session.send_message(orchestrator_agent, "Create a todo to buy milk.")
    # print(response.parts[0].text)
    # response = session.send_message(orchestrator_agent, "What is the weather in Paris?")
    # print(response.parts[0].text)
