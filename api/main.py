import os
from typing import AsyncGenerator
import aio_pika
from aio_pika.abc import AbstractConnection, AbstractChannel
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json

class EventRequest(BaseModel):
    event: int
    player_id: str
    lang: str | None = None

class RabbitMQConfig:
    EXCHANGE_NAME = "game.events"
    QUEUE_NAME = "game.events.graphic-unit"
    
    @classmethod
    def get_connection_url(cls) -> str:
        return f"amqp://{os.getenv('RABBITMQ_USER', 'guest')}:{os.getenv('RABBITMQ_PASSWORD', '123')}@{os.getenv('RABBITMQ_HOST', 'localhost')}:{os.getenv('RABBITMQ_PORT', 5672)}"

async def get_rabbitmq_connection() -> AsyncGenerator[AbstractConnection, None]:
    connection = await aio_pika.connect_robust(
        RabbitMQConfig.get_connection_url(),
        timeout=5,
        heartbeat=30
    )
    try:
        yield connection
    finally:
        await connection.close()

async def get_rabbitmq_channel(connection: AbstractConnection = Depends(get_rabbitmq_connection)) -> AsyncGenerator[AbstractChannel, None]:
    async with connection.channel() as channel:
        # Declare exchange and queue
        exchange = await channel.declare_exchange(
            RabbitMQConfig.EXCHANGE_NAME,
            aio_pika.ExchangeType.FANOUT,
            durable=True
        )
        queue = await channel.declare_queue(
            RabbitMQConfig.QUEUE_NAME,
            durable=True
        )
        await queue.bind(exchange)
        yield channel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root(event: int, channel: AbstractChannel = Depends(get_rabbitmq_channel)):
    message = {"player_id": 1, "event": event}
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(message).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key=RabbitMQConfig.QUEUE_NAME
    )
    return {"Hello": "World"}

@app.post("/events", status_code=202)
async def events(event_request: EventRequest, channel: AbstractChannel = Depends(get_rabbitmq_channel)):
    await channel.default_exchange.publish(
        aio_pika.Message(
            body=json.dumps(event_request.model_dump()).encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        ),
        routing_key=RabbitMQConfig.QUEUE_NAME
    )
    return {"msg": "event received!"}
