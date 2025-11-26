import pygame
import math
import time

class MoscaBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, level, player):
        super().__init__()
        self.level = level
        self.player = player

        # MUCHÍSIMO MÁS GRANDE
        self.width = 140
        self.height = 90
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # Colores
        self.body_color = (255, 40, 40)
        self.wing_color = (255, 200, 200)

        self.rect = self.image.get_rect(center=(x, y))

        # Vida más alta
        self.health = 20
        self.alive = True

        # Movimiento
        self.speed = 2.5
        self.float_angle = 0

        # Invencibilidad
        self.invincible = False
        self.inv_time = 0.35
        self.last_hit = 0

        self.update_image()

    def update_image(self):
        self.image.fill((0,0,0,0))
        pygame.draw.rect(self.image, self.body_color, (20, 20, 100, 50))
        pygame.draw.rect(self.image, self.wing_color, (0, 10, 30, 30))
        pygame.draw.rect(self.image, self.wing_color, (110, 10, 30, 30))

    def update(self, player):
        if not self.alive:
            return

        # Movimiento hacia el jugador
        dx = player.rect.centerx - self.rect.centerx
        dy = player.rect.centery - self.rect.centery
        ang = math.atan2(dy, dx)

        self.rect.x += math.cos(ang) * self.speed
        self.rect.y += math.sin(ang) * self.speed

        # Efecto flotación
        self.float_angle += 3
        self.rect.y += math.sin(math.radians(self.float_angle)) * 1.5

        # Ataque al jugador
        if self.rect.colliderect(player.rect) and not player.invincible:
            player.take_damage()

        # Daño por espada
        if player.attacking and player.sword_rect.colliderect(self.rect):
            self.take_damage()

        self.update_invincibility()
        self.update_image()

    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.last_hit = time.time()
            print("Boss hit! Vida restante:", self.health)
            if self.health <= 0:
                self.die()

    def update_invincibility(self):
        if self.invincible and (time.time() - self.last_hit >= self.inv_time):
            self.invincible = False

    def die(self):
        self.alive = False
        print("¡Jefe derrotado!")
    
    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)
