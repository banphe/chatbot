from .tool import Tool
from .tool_registry import ToolRegistry

def get_stock_price(symbol):
    return 4987

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="get_stock_price",
        description="Get the current stock price",
        function=get_stock_price,
        input_schema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock symbol"
                }
            },
            "required": ["symbol"]
        }
    ))