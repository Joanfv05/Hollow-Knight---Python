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

        # Cámara
        self.camera = Camera(WIDTH, HEIGHT, self.level_width, self.level_height)

        # Jugador (posición inicial)
        start_x = 100
        start_y = self.level_height - 100  # Aparece sobre el suelo visible

        self.player = Player(start_x, start_y)
        self.all_sprites = pygame.sprite.Group(self.player)

        # Si el sprite no tiene imagen, creamos una por defecto
        if not hasattr(self.player, "image") or self.player.image is None:
            self.player.image = pygame.Surface((40, 60))
            self.player.image.fill((200, 200, 255))
            self.player.rect = self.player.image.get_rect(topleft=(start_x, start_y))

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

        self.player.update_invincibility()
        self.all_sprites.update(self.platforms, [])
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
        self.screen.fill((25, 25, 35))  # Fondo tipo cueva

        # Plataformas
        for plat in self.platforms:
            pygame.draw.rect(self.screen, (130, 70, 0), self.camera.apply(plat))
            pygame.draw.rect(self.screen, (100, 50, 0), self.camera.apply(plat.inflate(-6, -6)))

        # Jugador
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        # HUD
        self.draw_lives()

        # Game Over
        if not self.player.alive:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)

        pygame.display.flip()


__all__ = ["Game"]
