import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from entities.player import Player
from core.level import Level
from core.level2 import Level2
from core.camera import Camera
from entities.guardia1 import Guardia1
from entities.mosca1 import Volador

class Game:
    def __init__(self):
        pygame.font.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Jugador
        start_x = 100
        start_y = HEIGHT-100
        self.player = Player(start_x, start_y)
        self.all_sprites = pygame.sprite.Group(self.player)

        # Nivel inicial
        self.level = Level()
        self.platforms = self.level.platforms

        # Enemigos
        self.level.enemies = pygame.sprite.Group(Guardia1(self.level))

        # Cámara
        self.camera = Camera(WIDTH, HEIGHT, WIDTH, HEIGHT)

        # Spawn Volador
        self.volador_spawn_time = None
        self.volador_spawn_delay = 5

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

        # Colisión con pinchos
        for spike in getattr(self.level, "spikes", []):
            if self.player.rect.colliderect(spike):
                if not self.player.invincible:
                    self.player.take_damage()
                    self.player.rect.y -= 20
                break

        # --- Actualizar todos los enemigos ---
        for enemy in getattr(self.level, "enemies", []):
            # Todos los enemigos deben recibir al jugador
            enemy.update(self.player)

        # --- Spawn del Volador si estamos en nivel 2 ---
        if isinstance(self.level, Level2):
            self.spawn_volador()

        # Colisión con salida
        if hasattr(self.level, "exit_rect"):
            if self.player.rect.colliderect(self.level.exit_rect):
                print("¡Nivel completado! Cargando Nivel 2...")
                self.load_level2()

    def load_level2(self):
        self.level = Level2()
        self.platforms = self.level.platforms
        self.player.rect.topleft = (100, HEIGHT-100)
        self.level.enemies = pygame.sprite.Group()
        self.volador_spawn_time = pygame.time.get_ticks()

    def spawn_volador(self):
        if self.volador_spawn_time is None:
            return
        elapsed = (pygame.time.get_ticks() - self.volador_spawn_time)/1000
        if elapsed >= self.volador_spawn_delay:
            self.level.enemies.add(Volador(300, 200, self.level, self.player))
            self.volador_spawn_time = None

    def draw_lives(self):
        mask_size = 25
        padding = 10
        x_start = 15
        y_start = 7
        for i in range(self.player.max_lives):
            x = x_start + i*(mask_size+padding)
            color = (255,0,0) if i<self.player.lives else (70,70,70)
            pygame.draw.circle(self.screen, color, (x+mask_size*0.3, y_start+mask_size*0.35), mask_size*0.3)
            pygame.draw.circle(self.screen, color, (x+mask_size*0.7, y_start+mask_size*0.35), mask_size*0.3)
            points = [(x, y_start+mask_size*0.4),(x+mask_size, y_start+mask_size*0.4),(x+mask_size/2,y_start+mask_size)]
            pygame.draw.polygon(self.screen, color, points)

    def draw(self):
        self.screen.fill((25,25,35))
        self.level.draw(self.screen)
        self.player.draw(self.screen)
        for enemy in getattr(self.level, "enemies", []):
            enemy.draw(self.screen)
        self.draw_lives()
        if not self.player.alive:
            font = pygame.font.SysFont(None,72)
            text = font.render("GAME OVER", True, (255,0,0))
            self.screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()
