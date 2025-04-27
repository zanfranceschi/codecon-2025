import pygame
import pygame.freetype
import math
import configs

LOGO_SPACING = 155
LOGO_SIZE = 150

sprites =  {
    "logo-ruby":       (LOGO_SPACING * 0, LOGO_SPACING * 0, LOGO_SIZE, LOGO_SIZE),
    "logo-kotlin":     (LOGO_SPACING * 1, LOGO_SPACING * 0, LOGO_SIZE, LOGO_SIZE),
    "logo-fsharp":     (LOGO_SPACING * 2, LOGO_SPACING * 0, LOGO_SIZE, LOGO_SIZE),
    "logo-cobol":      (LOGO_SPACING * 3, LOGO_SPACING * 0, LOGO_SIZE, LOGO_SIZE),
    "logo-go":         (LOGO_SPACING * 4, LOGO_SPACING * 0, LOGO_SIZE, LOGO_SIZE),

    "logo-lua":        (LOGO_SPACING * 0, LOGO_SPACING * 1, LOGO_SIZE, LOGO_SIZE),
    "logo-elixir":     (LOGO_SPACING * 1, LOGO_SPACING * 1, LOGO_SIZE, LOGO_SIZE),
    "logo-cpp":        (LOGO_SPACING * 2, LOGO_SPACING * 1, LOGO_SIZE, LOGO_SIZE),
    "logo-csharp":     (LOGO_SPACING * 3, LOGO_SPACING * 1, LOGO_SIZE, LOGO_SIZE),
    "logo-javascript": (LOGO_SPACING * 4, LOGO_SPACING * 1, LOGO_SIZE, LOGO_SIZE),

    "logo-dart":       (LOGO_SPACING * 0, LOGO_SPACING * 2, LOGO_SIZE, LOGO_SIZE),
    "logo-php":        (LOGO_SPACING * 1, LOGO_SPACING * 2, LOGO_SIZE, LOGO_SIZE),
    "logo-groovy":     (LOGO_SPACING * 2, LOGO_SPACING * 2, LOGO_SIZE, LOGO_SIZE),
    "logo-delphi":     (LOGO_SPACING * 3, LOGO_SPACING * 2, LOGO_SIZE, LOGO_SIZE),
    "logo-scala":      (LOGO_SPACING * 4, LOGO_SPACING * 2, LOGO_SIZE, LOGO_SIZE),

    "logo-r":          (LOGO_SPACING * 0, LOGO_SPACING * 3, LOGO_SIZE, LOGO_SIZE),
    "logo-typescript": (LOGO_SPACING * 1, LOGO_SPACING * 3, LOGO_SIZE, LOGO_SIZE),
    "logo-ocaml":      (LOGO_SPACING * 2, LOGO_SPACING * 3, LOGO_SIZE, LOGO_SIZE),
    "logo-clojure":    (LOGO_SPACING * 3, LOGO_SPACING * 3, LOGO_SIZE, LOGO_SIZE),
    "logo-elm":        (LOGO_SPACING * 4, LOGO_SPACING * 3, LOGO_SIZE, LOGO_SIZE),

    "logo-python":     (LOGO_SPACING * 0, LOGO_SPACING * 4, LOGO_SIZE, LOGO_SIZE),
    "logo-zig":        (LOGO_SPACING * 1, LOGO_SPACING * 4, LOGO_SIZE, LOGO_SIZE),
    "logo-swift":      (LOGO_SPACING * 2, LOGO_SPACING * 4, LOGO_SIZE, LOGO_SIZE),
    "logo-java":       (LOGO_SPACING * 3, LOGO_SPACING * 4, LOGO_SIZE, LOGO_SIZE),
    "logo-rust":       (LOGO_SPACING * 4, LOGO_SPACING * 4, LOGO_SIZE, LOGO_SIZE),

    "logo-erlang":     (LOGO_SPACING * 0, LOGO_SPACING * 5, LOGO_SIZE, LOGO_SIZE),
}

pygame.freetype.init()
GAME_FONT = pygame.freetype.SysFont(pygame.freetype.get_default_font(), 15)

class SpritesSheet(object):
    def __init__(self):
        self.sheet = pygame.image.load("images/spritessheet.png").convert()
        
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
        self.speed_multiplier = 2
        self.dx = dx * self.speed_multiplier
        self.dy = dy * self.speed_multiplier
        self.x = x
        self.y = y
        self.shooter_id = shooter_id

    def update(self):
        if (self.rect.x > configs.SCREEN_WIDTH or self.rect.y > configs.SCREEN_HEIGHT):
            self.kill()
        
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

class LangLogo(pygame.sprite.Sprite):

    @classmethod
    def valid_lang(cls, logo):
        return logo in sprites
    
    def __init__(self, id, logo, x, y, angle, shots, death_declaration):
        pygame.sprite.Sprite.__init__(self)
        self.original_image = SpritesSheet().image_at(sprites[logo])
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center = (x, y))
        self.velocity = 5
        self.shots = shots
        self.hp = 100
        self.angle = angle
        self.id = id
        self.is_moving = False
        self.moving_direction = None
        self.is_rotating = False
        self.rotating_direction = None
        self.death_declaration = death_declaration
        self.rotate()

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
        self.maybe_stop_moving(player_events)   
        self.maybe_stop_rotating(player_events)
        self.maybe_change_movement_direction(player_events)
        self.maybe_change_rotation_direction(player_events)
        self.maybe_continue_moving()
        self.maybe_continue_rotating()
        self.update_mask()
        
        if self.hp < 1:
            self.death_declaration.declare_death(self.id)
            self.kill()
    
    def maybe_stop_moving(self, events):
        stop_moving_events = [e.event for e in events
                        if e.event == configs.USER_EVENT_STOP_MOVING]
        
        if stop_moving_events:
            self.is_moving = False

    def maybe_stop_rotating(self, events):
        stop_rotating_events = [e.event for e in events
                        if e.event == configs.USER_EVENT_STOP_ROTATING]
        
        if stop_rotating_events:
            self.is_rotating = False

    def maybe_continue_moving(self):
        if self.is_moving:
            if self.moving_direction == "UP":
                self.rect.y -= self.velocity
            elif self.moving_direction == "UP_RIGHT":
                self.rect.y -= self.velocity
                self.rect.x += self.velocity
            elif self.moving_direction == "RIGHT":
                self.rect.x += self.velocity
            elif self.moving_direction == "DOWN_RIGHT":
                self.rect.y += self.velocity
                self.rect.x += self.velocity
            elif self.moving_direction == "DOWN":
                self.rect.y += self.velocity
            elif self.moving_direction == "DOWN_LEFT":
                self.rect.y += self.velocity
                self.rect.x -= self.velocity
            elif self.moving_direction == "LEFT":
                self.rect.x -= self.velocity
            elif self.moving_direction == "UP_LEFT":
                self.rect.y -= self.velocity
                self.rect.x -= self.velocity
    
    def rotate(self):
        self.angle = self.angle % 360
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center = self.rect.center)

    def maybe_continue_rotating(self):
        if self.is_rotating:
            if self.rotating_direction == "CW":
                self.angle -= 2
            elif self.rotating_direction == "CCW":
                self.angle += 2
            self.rotate()

    def maybe_change_movement_direction(self, events):
        change_direction_events = [e.event for e in events
                        if e.event in [configs.USER_EVENT_START_MOVING_UP         ,
                                       configs.USER_EVENT_START_MOVING_UP_RIGHT   ,
                                       configs.USER_EVENT_START_MOVING_RIGHT      ,
                                       configs.USER_EVENT_START_MOVING_DOWN_RIGHT ,
                                       configs.USER_EVENT_START_MOVING_DOWN       ,
                                       configs.USER_EVENT_START_MOVING_DOWN_LEFT  ,
                                       configs.USER_EVENT_START_MOVING_LEFT       ,
                                       configs.USER_EVENT_START_MOVING_UP_LEFT    ]]
        
        if change_direction_events:
            self.is_moving = True

        for direction in change_direction_events:
            if direction == configs.USER_EVENT_START_MOVING_UP:
                self.moving_direction = "UP"
            elif direction == configs.USER_EVENT_START_MOVING_UP_RIGHT:
                self.moving_direction = "UP_RIGHT"
            elif direction == configs.USER_EVENT_START_MOVING_RIGHT:
                self.moving_direction = "RIGHT"
            elif direction == configs.USER_EVENT_START_MOVING_DOWN_RIGHT:
                self.moving_direction = "DOWN_RIGHT"
            elif direction == configs.USER_EVENT_START_MOVING_DOWN:
                self.moving_direction = "DOWN"
            elif direction == configs.USER_EVENT_START_MOVING_DOWN_LEFT:
                self.moving_direction = "DOWN_LEFT"
            elif direction == configs.USER_EVENT_START_MOVING_LEFT:
                self.moving_direction = "LEFT"
            elif direction == configs.USER_EVENT_START_MOVING_UP_LEFT:
                self.moving_direction = "UP_LEFT"

    def maybe_change_rotation_direction(self, events):
        change_direction_events = [e.event for e in events
                        if e.event in [configs.USER_EVENT_START_ROTATING_CW  ,
                                       configs.USER_EVENT_START_ROTATING_CCW ]]
        
        if change_direction_events:
            self.is_rotating = True

        for direction in change_direction_events:
            if direction == configs.USER_EVENT_START_ROTATING_CW:
                self.rotating_direction = "CW"
            elif direction == configs.USER_EVENT_START_ROTATING_CCW:
                self.rotating_direction = "CCW"

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
                        if e.event in [configs.USER_EVENT_MOVE_LEFT,
                                        configs.USER_EVENT_MOVE_RIGHT,
                                        configs.USER_EVENT_MOVE_UP,
                                        configs.USER_EVENT_MOVE_DOWN]]
        for direction in move_events:
            if direction == configs.USER_EVENT_MOVE_LEFT:
                self.rect.x -= self.velocity
            elif direction == configs.USER_EVENT_MOVE_RIGHT:
                self.rect.x += self.velocity
            elif direction == configs.USER_EVENT_MOVE_UP:
                self.rect.y -= self.velocity
            elif direction == configs.USER_EVENT_MOVE_DOWN:
                self.rect.y += self.velocity

    def maybe_limit_movement(self):
        if self.rect.y + self.rect.h > configs.SCREEN_HEIGHT:
            self.rect.y = configs.SCREEN_HEIGHT - self.rect.h

        if self.rect.y < 0:
            self.rect.y = 0

        if self.rect.x + self.rect.w > configs.SCREEN_WIDTH:
            self.rect.x = configs.SCREEN_WIDTH - self.rect.w

        if self.rect.x < 0:
            self.rect.x = 0

    def maybe_rotate_from_events(self, events):
        rotate_events = [e.event for e in events
                        if e.event in [configs.USER_EVENT_ROTATE_CW,
                                        configs.USER_EVENT_ROTATE_CCW]]
        for rotate_event in rotate_events:
            if rotate_event == configs.USER_EVENT_ROTATE_CCW:
                self.angle += 2
            elif rotate_event == configs.USER_EVENT_ROTATE_CW:
                self.angle -= 2
            
            self.rotate()
           
    def maybe_shoot_from_events(self, events):
        shoot_events = [e.event for e in events
                        if e.event == configs.USER_EVENT_SHOOT]
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
            self.rotate()

    def maybe_collide(self):
        collided_sprites = pygame.sprite.spritecollide(self, self.shots, False, pygame.sprite.collide_mask)
        if (collided_sprites):
            for collided_sprite in collided_sprites:
                if (not collided_sprite.shooter_id == self.id):
                    collided_sprite.kill()
                    self.hp -= 5

class Text(pygame.sprite.Sprite):
    def __init__(self, screen, logo):
        pygame.sprite.Sprite.__init__(self)
        self.font = GAME_FONT
        self.screen = screen
        self.logo = logo

    def update(self, _events):
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
