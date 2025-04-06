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
    def screen_y(self, name=''):
        # Convert real position to screen coordinates
        return self.real_y / self.SCALE_FACTOR
    
    def draw(self, screen):
        # Draw trail
        for x, y, color in self.frames:
            pygame.draw.circle(screen, color, (int(x), int(y)), self.radius//2)
        
        # Draw body
        pygame.draw.circle(screen, self.color, (int(self.screen_x), int(self.screen_y)), self.radius)
        
        # Draw name if provided
        font = pygame.font.Font(None, 24)
        if self.name:
            text = font.render(self.name, True, self.color)
            screen.blit(text, (int(self.screen_x) + self.radius + 5, int(self.screen_y) - 10))
        else:
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

    def update_rk4(self, dt, bodies):
        # Store previous position for trail
        self.frames.pop()
        self.frames.insert(0, (self.screen_x, self.screen_y, self.dim(self.color)))
        
        # Store current state
        x0, y0 = self.real_x, self.real_y
        vx0, vy0 = self.real_vx, self.real_vy
        
        # Calculate k1 (equivalent to Euler method)
        k1_x, k1_y = vx0, vy0
        k1_vx, k1_vy = self.calculate_acceleration(bodies, x0, y0)
        
        # Calculate k2 (midpoint using k1)
        k2_x, k2_y = vx0 + 0.5*dt*k1_vx, vy0 + 0.5*dt*k1_vy
        k2_vx, k2_vy = self.calculate_acceleration(
            bodies, 
            x0 + 0.5*dt*k1_x, 
            y0 + 0.5*dt*k1_y
        )
        
        # Calculate k3 (midpoint using k2)
        k3_x, k3_y = vx0 + 0.5*dt*k2_vx, vy0 + 0.5*dt*k2_vy
        k3_vx, k3_vy = self.calculate_acceleration(
            bodies, 
            x0 + 0.5*dt*k2_x, 
            y0 + 0.5*dt*k2_y
        )
        
        # Calculate k4 (endpoint using k3)
        k4_x, k4_y = vx0 + dt*k3_vx, vy0 + dt*k3_vy
        k4_vx, k4_vy = self.calculate_acceleration(
            bodies, 
            x0 + dt*k3_x, 
            y0 + dt*k3_y
        )
        
        # Update position and velocity using weighted sum
        self.real_x = x0 + dt/6 * (k1_x + 2*k2_x + 2*k3_x + k4_x)
        self.real_y = y0 + dt/6 * (k1_y + 2*k2_y + 2*k3_y + k4_y)
        self.real_vx = vx0 + dt/6 * (k1_vx + 2*k2_vx + 2*k3_vx + k4_vx)
        self.real_vy = vy0 + dt/6 * (k1_vy + 2*k2_vy + 2*k3_vy + k4_vy)
    
    def calculate_acceleration(self, bodies, pos_x, pos_y):
        ax, ay = 0, 0
        
        for body in bodies:
            if body is not self:  # Don't apply gravity to itself
                # Vector from self to other (in meters)
                dx = body.real_x - pos_x
                dy = body.real_y - pos_y
                
                # Distance between bodies (in meters)
                r = np.sqrt(dx**2 + dy**2)
                
                # Avoid collision or division by zero
                min_distance = (self.radius + body.radius) * self.SCALE_FACTOR
                if r < min_distance:
                    continue
                
                # Calculate gravitational acceleration: a = G * m / r²
                acceleration = self.G * body.mass / (r**2)
                
                # Acceleration components
                ax += acceleration * dx / r
                ay += acceleration * dy / r
        
        return ax, ay

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
    @staticmethod
    def calc_cm(bodies: list["Body"]):
        yc = 0
        xc = 0
        M_sum = 0
        for body in bodies:
            xc += body.screen_x * body.mass
            yc += body.screen_y * body.mass
            M_sum += body.mass
        if M_sum == 0:
            return None
    
        return (xc//M_sum, yc//M_sum)
    # def out_of_bounds(self, bounds_x, bounds_y) -> bool:
    #     if self.real_x < -10 or self.real_x > bounds_x + 10:
    #         return True
    #     elif self.real_y < -10 or self.real_y > bounds_y + 10:
    #         return True
    #     else:
    #         return False