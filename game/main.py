import pygame
import math

SCREEN_HEIGHT = 1280 // 2 
SCREEN_WIDTH = 720 // 2

class Shot(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
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

    def update(self):
        if (self.rect.x > SCREEN_WIDTH or self.rect.y > SCREEN_HEIGHT):
            self.kill()
        
        self.x = self.x + self.dx
        self.y = self.y + self.dy

        self.rect.x = int(self.x)
        self.rect.y = int(self.y)


class LangLogo(pygame.sprite.Sprite):
    def __init__(self, logo_file, x, y, shots):
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

    def update(self):
        keys = pygame.key.get_pressed()
        self.maybe_collide()
        self.maybe_move(keys)
        self.maybe_rotate(keys)
        self.maybe_shoot(keys)
        
    def maybe_shoot(self, keys):
        if keys[pygame.K_RETURN]:
            angle = math.radians(self.angle * -1)
            dx = math.cos(angle) * self.velocity
            dy = math.sin(angle) * self.velocity
            shot = Shot(self.rect.centerx, self.rect.centery, dx, dy)
            self.shots.add(shot)

    def maybe_move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.velocity
        if keys[pygame.K_d]:
            self.rect.x += self.velocity
        if keys[pygame.K_w]:
            self.rect.y -= self.velocity
        if keys[pygame.K_s]:
            self.rect.y += self.velocity
        
    def maybe_rotate(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += 2
        if keys[pygame.K_RIGHT]:
            self.angle -= 2
        
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            self.angle = self.angle % 360
            self.image = pygame.transform.rotate(self.original_image, self.angle)
            self.rect = self.image.get_rect(center = self.rect.center)
        
    def maybe_collide(self):
        if pygame.sprite.spritecollide(self, self.shots, False):
            self.hp -= 1

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

lang = LangLogo("csharp-logo.png", 200, 200, shots)
logos.add(lang)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("white")

    #screen.blit(star.image, star.rect)
    #star.update()

    #screen.blit(logo.image, logo.rect)

    #screen.blit(shot.image, shot.rect)

    logos.update()
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