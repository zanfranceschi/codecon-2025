import pygame
import pygame.freetype
import math
from threading import Thread
import multiprocessing
from time import sleep
import random
import io

SCREEN_HEIGHT = 720 // 1
SCREEN_WIDTH = 1280 // 1

USER_EVENT_MOVE_UP    = 1
USER_EVENT_MOVE_DOWN  = 2
USER_EVENT_MOVE_RIGHT = 3
USER_EVENT_MOVE_LEFT  = 4
USER_EVENT_ROTATE_CW  = 5
USER_EVENT_ROTATE_CCW = 6
USER_EVENT_SHOOT      = 7
USER_EVENT_JOIN       = 8

logo_spacing = 155
logo_size = 155

sprites =  {
    "logo-ruby":    (logo_spacing * 0, logo_spacing * 0, logo_size, logo_size),
    "logo-kotlin":  (logo_spacing * 1, logo_spacing * 0, logo_size, logo_size),
    "logo-f#":      (logo_spacing * 2, logo_spacing * 0, logo_size, logo_size),
    "logo-cobol":   (logo_spacing * 3, logo_spacing * 0, logo_size, logo_size),
    "logo-go":      (logo_spacing * 4, logo_spacing * 0, logo_size, logo_size),

    "logo-lua":     (logo_spacing * 0, logo_spacing * 1, logo_size, logo_size),
    "logo-elixir":  (logo_spacing * 1, logo_spacing * 1, logo_size, logo_size),
    "logo-c++":     (logo_spacing * 2, logo_spacing * 1, logo_size, logo_size),
    "logo-c#":      (logo_spacing * 3, logo_spacing * 1, logo_size, logo_size),
    "logo-js":      (logo_spacing * 4, logo_spacing * 1, logo_size, logo_size),

    "logo-dart":    (logo_spacing * 0, logo_spacing * 2, logo_size, logo_size),
    "logo-php":     (logo_spacing * 1, logo_spacing * 2, logo_size, logo_size),
    "logo-groovy":  (logo_spacing * 2, logo_spacing * 2, logo_size, logo_size),
    "logo-cobol":   (logo_spacing * 3, logo_spacing * 2, logo_size, logo_size),
    "logo-scala":   (logo_spacing * 4, logo_spacing * 2, logo_size, logo_size),

    "logo-r":       (logo_spacing * 0, logo_spacing * 3, logo_size, logo_size),
    "logo-ts":      (logo_spacing * 1, logo_spacing * 3, logo_size, logo_size),
    "logo-ocaml":   (logo_spacing * 2, logo_spacing * 3, logo_size, logo_size),
    "logo-clojure": (logo_spacing * 3, logo_spacing * 3, logo_size, logo_size),
    "logo-elm":     (logo_spacing * 4, logo_spacing * 3, logo_size, logo_size),

    "logo-python":  (logo_spacing * 0, logo_spacing * 4, logo_size, logo_size),
    "logo-zig":     (logo_spacing * 1, logo_spacing * 4, logo_size, logo_size),
    "logo-swift":   (logo_spacing * 2, logo_spacing * 4, logo_size, logo_size),
    "logo-java":    (logo_spacing * 3, logo_spacing * 4, logo_size, logo_size),
    "logo-rust":    (logo_spacing * 4, logo_spacing * 4, logo_size, logo_size),

    "logo-erlang":  (logo_spacing * 0, logo_spacing * 5, logo_size, logo_size),
}

def get_random_user_event():
    return random.choice(
                [USER_EVENT_MOVE_UP,
                USER_EVENT_MOVE_DOWN,
                USER_EVENT_MOVE_RIGHT,
                USER_EVENT_MOVE_LEFT,
                USER_EVENT_ROTATE_CW,
                USER_EVENT_ROTATE_CCW,
                USER_EVENT_SHOOT])

class SpritesSheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("spritessheet.png").convert()
        
    def image_at(self, rectangle):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        colorkey = (255, 255, 255, 255)
        image.set_colorkey(colorkey)
        image.blit(self.sheet, (0, 0), rect)
        return image

class Shot(pygame.sprite.Sprite):
    def __init__(self, shooter_id, x, y, dx, dy):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([10, 10]) 
        self.image.fill("black")
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
    
    def __init__(self, id, logo, x, y, shots):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = SpritesSheet().image_at(sprites[logo])
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 5
        self.shots = shots
        self.hp = 100
        self.angle = 0
        self.id = id

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.image)

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
        self.maybe_limit_movement()

        self.update_mask()
        
        if self.hp < 1:
            self.kill()
        
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

    def maybe_limit_movement(self):
        if self.rect.y + self.rect.h > SCREEN_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - self.rect.h

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.x + self.rect.w > SCREEN_WIDTH:
            self.rect.x = SCREEN_WIDTH - self.rect.w

        if self.rect.x < 0:
            self.rect.x = 0

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
        collided_sprites = pygame.sprite.spritecollide(self, self.shots, False, pygame.sprite.collide_mask)
        if (collided_sprites):
            for collided_sprite in collided_sprites:
                if (not collided_sprite.shooter_id == self.id):
                    collided_sprite.kill()
                    self.hp -= 1


pygame.freetype.init()
game_font = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 15)

class Text(pygame.sprite.Sprite):
    def __init__(self, screen, logo):
        pygame.sprite.Sprite.__init__(self)
        self.font = game_font
        self.screen = screen
        self.logo = logo

    def update(self, events):
        ratio = 3
        life = self.logo.hp // ratio
        spaces = 100 // ratio - life
        life_chars = "|" * life
        space_chars = "." * spaces
        life_bar = f"[{ life_chars + space_chars }] - {self.logo.hp}%"
        self.image, self.rect = self.font.render(life_bar, "black", rotation=0)
        new_x = (self.logo.rect.x + self.logo.rect.w // 2) - self.rect.w // 2
        new_y = self.logo.rect.y + self.logo.rect.h + 2
        self.rect = (new_x, new_y)
        if self.logo.hp < 1:
            self.kill()

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

lang = LangLogo(1, "logo-c#", 200, 200, shots)
lang.angle = 0
texto = Text(screen, lang)
logos.add(lang)
logos.add(texto)

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
    while True:
        event = pygame.event.Event(pygame.USEREVENT, player_id=2, event=USER_EVENT_JOIN)
        pygame.event.post(event)
        sleep(60)
        
Thread(target = start_emitting_events).start()
Thread(target = add_random_player).start()


bg = pygame.image.load('backgrounds/12984081_5130888.svg')

while True:
    events = pygame.event.get()
    user_events = [event for event in events if event.type == pygame.USEREVENT]
    for event in events:
        if event.type == pygame.USEREVENT and event.event == USER_EVENT_JOIN:
            x = random.randint(0, SCREEN_WIDTH - 150)
            y = random.randint(0, SCREEN_HEIGHT - 150)
            angle = random.randint(0, 359)
            logo_img = random.choice(list(sprites))
            lang = LangLogo(event.player_id, logo_img, x, y, shots)
            lang.angle = angle
            texto = Text(screen, lang)
            logos.add(lang)
            logos.add(texto)
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    # fill the screen with a color to wipe away anything from last frame
    #screen.fill("white")
    screen.blit(bg, (0, 0))

    #screen.blit(star.image, star.rect)
    #star.update()

    #screen.blit(logo.image, logo.rect)

    #screen.blit(shot.image, shot.rect)

    shots.update()
    logos.update(user_events)
    
    shots.draw(screen)
    logos.draw(screen)
    
    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    # dt is delta time in seconds since last frame
    dt = clock.tick(60) / 1000

pygame.quit()