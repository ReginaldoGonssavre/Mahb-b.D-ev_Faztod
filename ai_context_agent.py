import requests

# ️ IA CONTEXT ENGINEERING PROMPT
# Arquitetura de Function Calling inspirada no diagrama
# Funções: Parsing, Intent Detection, Tool Selection, API Execution
class AIContextAgent:
    def __init__(self):
        self.history = []
        self.context = {}
        self.available_tools = {
            'calendar': self.use_calendar,
            'calculator': self.use_calculator,
            'web_search': self.use_web_search,
            'gemini_prompt_function': self.use_gemini_prompt_function # Nova ferramenta
        }

    def parse_request(self, user_input):
        parsed = self.nlp_parser(user_input)
        self.history.append(user_input)
        self.context['last_input'] = user_input
        return parsed

    def nlp_parser(self, text):
        # Simula análise NLP + entidades
        return {
            'intent': self.analyze_intent(text),
            'entities': self.extract_entities(text)
        }

    def analyze_intent(self, text):
        # Simulação de AI de intenção
        if "calcular" in text:
            return "usar_calculadora"
        elif "agenda" in text:
            return "abrir_calendario"
        elif "pesquisar" in text:
            return "fazer_busca"
        elif "gemini" in text.lower() or "perguntar" in text.lower(): # Nova intenção
            return "perguntar_gemini"
        return "intenção_desconhecida"

    def extract_entities(self, text):
        # Simulação de extração de entidades
        return {"dados": text.split()}

    def select_tool(self, intent):
        mapping = {
            'usar_calculadora': 'calculator',
            'abrir_calendario': 'calendar',
            'fazer_busca': 'web_search',
            'perguntar_gemini': 'gemini_prompt_function' # Mapeamento da nova intenção
        }
        return self.available_tools.get(mapping.get(intent, ''), self.tool_not_found)

    def execute_call(self, tool_function, parsed_request):
        return tool_function(parsed_request)

    def validate(self, response):
        return response is not None

    def respond(self, result):
        print("✅ Resposta do agente:", result)

    # --- Tools Simuladas ---
    def use_calculator(self, parsed):
        return "Resultado: 42"

    def use_calendar(self, parsed):
        return " Calendário aberto na data solicitada."

    def use_web_search(self, parsed):
        return " Resultado da busca: [link]"

    def use_gemini_prompt_function(self, parsed):
        """
        Faz uma chamada HTTP para a Supabase Edge Function 'gemini-prompt'.
        """
        prompt_text = " ".join(parsed['entities']['dados']) # Pega o texto do prompt das entidades
        supabase_edge_function_url = "https://zsuuikxrulddbfugiomw.supabase.co/functions/v1/gemini-prompt"
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpzdXVpa3hyb2xkZGJmdWdpb213Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1MzA2MzgzMywiZXhwIjoyMDY4NjM5ODMzfQ.gqiPJ3ExxCLX6fuNQikhdVB7HzdBhVh4faYIUFkqW5g' # Adicionado para autenticação
        }
        payload = {'prompt': prompt_text}

        try:
            response = requests.post(supabase_edge_function_url, headers=headers, json=payload)
            response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
            return f"Resposta da Gemini Edge Function: {response.json()}"
        except requests.exceptions.RequestException as e:
            return f"Erro ao chamar Gemini Edge Function: {e}"

    def tool_not_found(self, parsed):
        return "⚠️ Ferramenta não encontrada para essa intenção."

# -------------------------------
#  EXECUÇÃO
agent = AIContextAgent()
entrada_usuario = "Você pode calcular 7 vezes 6?"
parsed = agent.parse_request(entrada_usuario)
tool = agent.select_tool(parsed['intent'])
resultado = agent.execute_call(tool, parsed)
if agent.validate(resultado):
    agent.respond(resultado)

print("\n--- Teste com Gemini Edge Function ---")
entrada_gemini = "Perguntar Gemini: Qual é o algoritmo de Deutsch-Jozsa?"
parsed_gemini = agent.parse_request(entrada_gemini)
tool_gemini = agent.select_tool(parsed_gemini['intent'])
resultado_gemini = agent.execute_call(tool_gemini, parsed_gemini)
if agent.validate(resultado_gemini):
    agent.respond(resultado_gemini)
