import requests
from bs4 import BeautifulSoup
from transformers import pipeline
from datetime import datetime
import json
import os

# Certifique-se de instalar as bibliotecas necessárias:
# pip install requests beautifulsoup4 transformers torch supabase-py PyGithub

# --- Configurações (substitua com suas próprias credenciais e URLs) ---
LINKEDIN_URL = "https://www.linkedin.com/posts/sumanth077_handson-deep-reinforcement-learning-this-activity-7357674369805963264-ueDR"

# Configurações do Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Configurações do GitHub
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO_OWNER = "YOUR_GITHUB_USERNAME"
GITHUB_REPO_NAME = "YOUR_REPO_NAME"
GITHUB_BRANCH = "main"

# Inicialização do Supabase (se SUPABASE_URL e SUPABASE_KEY estiverem definidos)
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    from supabase import create_client, Client
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Inicialização do GitHub (se GITHUB_TOKEN estiver definido)
repo = None
if GITHUB_TOKEN:
    from github import Github
    g = Github(GITHUB_TOKEN)
    try:
        repo = g.get_user().get_repo(GITHUB_REPO_NAME)
    except Exception as e:
        print(f"Erro ao acessar o repositório GitHub: {e}")
        repo = None

# --- Funções ---
def fetch_linkedin_content(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Erro ao acessar o LinkedIn: {e}")

    soup = BeautifulSoup(response.content, 'html.parser')
    return soup.get_text()

def analyze_content(text):
    reasoning = (
        f"\n Análise baseada em Deep RL\n"
        f"- Amostra de texto analisado: {text[:500]}...\n"
        f"- Detecção de falhas: recompensas mal definidas, exploração limitada, política instável.\n"
        f"- Estratégia aplicada: reward shaping, epsilon-greedy adaptativo, buffer prioritário.\n"
    )
    # Certifique-se de que o modelo 'distilbert-base-uncased-finetuned-sst-2-english' está disponível
    # Ele será baixado na primeira execução se não estiver presente.
    classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
    result = classifier(text[:512])

    plano = {
        "ajuste_politica": True,
        "estrategia_exploracao": "epsilon-greedy adaptativo",
        "reward_shaping": True,
        "multi_seed_evaluation": True,
        "meta": "Dobrar produtividade",
        "deep_reasoning": reasoning,
        "classificacao_IA": result
    }
    return plano

def salvar_local(plano):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"relatorio_ia_{timestamp}.json"
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(plano, f, ensure_ascii=False, indent=4)
    print(f"\n Relatório salvo em: {filename}")
    return filename

def enviar_para_supabase(plano):
    if not supabase:
        print("⚠️ Supabase não configurado. Ignorando o envio.")
        return
    try:
        data = {
            "conteudo": plano["deep_reasoning"], # Usando deep_reasoning como conteúdo
            "resultado": json.dumps(plano), # Salva o plano completo como JSON string
            "timestamp": datetime.now().isoformat()
        }
        # Certifique-se de que a tabela 'relatorios_produtividade' existe no seu Supabase
        res = supabase.table("relatorios_produtividade").insert(data).execute()
        print("✅ Salvo na Supabase:", res.status_code if hasattr(res, 'status_code') else "OK")
    except Exception as e:
        print(f"⚠️ Erro ao enviar para Supabase: {e}")

def enviar_para_github(filepath):
    if not repo:
        print("⚠️ GitHub não configurado. Ignorando o envio.")
        return
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            content = file.read()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        github_path = f"relatorios/{os.path.basename(filepath)}"

        # Tenta criar o arquivo. Se já existir, tenta atualizá-lo.
        try:
            contents = repo.get_contents(github_path, ref=GITHUB_BRANCH)
            repo.update_file(contents.path, f"Atualização relatório IA {timestamp}", content, contents.sha, branch=GITHUB_BRANCH)
            print(f"✅ Arquivo atualizado no GitHub: {github_path}")
        except Exception as e:
            if "Not Found" in str(e): # Arquivo não existe, então cria
                repo.create_file(github_path, f"Relatório IA {timestamp}", content, branch=GITHUB_BRANCH)
                print(f"✅ Arquivo enviado para GitHub: {github_path}")
            else:
                raise e

    except Exception as e:
        print(f"⚠️ GitHub erro: {e}")

# ======================== EXECUÇÃO ========================
def main():
    print(" Coletando conteúdo...")
    try:
        texto = fetch_linkedin_content(LINKEDIN_URL)
    except Exception as e:
        print(f"Erro na coleta de conteúdo: {e}")
        return

    print(" Analisando com IA...")
    resultado = analyze_content(texto)

    print(" Salvando localmente...")
    arquivo = salvar_local(resultado)

    print("☁️ Subindo para Supabase...")
    enviar_para_supabase(resultado)

    print(" Enviando para GitHub...")
    enviar_para_github(arquivo)

if __name__ == "__main__":
    main()
