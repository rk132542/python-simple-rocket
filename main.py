import pygame

pygame.init()

WIN = pygame.display.set_mode((800, 500))
pygame.display.set_caption("Game")

# Rocket class to create a rocket object
class Rocket:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
    # Draw the rocket
    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), self.rect)   
        

rocket = Rocket(100, 100, 50, 50)


clock = pygame.time.Clock()

def main():
    run = True
    while run:
        clock.tick(60)
        
        # Clear the screen
        WIN.fill((255, 255, 255))
        # Draw the rocket
        rocket.draw(WIN)
        # Update the display
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
    
    pygame.quit()

if __name__ == "__main__":
    main()