import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from entities.player import Player
from core.level import Level
from core.camera import Camera
from entities.guardia1 import Guardia1

class Game:
    def __init__(self):
        pygame.font.init()

        # Ventana
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Nivel
        self.level = Level()
        self.platforms = self.level.platforms

        # Dimensiones del nivel
        self.level_width = 1000
        self.level_height = 600

        # Enemigos
        import random
        platform = random.choice(self.level.platforms[4:])  # evita paredes y suelo

        # ✅ FIX → comprobamos que el rango sea válido antes de usar randint
        left_limit = platform.left + 20
        right_limit = platform.right - 70
        if right_limit <= left_limit:
            x = platform.centerx  # usa el centro si la plataforma es estrecha
        else:
            x = random.randint(left_limit, right_limit)
        y = platform.top - 70

        self.enemy = Guardia1(x, y, self.level)

        # Cámara (aunque estática)
        self.camera = Camera(WIDTH, HEIGHT, self.level_width, self.level_height)

        # Jugador
        start_x = 100
        start_y = self.level_height - 100
        self.player = Player(start_x, start_y)
        self.all_sprites = pygame.sprite.Group(self.player)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.update()
            self.draw()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.running = False

    def update(self):
        if not self.player.alive:
            return

        # Actualiza jugador y cámara
        self.player.update(self.platforms, [])
        self.camera.update(self.player)

        # ⚠️ Colisión con pinchos (respeta inmunidad)
        for spike in self.level.spikes:
            if self.player.rect.colliderect(spike):
                # Solo recibe daño si no está invencible
                if not self.player.invincible:
                    self.player.take_damage()
                    # Rebote hacia atrás o pequeño impulso
                    self.player.rect.y -= 20
                break

        self.enemy.update(self.player, self.level)
        self.enemy.draw(self.screen)

    def draw_lives(self):
        mask_size = 25
        padding = 10
        x_start = 15
        y_start = 7

        for i in range(self.player.max_lives):
            x = x_start + i * (mask_size + padding)

            # Color: rojo si está viva, gris si perdida
            if i < self.player.lives:
                color = (255, 0, 0)
            else:
                color = (70, 70, 70)

            # Dibuja corazón (dos círculos + triángulo)
            center_left = (x + mask_size * 0.3, y_start + mask_size * 0.35)
            center_right = (x + mask_size * 0.7, y_start + mask_size * 0.35)
            radius = mask_size * 0.3

            # Parte superior redondeada
            pygame.draw.circle(self.screen, color, center_left, radius)
            pygame.draw.circle(self.screen, color, center_right, radius)

            # Parte inferior en punta
            points = [
                (x, y_start + mask_size * 0.4),
                (x + mask_size, y_start + mask_size * 0.4),
                (x + mask_size / 2, y_start + mask_size),
            ]
            pygame.draw.polygon(self.screen, color, points)

    def draw(self):
        self.screen.fill((25, 25, 35))

        # Dibuja el nivel completo (plataformas + pinchos + fondo)
        self.level.draw(self.screen)

        # Dibujar jugador + espada (usa su método propio)
        self.player.draw(self.screen)

        # Dibujar Enemigo + espada
        self.enemy.draw(self.screen)

        # HUD de vidas
        self.draw_lives()

        # Game Over
        if not self.player.alive:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)

        pygame.display.flip()


__all__ = ["Game"]
