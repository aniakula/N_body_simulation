import pygame
import numpy as np

class Body:
    G = 6.67430e-11

    def __init__(self, mass, x, y, vx, vy, radius=10, color=(255, 255, 255)):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.frames = [self] * 10

    def draw(self, screen):
        
        for frame in self.frames:
            # Draw the previous positions of the body
            pygame.draw.circle(screen, frame.color, (frame.x, frame.y), frame.radius//2)

        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)  # Draw the body as a circle
        

    def update(self, dt):
        # Update position based on velocity and time step)
        self.frames.pop()
        self.frames.insert(0, Body(self.mass, self.x, self.y, self.vx, self.vy, self.radius, self.dim(self.color)))
        self.x += self.vx * dt
        self.y += self.vy * dt

    @staticmethod
    def dim(color: tuple[int, int, int]):
        r, g, b = color
        return (r//2, g//2, b//2)
    
    @staticmethod
    def compute_dist(coord1, coord2):
        x1, y1 = coord1
        x2, y2 = coord2
        return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    
    def apply_force(self, fx, fy, dt=0.1):
        # Update velocity based on force and mass (F = ma -> a = F/m)
        ax = fx / self.mass
        ay = fy / self.mass
        
        # Apply acceleration for the given time step
        self.vx += ax * dt
        self.vy += ay * dt

    def apply_gravity(self, other):
        # Vector from self to other
        dx = other.x - self.x
        dy = other.y - self.y
        
        # Calculate distance (magnitude of the vector)
        r = np.sqrt(dx**2 + dy**2)
        
        # Avoid division by zero or objects that are too close
        if r < self.radius + other.radius:
            return
        
        # Calculate gravitational force
        force = self.G * (self.mass * other.mass) / (r**2)
        
        # Calculate force components (maintaining proper direction)
        fx = force * dx / r
        fy = force * dy / r
        
        # Apply the force
        self.apply_force(fx, fy)


planet1 = Body(mass=1, x=0, y=0, vx= 1, vy= 1, radius=10, color=(255, 0, 0)) #create a body object
planet2 = Body(mass=50e11, x=500, y=400, vx=0, vy=0, radius=10, color=(0, 255, 0))
for i in range(100):
    planet1.update(1)
    planet2.update(1)
    planet1.apply_gravity(planet2)
    planet2.apply_gravity(planet1)
