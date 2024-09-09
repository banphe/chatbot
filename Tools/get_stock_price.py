from .tool import Tool
from .tool_registry import ToolRegistry
import yfinance as yf

def get_stock_price(symbol: str) -> str:
    # Fetches the latest closing stock price for a given ticker symbol using Yahoo Finance API.
    try:
        stock = yf.Ticker(symbol)
        price = stock.history(period="1d")['Close'].iloc[-1]
        return str(price)
    except Exception as e:
        # Provides detailed error reporting on what went wrong during the API call.
        print(f"An error occurred: {e}")
        return None

def register(registry: ToolRegistry):
    registry.register_tool(Tool(
        name="get_stock_price",
        description="Retrieves the current stock price for a given ticker symbol. The ticker symbol must be a valid symbol for a publicly traded company on a major US stock exchange like NYSE or NASDAQ. The tool will return the latest trade price in USD. It should be used when the user asks about the current or most recent price of a specific stock. It will not provide any other information about the stock or company.Retrieves the current stock price for a given ticker symbol. The ticker symbol must be a valid symbol for a publicly traded company on a major US stock exchange like NYSE or NASDAQ. The tool will return the latest trade price in USD. It should be used when the user asks about the current or most recent price of a specific stock. It will not provide any other information about the stock or company.",
        function=get_stock_price,
        input_schema={
            "type": "object",
            "properties": {
                "symbol": {
                    "type": "string",
                    "description": "The stock ticker symbol, e.g. AAPL for Apple Inc."
                }
            },
            "required": ["symbol"]
        }
    ))