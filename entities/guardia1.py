import pygame
import time

GRAVITY = 0.6
MAX_FALL_SPEED = 12


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

        if level:
            for plat in level.platforms:
                if self.rect.colliderect(plat):
                    self.kill()
                    return

        if time.time() - self.spawn_time > self.lifetime:
            self.kill()


class Guardia1(pygame.sprite.Sprite):
    def __init__(self, level):
        super().__init__()
        self.image = pygame.Surface((50, 70))
        self.image.fill((180, 40, 40))
        self.rect = self.image.get_rect(topleft=(130, 326 - 70))

        # Movimiento
        self.speed = 1.5
        self.direction = 1
        self.vel_y = 0

        # Combate
        self.shoot_cooldown = 2.0
        self.last_shot = 0
        self.detection_range = 300
        self.health = 5
        self.alive = True

        # Dagas
        self.dagas = pygame.sprite.Group()

        # Mapa
        self.level = level

        # Invencibilidad
        self.invincible = False
        self.invincible_time = 0.5
        self.last_hit_time = 0

    # ----------------------------------------------------------
    #                  FÍSICAS + COLISIONES
    # ----------------------------------------------------------

    def apply_gravity(self):
        self.vel_y += GRAVITY
        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED
        self.rect.y += self.vel_y
        self.collide_vertical()

    def collide_vertical(self):
        for plat in self.level.platforms:
            if self.rect.colliderect(plat):

                if self.vel_y > 0:  # Cayendo
                    self.rect.bottom = plat.top
                    self.vel_y = 0

                elif self.vel_y < 0:  # Subiendo
                    self.rect.top = plat.bottom
                    self.vel_y = 0

    def move_x(self, amount):
        self.rect.x += amount

        for plat in self.level.platforms:
            if self.rect.colliderect(plat):

                if amount > 0:  # hacia la derecha
                    self.rect.right = plat.left
                else:  # izquierda
                    self.rect.left = plat.right

    # ----------------------------------------------------------
    #                         PINCHOS
    # ----------------------------------------------------------

    def check_spikes(self):
        for spike in self.level.spikes:
            if self.rect.colliderect(spike):
                print("⚠ Guardia ha tocado un pincho → Muerte instantánea")
                self.health = 0
                self.die()
                return True
        return False

    # ----------------------------------------------------------
    #                        IA BASICA
    # ----------------------------------------------------------

    def patrol(self):
        """Se mueve sobre LAS plataformas, sin caerse."""
        # detectar si hay suelo bajo los pies
        on_ground = False
        for plat in self.level.platforms:
            if self.rect.bottom == plat.top and \
               self.rect.centerx > plat.left and self.rect.centerx < plat.right:
                on_ground = True
                ground_plat = plat
                break

        if not on_ground:
            # está en el aire → dejar que la gravedad actúe
            return

        # si llega al borde derecho del suelo → girar
        if self.rect.right >= ground_plat.right:
            self.direction = -1

        # si llega al borde izquierdo del suelo → girar
        if self.rect.left <= ground_plat.left:
            self.direction = 1

        # moverse
        self.move_x(self.speed * self.direction)

    def shoot(self):
        now = time.time()
        if now - self.last_shot >= self.shoot_cooldown:
            daga_x = self.rect.centerx + (30 * self.direction)
            daga_y = self.rect.centery
            self.dagas.add(Daga(daga_x, daga_y, self.direction))
            self.last_shot = now

    # ----------------------------------------------------------
    #                          DAÑO
    # ----------------------------------------------------------

    def take_damage(self, knockback_dir=0):
        now = time.time()
        if not self.invincible:
            self.health -= 1
            print(f"Guardia dañado. Vida: {self.health}")

            self.invincible = True
            self.last_hit_time = now

            # Empuje sin atravesar paredes
            if knockback_dir != 0:
                self.move_x(20 * knockback_dir)

            if self.health <= 0:
                self.die()

    def update_invincibility(self):
        if self.invincible and time.time() - self.last_hit_time >= self.invincible_time:
            self.invincible = False

    # ----------------------------------------------------------
    #                        UPDATE GENERAL
    # ----------------------------------------------------------

    def update(self, player, level):

        if not self.alive:
            return

        # MUERTO POR PINCHOS
        if self.check_spikes():
            return

        # IA
        distance = abs(player.rect.centerx - self.rect.centerx)
        same_height = abs(player.rect.bottom - self.rect.bottom) < 80

        if distance < self.detection_range and same_height:
            self.direction = 1 if player.rect.centerx > self.rect.centerx else -1
            self.shoot()
        else:
            self.patrol()

        # Gravedad
        self.apply_gravity()

        # Dagas
        self.dagas.update(level)

        # ----------------------------------------------------------
        #        COLISIONES CON EL JUGADOR
        # ----------------------------------------------------------

        # Daga → jugador
        for daga in list(self.dagas):
            if player.rect.colliderect(daga.rect):
                if not player.invincible:
                    player.take_damage()
                daga.kill()

        # Cuerpo → jugador
        if self.rect.colliderect(player.rect):
            direction = -1 if player.rect.centerx < self.rect.centerx else 1
            player.rect.x += 20 * direction
            player.take_damage()

        # Espada jugador → guardia
        if player.attacking and player.sword_rect.colliderect(self.rect):
            kb = 1 if player.facing == "right" else -1
            self.take_damage(knockback_dir=kb)

        # Invencibilidad
        self.update_invincibility()

    # ----------------------------------------------------------
    #                          DIBUJO
    # ----------------------------------------------------------

    def die(self):
        self.alive = False
        self.image.fill((60, 60, 60))

    def draw(self, screen):
        if not self.alive:
            return
        screen.blit(self.image, self.rect)
        self.dagas.draw(screen)
