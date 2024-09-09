from .tool import Tool
from .tool_registry import ToolRegistry
from image_processor import process_image_from_path
from pathlib import Path

def describe_image(file_path):
    try:
        image_path = Path(file_path)
        if not image_path.exists():
            return "Error: File not found."
        
        image_data = process_image_from_path(str(image_path))
        
        return [
        
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": image_data.media_type,
                    "data": image_data.base64_data
                }
            }
        ]
    except Exception as e:
        return f"Error processing image: {str(e)}"

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="describe_image",
        description='''Analyzes and describes the contents of an image file from the user's hard drive.
        This tool should be used when the user wants to get a description of a specific image file.
        It reads the image file, converts it to base64 format, and returns it as a content block
        that can be sent to Claude for analysis. The tool handles various image formats including
        PNG, JPEG, and GIF. If there's an error reading or processing the image, it will return
        an error message instead.''',
        function=describe_image,
        input_schema={
            "type": "object",
            "properties": {
                "file_path": {
                    "type": "string",
                    "description": "The full path to the image file on the user's hard drive."
                }
            },
            "required": ["file_path"]
        }
    ))