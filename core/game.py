import pygame
from settings import WIDTH, HEIGHT, FPS, TITLE
from entities.player import Player
from core.camera import Camera
import random

class Game:
    def __init__(self):
        self.camera = Camera(WIDTH, HEIGHT)
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True

        # Jugador
        self.player = Player(100, 400)
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Plataformas: rectángulos (x, y, ancho, alto)
        self.platforms = [
            pygame.Rect(0, 500, 400, 40),     # suelo principal
            pygame.Rect(450, 450, 200, 20),   # plataforma pequeña
            pygame.Rect(700, 400, 200, 20),   # plataforma más alta
            pygame.Rect(950, 350, 150, 20),   # subida izquierda
            pygame.Rect(1100, 300, 200, 20)   # final alto
        ]

        # Pinchos
        self.hazards = [
            pygame.Rect(350, 480, 50, 20),  # pincho en suelo
            pygame.Rect(750, 380, 50, 20)
        ]

        # Objetos que caen
        self.falling_objects = [
            pygame.Rect(500, 0, 30, 30),
            pygame.Rect(900, 0, 30, 30)
        ]
        self.falling_speed = 5
        self.object_triggered = [False, False]  # solo caen cuando jugador pasa cerca

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
        self.all_sprites.update(self.platforms, self.hazards)
        self.update_falling_objects()
        self.camera.update(self.player) 

    def update_falling_objects(self):
        for i, obj in enumerate(self.falling_objects):
            # activar caída cuando jugador pasa cerca
            if not self.object_triggered[i] and self.player.rect.x > obj.x - 100:
                self.object_triggered[i] = True
            if self.object_triggered[i]:
                obj.y += self.falling_speed
                # colisión con plataformas
                for plat in self.platforms:
                    if obj.colliderect(plat):
                        obj.y = plat.top - obj.height
                        # detener caída del objeto
                        self.falling_speed = 0

    def draw(self):
        self.screen.fill((30, 30, 30))  # fondo oscuro (cueva)

        # dibujar plataformas con cámara
        for plat in self.platforms:
            pygame.draw.rect(self.screen, (150, 75, 0), self.camera.apply(plat))

        # dibujar pinchos
        for h in self.hazards:
            pygame.draw.rect(self.screen, (255, 0, 0), self.camera.apply(h))

        # dibujar objetos que caen
        for obj in self.falling_objects:
            pygame.draw.rect(self.screen, (255, 255, 0), self.camera.apply(obj))

        # dibujar jugador
        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, self.camera.apply(sprite.rect))

        pygame.display.flip()
