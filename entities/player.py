import pygame
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((100, 150, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

        self.speed = 5
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -12
        self.on_ground = False

        # Sistema de vidas
        self.max_lives = 5
        self.lives = self.max_lives
        self.invincible = False
        self.invincible_time = 3  # segundos
        self.last_hit_time = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

    def update(self, platforms, hazards):
        self.handle_input()
        self.apply_gravity()
        self.check_collision(platforms)
        self.check_hazards(hazards)
        self.update_invincibility()

    def check_collision(self, platforms):
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vel_y > 0 and self.rect.bottom <= plat.bottom:
                    self.rect.bottom = plat.top
                    self.vel_y = 0
                    self.on_ground = True

    def check_hazards(self, hazards):
        for h in hazards:
            if self.rect.colliderect(h):
                self.take_damage()

    def take_damage(self):
        current_time = time.time()
        if not self.invincible and self.lives > 0:
            self.lives -= 1
            self.invincible = True
            self.last_hit_time = current_time
            print(f"💀 Has recibido daño! Vidas restantes: {self.lives}")
            if self.lives <= 0:
                self.alive = False
                print("☠️ ¡GAME OVER!")

    def update_invincibility(self):
        if self.invincible:
            if time.time() - self.last_hit_time >= self.invincible_time:
                self.invincible = False
