from .agent import Agent

class BusinessPlanAgent(Agent):
    def __init__(self):
        super().__init__(
            name="Business Plan Agent",
            instructions="You are expert in creating business plans which are ready to use in real world scenarios.",
            temperature=0.2,
            tools=[]
        )
