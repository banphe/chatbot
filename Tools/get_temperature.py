from .tool import Tool
from .tool_registry import ToolRegistry

def get_temperature(location):
    return 22

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="get_temperature",
        description="Retrieves temperature",
        function=get_temperature,
        input_schema={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "location for which to return temperature"
                }
            },
            "required": ["location"]
        }
    ))