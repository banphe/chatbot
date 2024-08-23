class Agent:
    def __init__(self, name, instructions, temperature, tools):
        self.name = name
        self.instructions = instructions
        self.temperature = temperature
        self.tools = tools

    def get_name(self):
        return self.name

    def get_instructions(self):
        return self.instructions

    def get_temperature(self):
        return self.temperature

    def get_tools(self):
        return self.tools
