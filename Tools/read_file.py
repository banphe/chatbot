from .tool import Tool
from .tool_registry import ToolRegistry
import os

def read_file(file_path):
    try:
        if not os.path.exists(file_path):
            return f"Error: File does not exist: {file_path}"
        if not os.path.isfile(file_path):
            return f"Error: Path is not a file: {file_path}"
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if content:
                return content
            else:
                return f"File is empty: {file_path}"
    except Exception as e:
        return f"Error reading file: {file_path}\nException: {str(e)}\nCurrent working directory: {os.getcwd()}"

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="read_file",
        description="Reads the content of a file given its path",
        function=read_file,
        input_schema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Path to the file to read"
                }
            },
            "required": ["file_path"]
        }
    ))