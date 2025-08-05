# services/billing-service/src/stripe_webhooks.py
# Lógica para processar webhooks do Stripe e atualizar o status de créditos/assinaturas.

import json
import os
from flask import Flask, request, jsonify
import stripe

# from credit_manager import CreditManager # Importar o CreditManager

app = Flask(__name__)

# Configurar sua chave secreta do Stripe
# stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# Configurar o endpoint secreto do webhook (para segurança)
# webhook_secret = os.getenv('STRIPE_WEBHOOK_SECRET')

@app.route('/stripe-webhook', methods=['POST'])
def stripe_webhook():
    payload = request.get_data(as_text=True)
    sig_header = request.headers.get('stripe-signature')

    event = None

    try:
        # event = stripe.Webhook.construct_event(
        #     payload, sig_header, webhook_secret
        # )
        # Simulação de evento para demonstração
        event = json.loads(payload)
        print(f"[StripeWebhook] Evento recebido: {event['type']}")

    except ValueError as e:
        # Invalid payload
        print(f"[StripeWebhook] Erro de payload inválido: {e}")
        return jsonify({'error': 'Invalid payload'}), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f"[StripeWebhook] Erro de verificação de assinatura: {e}")
        return jsonify({'error': 'Invalid signature'}), 400
    except Exception as e:
        print(f"[StripeWebhook] Erro inesperado: {e}")
        return jsonify({'error': 'Internal server error'}), 500

    # Lidar com os tipos de eventos
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        print(f"[StripeWebhook] Checkout Session Completed: {session['id']}")
        # Aqui você adicionaria a lógica para:
        # 1. Obter o user_id associado à sessão (metadata)
        # 2. Obter o produto/plano comprado
        # 3. Chamar o CreditManager para adicionar créditos ou atualizar o status da assinatura
        # user_id = session.metadata.user_id
        # amount_of_credits = get_credits_for_product(session.line_items)
        # credit_manager.add_credits(user_id, amount_of_credits)

    elif event['type'] == 'invoice.payment_succeeded':
        invoice = event['data']['object']
        print(f"[StripeWebhook] Invoice Payment Succeeded: {invoice['id']}")
        # Lógica para renovação de assinatura, etc.

    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        print(f"[StripeWebhook] Customer Subscription Updated: {subscription['id']}")
        # Lógica para lidar com upgrades/downgrades de planos

    # Outros eventos do Stripe podem ser tratados aqui

    return jsonify({'status': 'success'}), 200

if __name__ == '__main__':
    # Para testar localmente, você pode usar o Stripe CLI para encaminhar eventos:
    # stripe listen --forward-to localhost:5000/stripe-webhook
    # E então enviar um evento de teste:
    # stripe trigger checkout.session.completed
    app.run(port=5000)
