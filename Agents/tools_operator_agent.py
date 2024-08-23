from .agent import Agent

class ToolsOperatorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Tools Operator",
            instructions="You are a helpful assistant.",
            temperature=0.2,
            tools=["get_temperature", "get_stock_price", "list_project_files", "read_file"]
        )
