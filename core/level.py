import pygame
import random

class Level:
    def __init__(self):
        self.platforms = []
        self.walls = []
        self.hazards = []
        self.falling_objects = []
        self.object_triggered = [] 

        # === CONFIGURACIÓN GENERAL ===
        self.level_width = 3000
        self.level_height = 600
        wall_width = 40
        ground_height = 40

        # === SUELO PRINCIPAL (camino largo) ===
        ground_rect = pygame.Rect(0, self.level_height - ground_height, self.level_width, ground_height)
        self.platforms.append(ground_rect)

        # === PAREDES LATERALES Y TECHO ===
        self.walls.append(pygame.Rect(0, 0, wall_width, self.level_height))                    # izquierda
        self.walls.append(pygame.Rect(self.level_width - wall_width, 0, wall_width, self.level_height))  # derecha
        self.walls.append(pygame.Rect(0, 0, self.level_width, wall_width))                     # techo

        # === PINCHOS EN EL CAMINO (algunos tramos aleatorios) ===
        for i in range(5):
            x = 500 + i * 400
            width = 100
            spike_rect = pygame.Rect(x, self.level_height - ground_height - 20, width, 20)
            self.hazards.append(spike_rect)

        # === HABITACIÓN FINAL ===
        self.room_start_x = 2500
        room_width = 500
        room_ground_y = self.level_height - ground_height

        # Pinchos en el suelo de la habitación (triángulos)
        self.room_spikes = []
        for x in range(self.room_start_x + 50, self.room_start_x + room_width - 50, 40):
            triangle = [(x, room_ground_y), (x + 20, room_ground_y - 20), (x + 40, room_ground_y)]
            self.room_spikes.append(triangle)

        # === PLATAFORMAS DENTRO DE LA HABITACIÓN (para subir) ===
        self.platforms += [
            pygame.Rect(self.room_start_x + 100, 450, 150, 20),
            pygame.Rect(self.room_start_x + 300, 350, 150, 20),
            pygame.Rect(self.room_start_x + 200, 250, 150, 20)
        ]

    def draw(self, screen):
        color_platform = (180, 100, 0)
        color_wall = (120, 70, 0)
        color_spike = (200, 0, 0)
        color_triangle = (255, 50, 50)

        # Plataformas
        for p in self.platforms:
            pygame.draw.rect(screen, color_platform, p)

        # Paredes
        for w in self.walls:
            pygame.draw.rect(screen, color_wall, w)

        # Pinchos rectangulares del camino
        for h in self.hazards:
            pygame.draw.rect(screen, color_spike, h)

        # Pinchos triangulares de la habitación
        for tri in self.room_spikes:
            pygame.draw.polygon(screen, color_triangle, tri)

    def check_collision(self, rect):
        # Retorna True si el rect colisiona con paredes o plataformas
        for wall in self.walls + self.platforms:
            if rect.colliderect(wall):
                return True
        return False

    def check_hazard_collision(self, rect):
        """Detecta si el jugador toca pinchos."""
        for h in self.hazards:
            if rect.colliderect(h):
                return True
        for tri in self.room_spikes:
            if self.point_in_triangle(rect.center, tri):
                return True
        return False

    def point_in_triangle(self, point, triangle):
        """Comprobación matemática de punto dentro de triángulo."""
        def sign(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1 = sign(point, triangle[0], triangle[1]) < 0.0
        b2 = sign(point, triangle[1], triangle[2]) < 0.0
        b3 = sign(point, triangle[2], triangle[0]) < 0.0
        return b1 == b2 and b2 == b3
