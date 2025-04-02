import pygame
from body import Body  # Import the Body class from body.py
from sys import exit
import math
import tkinter
root = tkinter.Tk()
SCREEN_W = root.winfo_screenwidth()
SCREEN_H = root.winfo_screenheight()
root.destroy()


# Initialize the game:{
pygame.init() #init pygame package
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags = pygame.RESIZABLE) #set JFrame size
pygame.display.set_caption("N-Body Simulator") #set JFrame title
clock = pygame.time.Clock() #Clock needed for frame rate
FPS = 60 #frames per second
#}

# Types of Surfaces:{
test_font = pygame.font.Font(None, 50) #load a font (None = default for Pygame)

# Create a surface (types = regular surface, image surface, text surface)
surf = pygame.Surface((SCREEN_W, SCREEN_H)) #Surface = a rectangular object for drawing
surf.fill("Black") #fill the surface with red color
#image_surf = pygame.image.load("images/DAG.png").convert() #load an image (images are also surfaces) 
#use convert to make game faster (convert_alpha for images with transparency)

# text params = text, antialias, color (anti-alias = smooth edges)
#text_surface = test_font.render("Hello World", True, "Green") #create an image surface with text
#}

#Animation: simply make a variable that changes over time to represent a position variable {
#text_x_pos = 0
#}

# Rectangles for surface movement:{
# player = pygame.image.load("images/wartortle.png").convert_alpha()
# player = pygame.transform.scale(player, (200, 200)).convert_alpha() #resize the image
# player_rect = player.get_rect(topleft = (0, 0)) #get the rectangle of the image (draws rect around surface given)

# #}
#1.989e30 -> sun
#5.972e24 -> earth
#7.34767e22 -> moon
bodies = []
# Create the Sun at the center
sun = Body(mass=1.989e30, x=SCREEN_W*3//4, y=SCREEN_H//2, vx=0, vy=0, radius=30, color=(255, 255, 0), pixel_dist=1e11)

# Create Earth (with tangential velocity for orbit)
earth_distance = 149.53  # pixels from sun
earth_velocity = 10  # appropriate orbital velocity
earth = Body(mass=5.972e24, 
             x=SCREEN_W*3//4 + earth_distance, 
             y=SCREEN_H//2, 
             vx=0, 
             vy=earth_velocity, 
             radius=10, 
             color=(0, 0, 255))

# Create Mars (further out)
moon_distance = 250.55  # pixels from earth
mars_velocity = 5  # slightly slower than Earth
mars = Body(mass=6.39e23, 
            x=SCREEN_W*3//4 + mars_distance, 
            y=SCREEN_H//2, 
            vx=0, 
            vy=mars_velocity, 
            radius=8, 
            color=(255, 0, 0))

bodies = [sun, earth, mars]

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
            exit() #system.exit(1)
    screen.blit(surf, (0, 0)) #blit = block image transfer = draw the surface on the screen

    for i, body in enumerate(bodies):
        for j, other in enumerate(bodies):
            if i != j:  # Don't apply gravity to itself
                body.apply_gravity(other)
    
    # Update positions
    for body in bodies:
        body.update(0.05)
        body.draw(screen)

    pygame.display.update() #update the display (repaint)
    clock.tick(FPS) #60 frames per second
#}