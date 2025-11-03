import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from entities.player import Player
from core.camera import Camera

class Game:
    def __init__(self):
        pygame.font.init()
        self.camera = Camera(WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Jugador
        self.player = Player(100, 400)
        self.all_sprites = pygame.sprite.Group(self.player)

        # Plataformas
        self.platforms = [
            pygame.Rect(0, 500, 400, 40),
            pygame.Rect(450, 450, 200, 20),
            pygame.Rect(700, 400, 200, 20),
            pygame.Rect(950, 350, 150, 20),
            pygame.Rect(1100, 300, 200, 20),
            pygame.Rect(1350, 250, 200, 20),
            pygame.Rect(1600, 200, 250, 20)
        ]

        # Pinchos rojos
        self.hazards = [
            pygame.Rect(350, 480, 50, 20),
            pygame.Rect(750, 380, 50, 20),
            pygame.Rect(1200, 280, 50, 20)
        ]

        # Objetos amarillos
        self.falling_objects = [
            pygame.Rect(500, 0, 30, 30),
            pygame.Rect(900, 0, 30, 30),
            pygame.Rect(1400, 0, 30, 30)  # estático, no cae
        ]
        self.falling_speed = 5
        self.object_triggered = [False] * len(self.falling_objects)

        # Paredes de cueva
        self.walls = [
            pygame.Rect(0, 0, 50, HEIGHT),
            pygame.Rect(1800, 0, 50, HEIGHT)
        ]

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

    def update(self):
        if not self.player.alive:
            return  # no actualizar nada si murió

        self.all_sprites.update(self.platforms, self.hazards)
        self.update_falling_objects()
        self.camera.update(self.player)

    def update_falling_objects(self):
        for i, obj in enumerate(self.falling_objects[:2]):  # solo los dos primeros caen
            # activar caída si el jugador se acerca
            if not self.object_triggered[i] and self.player.rect.x > obj.x - 100:
                self.object_triggered[i] = True

            if self.object_triggered[i]:
                obj.y += self.falling_speed

            # Colisión con cualquier plataforma o jugador
            collided = False
            for plat in self.platforms:
                if obj.colliderect(plat):
                    collided = True
                    break

            if obj.colliderect(self.player.rect):
                self.player.take_damage()
                collided = True

            # Si colisionó, se rompe
            if collided:
                self.falling_objects[i] = None
                self.object_triggered[i] = False

        # Limpiar objetos eliminados
        self.falling_objects = [o for o in self.falling_objects if o is not None]

    def draw_lives(self):
        # Tamaño y posición de las máscaras
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
        self.screen.fill((20, 20, 20))  # fondo tipo cueva

        # Paredes de cueva
        for wall in self.walls:
            pygame.draw.rect(self.screen, (50, 50, 50), self.camera.apply(wall))

        # Plataformas
        for plat in self.platforms:
            pygame.draw.rect(self.screen, (150, 75, 0), self.camera.apply(plat))

        # Pinchos rojos
        for h in self.hazards:
            pygame.draw.rect(self.screen, (255, 0, 0), self.camera.apply(h))

        # Objetos amarillos
        for obj in self.falling_objects:
            pygame.draw.rect(self.screen, (255, 255, 0), self.camera.apply(obj))

        # Jugador
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        # HUD: vidas
        self.draw_lives()

        # Game Over visual
        if not self.player.alive:
            font = pygame.font.SysFont(None, 72)
            text = font.render("GAME OVER", True, (255, 0, 0))
            rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(text, rect)

        pygame.display.flip()
