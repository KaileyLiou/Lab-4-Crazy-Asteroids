# Lab 4: Crazy Asteroids

A Pygame project created for my A.I. for Game Programming class to practice vectors, collision physics, and rotational movement.

This project displays six asteroids moving across the screen, along with a player-controlled spaceship and an enemy spaceship. Each asteroid has a randomized starting position, movement vector, and size. The asteroids wrap around the edges of the screen and bounce off each other when they collide. 

The player can rotate the spaceship and fire missiles toward the mouse cursor or straight ahead in the direction the ship is facing. The enemy spaceship uses distance and a dot product to determine whether the player is close enough and within its field of view. When it detects the player, it switches from a patrol state to an attack state and fires missiles toward the player's position.

## Features

- Six asteroids moving with random sizes, positions, and velocities
- Screen wrapping for the asteroids and the ship
- Asteroid-to-asteroid collisions
- A rotating spaceship you can move around with the keyboard
- Missiles that can be aimed at the mouse or fired straight ahead to destroy asteroids
- Display of spaceship speed and velocity
- An enemy spaceship with field-of-view detection using distance and dot product
- Enemy state shown with color and text along with its distance and dot product values
- Enemy fires missiles at the player once detected

## How to Play

Use the left and right arrow keys to rotate the ship, the up arrow to apply thrust, and the space bar to fire a missle.

<img width="1175" height="872" alt="Screenshot 2026-10-02 at 11 45 43 PM" src="https://github.com/user-attachments/assets/312c0747-1229-403b-9dea-2763b452821b" />
<img width="1178" height="877" alt="Screenshot 2026-10-02 at 11 45 32 PM" src="https://github.com/user-attachments/assets/aa44dac8-f065-4fba-99d5-3419e63ba8de" />
