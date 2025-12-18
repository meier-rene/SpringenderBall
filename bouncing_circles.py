#!/usr/bin/env python3
"""
Bouncing Circles Simulation
Visualizes 10 circles with diameters 2-5mm in a 10cm x 10cm world.
The circles perform idealized elastic collisions with walls and each other.
"""

import pygame
import random
import math
import sys

# Constants
WORLD_SIZE_CM = 10.0  # 10cm x 10cm world
PIXELS_PER_CM = 60  # Scale factor for visualization
WORLD_SIZE_PX = int(WORLD_SIZE_CM * PIXELS_PER_CM)  # 600 pixels

MIN_DIAMETER_MM = 2.0  # Minimum circle diameter in mm
MAX_DIAMETER_MM = 5.0  # Maximum circle diameter in mm
MM_TO_CM = 0.1  # Conversion factor

NUM_CIRCLES = 10
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLORS = [
    (255, 100, 100),  # Red
    (100, 255, 100),  # Green
    (100, 100, 255),  # Blue
    (255, 255, 100),  # Yellow
    (255, 100, 255),  # Magenta
    (100, 255, 255),  # Cyan
    (255, 150, 100),  # Orange
    (150, 100, 255),  # Purple
    (100, 255, 150),  # Lime
    (255, 200, 100),  # Gold
]


class Circle:
    """Represents a circle with position, velocity, and radius."""
    
    def __init__(self, x, y, radius_cm, vx, vy, color):
        """
        Initialize a circle.
        
        Args:
            x, y: Position in cm
            radius_cm: Radius in cm
            vx, vy: Velocity in cm/s
            color: RGB tuple
        """
        self.x = x
        self.y = y
        self.radius_cm = radius_cm
        self.vx = vx
        self.vy = vy
        self.color = color
        self.mass = math.pi * radius_cm ** 2  # Mass proportional to area
    
    def update(self, dt):
        """Update position based on velocity and time delta."""
        self.x += self.vx * dt
        self.y += self.vy * dt
    
    def check_wall_collision(self, world_size_cm):
        """Check and handle collision with walls (elastic collision)."""
        # Left and right walls
        if self.x - self.radius_cm < 0:
            self.x = self.radius_cm
            self.vx = abs(self.vx)  # Reverse and ensure positive
        elif self.x + self.radius_cm > world_size_cm:
            self.x = world_size_cm - self.radius_cm
            self.vx = -abs(self.vx)  # Reverse and ensure negative
        
        # Top and bottom walls
        if self.y - self.radius_cm < 0:
            self.y = self.radius_cm
            self.vy = abs(self.vy)  # Reverse and ensure positive
        elif self.y + self.radius_cm > world_size_cm:
            self.y = world_size_cm - self.radius_cm
            self.vy = -abs(self.vy)  # Reverse and ensure negative
    
    def get_pixel_pos(self):
        """Convert position from cm to pixels."""
        return (int(self.x * PIXELS_PER_CM), int(self.y * PIXELS_PER_CM))
    
    def get_pixel_radius(self):
        """Convert radius from cm to pixels."""
        return max(1, int(self.radius_cm * PIXELS_PER_CM))


def check_circle_collision(c1, c2):
    """
    Check if two circles are colliding.
    
    Returns:
        bool: True if circles are colliding
    """
    dx = c2.x - c1.x
    dy = c2.y - c1.y
    distance = math.sqrt(dx * dx + dy * dy)
    return distance < (c1.radius_cm + c2.radius_cm)


def resolve_circle_collision(c1, c2):
    """
    Resolve elastic collision between two circles.
    
    Uses conservation of momentum and energy for elastic collision.
    """
    # Calculate distance and normal vector
    dx = c2.x - c1.x
    dy = c2.y - c1.y
    distance = math.sqrt(dx * dx + dy * dy)
    
    if distance == 0:
        # Prevent division by zero
        return
    
    # Normal vector
    nx = dx / distance
    ny = dy / distance
    
    # Tangent vector
    tx = -ny
    ty = nx
    
    # Separate circles if overlapping
    overlap = (c1.radius_cm + c2.radius_cm) - distance
    if overlap > 0:
        c1.x -= nx * overlap * 0.5
        c1.y -= ny * overlap * 0.5
        c2.x += nx * overlap * 0.5
        c2.y += ny * overlap * 0.5
    
    # Velocities in normal and tangent directions
    v1n = c1.vx * nx + c1.vy * ny
    v1t = c1.vx * tx + c1.vy * ty
    v2n = c2.vx * nx + c2.vy * ny
    v2t = c2.vx * tx + c2.vy * ty
    
    # New normal velocities after elastic collision
    # Using formula: v1' = ((m1-m2)*v1 + 2*m2*v2) / (m1+m2)
    m1 = c1.mass
    m2 = c2.mass
    v1n_new = (v1n * (m1 - m2) + 2 * m2 * v2n) / (m1 + m2)
    v2n_new = (v2n * (m2 - m1) + 2 * m1 * v1n) / (m1 + m2)
    
    # Convert back to x,y velocities (tangent velocities unchanged)
    c1.vx = v1n_new * nx + v1t * tx
    c1.vy = v1n_new * ny + v1t * ty
    c2.vx = v2n_new * nx + v2t * tx
    c2.vy = v2n_new * ny + v2t * ty


def initialize_circles(num_circles, world_size_cm):
    """
    Initialize circles with random positions, sizes, and velocities.
    
    Args:
        num_circles: Number of circles to create
        world_size_cm: Size of the world in cm
    
    Returns:
        List of Circle objects
    """
    circles = []
    max_attempts = 1000
    
    for i in range(num_circles):
        placed = False
        attempts = 0
        
        while not placed and attempts < max_attempts:
            # Random diameter in mm, convert to radius in cm
            diameter_mm = random.uniform(MIN_DIAMETER_MM, MAX_DIAMETER_MM)
            radius_cm = (diameter_mm * MM_TO_CM) / 2
            
            # Random position (avoiding walls initially)
            margin = radius_cm * 1.5
            x = random.uniform(margin, world_size_cm - margin)
            y = random.uniform(margin, world_size_cm - margin)
            
            # Random velocity (cm/s)
            speed = random.uniform(5, 15)  # cm/s
            angle = random.uniform(0, 2 * math.pi)
            vx = speed * math.cos(angle)
            vy = speed * math.sin(angle)
            
            # Color
            color = COLORS[i % len(COLORS)]
            
            # Create circle
            new_circle = Circle(x, y, radius_cm, vx, vy, color)
            
            # Check if it overlaps with existing circles
            overlap = False
            for existing_circle in circles:
                if check_circle_collision(new_circle, existing_circle):
                    overlap = True
                    break
            
            if not overlap:
                circles.append(new_circle)
                placed = True
            
            attempts += 1
        
        # If we couldn't place it without overlap, place it anyway
        if not placed:
            print(f"Warning: Could not place circle {i+1} without overlap after {max_attempts} attempts")
            circles.append(new_circle)
    
    return circles


def main():
    """Main simulation loop."""
    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((WORLD_SIZE_PX, WORLD_SIZE_PX))
    pygame.display.set_caption("Bouncing Circles Simulation - 10cm x 10cm World")
    clock = pygame.time.Clock()
    
    # Initialize circles
    circles = initialize_circles(NUM_CIRCLES, WORLD_SIZE_CM)
    
    # Main loop
    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0  # Time delta in seconds
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        # Update circles
        for circle in circles:
            circle.update(dt)
            circle.check_wall_collision(WORLD_SIZE_CM)
        
        # Check for circle-to-circle collisions
        for i in range(len(circles)):
            for j in range(i + 1, len(circles)):
                if check_circle_collision(circles[i], circles[j]):
                    resolve_circle_collision(circles[i], circles[j])
        
        # Draw
        screen.fill(WHITE)
        
        # Draw border
        pygame.draw.rect(screen, BLACK, (0, 0, WORLD_SIZE_PX, WORLD_SIZE_PX), 2)
        
        # Draw circles
        for circle in circles:
            pos = circle.get_pixel_pos()
            radius = circle.get_pixel_radius()
            pygame.draw.circle(screen, circle.color, pos, radius)
            pygame.draw.circle(screen, BLACK, pos, radius, 1)  # Border
        
        # Draw info
        font = pygame.font.Font(None, 24)
        info_text = f"Circles: {NUM_CIRCLES} | World: {WORLD_SIZE_CM}cm x {WORLD_SIZE_CM}cm"
        text_surface = font.render(info_text, True, BLACK)
        screen.blit(text_surface, (10, WORLD_SIZE_PX - 30))
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
