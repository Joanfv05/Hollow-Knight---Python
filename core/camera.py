class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height

    def apply(self, rect):
        """Devuelve la posición del rectángulo con el offset de la cámara"""
        return rect.move(-self.offset_x, -self.offset_y)

    def update(self, target):
        """Actualiza el offset de la cámara según la posición del jugador"""
        # Queremos que el jugador esté centrado horizontalmente
        self.offset_x = target.rect.centerx - self.width // 2
        # opcional: limitar la cámara al inicio del mapa
        if self.offset_x < 0:
            self.offset_x = 0
        # aquí no limitamos verticalmente, porque puede haber cuevas más altas
        self.offset_y = 0  # fija verticalmente por ahora
