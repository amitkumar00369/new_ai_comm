import pika
import json
from app.utils.redis_session import save_voice_session
from app.utils.process_voice import process_voice_logic
# 🔥 Voice processing logic



def callback(ch, method, properties, body):
    try:
        if not body:
            print("⚠️ Empty message, skipping...")
            return

        data = json.loads(body)

        call_sid = data.get("call_sid")
        speech_text = data.get("text")

        print("\n📞 Voice Input")
        print("CallSid:", call_sid)
        print("User said:", speech_text)

        # 🔥 Process logic
        reply = process_voice_logic(speech_text)

        # 🔥 Store in Redis (IMPORTANT)
        save_voice_session(call_sid, reply, speech_text)

        print("🎤 Reply:", reply)

    except Exception as e:
        print("❌ Error:", str(e))

    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


# 🔗 RabbitMQ connection
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

# ✅ Use correct queue name
channel.queue_declare(queue="call_queue", durable=True)

# ✅ Fair dispatch
channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue="call_queue",
    on_message_callback=callback
)

print("🚀 Voice Worker running...")
channel.start_consuming()