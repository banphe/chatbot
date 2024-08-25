# This file makes the Tools directory a Python package
from .tool_registry import ToolRegistry
from . import get_stock_price, get_temperature, get_wikipedia_summary, list_project_files, read_file, get_you_tube_transcript

def initialize_tools():
    registry = ToolRegistry()
    get_stock_price.register(registry)
    get_temperature.register(registry)
    get_wikipedia_summary.register(registry)
    list_project_files.register(registry)
    read_file.register(registry)
    get_you_tube_transcript.register(registry)
    return registry