import pygame
import random
import sys

pygame.init()

class Asteroid:
    def __init__(self, position, velocity, radius):
        self.position = position
        self.velocity = velocity
        self.radius = radius

class Missile:
    def __init__(self, position, velocity):
        self.position = position
        self.velocity = velocity
        self.radius = 4

MISSILE_SPEED = 7

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Lab 4: Crazy Asteroids")

clock = pygame.time.Clock()
running = True

asteroids = []
missiles = []

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

def spawn_ship_position():
    return pygame.Vector2(400, 300)

ship_position = spawn_ship_position()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            target = pygame.Vector2(event.pos)

            direction = target - ship_position
            if direction.length() != 0:
                direction = direction.normalize()

                missile_velocity = direction * MISSILE_SPEED
                missiles.append(Missile(pygame.Vector2(ship_position), missile_velocity))

    screen.fill((0, 0, 0))

    pygame.draw.circle(screen, (0, 200, 255), (int(ship_position.x), int(ship_position.y)), 8)

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

    for missile in missiles[:]:
        missile.position += missile.velocity

        # remove missiles that fly off screen
        if (missile.position.x < 0 or missile.position.x > 800 or
                missile.position.y < 0 or missile.position.y > 600):
            missiles.remove(missile)
            continue

        pygame.draw.circle(screen, (255, 255, 0), (int(missile.position.x), int(missile.position.y)), missile.radius)

    for missile in missiles[:]:
        for asteroid in asteroids[:]:
            distance = missile.position.distance_to(asteroid.position)
            if distance < missile.radius + asteroid.radius:
                asteroid.position = pygame.Vector2(
                    random.randint(0, 800),
                    random.randint(0, 600)
                )
                asteroid.velocity = pygame.Vector2(
                    random.uniform(-3, 3),
                    random.uniform(-3, 3)
                )
                if missile in missiles:
                    missiles.remove(missile)
                break

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