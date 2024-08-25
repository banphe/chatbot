from .tool import Tool
from .tool_registry import ToolRegistry
import os

def read_file(file_path):
    try:
        # Normalizuj ścieżkę, aby obsłużyć względne ścieżki
        normalized_path = os.path.normpath(os.path.join('.', file_path))
        
        if not os.path.exists(normalized_path):
            return f"Error: File does not exist: {file_path}"
        if not os.path.isfile(normalized_path):
            return f"Error: Path is not a file: {file_path}"
        
        # Sprawdź, czy plik nie jest w folderze venv
        if 'venv' in normalized_path.split(os.sep):
            return f"Error: Cannot read files from venv folder: {file_path}"
        
        with open(normalized_path, 'r', encoding='utf-8') as file:
            content = file.read()
            if content:
                return content
            else:
                return f"File is empty: {file_path}"
    except UnicodeDecodeError:
        return f"Error: File {file_path} is not a text file or uses an unsupported encoding."
    except Exception as e:
        return f"Error reading file: {file_path}\nException: {str(e)}\nCurrent working directory: {os.getcwd()}"

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="read_file",
        description="Reads the content of a text file given its path. The path should be relative to the project root, as returned by the list_project_files tool. This tool can read any text file listed by list_project_files, except those in the 'venv' folder. It will return an error message for non-existent files, directories, binary files, or files with unsupported encodings.",
        function=read_file,
        input_schema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "Relative path to the file to read, as returned by list_project_files"
                }
            },
            "required": ["file_path"]
        }
    ))