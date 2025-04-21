import pygame
import pika
import json
import logging
import os
from threading import Thread

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def start_consuming():
    credentials = pika.PlainCredentials(
        os.getenv('RABBITMQ_USER', 'guest'),
        os.getenv('RABBITMQ_PASSWORD', 'guest')
    )
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', 'localhost'),
            port=os.getenv('RABBITMQ_PORT', 5672),
            credentials=credentials
        )
    )

    exchange_name = "game.events"
    queue_name = "game.events.graphic-unit"

    channel = connection.channel()

    channel.exchange_declare(exchange=exchange_name, exchange_type="fanout", durable=True)

    channel.queue_declare(queue=queue_name, durable=True)

    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    def callback(ch, method, properties, body):
        logger.info(body.decode())
        event = json.loads(body.decode())
        pygame_event = pygame.event.Event(pygame.USEREVENT, event)
        pygame.event.post(pygame_event)

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True,
    )
    channel.start_consuming()

def start_async():
    logger.info("Iniciando daemon...")
    Thread(target = start_consuming).start()
