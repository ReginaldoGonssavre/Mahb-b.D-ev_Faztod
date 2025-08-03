from typing import List, Dict

class ToolManager:
    def __init__(self):
        self.tools = [
            {
                "name": "search_docs",
                "description": "Busca em base de conhecimento vetorial",
                "parameters": {"query": "str"},
                "returns": "lista de trechos relevantes"
            },
            {
                "name": "generate_code",
                "description": "Gera código baseado no prompt",
                "parameters": {"language": "str", "objective": "str"},
                "returns": "string de código"
            }
        ]

    def get_tool_definitions(self) -> List[Dict]:
        return self.tools

    def dispatch_tool(self, tool_name: str, **kwargs):
        if tool_name == "generate_code":
            return f"# Código em {kwargs.get('language', 'unknown')} para: {kwargs.get('objective', 'nenhum objetivo')}\nprint('Hello Agent')"
        elif tool_name == "search_docs":
            return ["Doc 1: Como usar LangChain", "Doc 2: Setup do Supabase"]
        else:
            return "Ferramenta não encontrada."
