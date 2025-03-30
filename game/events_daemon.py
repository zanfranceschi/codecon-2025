import pygame
import pika
import json

from threading import Thread

def _start_consuming():
    credentials = pika.PlainCredentials('guest', '123')
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="127.0.0.100", port=5672, credentials=credentials),
    )

    exchange_name = "game.events"
    queue_name = "game.events.graphic-unit"

    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

    channel.queue_declare(queue=queue_name)

    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    def callback(ch, method, properties, body):
        print(f" [x] {body.decode()}")
        event = json.loads(body.decode())
        pygame_event = pygame.event.Event(pygame.USEREVENT, event)
        pygame.event.post(pygame_event)

    print("[*] Waiting for logs. To exit press CTRL+C")
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True,
    )
    channel.start_consuming()

def start_async():
    Thread(target = _start_consuming).start()
