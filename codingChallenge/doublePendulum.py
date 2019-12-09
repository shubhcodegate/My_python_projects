import pygame
import pygame.gfxdraw
import math

green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
lineRect = (300,300,10,100)
tomato = (255,99,71)
display_width = 400
display_height = 400
FPS = 15
pygame.init()
pygame.display.set_caption("Double Pendulum")
clock = pygame.time.Clock()

def rotate(win):
    rotated_image = pygame.transform.rotate(self.img,self.tilt)
    new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x,self.y)).center)
    win.blit(rotated_image,new_rect.topleft)

def simulate():
    g = 5
    L1 = 20
    L2 = 50
    x0 = int(display_width/2)
    y0 = int(100)
    m1 = 8
    m2 = 2
    theta1 = 1
    theta2 = 2
    theta1das = 0
    theta2das = 0
    v_coeff = 0.01
    theta1dasdas =( -g*(2*m1+m2)*math.sin(theta1)-m2*g*math.sin(theta1-2*theta2)-2*math.sin(theta1-theta2)*m2*(theta2das*theta2das*L2+theta1das*theta1das*L1*math.cos(theta1-theta2)) )/(L1*(2*m1+m2-m2*math.cos(2*theta1-2*theta2)))
    theta2dasdas = (2*math.sin(theta1- theta2)*(theta1das*theta1das*L1*(m1+m2)+g*(m1+m2)*math.cos(theta1)+theta2das*theta2das*L2*m2*math.cos(theta1-theta2)))/(L2*(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2)))
    # omega = math.sqrt(g/L)
    
    x1 = x0 + L1* math.sin(theta1)
    y1 = y0 + L1*math.cos(theta1)
    x2 = x1 + L2* math.sin(theta2)
    y2 = y1 + L2*math.cos(theta2)
    simulateDisplay = pygame.display.set_mode((display_width,display_height))
    while True:
        clock.tick(FPS)    
        
        num1 = (-g*(2*m1+m2)*math.sin(theta1)-m2*g*math.sin(theta1-2*theta2)-2*math.sin(theta1-theta2)*m2*(theta2das*theta2das*L2+theta1das*theta1das*L1*math.cos(theta1-theta2)))
        den1 = (L1*(2*m1+m2-m2*math.cos(2*theta1-2*theta2)))
        theta1dasdas =num1/den1
        num2 = (2*math.sin(theta1- theta2)*(theta1das*theta1das*L1*(m1+m2)+g*(m1+m2)*math.cos(theta1)+theta2das*theta2das*L2*m2*math.cos(theta1-theta2)))
        den2 = (L2*(2*m1 + m2 - m2*math.cos(2*theta1 - 2*theta2)))
        theta2dasdas = num2/den2
        theta1das+=theta1dasdas
        theta2das+=theta2dasdas
        theta1+=theta1das
        theta2+=theta2das

        theta1das*=(1-v_coeff)
        theta2das*=(1-v_coeff)

        x1 = x0 + L1* math.sin(theta1)
        y1 = y0 + L1*math.cos(theta1)
        x2 = x1 + L2* math.sin(theta2)
        y2 = y1 + L2*math.cos(theta2)
    
        simulateDisplay.fill(white)
        pygame.draw.line(simulateDisplay,black,(x0,y0),(x1,y1),3)
        pygame.draw.line(simulateDisplay,black,(x1,y1),(x2,y2),3)
        pygame.gfxdraw.filled_circle(simulateDisplay,int(x1),int(y1),int(m1),tomato)
        pygame.gfxdraw.filled_circle(simulateDisplay,int(x2),int(y2),int(m2),tomato)
        
        # pygame.display.flip()
        pygame.display.update()        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Close the game any way you want, or troll users who want to close your game.
                raise SystemExit





if __name__=="__main__":
    simulate()