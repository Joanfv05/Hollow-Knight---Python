import pygame
import random
from settings import WIDTH, HEIGHT


class Level:
    def __init__(self):
        self.platforms = []
        self.spikes = []

        wall_thickness = 40
        floor_height = HEIGHT - wall_thickness

        # === PAREDES Y SUELO ===
        self.platforms.append(pygame.Rect(0, 0, wall_thickness, HEIGHT))                       # izquierda
        self.platforms.append(pygame.Rect(WIDTH - wall_thickness, 0, wall_thickness, HEIGHT))  # derecha
        self.platforms.append(pygame.Rect(0, 0, WIDTH, wall_thickness))                        # techo
        self.platforms.append(pygame.Rect(0, floor_height, WIDTH, wall_thickness))             # suelo

        # === PARÁMETROS DE SALTO DEL JUGADOR ===
        jump_height = 135  # altura máxima alcanzable
        num_platforms = random.randint(4, 5)
        min_width = 130
        max_width = 230
        min_gap_y = 90
        max_gap_y = jump_height - 20

        # === PRIMERA PLATAFORMA (accesible desde el suelo) ===
        last_y = floor_height - random.randint(5,10)

        for i in range(num_platforms):
            if last_y < 150:
                break

            width = random.randint(min_width, max_width)
            height = 20
            y = last_y - random.randint(min_gap_y, max_gap_y)
            if y < 100:
                y = last_y - min_gap_y
            x = random.randint(80, WIDTH - width - 80)

            plat_rect = pygame.Rect(x, y, width, height)
            if plat_rect.left < 60:
                plat_rect.left = 60
            if plat_rect.right > WIDTH - 60:
                plat_rect.right = WIDTH - 60
            if plat_rect.top < wall_thickness + 20:
                plat_rect.top = wall_thickness + 20

            self.platforms.append(plat_rect)
            last_y = y

        # === PINCHOS ===
        spike_width = 40
        spike_height = 25
        max_spikes = 3  # 🔹 máximo de 3 pinchos totales
        player_safe_zone = pygame.Rect(50, floor_height - 120, 150, 120)

        def overlap(rect, rects):
            return any(rect.colliderect(r) for r in rects)

        # Intentar colocar pinchos en el suelo
        attempts = 0
        while len(self.spikes) < max_spikes and attempts < 50:
            x = random.randint(60, WIDTH - spike_width - 60)
            y = floor_height - spike_height
            new_spike = pygame.Rect(x, y, spike_width, spike_height)
            if not new_spike.colliderect(player_safe_zone) and not overlap(new_spike, self.spikes):
                self.spikes.append(new_spike)
            attempts += 1

        # Ocasionalmente colocar 1 pincho sobre plataformas (solo si queda hueco)
        for plat in self.platforms[4:]:
            if len(self.spikes) >= max_spikes:
                break
            if random.random() < 0.3:
                x = random.randint(int(plat.left) + 15, int(plat.right) - spike_width - 15)
                y = plat.top - spike_height + 2
                new_spike = pygame.Rect(x, y, spike_width, spike_height)
                if not overlap(new_spike, self.spikes):
                    self.spikes.append(new_spike)
                if len(self.spikes) >= max_spikes:
                    break

        self.level_width = WIDTH
        self.level_height = HEIGHT

    def draw(self, screen):
        # === Fondo ===
        screen.fill((25, 25, 35))

        # === Plataformas ===
        for p in self.platforms:
            pygame.draw.rect(screen, (150, 90, 40), p)
            pygame.draw.rect(screen, (100, 60, 20), p.inflate(-4, -4))

        # === Pinchos (sin borde, rojos) ===
        for s in self.spikes:
            pygame.draw.polygon(screen, (255, 0, 0), [
                (s.left, s.bottom),
                (s.centerx, s.top),
                (s.right, s.bottom)
            ])
