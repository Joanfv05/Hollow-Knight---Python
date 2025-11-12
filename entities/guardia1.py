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
    def __init__(self, x, y, level):
        super().__init__()

        # === Atributos principales ===
        self.image = pygame.Surface((50, 70))
        self.image.fill((180, 40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 1.5
        self.direction = 1
        self.shoot_cooldown = 2.0
        self.last_shot = 0
        self.detection_range = 300
        self.alive = True

        self.platform = None
        self.dagas = pygame.sprite.Group()

    def get_platform_below(self, level):
        """Devuelve la plataforma justo debajo del enemigo."""
        feet_x = self.rect.centerx
        feet_y = self.rect.bottom + 2
        for plat in level.platforms:
            if plat.left <= feet_x <= plat.right and plat.top <= feet_y <= plat.bottom + 10:
                return plat
        return None

    def check_platform_edges(self, level):
        """Devuelve True si hay suelo bajo los pies."""
        # Detectar suelo bajo cada pie
        left_foot = (self.rect.left + 5, self.rect.bottom + 4)
        right_foot = (self.rect.right - 5, self.rect.bottom + 4)

        on_left = any(p.collidepoint(left_foot) for p in level.platforms)
        on_right = any(p.collidepoint(right_foot) for p in level.platforms)

        return on_left, on_right

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
            # Patrullaje con detección de bordes
            self.patrol(level)

    def patrol(self, level):
        """Se mueve de izquierda a derecha y gira al llegar a un borde."""
        on_left, on_right = self.check_platform_edges(level)

        # Si va a la izquierda y no hay suelo bajo el pie izquierdo → girar
        if self.direction == -1 and not on_left:
            self.direction = 1
        # Si va a la derecha y no hay suelo bajo el pie derecho → girar
        elif self.direction == 1 and not on_right:
            self.direction = -1

        # Movimiento horizontal
        self.rect.x += self.speed * self.direction

        # Evitar salirse de los límites del mapa
        if self.rect.left < 40:
            self.rect.left = 40
            self.direction = 1
        elif self.rect.right > level.level_width - 40:
            self.rect.right = level.level_width - 40
            self.direction = -1

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
