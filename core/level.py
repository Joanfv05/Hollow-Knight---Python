import pygame
import random
from settings import WIDTH, HEIGHT

class Level:
    def __init__(self):
        self.platforms = []
        self.spikes = []  # 🧨 Lista de pinchos

        # === HABITACIÓN CERRADA ===
        wall_thickness = 40
        floor_height = HEIGHT - wall_thickness

        # Paredes
        self.platforms.append(pygame.Rect(0, 0, wall_thickness, HEIGHT))                       # izquierda
        self.platforms.append(pygame.Rect(WIDTH - wall_thickness, 0, wall_thickness, HEIGHT))  # derecha
        self.platforms.append(pygame.Rect(0, 0, WIDTH, wall_thickness))                        # techo
        self.platforms.append(pygame.Rect(0, floor_height, WIDTH, wall_thickness))             # suelo

        # === PLATAFORMAS INTERNAS ===
        self.platforms.append(pygame.Rect(WIDTH * 0.2, HEIGHT * 0.75, WIDTH * 0.15, 20))
        self.platforms.append(pygame.Rect(WIDTH * 0.45, HEIGHT * 0.63, WIDTH * 0.18, 20))
        self.platforms.append(pygame.Rect(WIDTH * 0.7, HEIGHT * 0.5, WIDTH * 0.15, 20))
        self.platforms.append(pygame.Rect(WIDTH * 0.3, HEIGHT * 0.38, WIDTH * 0.12, 20))

        # === PINCHOS ALEATORIOS ===
        spike_width = 40
        spike_height = 25
        player_safe_zone = pygame.Rect(50, floor_height - 120, 150, 120)  # zona donde inicia el jugador

        # 🔹 Dos pinchos en el suelo (evitando la zona segura)
        for _ in range(2):
            while True:
                x = random.randint(60, WIDTH - spike_width - 60)
                y = floor_height - spike_height
                spike_rect = pygame.Rect(x, y, spike_width, spike_height)
                if not spike_rect.colliderect(player_safe_zone):
                    self.spikes.append(spike_rect)
                    break

        # 🔹 Un pincho encima de una plataforma aleatoria
        base_platforms = self.platforms[4:]  # plataformas internas
        base = random.choice(base_platforms)
        x = random.randint(int(base.left) + 20, int(base.right) - spike_width - 20)
        y = base.top - spike_height + 1
        self.spikes.append(pygame.Rect(x, y, spike_width, spike_height))

        # Tamaño total del nivel
        self.level_width = WIDTH
        self.level_height = HEIGHT

    def draw(self, screen):
        # === Fondo ===
        screen.fill((25, 25, 35))

        # === Plataformas ===
        for p in self.platforms:
            pygame.draw.rect(screen, (150, 90, 40), p)
            pygame.draw.rect(screen, (100, 60, 20), p.inflate(-4, -4))

        # === PINCHOS (sin borde, rojos) ===
        for s in self.spikes:
            pygame.draw.polygon(screen, (255, 0, 0), [
                (s.left, s.bottom),   # izquierda abajo
                (s.centerx, s.top),   # punta
                (s.right, s.bottom)   # derecha abajo
            ])
