import requests
from bs4 import BeautifulSoup
from transformers import pipeline
import json
import os
from datetime import datetime
from supabase import create_client, Client
from github import Github

# --- Configuration (Load from environment variables for security) ---
LINKEDIN_URL = os.environ.get("LINKEDIN_URL", "https://www.linkedin.com/in/your-profile/")
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "your-github-username/your-repo-name")
GITHUB_BRANCH = os.environ.get("GITHUB_BRANCH", "main")

# --- Supabase Client Initialization ---
supabase: Client = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
else:
    print("⚠️ Supabase URL or Key not set. Supabase integration will be skipped.")

# --- GitHub Client Initialization ---
repo = None
if GITHUB_TOKEN:
    g = Github(GITHUB_TOKEN)
    try:
        repo = g.get_user().get_repo(GITHUB_REPO.split('/')[-1]) # Assumes repo name is last part of GITHUB_REPO
    except Exception as e:
        print(f"⚠️ GitHub repo initialization error: {e}. GitHub integration will be skipped.")
else:
    print("⚠️ GitHub Token not set. GitHub integration will be skipped.")

# --- Agent Instructions (Objetivo, Persona) ---
agent_instruction = {
    "role": "AI Coding Agent",
    "objective": "Ajudar a construir agentes autônomos com memória, ferramentas e RAG",
    "requirements": {
        "style": "conversacional, técnico",
        "steps": ["raciocínio", "execução", "resposta"]
    }
}

# --- Exemplos de Comportamento ---
behavior_examples = {
    "positive": [
        "Explica decisões de projeto antes de gerar código.",
        "Sugere melhoria no prompt antes de execução."
    ],
    "negative": [
        "Gera código sem considerar o objetivo do usuário.",
        "Responde superficialmente."
    ]
}

# --- Contexto de Conhecimento ---
external_context = {
    "domain": "Agentes Autônomos e LLMs",
    "workflow": "Prompt → Planejamento → Execução → Feedback",
    "task_docs": {
        "specs": "Use tools como LangChain, OpenAI, Supabase",
        "structured_data": "vetores, embeddings, JSONs"
    }
}

# --- Memória (Placeholder - will use Supabase MCP) ---
# This part is from your original script, but our MCP handles persistence.
# Keeping it here for context, but it won't be actively used for persistence
# if Supabase MCP is configured.
memory_file = "agent_memory.json"
def load_memory():
    if os.path.exists(memory_file):
        with open(memory_file) as f:
            return json.load(f)
    return {"short_term": [], "long_term": []}

def save_memory(memory):
    with open(memory_file, "w") as f:
        json.dump(memory, f, indent=2)

def add_to_memory(entry, term="short_term"):
    memory = load_memory()
    memory[term].append({
        "timestamp": datetime.utcnow().isoformat(),
        "entry": entry
    })
    save_memory(memory)

# --- Ferramentas (Tool Descriptions) ---
tools = [
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

# --- Resultados das Ferramentas ---
def tool_dispatch(tool_name, **kwargs):
    if tool_name == "generate_code":
        return f"# Código em {kwargs.get('language', 'unknown')} para: {kwargs.get('objective', 'nenhum objetivo')}\nprint('Hello Agent')"
    elif tool_name == "search_docs":
        return ["Doc 1: Como usar LangChain", "Doc 2: Setup do Supabase"]
    else:
        return "Ferramenta não encontrada."

# --- Funções de Coleta e Análise ---
def fetch_linkedin_content(url):
    try:
        res = requests.get(url)
        res.raise_for_status() # Raise an exception for HTTP errors
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.get_text()
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Erro ao buscar conteúdo do LinkedIn: {e}")
        return ""

def analyze_content(text):
    # Ensure text is not empty before processing
    if not text:
        return {"meta": "No content to analyze", "diagnostico": "Empty text input"}

    # Limit text length for the classifier
    text_for_classifier = text[:512]
    
    # Initialize the classifier only once if possible, or handle potential download
    try:
        classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
        result = classifier(text_for_classifier)
    except Exception as e:
        print(f"⚠️ Erro ao inicializar ou usar o classificador de texto: {e}")
        result = [{"label": "ERROR", "score": 0.0}] # Fallback result

    plano = {
        "meta": "Dobrar produtividade",
        "diagnostico": "Exploração subótima + reward mal calibrado",
        "estrategias": [
            "reward shaping",
            "epsilon decay adaptativo",
            "actor-critic em multi-agent",
            "buffer prioritário"
        ],
        "resultado_IA": result,
        "base_texto": text[:500]
    }
    return plano

def salvar_local(plano):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorio_{timestamp}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(plano, f, indent=4, ensure_ascii=False)
    print(f"✅ Salvo localmente: {filename}")
    return filename

def enviar_para_supabase(plano):
    if not supabase:
        print("⚠️ Supabase client not initialized. Skipping send to Supabase.")
        return
    data = {
        "conteudo": plano["base_texto"],
        "resultado": json.dumps(plano),
        "timestamp": datetime.now().isoformat()
    }
    try:
        res = supabase.table("relatorios_produtividade").insert(data).execute()
        print("✅ Salvo na Supabase:", res.status_code if hasattr(res, 'status_code') else "OK")
    except Exception as e:
        print(f"⚠️ Erro ao salvar no Supabase: {e}")

def enviar_para_github(filepath):
    if not repo:
        print("⚠️ GitHub client not initialized. Skipping send to GitHub.")
        return
    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    github_path = f"relatorios/{os.path.basename(filepath)}" # Use basename to avoid path issues
    try:
        # Check if file exists to decide between create_file and update_file
        contents = None
        try:
            contents = repo.get_contents(github_path, ref=GITHUB_BRANCH)
        except Exception:
            pass # File does not exist

        if contents:
            repo.update_file(contents.path, f"Update relatório IA {timestamp}", content, contents.sha, branch=GITHUB_BRANCH)
            print(f"✅ Arquivo atualizado no GitHub: {github_path}")
        else:
            repo.create_file(github_path, f"Relatório IA {timestamp}", content, branch=GITHUB_BRANCH)
            print(f"✅ Arquivo enviado para GitHub: {github_path}")
    except Exception as e:
        print(f"⚠️ GitHub erro: {e}")

# --- Entrada do agente (main function from your script) ---
def agent(input_text: str):
    add_to_memory({"user_input": input_text})
    
    # Análise simples de intenção
    if "gerar código" in input_text.lower():
        resposta = tool_dispatch("generate_code", language="python", objective=input_text)
    elif "buscar" in input_text.lower():
        resposta = tool_dispatch("search_docs", query=input_text)
    else:
        resposta = "Não entendi. Deseja gerar código ou buscar documentos?"
    
    add_to_memory({"agent_response": resposta})
    return resposta

# ======================== EXECUÇÃO ========================
def main():
    print("Coletando conteúdo...")
    texto = fetch_linkedin_content(LINKEDIN_URL)
    
    print("Analisando com IA...")
    resultado = analyze_content(texto)
    
    print("Salvando localmente...")
    arquivo = salvar_local(resultado)
    
    print("☁️ Subindo para Supabase...")
    enviar_para_supabase(resultado)
    
    print("Enviando para GitHub...")
    enviar_para_github(arquivo)

    print("\n--- Agent Interaction Example ---")
    entrada = input("Usuário diz (ex: 'gerar código para um bot'): ")
    resposta = agent(entrada)
    print("Agente responde:\n", resposta)

if __name__ == "__main__":
    main()
