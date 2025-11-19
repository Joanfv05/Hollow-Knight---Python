import pygame
from settings import WIDTH, HEIGHT

class Level:
    def __init__(self):
        self.platforms = []
        self.spikes = []

        # === PLATAFORMAS ===
        platform_data = [
            (0, 0, 40, 540),    # pared izquierda
            (0, 0, 960, 40),    # techo
            (0, 500, 960, 40),  # suelo
            (130, 326, 275, 20),
            (530, 205, 153, 20),
            (210, 145, 151, 20),
            (305, 454, 65, 46),
            (494, 381, 65, 119),
            (725, 260, 65, 243),
        ]

        # Crear plataformas iniciales
        for x, y, w, h in platform_data:
            self.platforms.append(pygame.Rect(x, y, w, h))

        # --- PARED DERECHA MODIFICADA (con hueco para puerta) ---
        # División: tramo superior, hueco, tramo inferior
        self.platforms.append(pygame.Rect(920, 0, 40, 400))    # parte superior
        self.platforms.append(pygame.Rect(920, 500, 40, 40))   # parte inferior

        # --- PUERTA / SALIDA ---
        # Un poco hacia dentro del nivel para que sea accesible
        self.exit_rect = pygame.Rect(900, 400, 60, 100)

        # === COLUMNAS (height > 60) ===
        self.columns = [p for p in self.platforms if p.height > 60]

        # === PINCHOS ===
        spike_data = [
            (372, 475, 40, 25),
            (580, 475, 40, 25),
            (208, 475, 40, 25),
        ]
        for x, y, w, h in spike_data:
            self.spikes.append(pygame.Rect(x, y, w, h))

        self.level_width = WIDTH
        self.level_height = HEIGHT

        # Imprimir info
        self.print_debug_info()

    def print_debug_info(self):
        print("=== PLATAFORMAS ===")
        for i, p in enumerate(self.platforms):
            print(f"{i}: x={p.x}, y={p.y}, w={p.width}, h={p.height}")

        print("=== PINCHOS ===")
        for i, s in enumerate(self.spikes):
            print(f"{i}: x={s.x}, y={s.y}, w={s.width}, h={s.height}")

        print("=== COLUMNAS ===")
        for i, c in enumerate(self.columns):
            print(f"{i}: x={c.x}, y={c.y}, w={c.width}, h={c.height}")

        print("=== PUERTA ===")
        print(f"exit: x={self.exit_rect.x}, y={self.exit_rect.y}, w={self.exit_rect.width}, h={self.exit_rect.height}")

    def draw(self, screen):
        screen.fill((25, 25, 35))

        # --- PLATAFORMAS ---
        for p in self.platforms:
            if p.height > 60:  # columna
                pygame.draw.rect(screen, (100, 70, 30), p)
                pygame.draw.rect(screen, (70, 45, 20), p.inflate(-4, -4))
            else:
                pygame.draw.rect(screen, (150, 90, 40), p)
                pygame.draw.rect(screen, (100, 60, 20), p.inflate(-4, -4))

        # --- PINCHOS ---
        spike_color = (50, 50, 50)
        for s in self.spikes:
            pygame.draw.polygon(screen, spike_color, [
                (s.left, s.bottom),
                (s.centerx, s.top),
                (s.right, s.bottom)
            ])

        # --- DIBUJAR PUERTA / SALIDA ---
        pygame.draw.rect(screen, (25, 25, 35), self.exit_rect)


