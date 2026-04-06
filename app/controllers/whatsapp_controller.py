from fastapi import FastAPI, Request
# import pika
# import json
import requests
# import os
from core.config import settings
app = FastAPI()
from rabbitmq_queue import publish_to_queue
from app.utils.whatsapp import send_reply



# ✅ Webhook API (Twilio → FastAPI)
async def whatsapp_webhook(request: Request):
    form_data = await request.form()
    print("Received webhook:", dict(form_data))


    if form_data.get("MessageStatus") in ["delivered", "sent", "read"]:
        print("Ignored status event")
        return {"status": "ignored"}


    if not form_data.get("Body"):
        print("Empty message ignored")
        return {"status": "ignored"}

    user_message = form_data.get("Body")
    from_number = form_data.get("From")

    # print("User message:", user_message)


    # reply_text = f"Hello 👋, you said: {user_message}"
    # send_reply(from_number, reply_text)


    message_data = {
        "from": from_number,
        "to": form_data.get("To"),
        "body": user_message,
        "messageSid": form_data.get("MessageSid"),
        "profileName": form_data.get("ProfileName"),
        "numMedia": form_data.get("NumMedia")
    }

    publish_to_queue(message_data)

    print("Queued:", message_data)

    return {"status": "received"}


# ✅ Send WhatsApp Message API

async def send_whatsapp_message(request: Request):
    data = await request.json()

    to_number = data.get("to")
    message_body = data.get("body")


    url = f"https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json"

    response = requests.post(
        url,
        auth=(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN),
        data={
            "From": f"whatsapp:{settings.TWILIO_PHONE_NUMBER}",
            "To": f"whatsapp:{to_number}",
            "Body": message_body
        }
    )

    if response.status_code == 201:
        return {"status": "message sent"}
    else:
        return {
            "status": "failed",
            "error": response.text
        }
        
async def status_callback(request: Request):
    form_data = await request.form()

    print("Message status:", form_data.get("MessageStatus"))

    return {"status": "received"}




