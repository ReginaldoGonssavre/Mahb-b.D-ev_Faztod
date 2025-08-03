import os

from refactored_agent import IntelligentAgent, MLComponent, NeuralAgentComponent
from supabase_manager import SupabaseManager
from src.cognition.agent_tools import AVAILABLE_TOOLS
import src.cognition.rpa_tools # Import RPA tools to populate AVAILABLE_TOOLS
import src.cognition.physical_automation_tools # Import physical automation tools to populate AVAILABLE_TOOLS
import json # For parsing tool calls
from src.cognition.decision_engine import DecisionEngine
from input_data import InputData # New import

class MyAgent(IntelligentAgent):
    def __init__(self, agent_id: str, supabase_manager: SupabaseManager | None = None):
        super().__init__(agent_id, supabase_manager, tools=AVAILABLE_TOOLS) # Pass AVAILABLE_TOOLS to parent
        self.decision_engine = DecisionEngine(self.gemini_client, self.tools) # Initialize DecisionEngine
        print(f"MyAgent '{agent_id}' initialized with RAG, Gemini, Supabase persistence, and Tool Use capabilities.")

    def perceive(self, environment: InputData):
        self.memory_manager.add_short_term_memory(environment) # Store the full InputData object
        print(f"Agent perceived: {environment.text}")

        # Use RAG to get relevant context based on the environment
        rag_context = ""
        if self.rag_module and environment.text:
            print(f"Searching RAG for context related to: {environment.text}")
            results = self.rag_module.query_vectors(environment.text)
            if results and results.matches:
                # Concatenate relevant text from RAG results
                for match in results.matches:
                    # Assuming metadata contains 'text' field
                    if 'text' in match.metadata:
                        rag_context += match.metadata['text'] + "\n"
                print(f"RAG context found: {rag_context[:100]}...") # Print first 100 chars
            else:
                print("No RAG context found.")
        else:
            print("RAG module not initialized or no text in environment. Cannot retrieve context.")
        return rag_context

    

    def act(self, intention: str, rag_context: str = "") -> str:
        print(f"Agent acting with intention: {intention}")
        return self.decision_engine.decide_and_act(intention, rag_context)

    # Placeholder for abstract methods from IntelligentAgent
    def _update_desires(self):
        return "" # Simplified for example

    def _form_intention(self):
        return "" # Simplified for example


if __name__ == "__main__":
    # Set environment variables for Pinecone and Gemini before running
    os.environ["PINECONE_API_KEY"] = "YOUR_FICTITIOUS_PINECONE_API_KEY"
    os.environ["PINECONE_ENVIRONMENT"] = "YOUR_FICTITIOUS_PINECONE_ENVIRONMENT"
    os.environ["PINECONE_INDEX_NAME"] = "my-index"
    os.environ["GEMINI_API_KEY"] = "YOUR_FICTITIOUS_GEMINI_API_KEY"
    os.environ["SUPABASE_URL"] = "http://localhost:8000" # Fictitious but valid URL format
    os.environ["SUPABASE_KEY"] = "YOUR_FICTITIOUS_SUPABASE_KEY"

    # Example of populating Pinecone index (run this once or as needed)
    # from rag_module import RAGModule
    # rag_module_example = RAGModule(
    #     os.getenv("PINECONE_API_KEY"),
    #     os.getenv("PINECONE_ENVIRONMENT"),
    #     os.getenv("PINECONE_INDEX_NAME", "my-index")
    # )
    # rag_module_example.upsert_vector("doc1", "O Qiskit é um framework Python de código aberto para computação quântica.")
    # rag_module_example.upsert_vector("doc2", "O Algoritmo de Deutsch-Jozsa é um algoritmo quântico que determina se uma função é constante ou balanceada.")
    # rag_module_example.upsert_vector("doc3", "Maḥbūb é uma plataforma open-source modular para orquestração de agentes de IA autônomos.")

    try:
        supabase_manager = SupabaseManager()
        print("SupabaseManager initialized for example usage.")
    except ValueError as e:
        print(f"Could not initialize SupabaseManager: {e}. Skipping Supabase persistence demo.")
        supabase_manager = None

    agent_id = "my_test_agent"
    agent = MyAgent(agent_id, supabase_manager)

    # Simulate a perception and action cycle
    user_query = InputData(text="O que é o Qiskit e qual a sua relação com o Maḥbūb?")
    context = agent.perceive(user_query)
    agent.act(f"Responder à pergunta do usuário sobre {user_query}", rag_context=context)
    if supabase_manager:
        agent.save_state_to_db()

    user_query_2 = InputData(text="Explique o algoritmo de Deutsch-Jozsa.")
    context_2 = agent.perceive(user_query_2)
    agent.act(f"Explicar o algoritmo de Deutsch-Jozsa para o usuário.", rag_context=context_2)
    if supabase_manager:
        agent.save_state_to_db()

    # Simulate a request that should trigger the Qiskit tool
    user_query_3 = InputData(text="Crie um circuito quântico com 2 qubits, um Hadamard no qubit 0 e um CNOT entre 0 e 1. Defina os observáveis 'IZ' e 'XX'.")
    context_3 = agent.perceive(user_query_3)
    print(f"\n--- Simulating Request to Trigger Qiskit Tool ---")
    qiskit_response = agent.act(f"Criar e descrever o circuito quântico e observáveis solicitados.", rag_context=context_3)
    print(f"Agent Response (Qiskit Tool): {qiskit_response}")
    if supabase_manager:
        agent.save_state_to_db()

    # Simulate a request that should trigger the RPA tool
    user_query_4 = InputData(text="Por favor, abra o portal de login e faça o login com as credenciais padrão.")
    context_4 = agent.perceive(user_query_4)
    print(f"\n--- Simulating Request to Trigger RPA Tool (abrir_e_logar) ---")
    rpa_response = agent.act(f"Realizar o login no portal conforme solicitado.", rag_context=context_4)
    print(f"Agent Response (RPA Tool): {rpa_response}")
    if supabase_manager:
        agent.save_state_to_db()

    # --- Demonstração de Orquestração com ChiefAgent ---
    from src.cognition.chief_agent import ChiefAgent, Task

    print("\n--- Iniciando Demonstração de Orquestração com ChiefAgent ---")
    chief_agent = ChiefAgent("chief_orchestrator", supabase_manager)

    # ChiefAgent adiciona uma tarefa de RPA
    chief_agent.add_task(
        description="Realizar o login no portal de administração usando a ferramenta RPA.",
        tool_name="abrir_e_logar",
        tool_parameters={}
    )

    # ChiefAgent orquestra a tarefa
    orchestration_result = chief_agent.act("orchestrate_tasks")
    print(f"ChiefAgent Orchestration Result: {orchestration_result}")

    # --- Simular o MyAgent (trabalhador) buscando e executando tarefas do Supabase ---
    print("\n--- MyAgent (Worker) buscando tarefas pendentes no Supabase ---")
    if supabase_manager:
        worker_agent_id = "my_test_agent" # O ID do MyAgent
        pending_tasks = supabase_manager.get_pending_tasks_for_agent(worker_agent_id)

        if pending_tasks:
            print(f"MyAgent (Worker) encontrou {len(pending_tasks)} tarefa(s) pendente(s).")
            for task_data in pending_tasks:
                task_from_chief = Task(**task_data)
                print(f"MyAgent (Worker) recebendo tarefa do ChiefAgent: {task_from_chief.description}")

                if task_from_chief.tool_name and task_from_chief.tool_name in AVAILABLE_TOOLS:
                    print(f"MyAgent (Worker) executando ferramenta: {task_from_chief.tool_name} com parâmetros: {task_from_chief.tool_parameters}")
                    tool_to_execute = AVAILABLE_TOOLS[task_from_chief.tool_name]
                    worker_tool_result = tool_to_execute(**task_from_chief.tool_parameters)
                    print(f"MyAgent (Worker) resultado da ferramenta: {worker_tool_result}")

                    # Atualizar o status da tarefa no Supabase
                    supabase_manager.update_task(task_from_chief.task_id, {"status": "completed", "result": worker_tool_result})
                    print(f"MyAgent (Worker) tarefa '{task_from_chief.task_id}' marcada como concluída no Supabase.")
                else:
                    print(f"MyAgent (Worker): Não foi possível executar a ferramenta para a tarefa: {task_from_chief.description}")
                    supabase_manager.update_task(task_from_chief.task_id, {"status": "failed", "result": "Ferramenta não encontrada ou inválida."})
