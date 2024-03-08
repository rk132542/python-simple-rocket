"""
5px is 1m
widthxheight
800x500 -> 400m x 250m
rocket -> 3m x 2m -> 15px x 10px

"""

import random
import pygame

import polygon

pygame.init()

WIDTH, HEIGHT = 800, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


def convert_to_px(meters):
    return meters * 5

# Rocket class to create a rocket object


class Rocket:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = [0, 0]  # in m/s
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.color = (128, 128, 128)
        self.mass = 1500  # in kg
        self.thrust_level = 0 # 0~1 -> 0~100%
        self.engine_on = False
        self.polygon = polygon.Polygon(
            (
                ((self.x, self.y), (self.x + self.width, self.y)), # top
                ((self.x + self.width, self.y), (self.x + self.width, self.y + self.height)), # right
                ((self.x + self.width, self.y + self.height), (self.x, self.y + self.height)), # bottom
                ((self.x, self.y + self.height), (self.x, self.y)) # left
            ), self.color)

    # Draw the rocket
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        self.x += convert_to_px(self.vel[0])
        self.y += convert_to_px(self.vel[1])
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.polygon = polygon.Polygon(
            (
                ((self.x, self.y), (self.x + self.width, self.y)),  # top
                ((self.x + self.width, self.y), (self.x + \
                 self.width, self.y + self.height)),  # right
                ((self.x + self.width, self.y + self.height),
                 (self.x, self.y + self.height)),  # bottom
                ((self.x, self.y + self.height), (self.x, self.y))  # left
            ), self.color)


stars = []

rocket = Rocket(WIDTH//2, 100, 15, 10)

clock = pygame.time.Clock()


def draw_bg():
    WIN.fill((0, 0, 0))

    for star in stars:
        pygame.draw.circle(WIN, (255, 255, 255), (star[0], star[1]), 1)

def draw_thrust_level(thrust_level, engine_on):
    gauge_color = (255, 0, 0)
    if not engine_on:
        gauge_color = (128, 128, 128)
    pygame.draw.rect(WIN, (255, 255, 255), (10, 10, 100, 20))
    pygame.draw.rect(WIN, gauge_color, (10, 10, 100 * thrust_level, 20))

def draw_rocket_info(win, vel, y):
    vel_text = "Velocity: " + str(round(vel[1], 2)) + " m/s"
    y_text = "Y: " + str(round(y, 2))
    vel_text_surface = pygame.font.SysFont("arial", 15).render(vel_text, True, (255, 255, 255))
    y_text_surface = pygame.font.SysFont("arial", 15).render(y_text, True, (255, 255, 255))
    WIN.blit(vel_text_surface, (10, 40))
    WIN.blit(y_text_surface, (10, 60))    

def init_stars():
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        stars.append((x, y))


GRAVITY = 1.625 / 60  # m/s

def draw_fire(x, y, thrust_level):
    flame_height = int(thrust_level * 20)
    flame_width = rocket.width - 10
    flame_x = x + 5
    flame_y = y + rocket.height
    flame_color = (255, 0, 0)
    
    
    if thrust_level > 0:
        pygame.draw.rect(WIN, flame_color,
                         (flame_x, flame_y, flame_width, flame_height))
        pygame.draw.polygon(WIN, flame_color, [(x + rocket.width // 2, y + rocket.height + flame_height),
                                               (x + rocket.width // 2 - 5, y + rocket.height + flame_height + 10),
                                               (x + rocket.width // 2 + 5, y + rocket.height + flame_height + 10)])


def main():

    init_stars()
    
    floor_polygon = polygon.Polygon(
        (
            ((0, HEIGHT-20), (WIDTH, HEIGHT-20)), # top
            ((WIDTH, HEIGHT-20), (WIDTH, HEIGHT)), # right
            ((WIDTH, HEIGHT), (0, HEIGHT)), # bottom
            ((0, HEIGHT), (0, HEIGHT-20)) # left
        ), (255, 255, 255))

    run = True
    while run:
        pygame.display.set_caption("FPS: " + str(clock.get_fps()))
        clock.tick(60)
        draw_bg()

        # Apply gravity -> moon 1.625 m/s^2
        # 60fps -> 1 frame is 1/60s
        rocket.vel[1] += GRAVITY

        # Apply normal force
        if rocket.y + rocket.height >= HEIGHT:
            rocket.vel[1] = 0
            rocket.y = HEIGHT - rocket.height
        if rocket.polygon.collides_with(floor_polygon):
            print("A") #not work
            rocket.vel[1] = 0
            rocket.y = 20 - HEIGHT - rocket.height
        if floor_polygon.point_inside((rocket.x, rocket.y)):
            print("B") #not working :(
            rocket.vel[1] = 0
            rocket.y = 20 - HEIGHT - rocket.height
        
            
        if rocket.engine_on:
            # 2700 N thrust
            # F = ma
            # a = F/m
            # a = 2700/1500
            # a = 1.8
            thrust = 1.8 / 60
            rocket.vel[1] -= (thrust * rocket.thrust_level)

            draw_fire(rocket.x, rocket.y, rocket.thrust_level)

        rocket.update()
        rocket.draw(WIN)

        draw_thrust_level(rocket.thrust_level, rocket.engine_on)
        draw_rocket_info(WIN, rocket.vel, rocket.y)

        # Update the display
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    rocket.engine_on = not rocket.engine_on
            
            elif event.type == pygame.MOUSEWHEEL:
                # precise_y -> scroll
                print(event.y) # -10 to 10
                rocket.thrust_level += -1 * event.y / 100
                rocket.thrust_level = max(0, rocket.thrust_level)
                rocket.thrust_level = min(1, rocket.thrust_level)

    pygame.quit()


if __name__ == "__main__":
    main()
