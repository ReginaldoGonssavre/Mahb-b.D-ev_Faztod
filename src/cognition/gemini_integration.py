import os

class GeminiClient:
    def __init__(self):
        print("GeminiClient initialized (placeholder).")
        # Simulate API key check
        if not os.getenv("GEMINI_API_KEY"):
            raise ValueError("GEMINI_API_KEY environment variable not set.")

    def generate_content(self, prompt: str) -> str:
        print(f"GeminiClient: Generating content for prompt: {prompt[:50]}... (placeholder).")
        # Simulate Gemini response
        if "abrir o portal de login" in prompt or "Realizar o login no portal conforme solicitado." in prompt:
            return '{"tool_name": "abrir_e_logar", "parameters": {}}'
        elif "ligar a luz" in prompt:
            return '{"tool_name": "ligar_dispositivo", "parameters": {"device_id": "luz_escritorio"}}'
        elif "ler a temperatura" in prompt:
            return '{"tool_name": "ler_sensor", "parameters": {"sensor_id": "sensor_temperatura_x"}}'
        elif "executar script tagui" in prompt:
            return '{"tool_name": "executar_script_tagui", "parameters": {"script_content": "simulated tagui script"}}'
        elif "executar script uivision" in prompt:
            return '{"tool_name": "executar_script_uivision", "parameters": {"script_json": "{\"Command\": \"open\", \"Target\": \"https://example.com\"}"}}'
        return f"Simulated Gemini response for: {prompt[:50]}..."