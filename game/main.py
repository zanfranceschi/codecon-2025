import pygame
import math
from threading import Thread
import multiprocessing
from time import sleep
import random

SCREEN_HEIGHT = 1280 // 2 
SCREEN_WIDTH = 720 // 2

USER_EVENT_MOVE_UP    = 1
USER_EVENT_MOVE_DOWN  = 2
USER_EVENT_MOVE_RIGHT = 3
USER_EVENT_MOVE_LEFT  = 4
USER_EVENT_ROTATE_CW  = 5
USER_EVENT_ROTATE_CCW = 6
USER_EVENT_SHOOT      = 7
USER_EVENT_JOIN       = 8

def get_random_user_event():
    return random.choice(
                [USER_EVENT_MOVE_UP,
                USER_EVENT_MOVE_DOWN,
                USER_EVENT_MOVE_RIGHT,
                USER_EVENT_MOVE_LEFT,
                USER_EVENT_ROTATE_CW,
                USER_EVENT_ROTATE_CCW,
                USER_EVENT_SHOOT])

class Shot(pygame.sprite.Sprite):
    def __init__(self, shooter_id, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10]) 
        self.image.fill("black")
        #self.image.set_colorkey(COLOR)
        #pygame.draw.rect(self.image, "black", pygame.Rect(0, 0, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.velocity = 10
        self.dx = dx
        self.dy = dy
        self.x = x
        self.y = y
        self.shooter_id = shooter_id

    def update(self):
        if (self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT):
            self.kill()
        
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


class LangLogo(pygame.sprite.Sprite):
    
    def __init__(self, id, logo_file, x, y, shots):
        pygame.sprite.Sprite.__init__(self)
        #self.original_image = pygame.image.load('csharp-logo.png')
        self.original_image = pygame.transform.smoothscale_by(
            pygame.image.load(logo_file).convert_alpha(), 0.2)
        #self.original_image.set_colorkey(self.original_image.get_at((0, 0)))
        self.image = self.original_image
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 5
        self.shots = shots
        self.hp = 100
        self.angle = 0
        self.id = id

    def update(self, events):
        keys = pygame.key.get_pressed()
        self.maybe_collide()
        self.maybe_move_from_key(keys)
        self.maybe_rotate_from_key(keys)
        self.maybe_shoot_from_key(keys)
        
        player_events = [e for e in events if e.player_id == self.id]
        self.maybe_move_from_events(player_events)
        self.maybe_rotate_from_events(player_events)
        self.maybe_shoot_from_events(player_events)
        
    def shoot(self):
        angle = math.radians(self.angle * -1)
        dx = math.cos(angle) * self.velocity
        dy = math.sin(angle) * self.velocity
        shot = Shot(self.id, self.rect.centerx, self.rect.centery, dx, dy)
        self.shots.add(shot)
    
    def maybe_shoot_from_key(self, keys):
        if keys[pygame.K_RETURN]:
            self.shoot()

    def maybe_move_from_events(self, events):
        move_events = [e.event for e in events
                        if e.event in [USER_EVENT_MOVE_LEFT,
                                        USER_EVENT_MOVE_RIGHT,
                                        USER_EVENT_MOVE_UP,
                                        USER_EVENT_MOVE_DOWN]]
        for direction in move_events:
            if direction == USER_EVENT_MOVE_LEFT:
                self.rect.x -= self.velocity
            elif direction == USER_EVENT_MOVE_RIGHT:
                self.rect.x += self.velocity
            elif direction == USER_EVENT_MOVE_UP:
                self.rect.y -= self.velocity
            elif direction == USER_EVENT_MOVE_DOWN:
                self.rect.y += self.velocity

    def maybe_rotate_from_events(self, events):
        rotate_events = [e.event for e in events
                        if e.event in [USER_EVENT_ROTATE_CW,
                                        USER_EVENT_ROTATE_CCW]]
        for rotate_event in rotate_events:
            if rotate_event == USER_EVENT_ROTATE_CCW:
                self.angle += 2
            elif rotate_event == USER_EVENT_ROTATE_CW:
                self.angle -= 2
            
            self.angle = self.angle % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center = self.rect.center)

    def maybe_shoot_from_events(self, events):
        shoot_events = [e.event for e in events
                        if e.event == USER_EVENT_SHOOT]
        for _ in shoot_events:
            self.shoot()

    def maybe_move_from_key(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.velocity
        if keys[pygame.K_d]:
            self.rect.x += self.velocity
        if keys[pygame.K_w]:
            self.rect.y -= self.velocity
        if keys[pygame.K_s]:
            self.rect.y += self.velocity
        
    def maybe_rotate_from_key(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 2
        if keys[pygame.K_RIGHT]:
            self.angle -= 2
        
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.angle = self.angle % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center = self.rect.center)
        
    def maybe_collide(self):
        collided_sprites = pygame.sprite.spritecollide(self, self.shots, False)
        if (collided_sprites):
            for collided_sprite in collided_sprites:
                if (not collided_sprite.shooter_id == self.id):
                    collided_sprite.kill()
                    self.hp -= 1
                    print("id", self.id, "HP", self.hp)

# pygame setup
pygame.init()
pygame.display.set_caption('CODECON SUMMIT 2025')
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

logos = pygame.sprite.Group()
shots = pygame.sprite.Group()

lang = LangLogo(1, "csharp-logo.png", 200, 200, shots)
lang.angle = 180
logos.add(lang)

def start_emitting_events():
    while True:
        event1 = pygame.event.Event(pygame.USEREVENT, player_id=1, event=get_random_user_event())
        event2 = pygame.event.Event(pygame.USEREVENT, player_id=2, event=get_random_user_event())
        try:
            pygame.event.post(event1)
            pygame.event.post(event2)
            sleep(0.04)
        except pygame.error as ex:
            exit()

def add_random_player():
    sleep(5)
    event = pygame.event.Event(pygame.USEREVENT, player_id=2, event=USER_EVENT_JOIN)
    pygame.event.post(event)
        
Thread(target = start_emitting_events).start()
Thread(target = add_random_player).start()

while True:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    user_events = [event for event in events if event.type == pygame.USEREVENT]
    for event in events:
        if event.type == pygame.USEREVENT and event.event == USER_EVENT_JOIN:
            print(event)
            lang = LangLogo(event.player_id, "java-logo-small.png", 100, 200, shots)
            logos.add(lang)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    #screen.blit(star.image, star.rect)
    #star.update()

    #screen.blit(logo.image, logo.rect)

    #screen.blit(shot.image, shot.rect)

    logos.update(user_events)
    shots.update()
    
    logos.draw(screen)
    shots.draw(screen)


    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    #dt = clock.tick(60) / 1000
    clock.tick(60) / 1000

pygame.quit()