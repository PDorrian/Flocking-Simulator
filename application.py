import pygame
import math
from Boid import Boid
white = (255,255,255)
black = (0,0,0)
grey = (200,200,200)
red = (255,0,0)
green = (0,255,0)
blue = (220,220,255)

size = width, height = 1000, 600
screen = pygame.display.set_mode(size)
image_orig = pygame.image.load ("boid.png")
image_orig = pygame.transform.scale(image_orig, (100,100))
image_rect = image_orig.get_rect(center=(200,500))
image = image_orig.copy()
angle = 0

boids = []
for i in range(100):
    boids.append(Boid(screen))

running = True
while running:
    screen.fill(blue)

    for boid in boids:
        boid.flock(boids)
        boid.draw()
        boid.move()

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                for boid in boids:
                    boid.rotate_left()
            if event.key == pygame.K_RIGHT:
                print("Right")
                for boid in boids:
                    boid.rotate_right()

        if event.type == pygame.KEYUP:
            for boid in boids:
                boid.stop_rotation()

        if event.type == pygame.QUIT:
            running = False

