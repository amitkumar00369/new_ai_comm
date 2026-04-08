# import pika
# import json

# def publish_to_queue(message_data):
#     try:
#         connection = pika.BlockingConnection(
#             pika.ConnectionParameters(host="localhost")
#         )
#         channel = connection.channel()

#         channel.queue_declare(queue="whatsapp_queue", durable=True)

#         channel.basic_publish(
#             exchange="",
#             routing_key="whatsapp_queue",
#             body=json.dumps(message_data),
#             properties=pika.BasicProperties(
#                 delivery_mode=2  # 🔥 make message persistent
#             )
#         )
#         print("Message published:", message_data)

#         connection.close()

#     except Exception as e:
#         print("RabbitMQ Error:", str(e))


import pika
import json
import threading

class RabbitMQClient:
    _connection = None
    _channel = None
    _lock = threading.Lock()

    @classmethod
    def get_channel(cls):
        with cls._lock:
            if cls._connection is None or cls._connection.is_closed:
                print("🔄 Connecting to RabbitMQ...")

                cls._connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host="localhost",
                        heartbeat=600,
                        blocked_connection_timeout=300
                    )
                )

                cls._channel = cls._connection.channel()

                cls._channel.queue_declare(
                    queue="whatsapp_queue",
                    durable=True
                )

            return cls._channel

    @classmethod
    def publish(cls, message_data):
        try:
            channel = cls.get_channel()

            if channel.is_closed:
                print("⚠️ Channel closed, reconnecting...")
                cls._connection = None
                channel = cls.get_channel()

            channel.basic_publish(
                exchange="",
                routing_key="whatsapp_queue",
                body=json.dumps(message_data),
                properties=pika.BasicProperties(delivery_mode=2)
            )

            print("✅ Published:", message_data)

        except Exception as e:
            print("❌ RabbitMQ Error:", str(e))
        
RabitMqService = RabbitMQClient()