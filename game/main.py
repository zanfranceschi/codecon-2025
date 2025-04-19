import pygame
import pygame.freetype
import random

import pygame.locals
import configs
import sprites
import functions
import events_daemon

from threading import Thread


# pygame setup
pygame.init()
pygame.display.set_caption('CODECON SUMMIT 2025')
screen = pygame.display.set_mode((configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT), pygame.locals.RESIZABLE)
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

logos = pygame.sprite.Group()
shots = pygame.sprite.Group()

lang = sprites.LangLogo(1, "logo-c#", 200, 200, shots)
lang.angle = 0
texto = sprites.Text(screen, lang)
#logos.add(lang)
#logos.add(texto)

Thread(target = functions.start_emitting_events).start()
Thread(target = functions.add_random_player).start()

events_daemon.start_async()

bg = pygame.image.load('images/background-01.jpg')

players = []

while True:
    events = pygame.event.get()
    configs.user_events = [event for event in events if event.type == pygame.USEREVENT]
    for event in events:
        if event.type == pygame.WINDOWRESIZED:
            configs.SCREEN_WIDTH, configs.SCREEN_HEIGHT = screen.get_width(), screen.get_height()
        if event.type == pygame.USEREVENT and event.event == configs.USER_EVENT_JOIN and event.lang is not None:
            if event.player_id not in players:
                players.append(event.player_id)
                x = random.randint(0, configs.SCREEN_WIDTH - 150)
                y = random.randint(0, configs.SCREEN_HEIGHT - 150)
                logo_img = f"logo-{event.lang}"
                lang = sprites.LangLogo(event.player_id, logo_img, x, y, shots)
                texto = sprites.Text(screen, lang)
                logos.add(lang)
                logos.add(texto)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")
    #screen.blit(bg, (0, 0))

    #screen.blit(star.image, star.rect)
    #star.update()

    #screen.blit(logo.image, logo.rect)

    #screen.blit(shot.image, shot.rect)

    shots.update()
    logos.update(configs.user_events)
    
    shots.draw(screen)
    logos.draw(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame
    dt = clock.tick(60) / 1000

pygame.quit()