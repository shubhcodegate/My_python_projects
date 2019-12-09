import Vector
import pygame
import random

green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)

c1 = 0.4    #Cognitive Parameter
c2 = 0.1    #Social Parameter
w = 0.8     #self momentum
WIN_WIDTH = 1000
WIN_HEIGHT = 600
unit_velocity = 10
block_size = 10
FPS = 15
pygame.init()
clock = pygame.time.Clock()


class Swarm:
    def __init__(self,n,target,collection=[]):
        self.n = n
        self.gbest = Vector.Vector2D([0,0])
        self.collection = collection
        self.target = target
    def addCollection(self,collection):
        self.collection=collection
    def drawSwarm(self,gameDisplay):
        for i in self.collection:
            i.draw(gameDisplay)
    def move(self):
        for i in self.collection:
            i.move()
            if Vector.relativeDistance(i.pbest,self.target) < Vector.relativeDistance(self.gbest,self.target):
                self.gbest = i.pbest
    def explore(self):
        for i in range(10):
            random.choice(self.collection).explore()
class Particle:
    particleCount = 0
    def __init__(self,swarm,randomGen):
        self.myswarm = swarm
        if randomGen:
            self.postion =  Vector.Vector2D(randomGen=True,maxMag= WIN_WIDTH)
            self.velocity = Vector.Vector2D()
        self.pbest = self.postion
        self.size = block_size
        self.rect = [self.postion.values[0],self.postion.values[1],self.size,self.size]
    def move(self):
        self.velocity = self.velocity * w + (self.pbest-self.postion) * c1 + (self.myswarm.gbest - self.postion) * c2
        self.postion += self.velocity
        self.velocity*=0.95
        if Vector.relativeDistance(self.pbest,self.myswarm.target) > Vector.relativeDistance(self.postion,self.myswarm.target):
            self.pbest = self.postion
        self.rect = [self.postion.values[0],self.postion.values[1],self.size,self.size]
    def explore(self):
        self.velocity = Vector.Vector2D()
        self.postion = Vector.Vector2D(randomGen=True,maxMag= WIN_WIDTH)
    def draw(self,gameDisplay):
        pygame.draw.rect(gameDisplay,green,self.rect)

def createSwarm(n,target):
    newSwarm = Swarm(n,target)
    collection = []
    for i in range(n):
        collection.append(Particle(newSwarm,True))
    newSwarm.addCollection(collection)
    return newSwarm

def start():
    count = 0
    target = Vector.Vector2D([100,100])
    gameDisplay = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
    thisswarm = createSwarm(100,target)
    gameLoop = True
    while True: # Ultra Game Loop
        while gameLoop:
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                # Close the game any way you want, or troll users who want to close your game.
                    raise SystemExit
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    print(pos)
                    thisswarm.target = Vector.Vector2D([pos[0],pos[1]])
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        mySnakeHead.changedir("left")        
                    if event.key == pygame.K_RIGHT:
                        mySnakeHead.changedir("right") 
                    if event.key == pygame.K_UP:
                        mySnakeHead.changedir("up") 
                    if event.key == pygame.K_DOWN:
                        mySnakeHead.changedir("down")
                    if event.key == pygame.K_c:
                        gameLoop = True
            thisswarm.move()
            gameDisplay.fill(white)  
            thisswarm.drawSwarm(gameDisplay)          
            pygame.display.update()
            if count>FPS:
                count=0
                thisswarm.explore()    
            count=count+1

        gameDisplay.fill(white)
        # displayonScreen(gameDisplay,"Game Over!",50,red,(display_width/2,display_height/2-30))
        # displayonScreen(gameDisplay,"Press C to Continue or Press Q to Quit..",25,red,(display_width/2,display_height/2+40))
        pygame.display.update()
        while not gameLoop:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameLoop = True
                    if event.key == pygame.K_q:
                        raise SystemExit


if __name__ == "__main__":
    start()