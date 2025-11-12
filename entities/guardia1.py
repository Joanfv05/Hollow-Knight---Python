import pygame
import time

class Daga(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((15, 5))
        self.image.fill((200, 200, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6 * direction
        self.spawn_time = time.time()
        self.lifetime = 2.5

    def update(self, level=None):
        self.rect.x += self.speed

        # Colisión con plataformas
        if level:
            for plat in level.platforms:
                if self.rect.colliderect(plat):
                    self.kill()
                    return

        # Tiempo de vida
        if time.time() - self.spawn_time > self.lifetime:
            self.kill()


class Guardia1(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        # Posición inicial sobre plataforma fija
        self.image = pygame.Surface((50, 70))
        self.image.fill((180, 40, 40))
        self.rect = self.image.get_rect(topleft=(130, 326 - 70))

        self.speed = 1.5
        self.direction = 1
        self.shoot_cooldown = 2.0
        self.last_shot = 0
        self.detection_range = 300
        self.alive = True
        self.health = 5

        self.level = level
        self.dagas = pygame.sprite.Group()

        self.invincible = False
        self.invincible_time = 0.5  # medio segundo de invulnerabilidad
        self.last_hit_time = 0

    def patrol(self):
        self.rect.x += self.speed * self.direction
        left_limit = 130
        right_limit = 130 + 275 - self.rect.width
        if self.rect.left <= left_limit:
            self.rect.left = left_limit
            self.direction = 1
        elif self.rect.right >= right_limit:
            self.rect.right = right_limit
            self.direction = -1

    def shoot(self):
        now = time.time()
        if now - self.last_shot >= self.shoot_cooldown:
            daga_x = self.rect.centerx + (30 * self.direction)
            daga_y = self.rect.centery
            self.dagas.add(Daga(daga_x, daga_y, self.direction))
            self.last_shot = now

    def update(self, player, level):
        if not self.alive:
            return

        # Patrullaje o ataque
        distance = abs(player.rect.centerx - self.rect.centerx)
        same_height = abs(player.rect.bottom - self.rect.bottom) < 80

        if distance < self.detection_range and same_height:
            self.direction = 1 if player.rect.centerx > self.rect.centerx else -1
            self.shoot()
        else:
            self.patrol()

        # Actualizar dagas
        self.dagas.update()

        # Colisión dagas → jugador
        for daga in self.dagas:
            if player.rect.colliderect(daga.rect) and not player.invincible:
                player.take_damage()
                daga.kill()

        # Colisión cuerpo → jugador
        if self.rect.colliderect(player.rect) and not player.invincible:
            player.take_damage()

        # Colisión espada jugador → enemigo
        if player.attacking and player.sword_rect.colliderect(self.rect):
            self.take_damage()

        # Actualizar dagas y colisiones con el mapa
        self.dagas.update(level)

        # Actualizar invencibilidad
        self.update_invincibility()


    def take_damage(self):
        now = time.time()
        if not self.invincible:
            self.health -= 1
            self.invincible = True
            self.last_hit_time = now
            print(f"Guardia ha recibido daño! Vidas restantes: {self.health}")
            if self.health <= 0:
                self.die()

    def update_invincibility(self):
        if self.invincible and (time.time() - self.last_hit_time >= self.invincible_time):
            self.invincible = False

    def die(self):
        self.alive = False
        self.image.fill((60, 60, 60))

    def draw(self, screen):
        if not self.alive:
            return
        screen.blit(self.image, self.rect)
        self.dagas.draw(screen)
