import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.player_pos = [WIDTH//2, HEIGHT//2]
        self.speed = 5

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
        keys = pygame.key.get_pressed()
        # Movimiento con WASD
        if keys[pygame.K_a]:  # izquierda
            self.player_pos[0] -= self.speed
        if keys[pygame.K_d]:  # derecha
            self.player_pos[0] += self.speed
        if keys[pygame.K_w]:  # arriba
            self.player_pos[1] -= self.speed
        if keys[pygame.K_s]:  # abajo
            self.player_pos[1] += self.speed

    def draw(self):
        self.screen.fill((30, 30, 30))
        pygame.draw.rect(self.screen, (200, 200, 255), (*self.player_pos, 50, 50))
        pygame.display.flip()