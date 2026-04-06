from fastapi import APIRouter, Request


from app.controllers.whatsapp_controller import whatsapp_webhook, send_whatsapp_message, status_callback
whatsappRouter: APIRouter = APIRouter()
whatsappRouter.post("/send")(send_whatsapp_message)
whatsappRouter.post("/getMessageByWebhook")(whatsapp_webhook)
whatsappRouter.post("/status")(status_callback)