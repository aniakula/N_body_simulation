import pygame
from body import Body  # Import the Body class from body.py
from sys import exit
import math
import tkinter
import random 
root = tkinter.Tk()
SCREEN_W = root.winfo_screenwidth()
SCREEN_H = root.winfo_screenheight()
root.destroy()
dt = 0.04
pos = [0, 0]
current = 0
# Initialize the game:{
pygame.init() #init pygame package
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags = pygame.RESIZABLE) #set JFrame size
pygame.display.set_caption("N-Body Simulator") #set JFrame title
clock = pygame.time.Clock() #Clock needed for frame rate
FPS = 60 #frames per second
paused = True
#}

# Types of Surfaces:{
font = pygame.font.Font(None, 50) #load a font (None = default for Pygame)

# Create a surface (types = regular surface, image surface, text surface)
surf = pygame.Surface((SCREEN_W, SCREEN_H)) #Surface = a rectangular object for drawing
surf.fill("Black") #fill the surface with red color

bodies = []

#pygame.draw.circle(surf, "Red", (SCREEN_W // 2, SCREEN_H // 2), 100) #draw a circle on the surface
# planet1 = Body(mass=5.972e24, x=SCREEN_W //10, y=SCREEN_H//2, vx= 5, vy= 15, radius=10, color=(255, 0, 0)) #create a body object
# planet2 = Body(mass=1.989e27, x=SCREEN_W * 7// 8, y=SCREEN_H //2, vx=0, vy=0, radius=10, color=(0, 255, 0))
# planet3 = Body(mass=7.34767e20, x=SCREEN_W // 11, y=SCREEN_H // 3, vx=7, vy=20, radius=5, color=(0, 0, 255))
# bodies.extend([planet1, planet2, planet3])

# Game Loop:{
# Set up the window 
while True: # game loop
    for event in pygame.event.get(): #get all the events that have happened (case here)
        if event.type == pygame.QUIT: #if the user clicks the close button (event)
            pygame.quit() #close the window (destructs the pygame object)
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
            elif event.key == pygame.K_r:
                bodies.clear()
            elif event.key == pygame.K_RETURN:
                if(current == 1):
                    r = random.randint(5, 255)
                    g = random.randint(5, 255)
                    b = random.randint(5, 255)
                    bodies.append(Body(mass = 1e43, x=pos[0] * Body.SCALE_FACTOR, y=pos[1] * Body.SCALE_FACTOR, vx=0, vy=0, radius=10, color=(r, g, b)))
                    current = 0
                else:
                    current += 1
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
                        if current == 1:
                            current -= 1
                    case pygame.K_DOWN:
                        if current == 0:
                            current += 1


        elif event.type == pygame.MOUSEBUTTONDOWN:
            posx, posy = pygame.mouse.get_pos()
            r = random.randint(5, 255)
            g = random.randint(5, 255)
            b = random.randint(5, 255)
            bodies.append(Body(mass = 1e43, x=posx * Body.SCALE_FACTOR, y=posy * Body.SCALE_FACTOR, vx=0, vy=0, radius=10, color=(r, g, b)))

    screen.blit(surf, (0, 0)) #blit = block image transfer = draw the surface on the screen

    if(not paused):
        for body in bodies:
            body.apply_all_gravity(bodies, dt)
        
        # Update positions
        for body in bodies:
            body.update(dt)
        
    for body in bodies:
        body.draw(screen)
        # if body.out_of_bounds(SCREEN_W, SCREEN_H):
        #     bodies.remove(body)
        
    if paused: 
        pause_info = font.render("Paused", True, (255, 255, 255)) 
    else: 
        pause_info = font.render("Simulating", True, (255, 255, 255)) 

    cols = ((255, 255, 255), (255, 255, 255))
    if current == 0: 
        cols = ((255, 0, 0), (255, 255, 255))
    else:
        cols = ((255, 255, 255), (255, 0, 0))

    coord_info_x = font.render(f"x: {pos[0]}", True, cols[0])
    coord_info_y = font.render(f"y: {pos[1]}", True, cols[1])

    screen.blit(pause_info, (10, 10))
    screen.blit(coord_info_x, (10, 50))
    screen.blit(coord_info_y, (10, 90))
    pygame.display.update() #update the display (repaint)
    clock.tick(FPS) #60 frames per second
#}