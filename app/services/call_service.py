from rabbitmq_queue import RabbitMQClient


async def background_tasks(call_sid, speech, reply):
    try:
        from app.utils.redis_session import save_voice_session

        # Redis
        save_voice_session(call_sid, reply, speech)

        # Queue (no await!)
        RabbitMQClient.publish_call({
            "call_sid": call_sid,
            "text": speech
        })

    except Exception as e:
        print("Background error:", e)