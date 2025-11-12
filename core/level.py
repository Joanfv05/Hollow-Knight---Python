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
        jump_height = 135  # altura máxima de salto
        num_platforms = random.randint(4, 5)
        min_width = 130
        max_width = 230
        min_gap_y = 90
        max_gap_y = jump_height - 20

        # === PRIMERA PLATAFORMA (accesible desde el suelo) ===
        last_y = floor_height - random.randint(5, 10)

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
            plat_rect.clamp_ip(pygame.Rect(60, wall_thickness + 20, WIDTH - 120, HEIGHT - 80))
            self.platforms.append(plat_rect)
            last_y = y

        # === NUEVAS COLUMNAS VERTICALES (tipo pilares desde el suelo) ===
        self._generate_vertical_columns(floor_height)

        # === PINCHOS ===
        spike_width = 40
        spike_height = 25
        max_spikes = 3
        player_safe_zone = pygame.Rect(50, floor_height - 120, 150, 120)

        def overlap(rect, rects):
            return any(rect.colliderect(r) for r in rects)

        attempts = 0
        while len(self.spikes) < max_spikes and attempts < 50:
            x = random.randint(60, WIDTH - spike_width - 60)
            y = floor_height - spike_height
            new_spike = pygame.Rect(x, y, spike_width, spike_height)

            # Evitar zona segura del jugador
            if new_spike.colliderect(player_safe_zone):
                attempts += 1
                continue

            # Evitar solapamiento con pinchos existentes
            if overlap(new_spike, self.spikes):
                attempts += 1
                continue

            # Evitar que esté dentro de columnas (height > 60)
            if any(new_spike.colliderect(c) for c in self.platforms if c.height > 60):
                attempts += 1
                continue

            self.spikes.append(new_spike)
            attempts += 1

        # Ocasionalmente colocar 1 pincho sobre plataformas horizontales
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

    def _generate_vertical_columns(self, floor_height):
        """Genera pilares verticales desde el suelo, evitando al jugador, pinchos y plataformas horizontales."""
        num_columns = random.randint(3, 4)
        column_width = random.randint(60, 80)
        min_height = 90
        max_height = 180

        player_zone = pygame.Rect(50, floor_height - 150, 200, 150)  # zona donde no poner columnas
        columns = []
        max_attempts = 20

        attempts = 0
        while len(columns) < num_columns and attempts < max_attempts:
            height = random.randint(min_height, max_height)
            x = random.randint(100, WIDTH - column_width - 100)
            y = floor_height - height
            column = pygame.Rect(x, y, column_width, height)

            # Evitar jugador
            if column.colliderect(player_zone):
                attempts += 1
                continue

            # Evitar solapamiento con otras columnas ya generadas
            if any(column.colliderect(c) for c in columns):
                attempts += 1
                continue

            # Evitar solapamiento con plataformas horizontales (height < 60)
            horizontal_platforms = [p for p in self.platforms if p.height <= 60]
            if any(column.colliderect(p) for p in horizontal_platforms):
                attempts += 1
                continue

            columns.append(column)
            attempts += 1

        # Ajustar altura de la columna más cercana al jugador
        if columns:
            nearest = min(columns, key=lambda c: abs(c.centerx - player_zone.centerx))
            nearest.height = max(min_height // 2, nearest.height // 2)
            nearest.y = floor_height - nearest.height

        self.platforms.extend(columns)

    def draw(self, screen):
        # === Fondo ===
        screen.fill((25, 25, 35))

        # === Plataformas horizontales y columnas ===
        for p in self.platforms:
            # Si la plataforma es más alta que ancha → color diferente (pilar)
            if p.height > 60:
                pygame.draw.rect(screen, (100, 70, 30), p)
                pygame.draw.rect(screen, (70, 45, 20), p.inflate(-4, -4))
            else:
                pygame.draw.rect(screen, (150, 90, 40), p)
                pygame.draw.rect(screen, (100, 60, 20), p.inflate(-4, -4))

        # === Pinchos ===
        spike_color = (50, 50, 50)  # 🔹 gris oscuro
        for s in self.spikes:
            pygame.draw.polygon(screen, spike_color, [
                (s.left, s.bottom),
                (s.centerx, s.top),
                (s.right, s.bottom)
            ])
