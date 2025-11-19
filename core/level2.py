import pygame
from settings import WIDTH, HEIGHT

class Level2:
    def __init__(self):
        self.platforms = []
        self.spikes = []

        # === PLATAFORMAS DEL NIVEL 2 ===
        platform_data = [
            (0, 0, 40, 540),    # pared izquierda
            (920, 0, 40, 540),  # pared derecha
            (0, 0, 960, 40),    # techo
            (0, 500, 960, 40),  # suelo
            (100, 400, 200, 20),
            (400, 300, 150, 20),
            (650, 200, 200, 20),
        ]
        for x, y, w, h in platform_data:
            self.platforms.append(pygame.Rect(x, y, w, h))

        # === PINCHOS DEL NIVEL 2 ===
        spike_data = [
            (200, 475, 40, 25),
            (500, 475, 40, 25),
        ]
        for x, y, w, h in spike_data:
            self.spikes.append(pygame.Rect(x, y, w, h))

        # === SALIDA / PUERTA ===
        self.exit_rect = pygame.Rect(920 - 40, 460, 40, 40)  # pared derecha abajo

    def draw(self, screen):
        screen.fill((25, 25, 35))

        # Plataformas
        for p in self.platforms:
            color = (100, 70, 30) if p.height > 60 else (150, 90, 40)
            pygame.draw.rect(screen, color, p)
            pygame.draw.rect(screen, (70, 45, 20), p.inflate(-4, -4))

        # Pinchos
        spike_color = (50, 50, 50)
        for s in self.spikes:
            pygame.draw.polygon(screen, spike_color, [
                (s.left, s.bottom),
                (s.centerx, s.top),
                (s.right, s.bottom)
            ])

        # Puerta / salida (igual al fondo)
        pygame.draw.rect(screen, (25, 25, 35), self.exit_rect)
