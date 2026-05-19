

from fastapi import FastAPI, Request
# import pika
# import json
import asyncio
from fastapi.concurrency import run_in_threadpool
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
import requests
from starlette.responses import JSONResponse
from sqlalchemy import JSON
# import os
from app.services.call_service import background_tasks
from app.utils.redis_session import get_voice_reply
from core.config import settings
app = FastAPI()
from rabbitmq_queue import RabbitMQClient
from fastapi.concurrency import run_in_threadpool
from app.utils.whatsapp import send_reply
from twilio.rest import Client
from core.config import settings
from app.utils.process_voice import process_voice_logic
def publish_async(message_data):
    RabbitMQClient.publish_call(message_data)

from fastapi import  Response
async def voice_webhook(request: Request):
    return Response(content="""
    <Response>
        <Say>Welcome Amit, please say something</Say>
        <Gather input="speech" action="/api/v1/voice/process" method="POST"/>
    </Response>
    """, media_type="application/xml")



async def make_async_call(data: dict):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    try:
        payload = jsonable_encoder(data)
        call = client.calls.create(
            to=payload["to"],
            from_=settings.TWILLIO_CALL_NUMBER,
            url="https://unsafetied-overfamiliar-kyra.ngrok-free.dev/api/v1/voice/webhook"
        )
        print(call.sid)
        return JSONResponse(content={"message": "Call initiated successfully"}, status_code=200)
    except Exception as e:

        return JSONResponse(content={"error": "Failed to initiate call","message": str(e)}, status_code=500)          
# async def process_voice(request: Request):
#     form = await request.form()
#     caller_number = form.get("From")   # 👈 WHO is callin
#     twilio_number = form.get("To")     # 👈 Your Twilio number
#     call_sid = form.get("CallSid")
#     print("Incoming call from:", caller_number)
#     print("Twilio number:", twilio_number)
#     print("Call SID:", call_sid)

#     speech = form.get("SpeechResult")

#     print("User said:", speech)

#     # ✅ 1. Instant processing (FAST)
#     reply = process_voice_logic(speech)

#     # ✅ 2. Save in Redis (optional)
#     from app.utils.redis_session import save_voice_session
#     save_voice_session(call_sid, reply, speech)

#     # ✅ 3. Background queue (optional)
#     message_data = {
#         "type": "voice",
#         "call_sid": call_sid,
#         "text": speech
#     }

#     await run_in_threadpool(
#         RabbitMQClient.publish_call,
#         message_data
#     )

#     # ✅ 4. Immediate Twilio response (IMPORTANT)
#     return Response(content=f"""
# <Response>
#     <Say voice="alice" language="en-IN">
#         {reply}
#     </Say>

#     <Pause length="1"/>

#     <Gather input="speech"
#             timeout="3"
#             speechTimeout="auto"
#             action="/api/v1/voice/process"
#             method="POST">
#     </Gather>

#     <!-- Fallback if no speech -->
#     <Say voice="alice" language="en-IN">
#         I didn’t catch that. Let me repeat.
#     </Say>

#     <Redirect method="POST">
#         /api/v1/voice/process
#     </Redirect>
# </Response>
# """, media_type="application/xml")
    


import asyncio

async def process_voice(request: Request):
    form = await request.form()

    speech = form.get("SpeechResult")
    caller_number = form.get("From")   # 👈 WHO is callin
    twilio_number = form.get("To")     # 👈 Your Twilio number
    call_sid = form.get("CallSid")
    print("Incoming call from:", caller_number)
    print("Twilio number:", twilio_number)
    print("Call SID:", call_sid)

    print(f"[{call_sid}] User:", speech)

    # ⚡ FAST LOGIC (must be instant)
    reply = process_voice_logic(speech)

    # ⚡ RETURN RESPONSE IMMEDIATELY
    response = Response(content=f""" <Response> <Say voice="alice" language="en-IN"> {reply} </Say> <Pause length="1"/> <Gather input="speech" timeout="3" speechTimeout="auto" action="/api/v1/voice/process" method="POST"> </Gather> <!-- Fallback if no speech --> <Say voice="alice" language="en-IN"> I didn’t catch that. Let me repeat. </Say> <Redirect method="POST"> /api/v1/voice/process </Redirect> </Response> """, media_type="application/xml")

    # 🔥 BACKGROUND TASKS (DO NOT BLOCK)
    asyncio.create_task(background_tasks(call_sid, speech, reply))

    return response
