from fastapi import Request
from redis_session import get_voice_reply
from fastapi.responses import Response

async def voice_reply(request: Request):
    form = await request.form()
    call_sid = form.get("CallSid")

    reply = get_voice_reply(call_sid)

    if not reply:
        reply = "Please wait, processing your request"

    return Response(content=f"""
    <Response>
        <Say>{reply}</Say>
        <Gather input="speech" action="/api/v1/voice/process"/>
    </Response>
    """, media_type="application/xml")