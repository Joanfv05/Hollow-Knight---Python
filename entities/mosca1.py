import pygame
import math
import time


class Volador(pygame.sprite.Sprite):
    def __init__(self, x, y, level, player):
        super().__init__()
        self.level = level
        self.player = player

        # Cuerpo
        self.width = 50
        self.height = 30
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.body_color = (200, 200, 200)
        self.wing_color = (255, 255, 255)

        self.rect = self.image.get_rect(center=(x, y))
        self.base_speed = 2
        self.chase_speed = 4
        self.direction = 1

        # Aleteo / flotación
        self.wing_angle = 0
        self.wing_direction = 1
        self.wing_speed = 8
        self.wing_offset_max = 12
        self.float_amplitude = 15
        self.float_angle = 0
        self.float_speed = 4

        # Vida
        self.health = 3
        self.alive = True
        self.invincible = False
        self.invincible_time = 0.5
        self.last_hit_time = 0

        # Detección jugador
        self.detection_range = 400

        # Spawn retrasado
        self.spawn_time = time.time()
        self.delay = 2  # segundos

        self.update_image()

    def update_image(self):
        """Dibuja cuerpo y alas con aleteo"""
        self.image.fill((0, 0, 0, 0))  # transparente
        pygame.draw.rect(self.image, self.body_color, (10, 10, 30, 20))
        wing_offset = int(math.sin(math.radians(self.wing_angle)) * self.wing_offset_max)
        pygame.draw.rect(self.image, self.wing_color, (0, 10 + wing_offset, 10, 10))
        pygame.draw.rect(self.image, self.wing_color, (40, 10 - wing_offset, 10, 10))

    def update(self, player):
        if time.time() - self.spawn_time < self.delay or not self.alive:
            return

        # IA: perseguir jugador
        distance = math.hypot(player.rect.centerx - self.rect.centerx,
                              player.rect.centery - self.rect.centery)
        if distance < self.detection_range:
            speed = self.chase_speed
            dx = player.rect.centerx - self.rect.centerx
            dy = player.rect.centery - self.rect.centery
            angle = math.atan2(dy, dx)
            self.collide_with_platforms(int(math.cos(angle) * speed),
                                        int(math.sin(angle) * speed))
        else:
            # patrulla horizontal
            self.collide_with_platforms(self.base_speed * self.direction, 0)

        # Aleteo y flotación
        self.wing_angle += self.wing_speed * self.wing_direction
        if self.wing_angle >= 180 or self.wing_angle <= 0:
            self.wing_direction *= -1
        self.float_angle += self.float_speed
        self.rect.y += math.sin(math.radians(self.float_angle)) * 0.5
        self.update_image()

        # Daño al jugador
        if self.rect.colliderect(player.rect) and not player.invincible:
            player.take_damage()

        # Daño por espada del jugador
        if player.attacking and player.sword_rect.colliderect(self.rect):
            self.take_damage()

        # Invencibilidad
        self.update_invincibility()

    def collide_with_platforms(self, dx, dy):
        """Evita atravesar plataformas"""
        self.rect.x += dx
        for plat in self.level.platforms:
            if self.rect.colliderect(plat):
                if dx > 0:
                    self.rect.right = plat.left
                    self.direction *= -1
                elif dx < 0:
                    self.rect.left = plat.right
                    self.direction *= -1

        self.rect.y += dy
        for plat in self.level.platforms:
            if self.rect.colliderect(plat):
                if dy > 0:
                    self.rect.bottom = plat.top
                elif dy < 0:
                    self.rect.top = plat.bottom

    def take_damage(self):
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.last_hit_time = time.time()
            if self.health <= 0:
                self.die()

    def update_invincibility(self):
        if self.invincible and (time.time() - self.last_hit_time >= self.invincible_time):
            self.invincible = False

    def die(self):
        self.alive = False

    def draw(self, screen):
        if time.time() - self.spawn_time < self.delay:
            return
        if self.alive:
            screen.blit(self.image, self.rect)
