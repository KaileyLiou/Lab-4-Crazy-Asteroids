import pygame
import random
import sys

pygame.init()

class Asteroid:
    def __init__(self, position, velocity, radius):
        self.position = position
        self.velocity = velocity
        self.radius = radius

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 4: Crazy Asteroids")

clock = pygame.time.Clock()
running = True

asteroids = []

for i in range(6):
    position = pygame.Vector2(
        random.randint(0, 800),
        random.randint(0, 600)
    )
    velocity = pygame.Vector2(
        random.uniform(-3, 3),
        random.uniform(-3, 3)
    )
    radius = random.randint(15, 35)

    asteroids.append(Asteroid(position, velocity, radius))


def check_collision(a, b):
    difference = b.position - a.position
    distance = difference.length() # distance between two centers
    if distance < a.radius + b.radius: # calculates a normal when a collision happens
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
    for asteroid in asteroids:
        asteroid.position += asteroid.velocity

        # for screen wrapping if asteroid goes off screen
        if asteroid.position.x < -asteroid.radius:
            asteroid.position.x = 800 + asteroid.radius
        elif asteroid.position.x > 800 + asteroid.radius:
            asteroid.position.x = -asteroid.radius

        if asteroid.position.y < -asteroid.radius:
            asteroid.position.y = 600 + asteroid.radius
        elif asteroid.position.y > 600 + asteroid.radius:
            asteroid.position.y = -asteroid.radius

        pygame.draw.circle(screen, (180, 180, 180), (int(asteroid.position.x), int(asteroid.position.y)), asteroid.radius)

    for i in range(len(asteroids)):
        for j in range(i + 1, len(asteroids)):
            a = asteroids[i]
            b = asteroids[j]
            normal = check_collision(a, b)
            if normal is not None:
                relative_velocity = b.velocity - a.velocity
                speed_toward_each_other = relative_velocity.dot(normal)

                if speed_toward_each_other < 0: # negative means moving toward each other
                    mass_i = a.radius * a.radius # give larger asteroids more mass
                    mass_j = b.radius * b.radius

                    impulse = (-2 * speed_toward_each_other) / (1 / mass_i + 1 / mass_j) # calc impulse for collisions
                    a.velocity -= (impulse / mass_i) * normal
                    b.velocity += (impulse / mass_j) * normal

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()