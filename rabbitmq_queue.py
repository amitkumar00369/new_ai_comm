import pika
import json

def publish_to_queue(message_data):
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host="localhost")
        )
        channel = connection.channel()

        channel.queue_declare(queue="whatsapp_queue")

        channel.basic_publish(
            exchange="",
            routing_key="whatsapp_queue",
            body=json.dumps(message_data)
        )

        connection.close()

    except Exception as e:
        print("RabbitMQ Error:", str(e))