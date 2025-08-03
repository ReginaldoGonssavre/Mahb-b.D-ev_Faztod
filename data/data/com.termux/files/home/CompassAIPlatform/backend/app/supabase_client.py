import os
from typing import Dict

# Carregue as variáveis de ambiente
# Em um ambiente de produção, use variáveis de ambiente seguras
# Para desenvolvimento, você pode criar um arquivo .env na raiz do backend
# e carregá-lo com python-dotenv (certifique-se de adicionar python-dotenv ao requirements.txt se for usar)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ATENÇÃO: As variáveis de ambiente SUPABASE_URL e SUPABASE_KEY não estão configuradas.")
    print("Por favor, defina-as ou crie um arquivo .env na raiz do backend com:")
    print("SUPABASE_URL='sua_url_supabase'")
    print("SUPABASE_KEY='sua_chave_anon_supabase'")

def get_supabase_client() -> Dict:
    """Retorna a URL base da API REST do Supabase e os cabeçalhos de autenticação."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("As credenciais do Supabase não estão configuradas.")
    
    # A URL base da API REST do Supabase
    base_url = f"{SUPABASE_URL}/rest/v1"
    
    # Os cabeçalhos de autorização
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }
    
    return {"base_url": base_url, "headers": headers}

# Exemplo de uso (apenas para demonstração, remova em produção)
if __name__ == "__main__":
    try:
        # Para este exemplo funcionar, você precisa definir as variáveis de ambiente
        # SUPABASE_URL e SUPABASE_KEY antes de executar este arquivo diretamente.
        supabase_config = get_supabase_client()
        print("Configuração do Supabase obtida com sucesso.")
        print(f"Base URL: {supabase_config["base_url"]}")
        print(f"Headers: {supabase_config["headers"]}")
    except ValueError as e:
        print(f"Erro ao obter configuração do Supabase: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
