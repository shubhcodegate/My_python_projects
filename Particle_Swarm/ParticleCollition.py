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
unit = 100

WIN_WIDTH = 1000
WIN_HEIGHT = 600
FPS = 30

pygame.init()
pygame.display.set_caption("Particle System")
clock = pygame.time.Clock()

class Swarm():
    def __init__(self,n,target,collection=[]):
        self.n = n
        self.gbest = physics.Vector2D([0,0])
        self.collection = collection
        self.target = target
    def addCollection(self,collection):
        self.collection=collection
    def move(self):
        for i in self.collection:
            i.move()
            if Vector.relativeDistance(i.pbest,self.target) < Vector.relativeDistance(self.gbest,self.target):
                self.gbest = i.pbest
    def drawSwarm(self,gameDisplay):
        for i in self.collection:
            i.draw(gameDisplay)


def createSwarm(n,target):
    newSwarm = Swarm(n,target)
    collection = []
    for i in range(n):
        randPos = [random.randint(0,WIN_WIDTH),random.randint(0,WIN_WIDTH)]
        collection.append(SwarmParticle(newSwarm,randPos,10,20))
    newSwarm.addCollection(collection)
    return newSwarm


class SwarmParticle(physics.Particle):
    def __init__(self,swarm,position,radius,mass,velocity=[0,0],accel=[0,0],w=0.8,c1=0.4,c2=0.1):
        physics.Particle.__init__(self,position,radius,mass,velocity,accel)  
        self.w = w    #Cognitive Parameter
        self.c1 = c1    #Social Parameter
        self.c2 = c2     #self momentum
        self.myswarm = swarm
        self.pbest = self.position
    
    def move(self):
        self.velocity = self.velocity * self.w + (self.pbest-self.position) * self.c1 + (self.myswarm.gbest - self.position) * self.c2
        super().move()
        if physics.relativeDistance(self.pbest,self.myswarm.target.position) > physics.relativeDistance(self.position,self.myswarm.target.position):
            self.pbest = self.position
    def draw(self,gameDisplay):
        pygame.gfxdraw.filled_circle(gameDisplay,int(self.position.getx()),int(self.position.gety()),int(self.size),tomato)

class TargetParticle(physics.Particle):
    def __init__(self,position,radius,mass,velocity=[0,0],accel=[0,0]):
        physics.Particle.__init__(self,position,radius,mass,velocity,accel)  
    def draw(self,gameDisplay):
        pygame.gfxdraw.filled_circle(gameDisplay,int(self.position.getx()),int(self.position.gety()),int(self.size),tomato)

def gameEnv():
    newParticle = TargetParticle([WIN_WIDTH/2,WIN_HEIGHT/2],10,100)
    newSwarm = createSwarm(5,newParticle)
    particles = [newParticle] + newSwarm.collection
    gameDisplay = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    Force = physics.Vector2D()
    myscene = list(combinations(particles,2))
    while True:
        clock.tick(FPS)
        gameDisplay.fill(white)
        newParticle.applyForce(Force)
        for obj in particles:
            obj.move()
        for obj in particles:
            obj.draw(gameDisplay)
        for obj1,obj2 in myscene:
            physics.collition(obj1,obj2) 
        # newParticle.draw(gameDisplay)
        # otherParticle.draw(gameDisplay)
        pygame.display.update()
        
        # Exit Condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Close the game any way you want, or troll users who want to close your game.
                raise SystemExit
            # if event.type == pygame.KEYDOWN:
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
                # if event.key == pygame.K_LEFT:
                #     Force -= physics.Vector2D([-unit,0])      
                # if event.key == pygame.K_RIGHT:
                #     Force -= physics.Vector2D([unit,0]) 
                # if event.key == pygame.K_UP:
                #     Force -= physics.Vector2D([0,-unit]) 
                # if event.key == pygame.K_DOWN:
                #     Force -= physics.Vector2D([0,unit])
if __name__ == "__main__":
    gameEnv()