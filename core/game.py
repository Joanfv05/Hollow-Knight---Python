import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from entities.player import Player
from core.camera import Camera
from core.level import Level

class Game:
    def __init__(self):
        pygame.font.init()

        # Ventana normal (ajústala si quieres pantalla completa)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)

        self.clock = pygame.time.Clock()
        self.running = True

        # Cámara
        self.camera = Camera(WIDTH, HEIGHT)

        # Nivel
        self.level = Level()
        self.platforms = self.level.platforms
        self.hazards = self.level.hazards
        self.walls = self.level.walls

        # Jugador
        start_x = 100
        start_y = 0
        for plat in self.platforms:
            if plat.left <= start_x <= plat.right:
                start_y = plat.top - 50
                break
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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        if not self.player.alive:
            return

        self.player.update_invincibility()
        self.all_sprites.update(self.platforms, self.hazards)
        self.camera.update(self.player, self.level.level_width, self.level.level_height)

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
        self.screen.fill((25, 25, 35))  # Fondo más oscuro tipo cueva

        # Paredes
        for wall in self.walls:
            pygame.draw.rect(self.screen, (60, 60, 60), self.camera.apply(wall))

        # Plataformas con variaciones de color
        for plat in self.platforms:
            pygame.draw.rect(self.screen, (130, 70, 0), self.camera.apply(plat))
            pygame.draw.rect(self.screen, (100, 50, 0), self.camera.apply(plat.inflate(-6, -6)))  # borde interior

        # Pinchos (detallados con colores)
        for h in self.hazards:
            pygame.draw.rect(self.screen, (255, 30, 30), self.camera.apply(h))
            pygame.draw.rect(self.screen, (180, 0, 0), self.camera.apply(h.inflate(-4, -4)))  # sombreado interior

        # Jugador
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        # HUD (vidas)
        self.draw_lives()

        # Game Over
        if not self.player.alive:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)

        pygame.display.flip()
