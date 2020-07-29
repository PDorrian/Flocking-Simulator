import pygame.gfxdraw
import pygame
import random
import math
from pygame.math import Vector2


class Boid:
    def __init__(self, screen):
        # Screen setup
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()

        # Position & direction setup
        self.x, self.y = x, y = random.randrange(0, self.width), random.randrange(0, self.height)
        self.pos = Vector2(x, y)
        self.dir = Vector2(random.uniform(-1, 1), random.uniform(-1, 1)).normalize()
        self.angle = -self.dir.as_polar()[1]            # Sprite direction
        self.rotation_direction = 0                     # Current rotation (>0 = Right, <0 = Left)

        # Sprite setup
        image = pygame.image.load("bird.png")
        self.image = pygame.transform.scale(image, (20, 20))
        self.image_rot = self.image.copy()
        self.rect = self.image.get_rect(center=(x, y))

        # Physics variables
        self.rotation_speed = 1                      # How quickly they rotate with arrow keys
        self.speed = 2

        self.alignmentness = 0.02
        self.cohesiveness = 0.03
        self.separateness = 0.1

        self.alignment_radius = 100
        self.cohesion_radius = 100
        self.separation_radius = 15

    def align(self, boids):
        perception_radius = self.alignment_radius
        count = 0
        average_dir = Vector2()
        for other in boids:
            if other != self and self.pos.distance_to(other.pos) < perception_radius:
                average_dir = average_dir + other.dir
                count += 1
        if count > 0:
            average_dir = average_dir / count
            average_dir = average_dir - self.dir    # The steering error
        if average_dir.length() != 0:
            average_dir = average_dir.normalize()
        return average_dir

    def cohere(self, boids):
        perception_radius = self.cohesion_radius
        count = 0
        average_pos = Vector2()
        for other in boids:
            if other != self and self.pos.distance_to(other.pos) < perception_radius:
                average_pos = average_pos + other.pos
                count += 1
        if count > 0:
            average_pos = average_pos / count
            average_pos = average_pos - self.pos    # The steering error
        if average_pos.length() != 0:
            average_pos = average_pos.normalize()
        return average_pos

    def separate(self, boids):
        perception_radius = self.separation_radius
        count = 0
        average_pos = Vector2()
        for other in boids:
            if other != self and self.pos.distance_to(other.pos) < perception_radius:
                average_pos = self.pos - other.pos
                if average_pos.magnitude() != 0:
                    average_pos = average_pos / average_pos.magnitude() ** 2
                else:
                    return Vector2(0, 0)
                average_pos += average_pos
                count += 1
        if count > 0:
            average_pos = average_pos / count
        if average_pos.length() != 0:
            average_pos = average_pos.normalize()
        return average_pos

    def flock(self, boids):
        alignment = self.align(boids)
        cohesion = self.cohere(boids)
        separation = self.separate(boids)
        self.dir += alignment * self.alignmentness
        self.dir += cohesion * self.cohesiveness
        self.dir += separation * self.separateness
        self.dir = self.dir.normalize()

    def rotate_right(self):
        self.rotation_direction = self.rotation_speed

    def rotate_left(self):
        self.rotation_direction = -self.rotation_speed

    def stop_rotation(self):
        self.rotation_direction = 0

    def move(self):
        self.pos += self.dir * self.speed
        self.dir.rotate_ip(self.rotation_direction)
        self.angle = -self.dir.as_polar()[1]

        x, y = self.pos.x, self.pos.y
        if x < 0:
            self.pos.x = self.width
        if x > self.width:
            self.pos.x = 0
        if y < 0:
            self.pos.y = self.height
        if y > self.height:
            self.pos.y = 0

    def draw(self):
        self.image_rot = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image_rot.get_rect(center=(self.pos.x, self.pos.y))
        self.screen.blit(self.image_rot, self.rect)

