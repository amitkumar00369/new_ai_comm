from fastapi import APIRouter, Request


from app.controllers.call_controller import voice_webhook, make_async_call, process_voice
voiceRouter: APIRouter = APIRouter()
voiceRouter.post("/webhook")(voice_webhook)
voiceRouter.post("/call")(make_async_call)
voiceRouter.post("/process")(process_voice)
# voiceRouter.post("/reply")(voice_reply)
