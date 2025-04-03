import pygame
import numpy as np
from body import Body  # Import the updated Body class
from sys import exit

# Initialize pygame
pygame.init()
SCREEN_W, SCREEN_H = 2000, 800
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags=pygame.RESIZABLE)
pygame.display.set_caption("Solar System Simulator")
clock = pygame.time.Clock()
FPS = 60
num_days = 0
font = pygame.font.Font(None, 30)
sub_font = pygame.font.Font(None, 20)

# Background
background = pygame.Surface((SCREEN_W, SCREEN_H))
background.fill("Black")

# Time controls
simulation_speed = 86400  # 1 day per simulation step (in seconds)
dt = simulation_speed / FPS  # Time step in seconds
controls_info = font.render("Space: Pause, Up/Down: Change speed", True, (255, 255, 255))
# Create bodies
bodies = []

# Sun (at center of screen)
sun_x = SCREEN_W / 10 * Body.SCALE_FACTOR
sun_y = SCREEN_H / 2 * Body.SCALE_FACTOR
sun = Body(
    mass=1.989e30,        # kg
    x=sun_x,              # meters
    y=sun_y,              # meters
    vx=0,                 # m/s
    vy=0,                 # m/s
    radius=20,            # pixels
    color=(255, 255, 0),  # yellow
    name="Sun"
)
bodies.append(sun)

# Earth
# Earth's orbital parameters
earth_dist = 149.6e9  # meters (1 AU)
earth_speed = 29800  # m/s

earth = Body(
    mass=5.972e24,        # kg
    x=sun_x + earth_dist,  # meters
    y=sun_y,              # meters
    vx=0,                 # m/s
    vy=earth_speed,  # m/s
    radius=8,             # pixels
    color=(0, 128, 255),  # blue
    name="Earth"
)
bodies.append(earth)

# Add Mars (optional)
mars_dist = 227.9e9  # meters (1.52 AU)
mars_speed = 24100  # m/s

mars = Body(
    mass=6.39e23,         # kg
    x=sun_x + mars_dist,  # meters
    y=sun_y,              # meters
    vx=0,                 # m/s
    vy=mars_speed,  # m/s
    radius=6,             # pixels
    color=(255, 100, 0),  # red-orange
    name="Mars"
)
bodies.append(mars)

# Initial position: adding moon_distance_from_earth to Earth's x
jupiter_dist = 764.53e9
jupiter_speed = 13.07e3
jupiter = Body(
    mass=1.898e27,        # kg
    x=sun_x + jupiter_dist,  # meters
    y=sun_y,       # meters
    # Combine Earth's velocity + moon's orbital velocity
    vx=0,                 # m/s
    vy=jupiter_speed,  # m/s
    radius=16,             # pixels
    color=(150, 105, 25),  # brown
    name="Jupiter"
)
bodies.append(jupiter)

# Initial position: adding moon_distance_from_earth to Earth's x
saturn_dist = 1e12
saturn_speed = 13.07e3
saturn = Body(
    mass=1.898e27,        # kg
    x=sun_x + saturn_dist,  # meters
    y=sun_y,       # meters
    # Combine Earth's velocity + moon's orbital velocity
    vx=0,                 # m/s
    vy=saturn_speed,  # m/s
    radius=10,             # pixels
    color=(209, 201, 163),  # light brown
    name="Saturn"
)
bodies.append(saturn)


# Main game loop
running = True
paused = False

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_UP:
                simulation_speed *= 2
                dt = simulation_speed / FPS
            elif event.key == pygame.K_DOWN:
                simulation_speed /= 2
                dt = simulation_speed / FPS
            elif event.key == pygame.K_ESCAPE:
                pygame.display.toggle_fullscreen()
    
    # Draw background
    screen.blit(background, (0, 0))
    
    if not paused:
        # Apply gravity between all bodies
        
        Body.apply_all_to_one(bodies, sun, dt)
        
        # Update positions
        for body in bodies:
            body.update(dt)
    
    # Draw all bodies
    for body in bodies:
        body.draw(screen)
    
    # Draw simulation info
    time_info = font.render(f"Time scale: {simulation_speed/86400:.1f} days/sec", True, (255, 255, 255))
    screen.blit(time_info, (10, 10))

    screen.blit(controls_info, (10, 40))

    days_info = sub_font.render(f"Its been: {num_days:.1f} days", True, (255, 255, 255))
    screen.blit(days_info, (10, 70))

    if not paused:
        num_days += (simulation_speed/86400)/FPS
    
    # Update display
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
exit()