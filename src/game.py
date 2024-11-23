import pygame
import math
from objects import CelestialObject, Asteroid
from settings import WIDTH, HEIGHT, WHITE, RED, OBJ_SIZE, PLANET_SIZE, PLANET_MASS, SHIP_MASS, VEL_SCALE


class Game:
    def __init__(self):
        """Initializes the game with imported settings and objects"""
        pygame.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Solar System Gravitation")
        self.background = pygame.transform.scale(pygame.image.load("assets/space_background.jpeg"), (WIDTH, HEIGHT))
        self.sun_img = pygame.transform.scale(pygame.image.load("assets/sun_img.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))
        self.asteroid_img = pygame.transform.scale(pygame.image.load("assets/asteroid.jpg"), (10, 10))

        self.planet = CelestialObject(WIDTH // 2, HEIGHT // 2, PLANET_MASS, self.sun_img)
        self.objects = []
        self.temp_obj_pos = None
        self.running = True
        self.paused = False
        self.quitting = False


    def user_creation(self, location, mouse):
        """Creates an asteroid from user input."""
        t_x, t_y = location
        m_x, m_y = mouse
        vel_x = (m_x - t_x) / VEL_SCALE
        vel_y = (m_y - t_y) / VEL_SCALE
        return Asteroid(t_x, t_y, vel_x, vel_y, SHIP_MASS, self.asteroid_img)


    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.quitting = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_q:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.temp_obj_pos:
                    obj = self.user_creation(self.temp_obj_pos, mouse_pos)
                    self.objects.append(obj)
                    self.temp_obj_pos = None
                else:
                    self.temp_obj_pos = mouse_pos


    def update(self):
        self.win.blit(self.background, (0, 0))
        if self.temp_obj_pos:
            pygame.draw.line(self.win, WHITE, self.temp_obj_pos, 
                             pygame.mouse.get_pos(), 2)
            pygame.draw.circle(self.win, RED, self.temp_obj_pos, OBJ_SIZE)

        for obj in self.objects[:]:
            obj.draw(self.win)
            obj.move([self.planet])
            off_screen = obj.x_pos < 0 or obj.x_pos > WIDTH or obj.y_pos < 0 \
                or obj.y_pos > HEIGHT
            collided = math.sqrt((obj.x_pos - self.planet.x_pos) ** 2 + 
                                 (obj.y_pos - self.planet.y_pos) ** 2) <= PLANET_SIZE
            if off_screen or collided:
                self.objects.remove(obj)

        self.planet.draw(self.win)
        pygame.display.update()


    def run(self):
        while self.running:
            self.handle_events()
            if not self.paused:
                self.update()
            elif self.quitting:
                print("Quitting")
                font = pygame.font.Font(None, 36)
                num = 3
                text = font.render(f"Quitting in {num}", True, WHITE)
                self.win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 - text.get_height() // 2))
                pygame.display.update()
            else:
                font = pygame.font.Font(None, 36)
                text = font.render("Paused", True, WHITE)
                self.win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 - text.get_height() // 2))
                pygame.display.update()
        pygame.quit()