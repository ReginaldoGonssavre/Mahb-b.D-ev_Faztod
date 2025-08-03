from fastapi import FastAPI, Request, Header
from fastapi.responses import FileResponse
import stripe
import os

stripe.api_key = os.getenv("STRIPE_API_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

app = FastAPI()

@app.get("/")
async def read_root():
    return FileResponse('index.html')

@app.get("/success")
async def read_success():
    return FileResponse('success.html')

@app.get("/cancel")
async def read_cancel():
    return FileResponse('cancel.html')

@app.post("/create-checkout-session")
async def create_checkout_session():
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'T-shirt',
                },
                'unit_amount': 2000,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    return {"id": session.id}

@app.post("/webhook")
async def webhook(request: Request, stripe_signature: str = Header(None)):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=stripe_signature, secret=webhook_secret
        )
    except ValueError as e:
        # Invalid payload
        return {"status": "invalid payload"}
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return {"status": "invalid signature"}

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        # Fulfill the purchase...
        print("Payment was successful.")
        print(session)

    return {"status": "success"}