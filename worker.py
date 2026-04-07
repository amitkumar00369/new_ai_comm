import pika
import json
from app.utils.whatsapp import send_reply
from app.utils.intent_reply import find_tenant_or_user_by_number

def callback(ch, method, properties, body):
    data = None
    
    if not body:
        print("⚠️ Empty message received, skipping...")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        return
    if body:
        data = json.loads(body)

    user_msg = data.get("body")
    # intent, entity = detect_intent_and_entity(user_msg)
    user_number = data.get("from")
    tenant_number = data.get("to")

    reply = find_tenant_or_user_by_number(user_msg, tenant_number, user_number)
    print("Replying to:", user_number, "with message:", reply)
    send_reply(user_number, reply)

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(
    pika.ConnectionParameters("localhost")
)

channel = connection.channel()
channel.queue_declare(queue="whatsapp_queue")

channel.basic_consume(queue="whatsapp_queue", on_message_callback=callback)

print("🚀 Worker running...")
channel.start_consuming()