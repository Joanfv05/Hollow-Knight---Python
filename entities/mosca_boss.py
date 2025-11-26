import pygame
import math
import time
import random

class MoscaBoss(pygame.sprite.Sprite):
    def __init__(self, x, y, level, player):
        super().__init__()
        self.level = level
        self.player = player

        # Tamaño del boss
        self.width = 140
        self.height = 90
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Cargar imagen o usar dibujo básico
        self.body_color = (200, 200, 200)
        self.wing_color = (255, 255, 255)
        self.hurt_color = (255, 100, 100)  # Color cuando es dañado

        self.rect = self.image.get_rect(center=(x, y))
        self.hitbox = pygame.Rect(0, 0, self.width * 0.6, self.height * 0.7)
        self.hitbox.center = self.rect.center

        # Estados del boss
        self.states = {
            "PATROL": 0,
            "DETECTED": 1,
            "ATTACKING": 2,
            "RETURNING": 3,
            "STUNNED": 4
        }
        self.current_state = self.states["PATROL"]
        self.state_timer = 0

        # Movimiento
        self.base_speed = 2
        self.attack_speed = 6
        self.direction = 1  # 1 = derecha, -1 = izquierda
        self.vertical_direction = 0
        
        # Ataques
        self.attack_patterns = ["vertical", "dash", "bomb"]
        self.current_attack = None
        self.attack_cooldown = 0
        self.attack_duration = 0
        
        # Posiciones importantes
        self.spawn_position = (x, y)
        self.patrol_bounds = (100, self.level.level_width - 100)
        self.patrol_height_range = (50, 150)

        # Aleteo / flotación
        self.wing_angle = 0
        self.wing_direction = 1
        self.wing_speed = 8
        self.wing_offset_max = 25
        self.float_angle = 0
        self.float_speed = 3
        self.float_amplitude = 2

        # Vida
        self.health = 20
        self.max_health = 20
        self.alive = True
        self.invincible = False
        self.invincible_time = 0.5
        self.last_hit_time = 0
        self.flash_timer = 0

        # Detección jugador
        self.detection_range = 400
        self.attack_range = 300
        self.lost_sight_time = 0
        self.max_lost_sight_time = 2.0  # segundos

        # Spawn retrasado
        self.spawn_time = time.time()
        self.delay = 2  # segundos

        # Física
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 0.2

        self.update_image()

    def update_image(self):
        """Dibuja cuerpo y alas con aleteo y efectos visuales"""
        self.image.fill((0, 0, 0, 0))
        
        # Efecto de parpadeo cuando es invencible
        current_color = self.body_color
        if self.invincible and int(self.flash_timer * 10) % 2 == 0:
            current_color = self.hurt_color
        
        # Cuerpo
        body_width = int(self.width * 0.7)
        body_height = int(self.height * 0.5)
        body_x = int((self.width - body_width) / 2)
        body_y = int((self.height - body_height) / 2)
        
        # Alas con aleteo
        wing_offset = int(math.sin(math.radians(self.wing_angle)) * self.wing_offset_max)
        
        # Ala izquierda
        pygame.draw.ellipse(self.image, self.wing_color, 
                           (body_x - body_width//2, body_y + wing_offset, 
                            body_width//1.5, body_height//1.5))
        
        # Ala derecha  
        pygame.draw.ellipse(self.image, self.wing_color,
                           (body_x + body_width - body_width//6, body_y - wing_offset,
                            body_width//1.5, body_height//1.5))
        
        # Cuerpo
        pygame.draw.ellipse(self.image, current_color, (body_x, body_y, body_width, body_height))
        
        # Ojos (señalan hacia el jugador)
        eye_radius = body_height // 5
        left_eye_x = body_x + body_width // 3
        right_eye_x = body_x + 2 * body_width // 3
        eye_y = body_y + body_height // 3
        
        pygame.draw.circle(self.image, (0, 0, 0), (left_eye_x, eye_y), eye_radius)
        pygame.draw.circle(self.image, (0, 0, 0), (right_eye_x, eye_y), eye_radius)

    def check_player_detection(self):
        """Mejorada detección del jugador con línea de visión"""
        player_x, player_y = self.player.rect.center
        boss_x, boss_y = self.rect.center
        
        # Distancia al jugador
        distance = math.sqrt((player_x - boss_x)**2 + (player_y - boss_y)**2)
        
        # Si está muy lejos, no detectar
        if distance > self.detection_range:
            return False
            
        # Verificar línea de visión
        line_of_sight = True
        test_points = 10
        
        for i in range(test_points + 1):
            test_x = boss_x + (player_x - boss_x) * i / test_points
            test_y = boss_y + (player_y - boss_y) * i / test_points
            test_rect = pygame.Rect(test_x - 10, test_y - 10, 20, 20)
            
            for plat in self.level.platforms:
                if plat.colliderect(test_rect) and plat.height > 40:
                    line_of_sight = False
                    break
                    
            if not line_of_sight:
                break
                
        return line_of_sight and distance <= self.detection_range

    def choose_attack(self):
        """Selecciona un patrón de ataque basado en la posición del jugador"""
        player_x, player_y = self.player.rect.center
        boss_x, boss_y = self.rect.center
        
        # Si el jugador está debajo, ataque vertical
        if player_y > boss_y + 50:
            return "vertical"
        # Si está a la misma altura, dash
        elif abs(player_y - boss_y) < 50:
            return "dash"
        # Si está arriba, lanzar "bombas" (proyectiles)
        else:
            return "bomb"

    def update_movement(self):
        """Actualiza el movimiento según el estado actual"""
        current_time = time.time()
        
        # Actualizar hitbox
        self.hitbox.center = self.rect.center
        
        # Aleteo y flotación constante
        self.wing_angle += self.wing_speed * self.wing_direction
        if self.wing_angle >= 180 or self.wing_angle <= 0:
            self.wing_direction *= -1
            
        self.float_angle += self.float_speed
        float_offset = math.sin(math.radians(self.float_angle)) * self.float_amplitude
        self.rect.y += float_offset
        
        # Máquina de estados
        if self.current_state == self.states["PATROL"]:
            self.patrol_movement()
            
        elif self.current_state == self.states["DETECTED"]:
            self.tracking_movement()
            
        elif self.current_state == self.states["ATTACKING"]:
            self.attack_movement()
            
        elif self.current_state == self.states["RETURNING"]:
            self.return_to_patrol()
            
        elif self.current_state == self.states["STUNNED"]:
            if current_time - self.state_timer > 0.5:  # 0.5 segundos de aturdimiento
                self.current_state = self.states["PATROL"]

        # Enfriamiento de ataque
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def patrol_movement(self):
        """Movimiento de patrulla básico"""
        self.rect.x += self.base_speed * self.direction
        
        # Cambiar dirección en bordes
        if self.rect.left <= self.patrol_bounds[0]:
            self.direction = 1
        elif self.rect.right >= self.patrol_bounds[1]:
            self.direction = -1
            
        # Flotación vertical aleatoria en patrulla
        if random.random() < 0.02:  # 2% de probabilidad por frame
            self.vertical_direction = random.choice([-1, 0, 1])
            
        self.rect.y += self.vertical_direction
        
        # Mantener dentro del rango de patrulla vertical
        if self.rect.top < self.patrol_height_range[0]:
            self.rect.top = self.patrol_height_range[0]
            self.vertical_direction = 1
        elif self.rect.bottom > self.patrol_height_range[1]:
            self.rect.bottom = self.patrol_height_range[1]
            self.vertical_direction = -1

    def tracking_movement(self):
        """Seguir al jugador sin atacar todavía"""
        player_x, player_y = self.player.rect.center
        boss_x, boss_y = self.rect.center
        
        # Moverse hacia el jugador pero mantener distancia
        if abs(player_x - boss_x) > 100:
            self.direction = 1 if player_x > boss_x else -1
            self.rect.x += self.base_speed * 1.5 * self.direction
            
        # Movimiento vertical para alinearse
        if abs(player_y - boss_y) > 50:
            vertical_dir = 1 if player_y > boss_y else -1
            self.rect.y += self.base_speed * vertical_dir

    def attack_movement(self):
        """Ejecutar el patrón de ataque actual"""
        if self.current_attack == "vertical":
            self.vertical_attack()
        elif self.current_attack == "dash":
            self.dash_attack()
        elif self.current_attack == "bomb":
            self.bomb_attack()

    def vertical_attack(self):
        """Ataque en picado vertical"""
        self.rect.y += self.attack_speed
        
        # Terminar ataque si llega al suelo o al jugador
        if self.rect.bottom >= self.level.level_height - 50:
            self.current_state = self.states["RETURNING"]
        elif self.rect.colliderect(self.player.rect):
            self.current_state = self.states["RETURNING"]

    def dash_attack(self):
        """Ataque de dash horizontal"""
        self.rect.x += self.attack_speed * self.direction
        
        # Terminar dash si choca con pared o pasa al jugador
        player_x = self.player.rect.centerx
        boss_x = self.rect.centerx
        
        if (self.direction > 0 and boss_x > player_x) or (self.direction < 0 and boss_x < player_x):
            self.current_state = self.states["RETURNING"]
            
        # Detección de colisión con paredes
        for plat in self.level.platforms:
            if plat.height > 60 and self.rect.colliderect(plat):
                self.current_state = self.states["STUNNED"]
                self.state_timer = time.time()
                break

    def bomb_attack(self):
        """Preparar lanzamiento de proyectiles"""
        # En una implementación completa, aquí se crearían proyectiles
        # Por ahora, solo se mueve hacia posición de lanzamiento
        target_y = max(50, self.player.rect.centery - 200)
        if self.rect.y > target_y:
            self.rect.y -= self.base_speed
            
        if abs(self.rect.y - target_y) < 10:
            self.current_state = self.states["RETURNING"]
            # Aquí se lanzarían bombas/proyectiles

    def return_to_patrol(self):
        """Volver a la posición de patrulla"""
        target_x = self.spawn_position[0]
        target_y = self.spawn_position[1]
        
        # Moverse hacia la posición de spawn
        if abs(self.rect.centerx - target_x) > 10:
            direction = 1 if target_x > self.rect.centerx else -1
            self.rect.x += self.base_speed * direction
            
        if abs(self.rect.centery - target_y) > 10:
            direction = 1 if target_y > self.rect.centery else -1
            self.rect.y += self.base_speed * direction
            
        # Si está lo suficientemente cerca, volver a patrulla
        if (abs(self.rect.centerx - target_x) < 20 and 
            abs(self.rect.centery - target_y) < 20):
            self.current_state = self.states["PATROL"]

    def handle_collisions(self):
        """Manejar colisiones con el escenario"""
        # Colisiones horizontales
        self.rect.x += self.velocity_x
        for plat in self.level.platforms:
            if self.rect.colliderect(plat) and plat.height > 40:  # Solo plataformas sólidas
                if self.velocity_x > 0:
                    self.rect.right = plat.left
                    self.velocity_x = 0
                    if self.current_state == self.states["ATTACKING"]:
                        self.current_state = self.states["STUNNED"]
                        self.state_timer = time.time()
                elif self.velocity_x < 0:
                    self.rect.left = plat.right
                    self.velocity_x = 0
                    if self.current_state == self.states["ATTACKING"]:
                        self.current_state = self.states["STUNNED"]
                        self.state_timer = time.time()
        
        # Colisiones verticales
        self.rect.y += self.velocity_y
        for plat in self.level.platforms:
            if self.rect.colliderect(plat) and plat.height > 40:
                if self.velocity_y > 0:
                    self.rect.bottom = plat.top
                    self.velocity_y = 0
                elif self.velocity_y < 0:
                    self.rect.top = plat.bottom
                    self.velocity_y = 0

    def update(self, player):
        if time.time() - self.spawn_time < self.delay or not self.alive:
            return

        # Actualizar temporizadores
        current_time = time.time()
        if self.invincible:
            self.flash_timer = current_time - self.last_hit_time

        # Detección del jugador y transiciones de estado
        player_detected = self.check_player_detection()
        
        if player_detected:
            if self.current_state == self.states["PATROL"]:
                self.current_state = self.states["DETECTED"]
                self.lost_sight_time = 0
            elif self.current_state == self.states["DETECTED"] and self.attack_cooldown <= 0:
                self.current_state = self.states["ATTACKING"]
                self.current_attack = self.choose_attack()
                self.attack_cooldown = 120  # 2 segundos aprox a 60 FPS
                self.state_timer = current_time
        else:
            if self.current_state in [self.states["DETECTED"], self.states["ATTACKING"]]:
                self.lost_sight_time += 1/60  # Asumiendo 60 FPS
                if self.lost_sight_time >= self.max_lost_sight_time:
                    self.current_state = self.states["RETURNING"]
                    self.lost_sight_time = 0

        # Actualizar movimiento y colisiones
        self.update_movement()
        self.handle_collisions()
        
        # Mantener dentro de los límites del nivel
        self.rect.left = max(40, min(self.rect.left, self.level.level_width - 40 - self.rect.width))
        self.rect.top = max(40, min(self.rect.top, self.level.level_height - 40 - self.rect.height))

        # Actualizar imagen
        self.update_image()

        # Detección de daño al jugador
        if (self.hitbox.colliderect(player.rect) and not player.invincible and 
            self.current_state == self.states["ATTACKING"]):
            player.take_damage()

        # Actualizar invencibilidad
        self.update_invincibility()

    def take_damage(self):
        if not self.invincible and self.alive:
            self.health -= 1
            self.invincible = True
            self.last_hit_time = time.time()
            
            # Efecto de retroceso
            self.velocity_x = -self.direction * 3
            self.velocity_y = -2
            
            # Cambiar a estado aturdido si no estaba atacando
            if self.current_state != self.states["ATTACKING"]:
                self.current_state = self.states["STUNNED"]
                self.state_timer = time.time()
                
            print("Boss hit! Vida restante:", self.health)
            
            if self.health <= 0:
                self.die()

    def update_invincibility(self):
        if self.invincible and (time.time() - self.last_hit_time >= self.invincible_time):
            self.invincible = False
            self.flash_timer = 0

    def die(self):
        self.alive = False
        # Aquí podrías añadir animación de muerte, sonidos, etc.
        print("¡Jefe derrotado!")

    def draw(self, screen):
        if time.time() - self.spawn_time < self.delay:
            return
        if self.alive:
            screen.blit(self.image, self.rect)
            
            # Opcional: Dibujar barra de vida
            bar_width = 100
            bar_height = 10
            bar_x = self.rect.centerx - bar_width // 2
            bar_y = self.rect.top - 20
            
            # Fondo de la barra
            pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
            # Vida actual
            health_width = int((self.health / self.max_health) * bar_width)
            pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, health_width, bar_height))