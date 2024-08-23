from .tool import Tool

class ToolRegistry:
    def __init__(self):
        self.tools = {}

    def register_tool(self, tool):
        self.tools[tool.name] = tool

    def get_tool(self, name):
        return self.tools.get(name)

    def list_tools(self):
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.input_schema
            }
            for tool in self.tools.values()
        ]

    def process_tool_call(self, tool_name, tool_input):
        tool = self.get_tool(tool_name)
        if tool:
            return tool.execute(**tool_input)
        else:
            return f"Unknown tool: {tool_name}"