from .tool import Tool
from .tool_registry import ToolRegistry
import requests 

def get_temperature(city):
    url = f"https://wttr.in/{city}?format=%t"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        temperature = response.text.strip()
        return f"The current temperature in {city} is {temperature}"
    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="get_temperature",
        description='''Retrieves the current temperature for a given city using the wttr.in service. 
        This tool should be used when the user asks about the current temperature in a specific city. 
        It returns the temperature in the format provided by wttr.in, typically in Celsius. 
        The tool does not require an API key and is suitable for basic temperature queries. 
        However, it relies on a free service, so it may have limitations in terms of request frequency and data availability. 
        It will not provide any other weather information beyond temperature.''',
        function=get_temperature,
        input_schema={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": '''The name of the city for which to retrieve the temperature, 
                    e.g. 'London' or 'New York'.'''
                }
            },
            "required": ["city"]
        }
    ))