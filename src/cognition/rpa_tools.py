from src.cognition.agent_tools import AgentTool, AVAILABLE_TOOLS
import time
import json

# Assuming Selenium is installed and configured.
# You might need to install it: pip install selenium
# And download a webdriver (e.g., chromedriver) for your browser.
try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
except ImportError:
    webdriver = None
    By = None

def abrir_navegador_login():
    if webdriver is None:
        return "Selenium is not installed or configured. Cannot execute RPA."
    
    browser = None
    try:
        # Using Chrome as an example. You might need to specify the path to your chromedriver.
        browser = webdriver.Chrome() 
        browser.get("https://example.com")
        
        # Assuming elements have 'id' attributes as in your example
        username_field = browser.find_element(By.ID, "username")
        password_field = browser.find_element(By.ID, "password")
        login_button = browser.find_element(By.ID, "Login") # Assuming 'Login' is the ID of the button

        username_field.send_keys("dr")
        password_field.send_keys("123456")
        login_button.click()
        
        time.sleep(5) # Wait for 5 seconds
        
        # Take screenshot (optional)
        browser.save_screenshot("tela.png")
        
        return "Login successful and screenshot taken."
    except Exception as e:
        return f"Error during RPA execution: {e}"
    finally:
        if browser:
            browser.quit() # Use quit() to close the browser and terminate the WebDriver session

def executar_script_tagui(script_content: str):
    """Simula a execução de um script RPA TagUI.

    Args:
        script_content (str): O conteúdo do script TagUI a ser executado.
    """
    print(f"[SIMULAÇÃO RPA] Executando script TagUI:\n{script_content[:100]}...")
    time.sleep(3) # Simula o tempo de execução
    # Em um ambiente real, aqui você chamaria o executável TagUI com o script.
    return f"Script TagUI executado com sucesso. Conteúdo: {script_content[:50]}..."

def executar_script_uivision(script_json: str):
    """Simula a execução de um script RPA UiVision.

    Args:
        script_json (str): O conteúdo do script UiVision em formato JSON.
    """
    print(f"[SIMULAÇÃO RPA] Executando script UiVision:\n{script_json[:100]}...")
    time.sleep(4) # Simula o tempo de execução
    # Em um ambiente real, aqui você chamaria a API ou CLI do UiVision.
    try:
        script_data = json.loads(script_json)
        return f"Script UiVision executado com sucesso. Comandos: {len(script_data)}."
    except json.JSONDecodeError:
        return "Erro: Conteúdo do script UiVision inválido (não é um JSON válido)."

# Define the AgentTool for 'abrir_e_logar'
abrir_e_logar_tool = AgentTool(
    name="abrir_e_logar",
    description="Abre um navegador, navega para example.com, insere credenciais e tenta fazer login.",
    parameters={}, # No parameters for this specific tool
    func=abrir_navegador_login
)

# Define the AgentTool for 'executar_script_tagui'
executar_script_tagui_tool = AgentTool(
    name="executar_script_tagui",
    description="Executa um script de automação de processo robótico (RPA) usando a sintaxe TagUI.",
    parameters={
        "script_content": {"type": "string", "description": "O conteúdo completo do script TagUI a ser executado."}
    },
    func=executar_script_tagui
)

# Define the AgentTool for 'executar_script_uivision'
executar_script_uivision_tool = AgentTool(
    name="executar_script_uivision",
    description="Executa um script de automação de processo robótico (RPA) usando a sintaxe JSON do UiVision.",
    parameters={
        "script_json": {"type": "string", "description": "O conteúdo do script UiVision em formato JSON."}
    },
    func=executar_script_uivision
)

# Add the tools to AVAILABLE_TOOLS
AVAILABLE_TOOLS[abrir_e_logar_tool.name] = abrir_e_logar_tool
AVAILABLE_TOOLS[executar_script_tagui_tool.name] = executar_script_tagui_tool
AVAILABLE_TOOLS[executar_script_uivision_tool.name] = executar_script_uivision_tool