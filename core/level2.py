import pygame
from settings import WIDTH, HEIGHT
from entities.mosca1 import Volador


class Level2:
    def __init__(self):
        # --- PLATAFORMAS ---
        self.platforms = []

        # Paredes y techo/suelo
        self.platforms.append(pygame.Rect(0, 0, 40, HEIGHT))          # pared izquierda
        self.platforms.append(pygame.Rect(WIDTH - 40, 0, 40, HEIGHT)) # pared derecha
        self.platforms.append(pygame.Rect(0, 0, WIDTH, 40))           # techo
        self.platforms.append(pygame.Rect(0, HEIGHT - 40, WIDTH, 40)) # suelo

        # Plataformas jugables
        self.platforms.append(pygame.Rect(95, 345, 200, 20))   # izquierda
        self.platforms.append(pygame.Rect(665, 345, 200, 20))  # derecha
        self.platforms.append(pygame.Rect(380, 470, 200, 30))  # columna baja central

        # --- PINCHOS ---
        self.spikes = []  # sin pinchos en este nivel

        # --- ENEMIGOS ---
        self.enemies = pygame.sprite.Group()  # los agregamos desde Game

        # --- COLUMNAS (height > 60) ---
        self.columns = [p for p in self.platforms if p.height > 60]

        # --- Dimensiones del nivel ---
        self.level_width = WIDTH
        self.level_height = HEIGHT

        # --- Debug info ---
        self.print_debug_info()

    def print_debug_info(self):
        print("=== PLATAFORMAS NIVEL 2 ===")
        for i, p in enumerate(self.platforms):
            print(f"{i}: x={p.x}, y={p.y}, w={p.width}, h={p.height}")

    def draw(self, screen):
        screen.fill((25, 25, 35))

        # Dibujar plataformas
        for p in self.platforms:
            color = (150, 90, 40) if p.height <= 60 else (100, 70, 30)
            pygame.draw.rect(screen, color, p)
            pygame.draw.rect(screen, (70, 45, 20), p.inflate(-4, -4))

        # Dibujar enemigos
        for enemy in self.enemies:
            enemy.draw(screen)