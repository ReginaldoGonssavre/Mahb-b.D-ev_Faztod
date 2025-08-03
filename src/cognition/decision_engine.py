import json
from typing import Dict, Any, Optional

from src.cognition.gemini_integration import GeminiClient
from src.cognition.agent_tools import AgentTool

class DecisionEngine:
    def __init__(self, gemini_client: GeminiClient, tools: Dict[str, AgentTool]):
        self.gemini_client = gemini_client
        self.tools = tools

    def _get_tool_definitions_for_gemini(self) -> str:
        if not self.tools:
            return ""
        tool_definitions = []
        for tool_name, tool_obj in self.tools.items():
            tool_definitions.append(f"Tool Name: {tool_obj.name}\nDescription: {tool_obj.description}\nParameters: {json.dumps(tool_obj.parameters)}")
        return "\n\nAvailable Tools:\n" + "\n---\n".join(tool_definitions) + "\n\n"

    def decide_and_act(self, intention: str, rag_context: str = "") -> str:
        tool_definitions_str = self._get_tool_definitions_for_gemini()

        prompt = f"Based on the following context: {rag_context}\n\nAnd the intention: {intention}\n\n{tool_definitions_str}"
        prompt += "If a tool is needed, respond with a JSON object like: {\"tool_name\": \"tool_name_here\", \"parameters\": {\"param1\": \"value1\"}}.\nOtherwise, provide a concise and helpful response."

        print(f"Sending prompt to Gemini: {prompt[:500]}...")
        gemini_response_text = self.gemini_client.generate_content(prompt)
        print(f"Gemini's raw response: {gemini_response_text}")

        try:
            tool_call = json.loads(gemini_response_text)
            # Assuming the JSON structure is {"tool_name": {"param1": "value1"}}
            # Extract tool_name and parameters dynamically
            tool_name = tool_call["tool_name"]
            parameters = tool_call["parameters"]

            if tool_name in self.tools:
                tool_obj = self.tools[tool_name]
                print(f"Executing tool: {tool_name} with parameters: {parameters}")
                tool_result = tool_obj(**parameters)
                print(f"Tool result: {tool_result}")

                follow_up_prompt = f"Based on the original intention: {intention}\nAnd the tool result from {tool_name}: {tool_result}\n\nProvide a concise and helpful final response."
                final_gemini_response = self.gemini_client.generate_content(follow_up_prompt)
                return final_gemini_response
            else:
                return f"Gemini suggested unknown tool: {tool_name}"
        except json.JSONDecodeError:
            return gemini_response_text
