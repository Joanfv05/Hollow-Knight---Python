import pygame

class Level:
    def __init__(self):
        # Plataformas principales
        self.platforms = [
            pygame.Rect(0, 500, 500, 40),
            pygame.Rect(550, 500, 500, 40),
            pygame.Rect(1100, 450, 200, 20),
            pygame.Rect(1150, 400, 150, 20),
            pygame.Rect(1200, 350, 100, 20),
            pygame.Rect(1250, 300, 100, 20),
            pygame.Rect(1300, 250, 150, 20),
            pygame.Rect(1450, 250, 250, 20)
        ]

        # Pinchos
        self.hazards = [
            pygame.Rect(400, 480, 50, 20),
            pygame.Rect(600, 480, 50, 20),
            pygame.Rect(1250, 280, 50, 20),
            pygame.Rect(1550, 230, 100, 20)
        ]

        # Objetos que caen
        self.falling_objects = [
            pygame.Rect(1150, 350, 30, 30),
            pygame.Rect(1250, 250, 30, 30),
            pygame.Rect(1400, 200, 30, 30)
        ]
        self.object_triggered = [False] * len(self.falling_objects)
        self.falling_speed = 5

        # Paredes
        self.walls = [
            pygame.Rect(0, 0, 50, 600),
            pygame.Rect(1800, 0, 50, 600),
            pygame.Rect(50, 0, 10, 500),
            pygame.Rect(1100, 0, 10, 500)
        ]
