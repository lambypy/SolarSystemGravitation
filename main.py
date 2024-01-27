import math
import pygame


pygame.init()

WIDTH, HEIGHT = 1280, 720
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System Gravitation")

background = pygame.transform.scale(pygame.image.load("Images/space_background.jpeg"), (WIDTH, HEIGHT))

WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

OBJ_SIZE = 5
PLANET_SIZE = 50
PLANET_MASS = 100
SHIP_MASS = 5
G = 5
VEL_SCALE = 100


# Sun and Planets 
sun = pygame.transform.scale(pygame.image.load("Images/sun_img.png"), (PLANET_SIZE*2, PLANET_SIZE*2))
asteroid = pygame.transform.scale(pygame.image.load("Images/asteroid.jpg"), (10, 10))


class Asteroid:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        win.blit(sun, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))



# Create asteroid/planet
class AsteroidCreation:
    def __init__(self, x, y, vel_x, vel_y, mass) -> None:
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass


    def move(self, planet=None):
        """Moving the asteroid based on the planet mass"""
        distance = math.sqrt((self.x - planet.x)**2 + (self.y - planet.y)**2)
        force = (G * self.mass * planet.mass) / distance ** 2
        
        acceleration = force / self.mass
        angle = math.atan2(planet.y - self.y, planet.x - self.x)

        acceleration_x = acceleration * math.cos(angle)
        acceleration_y = acceleration * math.sin(angle)

        self.vel_x += acceleration_x
        self.vel_y += acceleration_y

        self.x += self.vel_x
        self.y += self.vel_y


    def draw(self):
        """Updates the asteroid position on the screen"""
        win.blit(asteroid, (int(self.x), int(self.y)))




def add_planet_menu():
    """Shows the Planet Menu with choices of size and position."""
    pass



def user_creation(location, mouse):
    """Creates the asteroid based on location and mouse direction"""
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    obj = AsteroidCreation(t_x, t_y, vel_x, vel_y, SHIP_MASS)
    return obj


def main():
    running = True
    paused_flag = False

    planet = Asteroid(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None

    while running:
        mouse_pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: 
                    # Press "Q" to quit
                    print("pressed to quit.")
                    running = False
                elif event.key == pygame.K_r:
                    # Press "R" to reset
                    print("pressed to reset")
                elif event.key == pygame.K_p:
                    # Press "P" to pause
                    paused_flag = not paused_flag
                    print("pressed to pause")
            # Add in the user creation 
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = user_creation(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        if not paused_flag:
            win.blit(background, (0, 0))
            if temp_obj_pos:
                pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
                pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)


            for obj in objects[:]:
                obj.draw()
                obj.move(planet)
                off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
                collided = math.sqrt((obj.x - planet.x)**2 + (obj.y - planet.y)**2) <= PLANET_SIZE
                if off_screen or collided:
                    objects.remove(obj)

        # Adds the "Paused" label to the screen
        if paused_flag:
            font = pygame.font.Font(None, 36)
            text = font.render("Paused", True, WHITE)
            win.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 4 - text.get_height() // 2))

        planet.draw()
        pygame.display.update()

    pygame.quit()


if __name__=="__main__":
    main()


