from .tool import Tool
from .tool_registry import ToolRegistry
import os

def list_project_files():
    def walk_directory(directory):
        files_and_folders = []
        for root, dirs, files in os.walk(directory):
            if 'venv' in dirs:
                dirs.remove('venv')  # Pomija folder venv
            relative_root = os.path.relpath(root, directory)
            if relative_root != '.':
                files_and_folders.append(os.path.join(relative_root, ''))
            for file in files:
                files_and_folders.append(os.path.join(relative_root, file))
        return files_and_folders

    return walk_directory('.')

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="list_project_files",
        description="Lists all files and folders in the project directory, including files in subfolders, but excluding the 'venv' folder. It returns a list of relative paths to files and folders. Folders are indicated by a trailing slash.",
        function=list_project_files,
        input_schema={
            "type": "object",
            "properties": {},
            "required": []
        }
    ))