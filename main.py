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
text_surface = test_font.render("Hello World", True, "Green") #create an image surface with text
#}

#Animation: simply make a variable that changes over time to represent a position variable {
text_x_pos = 0
#}

# Rectangles for surface movement:{
# player = pygame.image.load("images/wartortle.png").convert_alpha()
# player = pygame.transform.scale(player, (200, 200)).convert_alpha() #resize the image
# player_rect = player.get_rect(topleft = (0, 0)) #get the rectangle of the image (draws rect around surface given)

# #}

#pygame.draw.circle(surf, "Red", (SCREEN_W // 2, SCREEN_H // 2), 100) #draw a circle on the surface
planet1 = Body(mass=1, x=SCREEN_W//4, y=SCREEN_H//2, vx= 5, vy= 15, radius=10, color=(255, 0, 0)) #create a body object
planet2 = Body(mass=50e14, x=SCREEN_W // 2, y=SCREEN_H // 2, vx=0, vy=0, radius=40, color=(0, 255, 0))
# Game Loop:{
# Set up the window
while True: # game loop
    for event in pygame.event.get(): #get all the events that have happened (case here)
        if event.type == pygame.QUIT: #if the user clicks the close button (event)
            pygame.quit() #close the window (destructs the pygame object)
            exit() #system.exit(1)
    screen.blit(surf, (0, 0)) #blit = block image transfer = draw the surface on the screen
    planet2.apply_gravity(planet1)
    planet1.apply_gravity(planet2) #apply a force to the planet (0, 0 = no force)
    planet1.update(0.1) #update the position of the planet
    planet2.update(0.1)

    planet1.draw(screen) #draw the planet on the screen
    planet2.draw(screen)
    #screen.blit(image_surf, (0, 0)) #draw the image on the screen
    #screen.blit(text_surface, (text_x_pos, 200)) #draw the text on the screen
    # text_x_pos = (text_x_pos + 5) % 800  #increment the x position of the text
    # screen.blit(player, player_rect) #draw the player on the screen using rect for position 
    # player_rect.x += 5 #increment the x position of the player
    # if player_rect.left > 800: player_rect.left = 0 #if the player goes off the screen, reset to 0
    pygame.display.update() #update the display (repaint)
    clock.tick(FPS) #60 frames per second
#}