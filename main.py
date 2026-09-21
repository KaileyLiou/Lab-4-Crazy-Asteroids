import pygame
import random
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 4: Crazy Asteroids")

clock = pygame.time.Clock()
running = True

asteroid_positions = []
asteroid_velocities = []
asteroid_radii = []

for i in range(6):
    position = pygame.math.Vector2(random.randint(0, 800), random.randint(0, 600))
    velocity = pygame.math.Vector2(random.uniform(-3, 3), random.uniform(-3, 3))
    radius = random.randint(15, 35)
    asteroid_positions.append(position)
    asteroid_velocities.append(velocity)
    asteroid_radii.append(radius)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    score = 0
    for i in range(6):
        asteroid_positions[i] += asteroid_velocities[i]

    pygame.display.flip()
    print(f"Score: {score}")
    clock.tick(10)

pygame.quit()
sys.exit()