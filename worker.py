import pika
import json
from app.utils.whatsapp import send_reply
from app.utils.intent_reply import find_tenant_or_user_by_number

# Dedup store (temporary memory)
processed_messages = set()


def is_duplicate(message_sid):
    if message_sid in processed_messages:
        return True
    processed_messages.add(message_sid)
    return False


def callback(ch, method, properties, body):
    try:
        if not body:
            print("⚠️ Empty message received, skipping...")
            return

        data = json.loads(body)

        message_sid = data.get("messageSid")

        #  Dedup check
        if message_sid and is_duplicate(message_sid):
            print("⚠️ Duplicate message ignored:", message_sid)
            return

        user_msg = data.get("body")
        user_number = data.get("from")
        tenant_number = data.get("to")

        # print("\n📩 New Message")
        # print("User:", user_number)
        # print("Message:", user_msg)

        reply = find_tenant_or_user_by_number(
            user_msg, tenant_number, user_number
        )

        # 🔥 fallback reply (VERY IMPORTANT)
        if not reply:
            reply = "😅 Sorry, I didn't understand, please tell me again."

        print(" Reply:", reply)

        send_reply(user_number, reply)

    except Exception as e:
        print("❌ Error processing message:", str(e))

    finally:
        # ALWAYS ACK (IMPORTANT)
        ch.basic_ack(delivery_tag=method.delivery_tag)


# Connection setup
connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()

#  Durable queue (IMPORTANT)
channel.queue_declare(queue="whatsapp_queue", durable=True)

#  Fair dispatch (one message per worker)
channel.basic_qos(prefetch_count=1)

channel.basic_consume(
    queue="whatsapp_queue",
    on_message_callback=callback
)

print("🚀 Worker running...")
channel.start_consuming()