import pygame
import pygame.gfxdraw
import physics
from itertools import combinations
import random

green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
tomato = (255,99,71)
unit = 50

WIN_WIDTH = 800
WIN_HEIGHT = 400
FPS = 30

pygame.init()
pygame.display.set_caption("Particle System")
clock = pygame.time.Clock()



class mySwarm(physics.Swarm):
    def __init__(self,n,target,collection=[]):
        super().__init__(n,target,collection=[])
    
    def drawSwarm(self,gameDisplay):
        for i in self.collection:
            i.draw(gameDisplay)
 
def createSwarm(n,target,particle_size=5,particle_mass=2):
    newSwarm = mySwarm(n,target)
    collection = []
    for i in range(n):
        randPos = [random.randint(0,400),random.randint(0,400)]
        # randPos = [i*100,100]
        collection.append(mySwarmParticle(newSwarm,randPos,particle_mass,particle_size))
    newSwarm.addCollection(collection)
    return newSwarm

class mySwarmParticle(physics.SwarmParticle):
    def __init__(self,swarm,position,mass,radius,velocity=[0,0],accel=[0,0],w=0.8,c1=0.4,c2=0.1):
        super().__init__(swarm,position,mass,radius,velocity,accel,w,c1,c2)
    def draw(self,gameDisplay):
        pygame.gfxdraw.filled_circle(gameDisplay,int(self.position.getx()),int(self.position.gety()),int(self.size),tomato)

class BoxTargetParticle(physics.BoxParticle):
    def __init__(self,position,mass,dimesion,velocity=[0,0],accel=[0,0]):
        super().__init__(position,mass,dimesion,velocity,accel)  
    
    def draw(self,gameDisplay):
        pygame.draw.rect(gameDisplay,green,[int(self.position.getx()),int(self.position.gety()),self.size[0],self.size[1]])

def gameEnv():
    count = 0
    Force = physics.Vector2D()
    # targetBall = physics.Vector2D([100,100])
    # targetBall = TargetParticle([WIN_WIDTH/2,WIN_HEIGHT/2],20,100)
    targetBall = BoxTargetParticle([WIN_WIDTH/2,WIN_HEIGHT/2],100,[100,50])

    thisswarm = createSwarm(5,targetBall,particle_size=5,particle_mass=10)
    targetBall.enableBoundary([0,0,WIN_WIDTH,WIN_HEIGHT])
    thisswarm.enableBoundary([0,0,WIN_WIDTH,WIN_HEIGHT])
    particles = thisswarm.collection + [targetBall]
    gameDisplay = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    myscene = list(combinations(particles,2))
    while True:
        clock.tick(FPS)

        thisswarm.move()
        targetBall.applyForce(Force)
        targetBall.move()
        gameDisplay.fill(white) 
        targetBall.draw(gameDisplay) 
        thisswarm.drawSwarm(gameDisplay)          
        pygame.display.update()
        for obj1,obj2 in myscene:
            physics.perfectCollition(obj1,obj2,0) 

        # if count>FPS:
        #     count=0
        #     thisswarm.explore()    
        # count=count+1
        
        # Exit Condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Close the game any way you want, or troll users who want to close your game.
                raise SystemExit
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                Force+=physics.Vector2D([-unit,0])    
            if keys[pygame.K_RIGHT]:
                Force+=physics.Vector2D([unit,0])    
            if keys[pygame.K_UP]:
                Force+=physics.Vector2D([0,-unit])   
            if keys[pygame.K_DOWN]:
                Force+=physics.Vector2D([0,unit]) 
            if event.type == pygame.KEYUP:
                Force = physics.Vector2D()
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                # thisswarm.target = physics.Vector2D([pos[0],pos[1]])

if __name__ == "__main__":
    gameEnv()