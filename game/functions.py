import pygame
import random
import configs

from time import sleep

def _get_random_user_event():
    return random.choice(
                [configs.USER_EVENT_MOVE_UP,
                configs.USER_EVENT_MOVE_DOWN,
                configs.USER_EVENT_MOVE_RIGHT,
                configs.USER_EVENT_MOVE_LEFT,
                configs.USER_EVENT_ROTATE_CW,
                configs.USER_EVENT_ROTATE_CCW,
                configs.USER_EVENT_SHOOT])

def start_emitting_events():
    while False:
        event1 = pygame.event.Event(pygame.USEREVENT, {"player_id": 1, "event": _get_random_user_event()})
        event2 = pygame.event.Event(pygame.USEREVENT, {"player_id": 2, "event": _get_random_user_event()})
        try:
            pygame.event.post(event1)
            pygame.event.post(event2)
            sleep(0.04)
        except pygame.error as ex:
            exit()

def add_random_player():
    while False:
        event = pygame.event.Event(pygame.USEREVENT, player_id=2, event=configs.USER_EVENT_JOIN)
        pygame.event.post(event)
        sleep(60)
