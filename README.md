# agent_sandbox

## Ball in a Rotating Box Simulation

This directory provides a simulation of a ball moving inside a rotating square box using Pygame and Pymunk.

### Requirements
- Python 3
- Pygame
- Pymunk

### Usage
Run the simulation with:
```
python rotating_box_simulation.py
```

### Features
- Spawns three balls inside the rotating box, each with a different mass (0.5, 1.0, and 2.0)
- Milder gravity for smoother, more “chill” motion (gravity = 1000)
- Box center moves in a smaller (50% max) circular path opposite the rotation, at faster angular speed (1.5 rad/s)
- Smaller rotating box (size = 400)
- Box rotation speed increased to 1.5 rad/s for a faster spin
- Enhanced visuals: background color, colored balls, dynamic wall hues, and FPS display
