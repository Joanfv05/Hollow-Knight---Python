import pygame
from settings import WIDTH, HEIGHT

class Level2:
    def __init__(self):
        # --- PLATAFORMAS ---
        self.platforms = []

        # Paredes y techo/suelo
        self.platforms.append(pygame.Rect(0, 0, 40, HEIGHT))        # pared izquierda
        self.platforms.append(pygame.Rect(WIDTH - 40, 0, 40, HEIGHT)) # pared derecha
        self.platforms.append(pygame.Rect(0, 0, WIDTH, 40))         # techo
        self.platforms.append(pygame.Rect(0, HEIGHT - 40, WIDTH, 40)) # suelo

        # Plataformas jugables
        self.platforms.append(pygame.Rect(90, 345, 200, 20))   # izquierda
        self.platforms.append(pygame.Rect(670, 345, 200, 20))  # derecha
        self.platforms.append(pygame.Rect(380, 470, 200, 30))  # columna baja central

        # --- PINCHOS ---
        self.spikes = []  # sin pinchos en este nivel

        # --- SALIDA / PUERTA (desactivada por ahora) ---
        self.exit_rect = pygame.Rect(WIDTH - 80, 400, 40, 40)  # dibujada pero no activa

        # --- ENEMIGOS ---
        self.enemies = pygame.sprite.Group()  # vacío por ahora

        # --- COLUMNAS (height > 60) ---
        self.columns = [p for p in self.platforms if p.height > 60]

        # --- Dimensiones del nivel ---
        self.level_width = WIDTH
        self.level_height = HEIGHT

        # Debug info
        self.print_debug_info()

    def print_debug_info(self):
        print("=== PLATAFORMAS NIVEL 2 ===")
        for i, p in enumerate(self.platforms):
            print(f"{i}: x={p.x}, y={p.y}, w={p.width}, h={p.height}")
        print("=== PUERTA NIVEL 2 (desactivada) ===")
        print(f"exit: x={self.exit_rect.x}, y={self.exit_rect.y}, w={self.exit_rect.width}, h={self.exit_rect.height}")

    def draw(self, screen):
        screen.fill((25, 25, 35))

        # Dibujar plataformas
        for p in self.platforms:
            color = (150, 90, 40) if p.height <= 60 else (100, 70, 30)
            pygame.draw.rect(screen, color, p)
            pygame.draw.rect(screen, (70, 45, 20), p.inflate(-4, -4))

        # No hay pinchos en este nivel

        # Dibujar puerta (solo como referencia, no activa)
        pygame.draw.rect(screen, (25, 25, 35), self.exit_rect)
