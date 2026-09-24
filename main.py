import pygame
import random
import sys
import math

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
        self.radius = 6

class Ship:
    def __init__(self, position):
        self.position = position
        self.angle = 90 # starts facing up
        self.rotation_speed = 3
        self.speed = 4

    def forward_vector(self):
        radians = math.radians(self.angle)
        return pygame.Vector2(math.cos(radians), -math.sin(radians))

MISSILE_SPEED = 7
WIDTH, HEIGHT = 800, 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lab 4: Crazy Asteroids")

clock = pygame.time.Clock()
running = True

asteroids = []
missiles = []

for i in range(6):
    position = pygame.Vector2(
        random.randint(0, WIDTH),
        random.randint(0, HEIGHT)
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

ship = Ship(pygame.Vector2(WIDTH/2, HEIGHT/2))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            target = pygame.Vector2(event.pos)
            direction = target - ship.position
            if direction.length() != 0:
                direction = direction.normalize()
                missile_velocity = direction * MISSILE_SPEED
                missiles.append(Missile(pygame.Vector2(ship.position), missile_velocity))

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                forward = ship.forward_vector()
                missile_velocity = forward * MISSILE_SPEED
                missiles.append(Missile(pygame.Vector2(ship.position), missile_velocity))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        ship.angle += ship.rotation_speed
    if keys[pygame.K_RIGHT]:
        ship.angle -= ship.rotation_speed

    forward = ship.forward_vector()

    if keys[pygame.K_UP]:
        ship.position += forward * ship.speed

    # screen wrapping for the ship
    if ship.position.x > WIDTH:
        ship.position.x = 0
    if ship.position.x < 0:
        ship.position.x = WIDTH
    if ship.position.y > HEIGHT:
        ship.position.y = 0
    if ship.position.y < 0:
        ship.position.y = HEIGHT

    screen.fill((0, 0, 0))

    left = forward.rotate(140)
    right = forward.rotate(-140)

    p1 = ship.position + forward * 22
    p2 = ship.position + left * 16
    p3 = ship.position + right * 16

    pygame.draw.polygon(screen, (255, 255, 255), [p1, p2, p3], 2)

    for asteroid in asteroids:
        asteroid.position += asteroid.velocity

        # for screen wrapping if asteroid goes off screen
        if asteroid.position.x < -asteroid.radius:
            asteroid.position.x = WIDTH + asteroid.radius
        elif asteroid.position.x > WIDTH + asteroid.radius:
            asteroid.position.x = -asteroid.radius

        if asteroid.position.y < -asteroid.radius:
            asteroid.position.y = HEIGHT + asteroid.radius
        elif asteroid.position.y > HEIGHT + asteroid.radius:
            asteroid.position.y = -asteroid.radius

        pygame.draw.circle(screen, (180, 180, 180), (int(asteroid.position.x), int(asteroid.position.y)), asteroid.radius)

    for missile in missiles[:]:
        missile.position += missile.velocity

        # remove missiles that fly off screen
        if (missile.position.x < 0 or missile.position.x > WIDTH or
                missile.position.y < 0 or missile.position.y > HEIGHT):
            missiles.remove(missile)
            continue

        pygame.draw.circle(screen, (255, 255, 0), (int(missile.position.x), int(missile.position.y)), missile.radius)

    for missile in missiles[:]:
        for asteroid in asteroids[:]:
            distance = missile.position.distance_to(asteroid.position)
            if distance < missile.radius + asteroid.radius:
                asteroid.position = pygame.Vector2(
                    random.randint(0, WIDTH),
                    random.randint(0, HEIGHT)
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

                    impulse = (-2 * speed_toward_each_other) / (1 / mass_i + 1 / mass_j)
                    a.velocity -= (impulse / mass_i) * normal
                    b.velocity += (impulse / mass_j) * normal

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()