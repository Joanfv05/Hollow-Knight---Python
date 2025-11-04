class Camera:
    def __init__(self, width, height, level_width, level_height):
        self.offset_x = 0
        self.offset_y = 0
        self.width = width
        self.height = height
        self.level_width = level_width
        self.level_height = level_height

    def apply(self, rect):
        """Devuelve el rect sin desplazamiento (cámara estática)."""
        return rect

    def update(self, target):
        """No mueve la cámara — permanece fija."""
        self.offset_x = 0
        self.offset_y = 0
