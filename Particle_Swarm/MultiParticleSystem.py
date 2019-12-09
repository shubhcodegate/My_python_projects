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
            if type(self.target) is TargetParticle:
                if physics.relativeDistance(i.pbest,self.target.position) < physics.relativeDistance(self.gbest,self.target.position):
                    self.gbest = i.pbest
            elif type(self.target) is physics.Vector2D:
                if physics.relativeDistance(i.pbest,self.target) < physics.relativeDistance(self.gbest,self.target):
                    self.gbest = i.pbest
            
    def explore(self):
        for i in range(10):
            random.choice(self.collection).explore()
    def drawSwarm(self,gameDisplay):
        for i in self.collection:
            i.draw(gameDisplay)


def createSwarm(n,target,particle_size=5,particle_mass=2):
    newSwarm = Swarm(n,target)
    collection = []
    for i in range(n):
        randPos = [random.randint(0,WIN_HEIGHT),random.randint(0,WIN_HEIGHT)]
        collection.append(SwarmParticle(newSwarm,randPos,particle_mass,particle_size))
    newSwarm.addCollection(collection)
    return newSwarm


class SwarmParticle(physics.Particle):
    def __init__(self,swarm,position,mass,radius,velocity=[0,0],accel=[0,0],w=0.8,c1=0.4,c2=0.1):
        physics.Particle.__init__(self,position,mass,radius,velocity,accel)  
        self.w = w    #Cognitive Parameter
        self.c1 = c1    #Social Parameter
        self.c2 = c2     #self momentum
        self.myswarm = swarm
        self.pbest = self.position
    
    def move(self):
        self.accel = ( (self.pbest-self.position) * self.c1 + (self.myswarm.gbest - self.position) * self.c2)/((1-self.w)*self.mass)
        super().move()
        if type(self.myswarm.target) is TargetParticle:
            if physics.relativeDistance(self.pbest,self.myswarm.target.position) > physics.relativeDistance(self.position,self.myswarm.target.position):
                self.pbest = self.position
        elif type(self.myswarm.target) is physics.Vector2D:
            if physics.relativeDistance(self.pbest,self.myswarm.target) > physics.relativeDistance(self.position,self.myswarm.target):
                self.pbest = self.position
        self.boundaryCondition()

    def boundaryCondition(self):
        if self.position.values[0]>=WIN_WIDTH-self.size:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = WIN_WIDTH-self.size
        if self.position.values[0]<=self.size:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = self.size
        if self.position.values[1]>=WIN_HEIGHT-self.size:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1]=WIN_HEIGHT-self.size
        if self.position.values[1]<=self.size:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1] = self.size
    def explore(self):
        randForce = physics.Vector2D([random.randint(0,100),random.randint(0,100)])
        self.applyForce(randForce)

    def draw(self,gameDisplay):
        pygame.gfxdraw.filled_circle(gameDisplay,int(self.position.getx()),int(self.position.gety()),int(self.size),tomato)

class TargetParticle(physics.Particle):
    def __init__(self,position,mass,radius,velocity=[0,0],accel=[0,0]):
        physics.Particle.__init__(self,position,mass,radius,velocity,accel)  
    def move(self):
        super().move()
        self.boundaryCondition()
    def boundaryCondition(self):
        if self.position.values[0]>=WIN_WIDTH-self.size:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = WIN_WIDTH-self.size
        if self.position.values[0]<=self.size:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = self.size
        if self.position.values[1]>=WIN_HEIGHT-self.size:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1]=WIN_HEIGHT-self.size
        if self.position.values[1]<=self.size:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1] = self.size
    
    def draw(self,gameDisplay):
        pygame.gfxdraw.filled_circle(gameDisplay,int(self.position.getx()),int(self.position.gety()),int(self.size),green)

def gameEnv():
    count = 0
    # targetBall = physics.Vector2D([100,100])
    targetBall = TargetParticle([WIN_WIDTH/2,WIN_HEIGHT/2],100,20)
    thisswarm = createSwarm(10,targetBall,5,particle_mass=50)
    thatswarm =  createSwarm(10,targetBall,5,particle_mass=50)
    thirdswarm = createSwarm(10,targetBall,5,particle_mass=50)
    forthswarm = createSwarm(10,targetBall,5,particle_mass=50)
    particles = thisswarm.collection + thatswarm.collection + thirdswarm.collection + forthswarm.collection + [targetBall]
    gameDisplay = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))

    myscene = list(combinations(particles,2))
    while True:
        clock.tick(FPS)

        thisswarm.move()
        thatswarm.move()
        thirdswarm.move()
        forthswarm.move()
        for obj1,obj2 in myscene:
            physics.perfectCollition(obj1,obj2,0.5) 
        targetBall.move()
        gameDisplay.fill(white) 
        targetBall.draw(gameDisplay) 
        thisswarm.drawSwarm(gameDisplay) 
        thatswarm.drawSwarm(gameDisplay)
        thirdswarm.drawSwarm(gameDisplay)
        forthswarm.drawSwarm(gameDisplay)

        pygame.display.update()
        

        if count>FPS:
            count=0
            thisswarm.explore() 
            thatswarm.explore()
            thirdswarm.explore()
            forthswarm.explore()
        count=count+1
        
        # Exit Condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Close the game any way you want, or troll users who want to close your game.
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                thisswarm.target = physics.Vector2D([pos[0],pos[1]])
                thatswarm.target = physics.Vector2D([pos[0],pos[1]])
                thirdswarm.target = physics.Vector2D([pos[0],pos[1]])
                forthswarm.target = physics.Vector2D([pos[0],pos[1]])

if __name__ == "__main__":
    gameEnv()