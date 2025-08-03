from oqs import KeyEncapsulation, Signature

def generate_kem_keys(kem_alg: str):
    """Gera um par de chaves para Key Encapsulation Mechanism (KEM).

    Args:
        kem_alg (str): O algoritmo KEM a ser usado (ex: 'Kyber768').

    Returns:
        tuple: (public_key, private_key)
    """
    try:
        client = KeyEncapsulation(kem_alg)
        public_key = client.generate_keypair()
        private_key = client.export_secret_key()
        return public_key, private_key
    except Exception as e:
        print(f"Erro ao gerar chaves KEM: {e}")
        return None, None

def encapsulate_secret(kem_alg: str, public_key: bytes):
    """Encapsula um segredo usando a chave pública KEM.

    Args:
        kem_alg (str): O algoritmo KEM a ser usado.
        public_key (bytes): A chave pública do destinatário.

    Returns:
        tuple: (ciphertext, shared_secret)
    """
    try:
        client = KeyEncapsulation(kem_alg)
        ciphertext, shared_secret = client.encap_secret(public_key)
        return ciphertext, shared_secret
    except Exception as e:
        print(f"Erro ao encapsular segredo: {e}")
        return None, None

def decapsulate_secret(kem_alg: str, private_key: bytes, ciphertext: bytes):
    """Decapsula um segredo usando a chave privada KEM e o ciphertext.

    Args:
        kem_alg (str): O algoritmo KEM a ser usado.
        private_key (bytes): A chave privada do destinatário.
        ciphertext (bytes): O ciphertext recebido.

    Returns:
        bytes: O segredo compartilhado decapsulado.
    """
    try:
        client = KeyEncapsulation(kem_alg)
        shared_secret = client.decap_secret(private_key, ciphertext)
        return shared_secret
    except Exception as e:
        print(f"Erro ao decapsular segredo: {e}")
        return None

def generate_signature_keys(sig_alg: str):
    """Gera um par de chaves para assinatura digital pós-quântica.

    Args:
        sig_alg (str): O algoritmo de assinatura a ser usado (ex: 'Dilithium3').

    Returns:
        tuple: (public_key, private_key)
    """
    try:
        signer = Signature(sig_alg)
        public_key = signer.generate_keypair()
        private_key = signer.export_secret_key()
        return public_key, private_key
    except Exception as e:
        print(f"Erro ao gerar chaves de assinatura: {e}")
        return None, None

def sign_message(sig_alg: str, private_key: bytes, message: bytes):
    """Assina uma mensagem usando a chave privada de assinatura.

    Args:
        sig_alg (str): O algoritmo de assinatura a ser usado.
        private_key (bytes): A chave privada do signatário.
        message (bytes): A mensagem a ser assinada.

    Returns:
        bytes: A assinatura digital.
    """
    try:
        signer = Signature(sig_alg)
        signer.import_secret_key(private_key)
        signature = signer.sign(message)
        return signature
    except Exception as e:
        print(f"Erro ao assinar mensagem: {e}")
        return None

def verify_signature(sig_alg: str, public_key: bytes, message: bytes, signature: bytes):
    """Verifica uma assinatura digital usando a chave pública do signatário.

    Args:
        sig_alg (str): O algoritmo de assinatura a ser usado.
        public_key (bytes): A chave pública do signatário.
        message (bytes): A mensagem original.
        signature (bytes): A assinatura a ser verificada.

    Returns:
        bool: True se a assinatura for válida, False caso contrário.
    """
    try:
        verifier = Signature(sig_alg)
        verifier.import_public_key(public_key)
        is_valid = verifier.verify(message, signature)
        return is_valid
    except Exception as e:
        print(f"Erro ao verificar assinatura: {e}")
        return False

if __name__ == "__main__":
    # Exemplo de uso para KEM (Key Encapsulation Mechanism)
    kem_algorithm = 'Kyber768'
    print(f"\n--- Testando KEM com {kem_algorithm} ---")
    # Alice gera suas chaves KEM
    alice_public_key, alice_private_key = generate_kem_keys(kem_algorithm)
    if alice_public_key and alice_private_key:
        print("Alice gerou chaves KEM.")

        # Bob encapsula um segredo para Alice
        bob_ciphertext, bob_shared_secret = encapsulate_secret(kem_algorithm, alice_public_key)
        if bob_ciphertext and bob_shared_secret:
            print("Bob encapsulou um segredo.")

            # Alice decapsula o segredo de Bob
            alice_decapsulated_secret = decapsulate_secret(kem_algorithm, alice_private_key, bob_ciphertext)
            if alice_decapsulated_secret:
                print("Alice decapsulou o segredo.")
                print(f"Segredo compartilhado de Bob: {bob_shared_secret.hex()}")
                print(f"Segredo decapsulado por Alice: {alice_decapsulated_secret.hex()}")
                if bob_shared_secret == alice_decapsulated_secret:
                    print("KEM bem-sucedido: Segredos compartilhados correspondem!")
                else:
                    print("KEM falhou: Segredos não correspondem.")

    # Exemplo de uso para Assinatura Digital
    sig_algorithm = 'Dilithium3'
    print(f"\n--- Testando Assinatura Digital com {sig_algorithm} ---")
    # Carol gera suas chaves de assinatura
    carol_public_key, carol_private_key = generate_signature_keys(sig_algorithm)
    if carol_public_key and carol_private_key:
        print("Carol gerou chaves de assinatura.")

        message_to_sign = b"Esta e uma mensagem secreta para ser assinada."
        # Carol assina a mensagem
        signature = sign_message(sig_algorithm, carol_private_key, message_to_sign)
        if signature:
            print("Carol assinou a mensagem.")

            # Dave verifica a assinatura de Carol
            is_valid = verify_signature(sig_algorithm, carol_public_key, message_to_sign, signature)
            print(f"Assinatura válida: {is_valid}")

            # Teste com mensagem alterada
            altered_message = b"Esta e uma mensagem secreta para ser assinada. Alterada!"
            is_valid_altered = verify_signature(sig_algorithm, carol_public_key, altered_message, signature)
            print(f"Assinatura válida (mensagem alterada): {is_valid_altered}")

            # Teste com assinatura alterada
            altered_signature = signature[:-1] + b'\x00' # Altera o ultimo byte
            is_valid_altered_sig = verify_signature(sig_alg, carol_public_key, message_to_sign, altered_signature)
            print(f"Assinatura válida (assinatura alterada): {is_valid_altered_sig}")

