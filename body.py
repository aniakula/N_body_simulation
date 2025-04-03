import pygame
import numpy as np

class Body:
    

    def __init__(self, mass, x, y, vx, vy, radius=10, color=(255, 255, 255), name=None):
        # Physical properties (SI units)
        self.mass = mass                  # kg
        self.real_x = x                   # meters
        self.real_y = y                   # meters
        self.real_vx = vx                 # m/s
        self.real_vy = vy                 # m/s
        
        # Display properties (pixels)
        self.radius = radius              # pixels
        self.color = color
        self.name = name
        
        # Trail for visualization
        self.frames = []
        for _ in range(10):
            self.frames.append((self.screen_x, self.screen_y, self.dim(self.color)))
    
    # Scale factor for converting between real distances and screen pixels
    # Adjust this value based on your simulation needs
    SCALE_FACTOR = 1e9  # 1 pixel = 1 billion meters (≈6.68 AU)
    G = 6.67428e-11  # Gravitational constant

    @property
    def screen_x(self):
        # Convert real position to screen coordinates
        return self.real_x / self.SCALE_FACTOR
    
    @property
    def screen_y(self):
        # Convert real position to screen coordinates
        return self.real_y / self.SCALE_FACTOR
    
    def draw(self, screen):
        # Draw trail
        for x, y, color in self.frames:
            pygame.draw.circle(screen, color, (int(x), int(y)), self.radius//2)
        
        # Draw body
        pygame.draw.circle(screen, self.color, (int(self.screen_x), int(self.screen_y)), self.radius)
        
        # Draw name if provided
        if self.name:
            font = pygame.font.Font(None, 24)
            text = font.render(self.name, True, self.color)
            screen.blit(text, (int(self.screen_x) + self.radius + 5, int(self.screen_y) - 10))

    def update(self, dt):
        # Update position based on velocity
        # dt should be in seconds (real time)
        
        # Store previous position for trail
        self.frames.pop()
        self.frames.insert(0, (self.screen_x, self.screen_y, self.dim(self.color)))
        
        # Update real position
        self.real_x += self.real_vx * dt
        self.real_y += self.real_vy * dt

    @staticmethod
    def dim(color: tuple[int, int, int]):
        r, g, b = color
        return (r//2, g//2, b//2)
    
    def apply_force(self, fx, fy, dt):
        # F = ma → a = F/m
        ax = fx / self.mass
        ay = fy / self.mass
        
        # Update velocities
        self.real_vx += ax * dt
        self.real_vy += ay * dt

    def apply_gravity(self, other, dt):
        # Vector from self to other (in meters)
        dx = other.real_x - self.real_x
        dy = other.real_y - self.real_y
        
        # Distance between bodies (in meters)
        r = np.sqrt(dx**2 + dy**2)
        
        # Avoid collision or division by zero
        min_distance = (self.radius + other.radius) * self.SCALE_FACTOR
        if r < min_distance:
            return
        
        # Calculate gravitational force: F = G * (m1 * m2) / r²
        force = self.G * (self.mass * other.mass) / (r**2)
        
        # Force components
        fx = force * dx / r
        fy = force * dy / r
        
        # Apply force
        self.apply_force(fx, fy, dt)

    def apply_all_gravity(self, bodies, dt):
        for body in bodies:
            if body is not self:  # Don't apply gravity to itself
                self.apply_gravity(body, dt)
    
    @staticmethod
    def apply_all_to_one(bodies, one, dt):
        for body in bodies:
            if body is not one:
                body.apply_gravity(one, dt)

    # def out_of_bounds(self, bounds_x, bounds_y) -> bool:
    #     if self.real_x < -10 or self.real_x > bounds_x + 10:
    #         return True
    #     elif self.real_y < -10 or self.real_y > bounds_y + 10:
    #         return True
    #     else:
    #         return False