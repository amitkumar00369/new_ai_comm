import re

import redis
import json
VOICE_EXPIRY = 300
r = redis.Redis(host="localhost", port=6379, db=0)

def save_session(user_number, data):
    r.setex(user_number, 300, json.dumps(data))  # 5 min expiry

def get_session(user_number):
    data = r.get(user_number)
    return json.loads(data) if data else {}

def get_last_message(session_id):
    session = get_session(session_id)


    if not session:
        return None
    # print("sesssss shivam", session)

    return session.get("last_intent")  # 👈 last message
def save_voice_session(call_sid, reply, user_text=None):
    key = f"voice:{call_sid}"

    session = get_voice_session(call_sid)

    # maintain history
    history = session.get("history", [])
    if user_text:
        history.append({"user": user_text, "bot": reply})

    data = {
        "reply": reply,
        "history": history
    }

    r.setex(key, VOICE_EXPIRY, json.dumps(data))
    
def get_voice_session(call_sid):
    key = f"voice:{call_sid}"

    data = r.get(key)
    return json.loads(data) if data else {}

def get_voice_reply(call_sid):
    session = get_voice_session(call_sid)
    return session.get("reply")