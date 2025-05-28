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
from google.adk.tools import function_tool

# --- Placeholder Tool for Weather API ---
def get_weather(location: str, date: str = "today") -> str:
  """Fetches weather information for a given location and date."""
  # TODO: Implement actual Weather API call.
  # This will require choosing a weather API provider, getting an API key,
  # and using a tool like openapi_tool or a generic HTTP client.
  return f"Placeholder: Fetching weather for {location} on {date}."

# --- Weather API Agent Definition ---
weather_agent = Agent(
    model="gemini-1.5-pro-latest",
    name="weather_agent",
    description="Fetches weather information using a weather API.",
    instruction="""
You are responsible for providing weather forecasts.
Use the get_weather tool to fetch weather information for the specified location and date.
""",
    tools=[
        function_tool.FunctionTool(fn=get_weather),
    ],
)

if __name__ == '__main__':
    # Placeholder for testing
    print("Weather API agent defined with a placeholder tool.")
    # Example usage (testing a tool):
    # print(get_weather(location="London, UK", date="tomorrow"))
