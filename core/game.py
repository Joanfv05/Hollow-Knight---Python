import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from entities.player import Player
from core.level import Level
from core.camera import Camera
from entities.guardia1 import Guardia1
from core.level2 import Level2


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
        self.level_width = WIDTH
        self.level_height = HEIGHT

        # Enemigo: Guardia1 sobre plataforma fija
        self.enemy = Guardia1(self.level)

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

        # Colisión con pinchos (respeta inmunidad)
        for spike in self.level.spikes:
            if self.player.rect.colliderect(spike):
                if not self.player.invincible:
                    self.player.take_damage()
                    self.player.rect.y -= 20
                break

       # Actualizar todos los enemigos del nivel actual
        for enemy in self.level.enemies:
            enemy.update(self.player, self.level)   

        # --- COLISIÓN CON SALIDA ---
        if self.player.rect.colliderect(self.level.exit_rect):
            print("¡Nivel completado! Cargando Nivel 2...")
            self.level = Level2()
            self.platforms = self.level.platforms
            # Reposicionar jugador al inicio del nuevo nivel
            self.player.rect.topleft = (100, HEIGHT - 100)


    def draw_lives(self):
        mask_size = 25
        padding = 10
        x_start = 15
        y_start = 7

        for i in range(self.player.max_lives):
            x = x_start + i * (mask_size + padding)
            color = (255, 0, 0) if i < self.player.lives else (70, 70, 70)

            center_left = (x + mask_size * 0.3, y_start + mask_size * 0.35)
            center_right = (x + mask_size * 0.7, y_start + mask_size * 0.35)
            radius = mask_size * 0.3

            pygame.draw.circle(self.screen, color, center_left, radius)
            pygame.draw.circle(self.screen, color, center_right, radius)

            points = [
                (x, y_start + mask_size * 0.4),
                (x + mask_size, y_start + mask_size * 0.4),
                (x + mask_size / 2, y_start + mask_size),
            ]
            pygame.draw.polygon(self.screen, color, points)

    def draw(self):
        self.screen.fill((25, 25, 35))

        # Dibujar nivel
        self.level.draw(self.screen)

        # Dibujar jugador
        self.player.draw(self.screen)

        # Dibujar todos los enemigos
        for enemy in self.level.enemies:
            enemy.draw(self.screen)

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
