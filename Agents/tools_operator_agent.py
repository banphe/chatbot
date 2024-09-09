from .agent import Agent

class ToolsOperatorAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Tools Operator",
            instructions="You are a helpful assistant capable of analyzing images and providing various information.",
            temperature=0.2, 
            tools=[
                "get_temperature", 
                "get_stock_price", 
                "get_wikipedia_summary", 
                "list_project_files", 
                "get_you_tube_transcript", 
                "read_file",
                "describe_image"  # Add the new tool here
            ]
        )