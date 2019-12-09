import pygame
import random
import neat
import os
green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)

display_width = 900
display_height = 600
block_size = 20
fruit_block_size = 20
unit_velocity = 20
FPS = 80

pygame.init()
clock = pygame.time.Clock()
# pygame.display.set_caption("Snake Game")
# pygame.display.update()

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_vel = unit_velocity
        self.y_vel = 0
        self.size = block_size
        self.rect = [self.x,self.y,self.size,self.size]
        self.length = 1
        self.body = [self.rect]
    def motion(self):
        self.x += self.x_vel
        self.y +=self.y_vel
        self.rect = [self.x,self.y,self.size,self.size]
        self.body.append(self.rect)
        for eachPart in self.body[:-self.length]:
            self.body.remove(eachPart)

    def increase_length(self):
        self.length+=1
    def selfCollide(self):
        for eachPart in self.body[:-1]:
            if eachPart[0]==self.x and eachPart[1]==self.y:
                return True

    def changedir(self,dirn):
        if dirn =="left":
            self.x_vel = -unit_velocity
            self.y_vel = 0
        elif dirn =="right":
            self.x_vel = unit_velocity
            self.y_vel = 0
        elif dirn =="up":
            self.x_vel = 0
            self.y_vel = -unit_velocity
        elif dirn =="down":
            self.x_vel = 0
            self.y_vel = unit_velocity

    def draw(self, gameDisplay):
        for eachPart in self.body:
            pygame.draw.rect(gameDisplay,green,eachPart)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.rect)

class Fruits:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = fruit_block_size
        self.rect = [self.x,self.y,self.size,self.size]
        
    def draw(self, gameDisplay):
        pygame.draw.rect(gameDisplay,red,self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.rect)

def displayonScreen(gameDisplay,massage,size,color,position):
    font = pygame.font.SysFont(None, size)  
    textSurface = font.render(massage, True, color) 
    textRect = textSurface.get_rect()
    textRect.center = position
    gameDisplay.blit(textSurface,textRect)  

def checkCollition(item1,item2):
    collide = True
    if item1.x + item1.size <= item2.x or item1.x >= item2.x + item2.size:
        collide =  False
    if item1.y + item1.size <= item2.y or item1.y >=item2.y + item2.size:
            collide =  False
    return collide
        

    # Mask1 = item1.get_mask()
    # Mask2 = item2.get_mask()
    # offset = (item1.x - item2.x, item1.y - item2.y)
    # return Mask2.overlap(Mask1,offset)

            


# pygame.quit()
# quit()
# input("Press Enter to continue...")
def playGame(genomes, config):
    # nets = []
    # ge = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        # nets.append(net)
        # ge.append(genome)  
        genome.fitness = 0  
        score = 0
        gameDisplay = pygame.display.set_mode((display_width,display_height))
        # gameExit = False
        gameLoop = True
        stuck = 0
        mySnakeHead = Snake(display_width/2,display_height/2)
        myFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))     
        
        while gameLoop:
            clock.tick(FPS)
            output = net.activate((abs(mySnakeHead.x - myFruit.x),abs(mySnakeHead.y - myFruit.y),mySnakeHead.x,mySnakeHead.y))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                # Close the game any way you want, or troll users who want to close your game.
                    raise SystemExit
            dirn = output.index(max(output))
            if dirn == 0 and output[dirn]>0.5:
                mySnakeHead.changedir("left")        
            elif dirn == 1 and output[dirn]>0.5:
                mySnakeHead.changedir("right") 
            elif dirn == 2 and output[dirn]>0.5:
                mySnakeHead.changedir("up") 
            elif dirn == 3 and output[dirn]>0.5:
                mySnakeHead.changedir("down")
            stuck+=1
            gameDisplay.fill(white)
            displayonScreen(gameDisplay,"Score: "+ str(score),30,black,(display_width/2-50-len("Score"+ str(score)),10))
            displayonScreen(gameDisplay,"Genome id : "+ str(genome_id),30,black,(display_width/2-50-len("Genome id :"+ str(genome_id)),40))
            myFruit.draw(gameDisplay)
            mySnakeHead.motion()
            genome.fitness += 0.1
            mySnakeHead.draw(gameDisplay)
            pygame.display.update()
            if stuck>=FPS*2:
                genome.fitness -=5
                gameLoop = False
            if mySnakeHead.selfCollide():
                genome.fitness -=  5
                gameLoop = False
            if checkCollition(mySnakeHead,myFruit):
                del myFruit
                myFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))
                score+=1
                genome.fitness += 15
                mySnakeHead.increase_length()
                
                stuck=0 
                # print("Yo ! I Collided")
            if mySnakeHead.x > display_width - mySnakeHead.size or mySnakeHead.x < 0 or mySnakeHead.y > display_height - mySnakeHead.size or mySnakeHead.y<0: # Outside of game screen test
                genome.fitness -= 15
                gameLoop = False          

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
    neat.DefaultSpeciesSet,neat.DefaultStagnation,
    config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(playGame,50)     # Winner is genome object . Use pickle (import pickle) to save this winner genome. then unpickle and use wherever you want
    print('\nBest genome:\n{!s}'.format(winner))


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)