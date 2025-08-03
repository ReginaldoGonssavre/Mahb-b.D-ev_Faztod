"""
Base agent implementation.
This agent incorporates a core intelligence, memory (MCP), and tool usage.
"""

from mahbub_agent_framework.core.transformer_core import TransformerCore
from mahbub_agent_framework.mcp.mcp import MCP
from mahbub_agent_framework.tools.tool_manager import ToolManager

class Agent:
    def __init__(self, agent_id="default_agent"):
        print(f"--- [Agent] Initializing agent with ID: '{agent_id}' ---")
        self.agent_id = agent_id
        self.core = TransformerCore()
        self.mcp = MCP(agent_id=self.agent_id)
        self.tool_manager = ToolManager()
        print(f"--- [Agent] '{self.agent_id}' is now online. ---")

    def execute(self, input_text: str):
        """
        Executes a task based on the input text, using core intelligence, memory, and tools.
        """
        print(f"--- [Agent] '{self.agent_id}' received input: '{input_text}' ---")
        
        # Add user input to memory
        self.mcp.update_context("last_user_input", input_text)

        # Simple intention analysis (from agent_multi_context.py)
        response = ""
        if "gerar código" in input_text.lower():
            # Use the tool manager to dispatch the tool
            response = self.tool_manager.dispatch_tool("generate_code", language="python", objective=input_text)
        elif "buscar" in input_text.lower():
            response = self.tool_manager.dispatch_tool("search_docs", query=input_text)
        else:
            # If no specific tool is identified, use the core intelligence
            print("--- [Agent] No specific tool identified. Using core intelligence. ---")
            # Recall relevant context from memory before processing with core
            last_task_result = self.mcp.get_context("last_task_result")
            if last_task_result:
                input_for_core = f"{input_text} (context: previous result was '{last_task_result}')"
            else:
                input_for_core = input_text
            
            response = self.core.process(input_for_core)
            self.mcp.update_context("last_task_result", response) # Save core's response to memory

        # Add agent response to memory
        self.mcp.update_context("last_agent_response", response)
        
        print(f"--- [Agent] '{self.agent_id}' finished execution. ---")
        return response
