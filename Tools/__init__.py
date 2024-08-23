# This file makes the Tools directory a Python package
from .tool_registry import ToolRegistry
from . import get_stock_price, get_temperature, list_project_files, read_file

def initialize_tools():
    registry = ToolRegistry()
    get_stock_price.register(registry)
    get_temperature.register(registry)
    list_project_files.register(registry)
    read_file.register(registry)
    return registry