import pygame
from settings import WIDTH, HEIGHT

class Level:
    def __init__(self):
        # Lista de plataformas y paredes
        self.platforms = []

        # === HABITACIÓN CERRADA ===
        wall_thickness = 40
        floor_height = HEIGHT - wall_thickness

        # Paredes (izquierda, derecha, techo y suelo)
        self.platforms.append(pygame.Rect(0, 0, wall_thickness, HEIGHT))                       # izquierda
        self.platforms.append(pygame.Rect(WIDTH - wall_thickness, 0, wall_thickness, HEIGHT))  # derecha
        self.platforms.append(pygame.Rect(0, 0, WIDTH, wall_thickness))                        # techo
        self.platforms.append(pygame.Rect(0, floor_height, WIDTH, wall_thickness))             # suelo

        # === PLATAFORMAS INTERNAS (para saltar) ===
        # Las ubicamos en proporción al tamaño de la pantalla
        self.platforms.append(pygame.Rect(WIDTH * 0.2, HEIGHT * 0.75, WIDTH * 0.15, 20))
        self.platforms.append(pygame.Rect(WIDTH * 0.45, HEIGHT * 0.63, WIDTH * 0.18, 20))
        self.platforms.append(pygame.Rect(WIDTH * 0.7, HEIGHT * 0.5, WIDTH * 0.15, 20))
        self.platforms.append(pygame.Rect(WIDTH * 0.3, HEIGHT * 0.38, WIDTH * 0.12, 20))

        # Guardamos el tamaño total del nivel (por compatibilidad con la cámara)
        self.level_width = WIDTH
        self.level_height = HEIGHT

    def draw(self, screen):
        color = (160, 90, 40)
        screen.fill((20, 20, 30))  # Fondo
        for p in self.platforms:
            pygame.draw.rect(screen, color, p)
            pygame.draw.rect(screen, (100, 60, 20), p.inflate(-4, -4))
