# 2D Gravity Simulator with Trail Rendering, Collisions, and Launch Controls
# Features: gravity toggle, pause, merge mode, trail fade, and HUD info

# --- Imports ---
import pygame
import numpy as np
from particle import Particle
from physics import handle_collisions, total_energy
paused = False
merge_mode = False
from particle import G  # Optional: or just track G here instead

# Simulation pause toggle
paused = False
merge_mode = False

# Gravitational constant (tunable)
G_value = 20

# Gravity direction sign (1 for attract, -1 for repel)
gravity_sign = 1

# --- Settings ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Initialize Pygame and display
pygame.font.init()
font = pygame.font.SysFont("monospace", 18)
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
trail_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
pygame.display.set_caption("2D Gravity Simulator")
clock = pygame.time.Clock()

# Initialize particles with random positions, velocities, and masses
particles = []
for _ in range(10):
    x = np.random.randint(100, WIDTH - 100)
    y = np.random.randint(100, HEIGHT - 100)
    vx = np.random.uniform(-0.5, 0.5)
    vy = np.random.uniform(-0.5, 0.5)
    mass = np.random.uniform(2, 10)
    particles.append(Particle(x, y, vx, vy, mass))


# --- Drag-to-Launch Setup ---
dragging = False
start_pos = None


# --- Main Loop ---
running = True
while running:
    clock.tick(FPS)

    # Apply trail fading effect for smoother visuals
    fade_overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    fade_overlay.fill((0, 0, 0, 10))  # small alpha → slow fade
    trail_surface.blit(fade_overlay, (0, 0))
    screen.fill((0, 0, 0))

    # --- Event Handling ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            dragging = True
            start_pos = np.array(pygame.mouse.get_pos(), dtype=float)
        elif event.type == pygame.MOUSEBUTTONUP and dragging:
            end_pos = np.array(pygame.mouse.get_pos(), dtype=float)
            velocity = (end_pos - start_pos) * 0.05
            particles.append(Particle(*start_pos, *velocity, np.random.uniform(2, 5)))
            dragging = False
        elif event.type == pygame.KEYDOWN:
            # Toggle pause with spacebar
            if event.key == pygame.K_SPACE:
                paused = not paused
            # Increase/decrease G with arrow keys
            elif event.key == pygame.K_UP:
                G_value *= 2
            elif event.key == pygame.K_DOWN:
                G_value /= 2
            # Toggle merge mode and gravity direction
            elif event.key == pygame.K_m:
                merge_mode = not merge_mode
            elif event.key == pygame.K_g:
                gravity_sign *= -1
                print("Gravity reversed!" if gravity_sign == -1 else "Gravity normal")

    # --- Physics Updates ---
    if not paused:
        for p in particles:
            # Apply gravitational force
            p.apply_gravity(particles, G_value * gravity_sign)
            # Handle collisions
            handle_collisions(particles, merge_mode)
        # Blit trail surface after fading
        screen.blit(trail_surface, (0, 0))
        # Update positions and draw trails/particles
        for p in particles:
            p.update_position()
            p.draw(screen, trail_surface)

    # Draw an arrow showing launch direction while dragging
    if dragging:
        current_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 255, 255), start_pos.astype(int), current_pos, 1)

    # --- HUD Info Display ---
    # Log energy to console for analysis
    ke, pe = total_energy(particles)
    print(f"KE: {ke:.2f} | PE: {pe:.2f} | Total: {ke + pe:.2f}", end='\r')

    info_text = [f"G: {G_value:.2f}", f"Particles: {len(particles)}", f"{'Paused' if paused else 'Running'}", f"Merge Mode: {'ON' if merge_mode else 'OFF'}", f"Gravity Mode: {'Attract' if gravity_sign == 1 else 'Repel'}"]
    for i, line in enumerate(info_text):
        text_surf = font.render(line, True, (255, 255, 255))
        screen.blit(text_surf, (10, 10 + i * 20))
    
    pygame.display.flip()

pygame.quit()
