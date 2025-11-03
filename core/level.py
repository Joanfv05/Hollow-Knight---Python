import pygame

class Level:
    def __init__(self):
        self.platforms = []
        self.hazards = []
        self.walls = []
        self.falling_objects = []

        # --- Gran plataforma para moverse ---
        self.platforms.append(pygame.Rect(0, 500, 1500, 40))  # gran suelo

        # --- Objetos que caen ---
        # Colocados estratégicamente sobre la plataforma
        for i in range(5):
            x = 200 + i*250
            y = 50  # empiezan desde arriba
            self.falling_objects.append(pygame.Rect(x, y, 30, 30))

        # Trigger de caída
        self.object_triggered = [False] * len(self.falling_objects)
        self.falling_speed = 5

    def draw(self, screen):
        # Color marrón para plataforma y objetos
        color_platform = (200, 100, 0)

        # Dibujar plataforma
        for p in self.platforms:
            pygame.draw.rect(screen, color_platform, p)

        # Dibujar objetos que caen (mismo color marrón)
        for obj in self.falling_objects:
            pygame.draw.rect(screen, color_platform, obj)
