from .tool import Tool
from .tool_registry import ToolRegistry
import os

def list_project_files():
    return [f for f in os.listdir('.') if os.path.isfile(f)]

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="list_project_files",
        description="Lists all files in the current directory",
        function=list_project_files,
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ))