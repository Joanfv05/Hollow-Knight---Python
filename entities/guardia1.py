import pygame
import time
import random


class Daga(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((15, 5))
        self.image.fill((200, 200, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6 * direction
        self.spawn_time = time.time()
        self.lifetime = 2.5  # segundos hasta desaparecer

    def update(self):
        self.rect.x += self.speed
        if time.time() - self.spawn_time > self.lifetime:
            self.kill()


class Guardia1(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()

        # === Atributos principales ===
        self.image = pygame.Surface((50, 70))
        self.image.fill((180, 40, 40))
        # Posicionar al guardia sobre la plataforma fija
        platform_rect = pygame.Rect(130, 326, 275, 20)
        self.rect = self.image.get_rect(midbottom=(platform_rect.centerx, platform_rect.top))

        self.speed = 1.5
        self.direction = 1
        self.shoot_cooldown = 2.0
        self.last_shot = 0
        self.detection_range = 300
        self.alive = True

        # Plataforma fija
        self.platform = platform_rect

        # Grupo de dagas
        self.dagas = pygame.sprite.Group()

    def update(self, player, level):
        if not self.alive:
            return

        self.dagas.update()

        distance = abs(player.rect.centerx - self.rect.centerx)
        same_height = abs(player.rect.bottom - self.rect.bottom) < 80

        if distance < self.detection_range and same_height:
            # Se gira hacia el jugador y dispara
            self.direction = 1 if player.rect.centerx > self.rect.centerx else -1
            self.shoot()
        else:
            # Patrulla sobre la plataforma fija
            self.patrol()

    def patrol(self):
        """Patrulla izquierda-derecha sobre la plataforma fija."""
        # Girar si llega al borde de la plataforma
        if self.rect.left <= self.platform.left:
            self.rect.left = self.platform.left
            self.direction = 1
        elif self.rect.right >= self.platform.right:
            self.rect.right = self.platform.right
            self.direction = -1

        # Movimiento horizontal
        self.rect.x += self.speed * self.direction

    def shoot(self):
        now = time.time()
        if now - self.last_shot >= self.shoot_cooldown:
            dagger_x = self.rect.centerx + (30 * self.direction)
            dagger_y = self.rect.centery
            daga = Daga(dagger_x, dagger_y, self.direction)
            self.dagas.add(daga)
            self.last_shot = now

    def draw(self, screen):
        if not self.alive:
            return
        screen.blit(self.image, self.rect)
        self.dagas.draw(screen)
