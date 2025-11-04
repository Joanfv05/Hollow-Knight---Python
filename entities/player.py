import pygame
import time

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill((100, 150, 255))
        self.rect = self.image.get_rect(topleft=(x, y))

        # Movimiento
        self.speed = 5
        self.vel_y = 0
        self.gravity = 0.5
        self.jump_power = -12
        self.on_ground = False

        # Vidas e invencibilidad
        self.max_lives = 5
        self.lives = self.max_lives
        self.invincible = False
        self.invincible_time = 3  # segundos
        self.last_hit_time = 0
        self.alive = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.dx = 0
        if keys[pygame.K_a]:
            self.dx = -self.speed
        if keys[pygame.K_d]:
            self.dx = self.speed
        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > 15:  # velocidad terminal
            self.vel_y = 15

    def update(self, platforms, hazards):
        if not self.alive:
            return

        self.handle_input()
        self.apply_gravity()

        # Movimiento horizontal
        self.rect.x += self.dx
        self.collide(platforms, "x")

        # Movimiento vertical
        self.rect.y += self.vel_y
        self.collide(platforms, "y")

        self.check_hazards(hazards)
        self.update_invincibility()

    def collide(self, platforms, direction):
        """Colisión sólida con paredes, techo y suelo."""
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if direction == "x":
                    if self.dx > 0:  # moviendo derecha
                        self.rect.right = plat.left
                    elif self.dx < 0:  # moviendo izquierda
                        self.rect.left = plat.right
                elif direction == "y":
                    if self.vel_y > 0:  # cayendo
                        self.rect.bottom = plat.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:  # subiendo
                        self.rect.top = plat.bottom
                        self.vel_y = 0

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
        if self.invincible and (time.time() - self.last_hit_time >= self.invincible_time):
            self.invincible = False
