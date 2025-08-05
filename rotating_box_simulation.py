#!/usr/bin/env python3
"""
Physics Simulation: Ball in a Rotating Box

This script creates a Pygame window with a Pymunk physics simulation where a ball moves inside
a rotating square box under gravity, colliding elastically with the walls.
"""

import sys

import pygame
import pymunk
import math
import colorsys


def main():
    # Initialize Pygame
    pygame.init()
    screen_size = 800
    screen = pygame.display.set_mode((screen_size, screen_size))
    pygame.display.set_caption("Ball in a Rotating Box")
    clock = pygame.time.Clock()

    # Create Pymunk space with gravity
    space = pymunk.Space()
    # Milder downward gravity for smoother motion
    space.gravity = (0, -1000)

    # Create a smaller rotating square box as a kinematic body
    box_size = 400
    half = box_size / 2
    center = (screen_size / 2, screen_size / 2)
    box_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
    # Configure circular path: smaller radius (50% of max) and faster speed
    base_radius = screen_size / 2 - box_size / 2
    motion_radius = base_radius * 0.5
    circular_speed = 1.5  # rad/s for center motion (faster)
    # Start box at rightmost point of its circular trajectory
    box_body.position = (center[0] + motion_radius, center[1])
    # Rotate at a fixed angular velocity (radians per second)
    rotation_speed = 1.5  # faster spin
    box_body.angular_velocity = rotation_speed
    # Record initial time for center-motion phase
    start_time = pygame.time.get_ticks()
    # Define the four walls of the box (segments)
    walls = []
    coords = [(-half, -half), (half, -half), (half, half), (-half, half)]
    thickness = 5
    for i in range(4):
        a = coords[i]
        b = coords[(i + 1) % 4]
        seg = pymunk.Segment(box_body, a, b, thickness)
        seg.elasticity = 1.0
        seg.friction = 0.5
        walls.append(seg)
    space.add(box_body, *walls)

    # Create multiple balls with different masses inside the box
    radius = 20
    # Define (horizontal offset, mass) for each ball
    ball_params = [(-half / 2, 0.5), (0, 1.0), (half / 2, 2.0)]
    balls = []
    # Assign colors to balls based on their index
    ball_colors = [(200, 50, 50), (50, 200, 50), (50, 50, 200)]
    for idx, (dx, mass) in enumerate(ball_params):
        inertia = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, inertia)
        body.position = (center[0] + dx, center[1] + half - radius - 1)
        shape = pymunk.Circle(body, radius)
        shape.elasticity = 0.9
        shape.friction = 0.5
        space.add(body, shape)
        balls.append((body, ball_colors[idx]))

    # Main loop
    running = True
    # Prepare font for FPS display
    font = pygame.font.SysFont(None, 24)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update kinematic center velocity for circular motion (opposite spin)
        t = (pygame.time.get_ticks() - start_time) / 1000.0
        vx = -motion_radius * circular_speed * math.sin(circular_speed * t)
        vy = -motion_radius * circular_speed * math.cos(circular_speed * t)
        box_body.velocity = vx, vy

        # Step physics
        dt = 1 / 60.0
        space.step(dt)

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw rotating box walls with dynamic color
        hue = (box_body.angle / (2 * math.pi)) % 1.0
        wr, wg, wb = colorsys.hsv_to_rgb(hue, 0.9, 0.9)
        wall_color = (int(wr * 255), int(wg * 255), int(wb * 255))
        for wall in walls:
            a = box_body.local_to_world(wall.a)
            b = box_body.local_to_world(wall.b)
            pa = int(a.x), int(screen_size - a.y)
            pb = int(b.x), int(screen_size - b.y)
            pygame.draw.line(screen, wall_color, pa, pb, thickness)

        # Draw balls with assigned colors
        for body, color in balls:
            p = body.position
            ball_pos = int(p.x), int(screen_size - p.y)
            pygame.draw.circle(screen, color, ball_pos, radius)

        # Display FPS
        fps_text = font.render(f"FPS: {clock.get_fps():.1f}", True, (200, 200, 200))
        screen.blit(fps_text, (10, 10))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit(0)


if __name__ == '__main__':
    main()
