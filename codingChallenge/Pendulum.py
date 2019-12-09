import pygame
import pygame.gfxdraw
import math

green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
lineRect = (300,300,10,100)
display_width = 600
display_height = 600
FPS = 30
pygame.init()
clock = pygame.time.Clock()

def rotate(win):
    rotated_image = pygame.transform.rotate(self.img,self.tilt)
    new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
    win.blit(rotated_image,new_rect.topleft)

def simulate():
    g = 1
    L = 50
    theta = 1
    thetadas = 0
    x0 = 300
    y0 = 50
    thetadasdas = (-g/L)*theta

    omega = math.sqrt(g/L)
    
    mass = 20
    x1 = x0 + L* math.sin(theta)
    y1 = y0 + L*math.cos(theta)
    
    simulateDisplay = pygame.display.set_mode((display_width,display_height))
    while True:
        clock.tick(FPS)
        # L-=1
        thetadasdas = (-g/L)*theta
        thetadas+=thetadasdas
        # thetadas*=0.99
        theta+=thetadas
        x1 = x0 + L* math.sin(theta)
        y1 = y0 + L*math.cos(theta)
        simulateDisplay.fill(white)
        # pygame.draw.lines(screen, color, closed, pointlist, thickness)
        # pygame.draw.line(simulateDisplay,black,(300,50),(x1,y1),3)
        # pygame.gfxdraw.line(simulateDisplay,300,300,int(x1),int(y1),red)
        # pygame.draw.circle(screen, color, (x1,y1), radius, thickness)
        # pygame.draw.circle(simulateDisplay, red, (int(x1),int(y1)), 20, 10)
        pygame.draw.line(simulateDisplay,black,(x0,y0),(x1,y1),3)
        pygame.gfxdraw.filled_circle(simulateDisplay,int(x1),int(y1),mass,red)

        # pygame.display.flip()
        pygame.display.update()        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Close the game any way you want, or troll users who want to close your game.
                raise SystemExit





if __name__=="__main__":
    simulate()