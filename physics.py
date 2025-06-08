# Physics functions for the gravity simulator
# Includes collision handling, particle merging, and energy calculation

# --- Imports ---
import numpy as np

# Gravitational constant used in energy calculations
G = 20

# --- Collision Handling Function ---
def handle_collisions(particles, merge=False):
    # Track particles already merged this frame
    merged = set()
    for i in range(len(particles)):
        # Compare each unique pair once
        for j in range(i + 1, len(particles)):
            if i in merged or j in merged:
                continue
            a, b = particles[i], particles[j]
            r_vec = b.pos - a.pos
            dist = np.linalg.norm(r_vec)
            if dist < a.radius + b.radius:
                if merge:
                    # Compute new mass and velocity for merged particle
                    total_mass = a.mass + b.mass
                    new_vel = (a.vel * a.mass + b.vel * b.mass) / total_mass
                    a.mass = total_mass
                    a.vel = new_vel
                    a.radius = max(3, int(a.mass))
                    # Remove merged particle from list
                    particles.pop(j)
                    # Mark index as merged to skip in future
                    merged.add(j)
                    break
                else:
                    resolve_collision(a, b)

# --- Elastic Collision Resolution ---
def resolve_collision(a, b):
    # Vector from a to b
    r = b.pos - a.pos
    # Relative velocity
    v = b.vel - a.vel
    dist = np.linalg.norm(r)
    if dist == 0:
        return
    r_hat = r / dist
    v_dot_r = np.dot(v, r_hat)
    if v_dot_r > 0:
        return
    m1, m2 = a.mass, b.mass
    # Calculate impulse scalar for elastic collision
    impulse = (2 * v_dot_r) / (m1 + m2)
    # Update velocities based on impulse and masses
    a.vel += impulse * m2 * r_hat
    b.vel -= impulse * m1 * r_hat

# --- Energy Calculation Function ---
def total_energy(particles):
    # Calculate total kinetic energy of all particles
    KE = sum(0.5 * p.mass * np.linalg.norm(p.vel)**2 for p in particles)
    PE = 0
    # Sum potential energy over all unique pairs
    for i in range(len(particles)):
        for j in range(i + 1, len(particles)):
            dist = np.linalg.norm(particles[i].pos - particles[j].pos)
            if dist == 0:
                continue
            PE -= G * particles[i].mass * particles[j].mass / dist
    return KE, PE
