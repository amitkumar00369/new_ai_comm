
from fastapi.responses import JSONResponse
from starlette.responses import JSONResponse
from fastapi import FastAPI, Request, HTTPException
app = FastAPI()
from starlette import status
from app.services.stripe_service import stripe_service
import stripe
from core.config import settings
from app.schemas.stripe_schema import CreateUser
from fastapi.concurrency import run_in_threadpool




async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        # Invalid payload
        print("Invalid payload")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print("Invalid signature")
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST)

    # Handle the event account created and customer created
    # print("arjun ", event)
    if event["type"] == "account.created":
        account = event["data"]["object"]
        print(f"Account created: {account['id']}")
    elif event["type"] == "customer.created":
        customer = event["data"]["object"]
        print(f"Customer created: {customer['id']} and details is  {event}")
    elif event["type"] == "payment_intent.succeeded":
        payment_intent = event["data"]["object"]
        print("PaymentIntent was successful!")
    elif event["type"] == "charge.succeeded":
        charge = event["data"]["object"]
        print("Charge was successful!")
    else:
        print(f"Unhandled event type {event['type']}")

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "Webhook received"})


async def create_stripe_customer(data: CreateUser):
    try:
        result = stripe_service.create_customer(data.dict())

        return {
            "status": "success",
            "customer_id": result.id
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
    