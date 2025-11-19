import pygame
import math
import time

GRAVITY = 0.6  # opcional, si quieres que tenga caída (puede ignorarse para volar)

class Volador(pygame.sprite.Sprite):
    def __init__(self, x, y, level):
        super().__init__()
        self.level = level

        # Cuerpo del enemigo
        self.width = 50
        self.height = 30
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.body_color = (200, 200, 200)  # gris claro
        self.wing_color = (255, 255, 255)  # alas blancas

        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 2
        self.base_speed = 2
        self.chase_speed = 4
        self.direction = 1  # 1 = derecha, -1 = izquierda
        self.vel_y = 0

        # Aleteo
        self.wing_angle = 0
        self.wing_direction = 1  # 1 = subir, -1 = bajar
        self.wing_speed = 5  # control de aleteo

        # Vida
        self.health = 3
        self.alive = True
        self.invincible = False
        self.invincible_time = 0.5
        self.last_hit_time = 0

        # Detección
        self.detection_range = 400

        # Actualizar imagen inicial
        self.update_image()

    def update_image(self):
        """Dibuja cuerpo y alas en el Surface"""
        self.image.fill((0, 0, 0, 0))  # transparente
        # cuerpo
        pygame.draw.rect(self.image, self.body_color, (10, 10, 30, 20))
        # alas (simulación simple de aleteo)
        wing_offset = int(math.sin(math.radians(self.wing_angle)) * 10)
        pygame.draw.rect(self.image, self.wing_color, (0, 10 + wing_offset, 10, 10))   # ala izquierda
        pygame.draw.rect(self.image, self.wing_color, (40, 10 - wing_offset, 10, 10))  # ala derecha

    def update(self, player):
        if not self.alive:
            return

        # --- IA DETECCIÓN ---
        distance = math.hypot(player.rect.centerx - self.rect.centerx,
                              player.rect.centery - self.rect.centery)

        if distance < self.detection_range:
            # Perseguir jugador
            self.speed = self.chase_speed
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            angle = math.atan2(dy, dx)
            self.rect.x += int(math.cos(angle) * self.speed)
            self.rect.y += int(math.sin(angle) * self.speed)
        else:
            # Movimiento patrullaje simple (horizontal)
            self.speed = self.base_speed
            self.rect.x += self.speed * self.direction
            # Cambiar dirección al tocar paredes
            for plat in self.level.platforms:
                if self.rect.colliderect(plat):
                    self.direction *= -1
                    self.rect.x += self.speed * self.direction
                    break

        # --- Aleteo ---
        self.wing_angle += self.wing_speed * self.wing_direction
        if self.wing_angle >= 180 or self.wing_angle <= 0:
            self.wing_direction *= -1
        self.update_image()

        # --- Colisión con jugador ---
        if self.rect.colliderect(player.rect) and not player.invincible:
            player.take_damage()
            # Knockback opcional
            if player.rect.centerx < self.rect.centerx:
                player.rect.x -= 20
            else:
                player.rect.x += 20

    def take_damage(self):
        now = time.time()
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.last_hit_time = now
            if self.health <= 0:
                self.die()

    def update_invincibility(self):
        if self.invincible and (time.time() - self.last_hit_time >= self.invincible_time):
            self.invincible = False

    def die(self):
        self.alive = False

    def draw(self, screen):
        if self.alive:
            screen.blit(self.image, self.rect)
