"""
5px is 1m
widthxheight
800x500 -> 400m x 250m
rocket -> 3m x 2m -> 15px x 10px

"""

import random
import pygame

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

    # Draw the rocket
    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def update(self):
        self.x += convert_to_px(self.vel[0])
        self.y += convert_to_px(self.vel[1])
        self.rect.x = self.x
        self.rect.y = self.y


stars = []

rocket = Rocket(WIDTH//2, 100, 15, 10)

clock = pygame.time.Clock()


def draw_bg():
    WIN.fill((0, 0, 0))

    for star in stars:
        pygame.draw.circle(WIN, (255, 255, 255), (star[0], star[1]), 1)


def init_stars():
    for _ in range(100):
        x = random.randint(0, WIDTH)
        y = random.randint(0, HEIGHT)
        stars.append((x, y))


GRAVITY = 1.625 / 60  # m/s


def draw_fire(x, y):
    pygame.draw.rect(WIN, (255, 0, 0), (x+5, y + rocket.height, rocket.width-10, 10))
    pygame.draw.polygon(WIN, (255, 0, 0), [(x+rocket.width//2, y+rocket.height+10), (x+rocket.width//2-5, y+rocket.height+20), (x+rocket.width//2+5, y+rocket.height+20)])


def main():

    init_stars()

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
            
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            # 2700 N thrust
            # F = ma
            # a = F/m
            # a = 2700/1500
            # a = 1.8
            rocket.vel[1] -= 1.8 / 60

            draw_fire(rocket.x, rocket.y)

        rocket.update()
        rocket.draw(WIN)

        # Update the display
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

    pygame.quit()


if __name__ == "__main__":
    main()
