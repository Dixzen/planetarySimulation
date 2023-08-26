#Akshat Dixit


import pygame
import math
pygame.init()

WIDTH, HEIGHT = 1050, 1050

#pygame surface or window

WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet-Simulation")


WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100, 149, 237)
GREY = (90, 90, 90)
WHITEYELLOW = (242, 240, 223)
RUSTYRED = (175,47,13)
BROWN = (205,127,50)


#initializing font

FONT = pygame.font.SysFont("comicsans", 20)

#drawing planets

class Planet:
    
    # Astronomical Values
    
    AU = 149.6e6 * 1000
    G = 6.67428e-11

    # scale the orbit down to fit into the pygame window
    
    SCALE = 100 / AU
    
    TIMESTEP =  3600*24          # 1s = 1day
    

    #initialization values (in meters)
    
    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass                  
        self.orbit= []              # keeping tracks of all the points this planet has travelled along
        self.sun = False
        self.distance_to_sun = 0
        self.x_vel = 0
        self.y_vel = 0
        
        
    
    #drawing planet
    
    def draw(self, win):
        
        #scaling
        
        x = self.x * self.SCALE + WIDTH / 2         #(0,0) -> is the TOP LEFT HAND CORNER OF THE SCREEN
        y = self.y * self.SCALE + HEIGHT / 2
        
        if len(self.orbit) >= 2:
            
            updated_Points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_Points.append((x, y))
        
            # orbits
            pygame.draw.lines(win, self.color, False, updated_Points, 1  )
      
            
        # planets
        pygame.draw.circle(win, self.color, (x, y) , self.radius )
        
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            win.blit(distance_text, (x ,y))
        
        
    # Calculating Force of attraction b/w current object and another object
    
    def attraction(self, other):
                
        #other is an object        
        other_x, other_y = other.x, other.y
        
        #calc dist b/w current and other object        
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        
        distance = math.sqrt(distance_x**2 + distance_y**2)
        
        if(other.sun):
            self.distance_to_sun = distance
            
        
        # straight line force
        force = (self.G * self.mass * other.mass) / distance**2
        
        #finding theta to calc Force components
        
        theta = math.atan2(distance_y, distance_x)  # tan-1 
        
        #force components
        
        force_x = force * math.cos(theta)
        force_y = force * math.sin(theta)
        return force_x, force_y
    
        
    #updating the position of each planet based on the force of attrac with every single other planet
    
    def updatePosition(self, planets):
        
        #going to look through all the planets

        total_fx = total_fy = 0
        
        #summing all forces together
        
        for planet in planets:
            
            # force with itself does not exists
            
            if(self == planet):
                continue
            
            fx, fy = self.attraction(planet)
            
            total_fx = total_fx + fx
            total_fy = total_fy + fy
    
    
        #calculating the velociy using F=ma equation
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP
        
        # changing position
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        
        # storing points the planet has travelled along to later draw circle
        self.orbit.append((self.x, self.y))
        

def main():
    
    run = True
    
    # limiting frame rate
    clock = pygame.time.Clock()
    
    
    sun = Planet(0, 0, 30, YELLOW, 1.98892 * 10**30 )
    sun.sun = True
    
    # creating planets 
    
    earth = Planet( -1 * Planet.AU, 0, 16, BLUE, 5.9722 * 10**24 )  # -1.AU means left 1 means right
    
    mercury = Planet( 0.44 * Planet.AU, 0, 6, GREY, 3.285 * 10**23 )
    
    venus = Planet( 0.73 * Planet.AU, 0, 14, WHITEYELLOW, 4.867 * 10**24 )
    
    mars = Planet( -1.63 * Planet.AU, 0, 8, RUSTYRED, 6.39 * 10**23 )
    
    jupiter = Planet( -4.96 * Planet.AU, 0, 20, BROWN, 1.89813 * 10**27 )

        
    # Giving initial y-velocity so that planets do not collapse in the sun    
    earth.y_vel = 30.29 * 1000 # in meters
    mercury.y_vel = -47.4 * 1000
    venus.y_vel = -35.02 * 1000
    mars.y_vel = 24.077 * 1000
    jupiter.y_vel = 12.44 * 1000
    
    planets = [sun, earth, venus, mercury, mars, jupiter]
    
    # event loop
    
    while run:
        
        # max 60 times
        
        clock.tick(60)     

        # backgroung color (keeps refreshing)
          
        WIN.fill((1,11,25))
        
        # getting different events running in pygame (keypresses, mouse movement etc.)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
        for planet in planets:
            planet.updatePosition(planets)
            planet.draw(WIN)
            
        pygame.display.update()
        
    pygame.quit()

main()

    

            
            

