from typing import Callable, Dict, Any

class AgentTool:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any], func: Callable):
        self.name = name
        self.description = description
        self.parameters = parameters
        self._func = func

    def __call__(self, **kwargs):
        return self._func(**kwargs)

# This dictionary will hold all available tools for the agents.
# RPA tools will be added here.
AVAILABLE_TOOLS: Dict[str, AgentTool] = {}
