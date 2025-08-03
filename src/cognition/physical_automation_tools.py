from src.cognition.agent_tools import AgentTool, AVAILABLE_TOOLS
import time

# --- Ferramentas de Automação Física (Exemplos) ---

def ligar_dispositivo(device_id: str):
    """Simula o ato de ligar um dispositivo físico.

    Args:
        device_id (str): O ID único do dispositivo a ser ligado.
    """
    print(f"[SIMULAÇÃO FÍSICA] Ligando dispositivo: {device_id}...")
    time.sleep(1) # Simula o tempo de operação
    return f"Dispositivo {device_id} ligado com sucesso."

def desligar_dispositivo(device_id: str):
    """Simula o ato de desligar um dispositivo físico.

    Args:
        device_id (str): O ID único do dispositivo a ser desligado.
    """
    print(f"[SIMULAÇÃO FÍSICA] Desligando dispositivo: {device_id}...")
    time.sleep(1) # Simula o tempo de operação
    return f"Dispositivo {device_id} desligado com sucesso."

def ler_sensor(sensor_id: str) -> float:
    """Simula a leitura de dados de um sensor físico.

    Args:
        sensor_id (str): O ID único do sensor a ser lido.

    Returns:
        float: Um valor simulado da leitura do sensor.
    """
    print(f"[SIMULAÇÃO FÍSICA] Lendo sensor: {sensor_id}...")
    time.sleep(0.5) # Simula o tempo de operação
    # Retorna um valor aleatório para simular a leitura do sensor
    import random
    return round(random.uniform(20.0, 30.0), 2)

# --- Definições das AgentTools para Automação Física ---

ligar_dispositivo_tool = AgentTool(
    name="ligar_dispositivo",
    description="Liga um dispositivo físico específico usando seu ID.",
    parameters={
        "device_id": {"type": "string", "description": "O ID único do dispositivo a ser ligado."}
    },
    func=ligar_dispositivo
)

desligar_dispositivo_tool = AgentTool(
    name="desligar_dispositivo",
    description="Desliga um dispositivo físico específico usando seu ID.",
    parameters={
        "device_id": {"type": "string", "description": "O ID único do dispositivo a ser desligado."}
    },
    func=desligar_dispositivo
)

ler_sensor_tool = AgentTool(
    name="ler_sensor",
    description="Lê o valor atual de um sensor físico específico usando seu ID.",
    parameters={
        "sensor_id": {"type": "string", "description": "O ID único do sensor a ser lido."}
    },
    func=ler_sensor
)

# --- Adicionar as ferramentas ao dicionário global AVAILABLE_TOOLS ---

AVAILABLE_TOOLS[ligar_dispositivo_tool.name] = ligar_dispositivo_tool
AVAILABLE_TOOLS[desligar_dispositivo_tool.name] = desligar_dispositivo_tool
AVAILABLE_TOOLS[ler_sensor_tool.name] = ler_sensor_tool
