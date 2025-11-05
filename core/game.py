import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from entities.player import Player
from core.level import Level
from core.camera import Camera

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

    def draw_lives(self):
        mask_width = 30
        mask_height = 30
        padding = 5
        x_start = 10
        y_start = 10

        for i in range(self.player.max_lives):
            x = x_start + i * (mask_width + padding)
            color = (255, 255, 0) if i < self.player.lives else (50, 50, 50)
            pygame.draw.rect(self.screen, color, (x, y_start, mask_width, mask_height))

    def draw(self):
        self.screen.fill((25, 25, 35))

        # Plataformas
        for plat in self.platforms:
            pygame.draw.rect(self.screen, (130, 70, 0), plat)
            pygame.draw.rect(self.screen, (100, 50, 0), plat.inflate(-6, -6))

        # 🔥 Dibujar jugador + espada (usa su método propio)
        self.player.draw(self.screen)

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
