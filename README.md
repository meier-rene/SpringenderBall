# SpringenderBall

A Python simulation that visualizes the movement of 10 circles with diameters between 2-5mm in a 2D world (10cm x 10cm square). The circles perform idealized elastic collisions with walls and each other.

## Features

- 10 circles with random diameters (2-5mm)
- Random initial velocities
- Elastic collisions with walls
- Elastic collisions between circles (conservation of momentum and energy)
- Real-time visualization using Pygame
- Proper unit conversions (mm, cm to pixels)

## Requirements

- Python 3.6 or higher
- Pygame 2.5.0 or higher

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the simulation:
```bash
python bouncing_circles.py
```

Press ESC or close the window to exit the simulation.

## Physics

The simulation implements:
- **Wall collisions**: When a circle hits a wall, its velocity component perpendicular to the wall is reversed
- **Circle-to-circle collisions**: Uses conservation of momentum and energy for elastic collisions between circles of different masses (mass proportional to area)