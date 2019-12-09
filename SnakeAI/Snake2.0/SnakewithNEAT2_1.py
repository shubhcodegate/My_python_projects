import pygame
import random
import neat
import os
green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
############# No Reference to body given and no self collition ###########################
Font = "comicsansms"

display_width = 1080
display_height = 600
block_size = 10
fruit_block_size = 10
unit_velocity = 10
FPS = 80

pygame.init()
clock = pygame.time.Clock()
# pygame.display.set_caption("Snake Game")
# pygame.display.update()

class Snake:
    totalSnakes = 0
    def __init__(self, x, y):
        Snake.totalSnakes +=1
        self.id = Snake.totalSnakes
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
            font = pygame.font.SysFont(Font, int(self.size*0.8))  
            textSurface = font.render(str(self.id), True, black) 
            pygame.draw.rect(gameDisplay,green,eachPart)
            gameDisplay.blit(textSurface,eachPart)

    def get_mask(self):
        return pygame.mask.from_surface(self.rect)

class Fruits:
    totalFruits = 0
    def __init__(self, x, y):
        Fruits.totalFruits+=1
        self.id = Fruits.totalFruits
        self.x = x
        self.y = y
        self.size = fruit_block_size
        self.rect = [self.x,self.y,self.size,self.size]
        
        
    def draw(self, gameDisplay):
        font = pygame.font.SysFont(Font, int(self.size*0.8))  
        textSurface = font.render(str(self.id), True, black) 
        pygame.draw.rect(gameDisplay,red,self.rect)
        gameDisplay.blit(textSurface,self.rect)

    def get_mask(self):
        return pygame.mask.from_surface(self.rect)

def displayonScreen(gameDisplay,massage,size,color,position):
    font = pygame.font.SysFont(Font, size)  
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

class snakeStats:
    
    def __init__(self):
        self.score = 0
        self.timeout = 0
        
    def increase_score(self):
        self.score+=1
    def increase_timeout(self):
        self.timeout+=1
def getScore(statobj):
    return  statobj.score              
def getTimeout(statobj):
    return  statobj.timeout 

# pygame.quit()
# quit()
# input("Press Enter to continue...")
def playGame(genomes, config):
    nets = []
    genomeList = []
    mySnakeHeads = []
    myFruits = []
    stats = []
    Snake.totalSnakes = 0
    Fruits.totalFruits = 0
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome,config)
        nets.append(net)
        mySnakeHeads.append(Snake(display_width/2,display_height/2))
        myFruits.append(Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size)))
        genome.fitness = 0
        genomeList.append(genome)
        stats.append(snakeStats())

        
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    # gameExit = False
    gameLoop = True
    # mySnakeHead = Snake(display_width/2,display_height/2)
    # myFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))     
    
    while gameLoop:
        clock.tick(FPS)
        scores = [i.score for i in stats]
        [i.increase_timeout() for i in stats]
        
        gameDisplay.fill(white)
        displayonScreen(gameDisplay,"Score: "+ str(max(scores)),30,black,(display_width/2-50-len("Score"+ str(max(scores))),10))
        displayonScreen(gameDisplay,"Alive "+ str(len(mySnakeHeads)),30,black,(display_width/2-50-len("Alive :"+ str(len(mySnakeHeads))),40))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
            # Close the game any way you want, or troll users who want to close your game.
                print('\nBest genome:\n{!s}'.format(genomeList[0]))
                raise SystemExit
            # if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_LEFT:
            #             mySnakeHeads[0].changedir("left")        
            #         if event.key == pygame.K_RIGHT:
            #             mySnakeHeads[0].changedir("right") 
            #         if event.key == pygame.K_UP:
            #             mySnakeHeads[0].changedir("up") 
            #         if event.key == pygame.K_DOWN:
            #             mySnakeHeads[0].changedir("down")
            #         if event.key == pygame.K_c:
            #             gameLoop = True
        
        for x, mySnakeHead in enumerate(mySnakeHeads):
            currNet = nets[x]
            currGenomeList = genomeList[x]
            currMySnakeHeads = mySnakeHeads[x]
            currMyFruits = myFruits[x]
            currStats = stats[x]

            currMySnakeHeads.motion()
            
            genomeList[x].fitness += 0.01
            netInput =(currMyFruits.x-currMySnakeHeads.x,currMyFruits.y-currMySnakeHeads.y,currMySnakeHeads.x_vel,currMySnakeHeads.y_vel)
            output = currNet.activate(netInput)
            dirn = output.index(max(output))
            if dirn == 0 and output[dirn]>0.5:
                currMySnakeHeads.changedir("left")        
            elif dirn == 1 and output[dirn]>0.5:
                currMySnakeHeads.changedir("right") 
            elif dirn == 2 and output[dirn]>0.5:
                currMySnakeHeads.changedir("up") 
            elif dirn == 3 and output[dirn]>0.5:
                currMySnakeHeads.changedir("down")
            # if output[0]<0 and output[1]<0:
            #     currMySnakeHeads.changedir("left")        
            # elif output[0]<0 and output[1]>0:
            #     currMySnakeHeads.changedir("right") 
            # elif output[0]>0 and output[1]<0:
            #     currMySnakeHeads.changedir("up") 
            # elif output[0]>0 and output[1]>0:
            #     currMySnakeHeads.changedir("down")          
            
           
            currMyFruits.draw(gameDisplay)
            currMySnakeHeads.draw(gameDisplay)

            if currStats.timeout >= FPS*2:
                currGenomeList.fitness -= 2
                mySnakeHeads.remove(currMySnakeHeads)
                myFruits.remove(currMyFruits)
                genomeList.remove(currGenomeList)
                nets.remove(currNet)
                stats.remove(currStats)
            # elif currMySnakeHeads.selfCollide():
            #     genomeList[x].fitness -=  5
            #     myFruits.remove(currMyFruits)
            #     mySnakeHeads.remove(currMySnakeHeads)
            #     genomeList.remove(currGenomeList)
            #     nets.remove(currNet)
            #     stats.remove(currStats)

            elif checkCollition(currMySnakeHeads,currMyFruits): #Nom nom fruit
                fruit_id = currMyFruits.id
                myFruits.remove(currMyFruits)
                newFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))
                newFruit.id = fruit_id
                myFruits.insert(x,newFruit)
                currGenomeList.fitness += 20
                currMySnakeHeads.increase_length()
                currStats.timeout = 0
                currStats.score+=1
            elif  currMySnakeHeads.x > display_width - currMySnakeHeads.size or currMySnakeHeads.x < 0 or currMySnakeHeads.y > display_height - currMySnakeHeads.size or currMySnakeHeads.y<0: # Outside of game screen test
                currGenomeList.fitness -= 5
                myFruits.remove(currMyFruits)
                mySnakeHeads.remove(currMySnakeHeads)
                genomeList.remove(currGenomeList)
                nets.remove(currNet)
                stats.remove(currStats)
            
        # displayonScreen(gameDisplay,"Score: "+ str(max(scores)),30,black,(display_width/2-50-len("Score"+ str(max(scores))),10))
        # displayonScreen(gameDisplay,"Alive "+ str(len(mySnakeHeads)),30,black,(display_width/2-50-len("Alive :"+ str(len(mySnakeHeads))),40))
                         
        pygame.display.update()
        if len(mySnakeHeads) <= 0:
            gameLoop = False
          

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
    neat.DefaultSpeciesSet,neat.DefaultStagnation,
    config_path)
    
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(playGame,5000)     # Winner is genome object . Use pickle (import pickle) to save this winner genome. then unpickle and use wherever you want
    print('\nBest genome:\n{!s}'.format(winner))
    

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    run(config_path)