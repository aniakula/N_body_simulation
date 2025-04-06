import pygame
import numpy as np
import matplotlib.pyplot as plt
from body import Body  # Import the Body class
from sys import exit
import math
import tkinter
import random

# Initialize tkinter for screen dimensions
root = tkinter.Tk()
SCREEN_W = root.winfo_screenwidth()
SCREEN_H = root.winfo_screenheight()
root.destroy()

# Simulation parameters
dt = 0.07
pos = [0, 0]
current = 0
time = 0  # Add time tracking
show_cm = True # boolean for displaying center of mass of all bodies
# For storing position, velocity, and time data
data = {}  # Format: {body_name: {'t': [], 'x': [], 'y': [], 'vx': [], 'vy': []}}

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags=pygame.RESIZABLE)
pygame.display.set_caption("N-Body Simulator with Time Graphs")
clock = pygame.time.Clock()
FPS = 60
paused = True

# Create surface
surf = pygame.Surface((SCREEN_W, SCREEN_H))
surf.fill("Black")

# Lists to hold bodies and their names
bodies = []
body_names = []

# Function to create position and velocity vs time plots
def create_time_plots():
    if not data:  # No data collected
        print("No data to plot. Simulation ended too quickly.")
        return
        
    # Position vs Time plots
    plt.figure(figsize=(15, 10))
    num_bodies = len(data)
    rows = int(np.ceil(num_bodies / 2))
    cols = min(2, num_bodies)
    
    for i, name in enumerate(data.keys()):
        plt.subplot(rows, cols, i+1)
        
        # Plot x and y position vs time
        plt.plot(data[name]['t'], data[name]['x'], 'b-', label='X Position')
        plt.plot(data[name]['t'], data[name]['y'], 'g-', label='Y Position')
        
        plt.title(f'Position vs Time for {name}')
        plt.xlabel('Time (s)')
        plt.ylabel('Position')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
    
    plt.tight_layout()
    plt.savefig('graphs/position_vs_time.png')
    print("Position vs time plot saved as 'position_vs_time.png'")
    
    # Velocity vs Time plots
    plt.figure(figsize=(15, 10))
    
    for i, name in enumerate(data.keys()):
        plt.subplot(rows, cols, i+1)
        
        # Plot vx and vy vs time
        plt.plot(data[name]['t'], data[name]['vx'], 'r-', label='X Velocity')
        plt.plot(data[name]['t'], data[name]['vy'], 'm-', label='Y Velocity')
        
        plt.title(f'Velocity vs Time for {name}')
        plt.xlabel('Time (s)')
        plt.ylabel('Velocity')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
    
    plt.tight_layout()
    plt.savefig('graphs/velocity_vs_time.png')
    print("Velocity vs time plot saved as 'velocity_vs_time.png'")
    
    plt.show()

# Initialize data collection for each body
for body in bodies:
    name = body.name if body.name else f"Body_{len(body_names)}"
    body_names.append(name)
    data[name] = {'t': [], 'x': [], 'y': [], 'vx': [], 'vy': []}

# Game Loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            create_time_plots()
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                bodies.clear()
                data.clear()
                body_names.clear()
                time = 0
            elif event.key == pygame.K_RETURN:
                if(current == 1):
                    r = random.randint(5, 255)
                    g = random.randint(5, 255)
                    b = random.randint(5, 255)
                    new_body = Body(mass=1e42, x=pos[0] * Body.SCALE_FACTOR, y=pos[1] * Body.SCALE_FACTOR, 
                                  vx=0, vy=0, radius=10, color=(r, g, b))
                    name = f"Body_{len(body_names)}"
                    body_names.append(name)
                    data[name] = {'t': [], 'x': [], 'y': [], 'vx': [], 'vy': []}
                    bodies.append(new_body)
                    current = 0
                else:
                    current += 1
            elif event.key == pygame.K_p:
                create_time_plots()
            else:
                match event.key:
                    case pygame.K_0:
                        pos[current] = int(str(pos[current]) + "0")
                    case pygame.K_1:
                        pos[current] = int(str(pos[current]) + "1")
                    case pygame.K_2:
                        pos[current] = int(str(pos[current]) + "2")
                    case pygame.K_3:
                        pos[current] = int(str(pos[current]) + "3")
                    case pygame.K_4:
                        pos[current] = int(str(pos[current]) + "4")
                    case pygame.K_5:
                        pos[current] = int(str(pos[current]) + "5")
                    case pygame.K_6:
                        pos[current] = int(str(pos[current]) + "6")
                    case pygame.K_7:
                        pos[current] = int(str(pos[current]) + "7")
                    case pygame.K_8:
                        pos[current] = int(str(pos[current]) + "8")
                    case pygame.K_9:
                        pos[current] = int(str(pos[current]) + "9")
                    case pygame.K_BACKSPACE:
                        pos[current] = 0
                    case pygame.K_UP:
                        if current == 0:
                            current -= 1
                    case pygame.K_DOWN:
                        if current == 0:
                            current += 1

        elif event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = pygame.mouse.get_pos()
            r = random.randint(5, 255)
            g = random.randint(5, 255)
            b = random.randint(5, 255)
            new_body = Body(mass=1e42, x=posx * Body.SCALE_FACTOR, y=posy * Body.SCALE_FACTOR, 
                          vx=0, vy=0, radius=10, color=(r, g, b))
            name = f"Body_{len(body_names)}"
            body_names.append(name)
            data[name] = {'t': [], 'x': [], 'y': [], 'vx': [], 'vy': []}
            bodies.append(new_body)

    screen.blit(surf, (0, 0))

    if show_cm and (cm := Body.calc_cm(bodies)) is not None:
        pygame.draw.circle(screen, (255, 255, 255), cm, 10)
        for body in bodies:
            pygame.draw.line(screen, (255, 255, 255), cm, (body.screen_x, body.screen_y), width=1) 

    if not paused:
        time += dt  # Increment time
        for i, body in enumerate(bodies):
            name = body.name if body.name else body_names[i]
            
            # Record data
            data[name]['t'].append(time)
            data[name]['x'].append(body.real_x / Body.SCALE_FACTOR)
            data[name]['y'].append(body.real_y / Body.SCALE_FACTOR)
            data[name]['vx'].append(body.real_vx)
            data[name]['vy'].append(body.real_vy)
            
        for body in bodies:
            body.update_rk4(dt, bodies)
    
    for body in bodies:
        body.draw(screen)
        
    if paused: 
        pause_info = pygame.font.Font(None, 50).render("Paused", True, (255, 255, 255)) 
    else: 
        pause_info = pygame.font.Font(None, 50).render(f"Simulating (t={time:.2f}s)", True, (255, 255, 255)) 

    cols = ((255, 255, 255), (255, 255, 255))
    if current == 0: 
        cols = ((255, 0, 0), (255, 255, 255))
    else:
        cols = ((255, 255, 255), (255, 0, 0))

    coord_info_x = pygame.font.Font(None, 50).render(f"x: {pos[0]}", True, cols[0])
    coord_info_y = pygame.font.Font(None, 50).render(f"y: {pos[1]}", True, cols[1])
    plot_info = pygame.font.Font(None, 30).render("Press P to generate time plots", True, (255, 255, 255))

    screen.blit(pause_info, (10, 10))
    screen.blit(coord_info_x, (10, 50))
    screen.blit(coord_info_y, (10, 90))
    screen.blit(plot_info, (10, 130))
    
    pygame.display.update()
    clock.tick(FPS)