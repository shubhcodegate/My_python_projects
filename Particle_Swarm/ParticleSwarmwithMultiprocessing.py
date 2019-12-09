import pygame
import pygame.gfxdraw
import physics
from itertools import combinations
import random
import time
# from multiprocessing import Pool
# from multiprocessing.pool import ThreadPool

green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
tomato = (255,99,71)
unit = 100

WIN_WIDTH = 800
WIN_HEIGHT = 400
FPS = 30

pygame.init()
pygame.display.set_caption("Particle System")
clock = pygame.time.Clock()
UniversalBoundary = [1,1,WIN_WIDTH-1,WIN_HEIGHT-1]


def timelogged(function):
    def inner(*args,**kwargs):
        begin = time.time()
        function(*args,**kwargs)
        end = time.time()
        print("Total time taken in : ", function.__name__, (end - begin)*1000," milliseconds") 
    return inner

multiScene = timelogged(physics.multiScene)

class mySwarm(physics.Swarm):
    def __init__(self,n,target,color,collection=[]):
        super().__init__(n,target,collection=[])
        self.color = color
    @timelogged
    def drawSwarm(self,gameDisplay):
        for i in self.collection:
            i.draw(gameDisplay)
    
class myTarget(physics.TargetParticle):
    def __init__(self,position,mass,radius,color,velocity=[0,0],accel=[0,0]):
        super().__init__(position,mass,radius,velocity,accel)
        self.color = color
    def draw(self,gameDisplay):
        pygame.gfxdraw.filled_circle(gameDisplay,int(self.position.getx()),int(self.position.gety()),int(self.size),self.color)

def createSwarm(n,target,color,particle_size=5,particle_mass=2):
    newSwarm = mySwarm(n,target,color)
    collection = []
    for i in range(n):
        randPos = [random.randint(0,400),random.randint(0,400)]
        # randPos = [i*100,100]
        collection.append(mySwarmParticle(newSwarm,randPos,particle_mass,particle_size,color))
    newSwarm.addCollection(collection)
    return newSwarm

class mySwarmParticle(physics.SwarmParticle):
    def __init__(self,swarm,position,mass,radius,color,velocity=[0,0],accel=[0,0],w=0.8,c1=0.4,c2=0.1):
        super().__init__(swarm,position,mass,radius,velocity,accel,w,c1,c2)
        self.color = color
    def draw(self,gameDisplay):
        pygame.gfxdraw.filled_circle(gameDisplay,int(self.position.getx()),int(self.position.gety()),int(self.size),self.color)
class myHunterParticle(physics.HunterParticle):
    def __init__(self,position,mass,radius,color,target=[],velocity=[0,0],accel=[0,0],w=0.8,c1=0.4,c2=0.1):
        super().__init__(position,mass,radius,target,velocity,accel)
        self.color = color
    def draw(self,gameDisplay):
        pygame.gfxdraw.filled_circle(gameDisplay,int(self.position.getx()),int(self.position.gety()),int(self.size),self.color)

def gameEnv():
    count = 0
    targetBall = physics.Vector2D([WIN_WIDTH/2,WIN_HEIGHT/2])
    hunter = myHunterParticle([100,100],mass=50,radius=10,color=red)
    hunter2 = myHunterParticle([100,100],mass=50,radius=5,color=tomato)
    # targetBall = myTarget([WIN_WIDTH/2,WIN_HEIGHT/2],20,100,black)
    thisswarm = createSwarm(100,targetBall,green,particle_size=1,particle_mass=20)
    # enemyswarm = createSwarm(10,thisswarm.collection[0],tomato,particle_size=5,particle_mass=50)
    # thisswarm.addHunters(enemyswarm.collection)
    thisswarm.addHunters([hunter,hunter2])
    hunter.addTarget(thisswarm.collection[0])
    hunter2.addTarget(thisswarm.collection[0])
    particles = thisswarm.collection + [hunter,hunter2]

    gameDisplay = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    myscene = list(combinations(particles,2))

    hunter.enableBoundary(UniversalBoundary)
    hunter2.enableBoundary(UniversalBoundary)
    # targetBall.enableBoundary(UniversalBoundary)
    thisswarm.enableBoundary(UniversalBoundary)
    # enemyswarm.enableBoundary(UniversalBoundary)
    while True:
        clock.tick(FPS)
        # Give Particles Life
        hunter.addTarget(thisswarm.collection[0])
        hunter2.addTarget(thisswarm.collection[1])
        
        thisswarm.move()
        hunter.move()
        hunter2.move()
        # targetBall.move()
        # enemyswarm.move()

        # Draw Simulation
        gameDisplay.fill(white) 

        # targetBall.draw(gameDisplay) 
        thisswarm.drawSwarm(gameDisplay)
        hunter.draw(gameDisplay)
        hunter2.draw(gameDisplay)
        # enemyswarm.drawSwarm(gameDisplay)          
        pygame.display.update()
        
        multiScene(myscene)

        if count>FPS:
            count=0
            thisswarm.explore()    
        count=count+1
        # enemyswarm.target = thisswarm.collection[0]

        # Exit Condition
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Close the game any way you want, or troll users who want to close your game.
                raise SystemExit
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                print(pos)
                thisswarm.target = physics.Vector2D([pos[0],pos[1]])
                # enemyswarm.target = physics.Vector2D([pos[0],pos[1]])

if __name__ == "__main__":
    gameEnv()