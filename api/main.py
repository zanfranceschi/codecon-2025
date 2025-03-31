import pika
import json
from typing import Union

import pika.connection
import pika.exceptions

from fastapi import FastAPI
from pydantic import BaseModel

class EventRequest(BaseModel):
    event: int
    player_id: str
    lang: str | None = None

class MessageBroker(object):
    
    EXCHANGE_NAME = "game.events"
    QUEUE_NAME = "game.events.graphic-unit"

    def __init__(self):
        self.credentials = pika.PlainCredentials('guest', '123')
        self.connection_parameters = pika.ConnectionParameters(
            host="127.0.0.100",
            port=5672,
            credentials=self.credentials)
        self.connection = None
        self.channel = None

    def _ensure_is_connected(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.connection_parameters)
            self.channel = self.connection.channel()
        
        if self.channel is None or self.channel.is_closed:
            self.channel = self.connection.channel()
   
    def _ensure_objects(self):
        self.get_channel().exchange_declare(
            exchange=self.EXCHANGE_NAME,
            exchange_type="fanout")
        self.get_channel().queue_declare(
            queue=self.QUEUE_NAME)
        self.get_channel().queue_bind(
            exchange=self.EXCHANGE_NAME,
            queue=self.QUEUE_NAME)
    
    def get_connection(self):
        self._ensure_is_connected()
        return self.connection

    def get_channel(self):
        self._ensure_is_connected()
        return self.channel
    
    def publish_message(self, message):
        try:
            self.get_channel().basic_publish(
                exchange=self.EXCHANGE_NAME,
                routing_key='',
                body=json.dumps(message))
        except pika.exceptions.ChannelClosedByBroker as ex:
            if "NOT_FOUND" in str(ex):
                self._ensure_objects()
                self.get_channel().basic_publish(
                    exchange=self.EXCHANGE_NAME,
                    routing_key='',
                    body=json.dumps(message))
            else:
                raise ex

app = FastAPI()

msg_broker = MessageBroker()

@app.get("/")
def read_root(event: int):
    event = {"player_id": 1, "event": event}
    msg_broker.publish_message(event)
    return {"Hello": "World"}

@app.post("/events", status_code=202)
def events(event_request: EventRequest):
    msg_broker.publish_message(event_request.model_dump())
    return {"msg": "event received!"}