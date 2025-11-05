import pygame
import time
import math


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

        # Dirección principal
        self.facing = "right"  # "right", "left", "up", "down"

        # Espada / ataque
        self.attacking = False
        self.attack_time = 0
        self.attack_duration = 250  # ms
        self.attack_start_angle = 0
        self.attack_sweep = 0

        self.sword_length = 45
        self.sword_width = 10
        self.sword_image = pygame.Surface(
            (self.sword_length, self.sword_width), pygame.SRCALPHA
        )
        self.sword_image.fill((255, 255, 100))
        self.sword_rotated = self.sword_image
        self.sword_rect = self.sword_image.get_rect()
        self.sword_origin = (0, 0)
        self.sword_angle = 0

        # Vidas e invincibilidad
        self.max_lives = 5
        self.lives = self.max_lives
        self.invincible = False
        self.invincible_time = 3
        self.last_hit_time = 0
        self.alive = True

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.dx = 0

        # Movimiento y dirección
        if keys[pygame.K_a]:
            self.dx = -self.speed
            self.facing = "left"
        elif keys[pygame.K_d]:
            self.dx = self.speed
            self.facing = "right"
        elif keys[pygame.K_w]:
            self.facing = "up"
        elif keys[pygame.K_s]:
            self.facing = "down"

        if keys[pygame.K_SPACE] and self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

        # Ataque con click izquierdo
        mouse_buttons = pygame.mouse.get_pressed()
        if mouse_buttons[0] and not self.attacking:
            self.start_attack()

    def start_attack(self):
        """Empieza ataque según dirección (empieza arriba y baja)."""
        self.attacking = True
        self.attack_time = pygame.time.get_ticks()

        # Movimiento descendente en espejo
        if self.facing == "right":
            # Empieza arriba (-45°) → termina abajo (+45°)
            self.attack_start_angle = -45
            self.attack_sweep = 90
            self.sword_origin = (self.rect.right + 5, self.rect.centery)

        elif self.facing == "left":
            # Empieza arriba (225°) → termina abajo (135°)
            self.attack_start_angle = 225
            self.attack_sweep = -90
            self.sword_origin = (self.rect.left - 5, self.rect.centery)

        elif self.facing == "up":
            # Barrido completo de 180° por encima del personaje
            # Empieza arriba-izquierda (-180°) → termina arriba-derecha (0°)
            self.attack_start_angle = -180
            self.attack_sweep = 180
            self.sword_origin = (self.rect.centerx, self.rect.top - 5)

        elif self.facing == "down":
            # Barrido completo de 180° por debajo del personaje
            # Empieza abajo-izquierda (180°) → termina abajo-derecha (0°)
            self.attack_start_angle = 180
            self.attack_sweep = -180
            self.sword_origin = (self.rect.centerx, self.rect.bottom + 5)

        # Inicializamos el ángulo visual inmediato
        self.sword_angle = self.attack_start_angle
        self.sword_rotated = pygame.transform.rotate(self.sword_image, -self.sword_angle)
        self.sword_rect = self.sword_rotated.get_rect(center=self.sword_origin)

    def update_attack(self, platforms):
        if not self.attacking:
            return

        elapsed = pygame.time.get_ticks() - self.attack_time
        progress = elapsed / self.attack_duration
        if progress >= 1:
            self.attacking = False
            return

        # Recalcular el origen dinámicamente según la posición actual del jugador
        if self.facing == "right":
            self.sword_origin = (self.rect.right + 5, self.rect.centery)
        elif self.facing == "left":
            self.sword_origin = (self.rect.left - 5, self.rect.centery)
        elif self.facing == "up":
            self.sword_origin = (self.rect.centerx, self.rect.top - 5)
        elif self.facing == "down":
            self.sword_origin = (self.rect.centerx, self.rect.bottom + 5)

        # Ángulo según start + progress * sweep
        self.sword_angle = self.attack_start_angle + progress * self.attack_sweep

        # Rotar espada
        self.sword_rotated = pygame.transform.rotate(self.sword_image, -self.sword_angle)

        # Posicionar extremo de la espada
        radius = self.sword_length + 5
        cx, cy = self.sword_origin
        offset_x = math.cos(math.radians(self.sword_angle)) * radius
        offset_y = math.sin(math.radians(self.sword_angle)) * radius
        sx = cx + offset_x
        sy = cy + offset_y

        self.sword_rect = self.sword_rotated.get_rect(center=(sx, sy))

        # Colisión con plataformas → cancelar ataque
        for plat in platforms:
            if self.sword_rect.colliderect(plat):
                self.attacking = False
                break

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > 15:
            self.vel_y = 15

    def update(self, platforms, hazards):
        if not self.alive:
            return

        self.handle_input()
        self.apply_gravity()

        # Movimiento
        self.rect.x += self.dx
        self.collide(platforms, "x")
        self.rect.y += self.vel_y
        self.collide(platforms, "y")

        # Actualizar ataque
        self.update_attack(platforms)
        self.check_hazards(hazards)
        self.update_invincibility()

    def collide(self, platforms, direction):
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                if direction == "x":
                    if self.dx > 0:
                        self.rect.right = plat.left
                    elif self.dx < 0:
                        self.rect.left = plat.right
                elif direction == "y":
                    if self.vel_y > 0:
                        self.rect.bottom = plat.top
                        self.vel_y = 0
                        self.on_ground = True
                    elif self.vel_y < 0:
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

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.attacking and self.sword_rotated:
            screen.blit(self.sword_rotated, self.sword_rect)
