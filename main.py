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

def check_collision(i, j):
    difference = asteroid_positions[j] - asteroid_positions[i]
    distance = difference.length() # to find distance between two centers
    if distance < asteroid_radii[i] + asteroid_radii[j]: # calculates a normal when a collision happens
        if distance == 0:
            normal = pygame.math.Vector2(1, 0)
        else:
            normal = difference.normalize()
        return normal
    return None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))
    for i in range(6):
        asteroid_positions[i] += asteroid_velocities[i]

        # for screen wrapping if asteroid goes off screen
        if asteroid_positions[i].x < 0:
            asteroid_positions[i].x = 800
        if asteroid_positions[i].x > 800:
            asteroid_positions[i].x = 0
        if asteroid_positions[i].y < 0:
            asteroid_positions[i].y = 600
        if asteroid_positions[i].y > 600:
            asteroid_positions[i].y = 0

        pygame.draw.circle(screen, (180, 180, 180), (int(asteroid_positions[i].x), int(asteroid_positions[i].y)), asteroid_radii[i])

    for i in range(6):
        for j in range(i + 1, 6):
            normal = check_collision(i, j)
            if normal is not None:
                relative_velocity = asteroid_velocities[j] - asteroid_velocities[i]
                speed_toward_each_other = relative_velocity.dot(normal)

                if speed_toward_each_other < 0: # negative means moving toward each other
                    mass_i = asteroid_radii[i] * asteroid_radii[i] # give larger asteroids more mass
                    mass_j = asteroid_radii[j] * asteroid_radii[j]

                    impulse = (-2 * speed_toward_each_other) / (1 / mass_i + 1 / mass_j) # calc impulse for collisions
                    asteroid_velocities[i] -= (impulse / mass_i) * normal
                    asteroid_velocities[j] += (impulse / mass_j) * normal

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()