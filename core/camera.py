class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height

    def apply(self, rect):
        """Devuelve la posición del rectángulo con el offset de la cámara"""
        return rect.move(-self.offset_x, -self.offset_y)

    def update(self, target, level_width, level_height):
        """Actualiza el offset de la cámara según la posición del jugador"""
        # Centrar horizontalmente
        self.offset_x = target.rect.centerx - self.width // 2
        if self.offset_x < 0:
            self.offset_x = 0
        elif self.offset_x > level_width - self.width:
            self.offset_x = level_width - self.width

        # Centrar verticalmente (para ver el suelo)
        self.offset_y = target.rect.centery - self.height // 2
        if self.offset_y < 0:
            self.offset_y = 0
        elif self.offset_y > level_height - self.height:
            self.offset_y = level_height - self.height
