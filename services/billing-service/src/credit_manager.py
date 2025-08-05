# services/billing-service/src/credit_manager.py
# Lógica para gerenciar créditos de uso dos agentes na plataforma MAHBUB.

class CreditManager:
    def __init__(self, supabase_client):
        self.supabase = supabase_client

    def get_user_credits(self, user_id: str) -> int:
        """
        Obtém o número de créditos disponíveis para um usuário.
        """
        # Simulação: Em um cenário real, buscaria no Supabase
        print(f"[CreditManager] Buscando créditos para o usuário: {user_id}")
        # Exemplo de como seria a query no Supabase:
        # response = self.supabase.table('user_profiles').select('credits').eq('id', user_id).execute()
        # if response.data:
        #     return response.data[0]['credits']
        return 100 # Créditos de exemplo

    def consume_credits(self, user_id: str, amount: int) -> bool:
        """
        Consome uma quantidade de créditos de um usuário.
        Retorna True se a operação for bem-sucedida, False caso contrário.
        """
        current_credits = self.get_user_credits(user_id)
        if current_credits >= amount:
            new_credits = current_credits - amount
            print(f"[CreditManager] Consumindo {amount} créditos do usuário {user_id}. Créditos restantes: {new_credits}")
            # Simulação: Em um cenário real, atualizaria no Supabase
            # self.supabase.table('user_profiles').update({'credits': new_credits}).eq('id', user_id).execute()
            return True
        print(f"[CreditManager] Usuário {user_id} não tem créditos suficientes. Necessário: {amount}, Disponível: {current_credits}")
        return False

    def add_credits(self, user_id: str, amount: int):
        """
        Adiciona créditos a um usuário (ex: após compra de licença).
        """
        print(f"[CreditManager] Adicionando {amount} créditos ao usuário {user_id}")
        # Simulação: Em um cenário real, atualizaria no Supabase
        # current_credits = self.get_user_credits(user_id)
        # new_credits = current_credits + amount
        # self.supabase.table('user_profiles').update({'credits': new_credits}).eq('id', user_id).execute()

# Exemplo de uso (em um contexto de backend)
if __name__ == "__main__":
    # Suponha que 'supabase_client' é uma instância do cliente Supabase
    # from supabase import create_client
    # supabase_url = "SUA_URL_SUPABASE"
    # supabase_key = "SUA_ANON_KEY_SUPABASE"
    # supabase_client = create_client(supabase_url, supabase_key)

    # Para este exemplo, usaremos um mock
    class MockSupabaseClient:
        def table(self, table_name):
            return self
        def select(self, column):
            return self
        def eq(self, column, value):
            return self
        def execute(self):
            return type('obj', (object,), {'data': [{'credits': 100}]})()
        def update(self, data):
            return self

    mock_supabase = MockSupabaseClient()
    manager = CreditManager(mock_supabase)

    user_id = "test_user_123"

    print(f"Créditos iniciais: {manager.get_user_credits(user_id)}")

    if manager.consume_credits(user_id, 20):
        print("Créditos consumidos com sucesso.")
    else:
        print("Falha ao consumir créditos.")

    print(f"Créditos após consumo: {manager.get_user_credits(user_id)}")

    manager.add_credits(user_id, 50)
    print(f"Créditos após adição: {manager.get_user_credits(user_id)}")
