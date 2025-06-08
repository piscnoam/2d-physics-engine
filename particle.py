# Particle class for 2D gravity simulator
# Handles physics updates, trail rendering, and gravitational interactions

# --- Imports ---
import pygame
import numpy as np
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import pygame.surface
# Default gravitational constant (can be overridden from main)
G = 20  # Gravitational constant

# --- Particle Class ---
class Particle:
    def __init__(self, x, y, vx, vy, mass):
        self.pos = np.array([x, y], dtype=float)  # Position vector
        self.vel = np.array([vx, vy], dtype=float)  # Velocity vector
        self.mass = mass  # Scalar mass
        self.radius = max(5, int(self.mass))  # Visual size scaled by mass
        self.trail = []  # List of recent positions for drawing motion trail

    def apply_gravity(self, others, G):
        # Compute net gravitational force from all other particles
        total_force = np.zeros(2)
        for other in others:
            # Skip self
            if other is self:
                continue
            # Direction vector to other
            r_vec = other.pos - self.pos
            # Distance magnitude
            r_mag = np.linalg.norm(r_vec)
            if r_mag == 0:
                continue
            # Unit direction vector
            r_hat = r_vec / r_mag
            # Gravitational force magnitude
            force_mag = G * self.mass * other.mass / r_mag**2
            # Accumulate force vector
            total_force += force_mag * r_hat
        # Compute resulting acceleration and update velocity
        acceleration = total_force / self.mass
        self.vel += acceleration

    def update_position(self):
        # Update particle position and store trail history
        self.pos += self.vel
        self.trail.append(self.pos.copy())
        # Limit trail length to 100 points
        if len(self.trail) > 100:
            self.trail.pop(0)

    def draw(self, surface, trail_surface):
        # Compute particle speed for color scaling
        speed = np.linalg.norm(self.vel)
        color = (min(255, int(speed * 50)), 100, 255)
    
        # Draw trail segments with fading alpha
        if len(self.trail) > 1:
            for i in range(1, len(self.trail)):
                start = self.trail[i - 1].astype(int)
                end = self.trail[i].astype(int)
                alpha = int(255 * (i / len(self.trail)))  # older = more transparent
                trail_color = (*color[:3], alpha)
                pygame.draw.line(trail_surface, trail_color, start, end, 2)
        
        # Draw particle body as filled circle
        pygame.draw.circle(surface, color, self.pos.astype(int), self.radius)
