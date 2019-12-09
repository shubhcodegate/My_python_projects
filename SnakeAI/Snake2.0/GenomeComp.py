import pygame
import random
import neat
import os
import pickle
green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
############# No Reference to body given ###########################
Font = "comicsansms"
toggle_selfcollition = True
display_width = 600
display_height = 600
block_size = 10
fruit_block_size = 10
unit_velocity = 10
FPS = 15

pygame.init()
clock = pygame.time.Clock()
# pygame.display.set_caption("Snake AI")


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
        self.body_direction = "left"
    def vision(self):
        least_left_x = self.x
        least_right_x = display_width - self.x - self.size
        least_up_y = self.y
        least_down_y = display_height - self.y - self.size
        for i,segment in enumerate(self.body):
            if segment[0] == self.x:
                if segment[1] - self.y - self.size  >= 0 and segment[1] - self.y - self.size  < least_down_y:
                    least_down_y = segment[1] - self.y - self.size 
                if self.y - segment[1] - self.size  >= 0 and self.y - segment[1] - self.size  < least_up_y:
                    least_up_y = self.y - segment[1] - self.size 
            if segment[1]==self.y: 
                if segment[0]-self.x - self.size >= 0 and segment[0] - self.x - self.size < least_right_x:
                    least_right_x = segment[0]-self.x -self.size    
                if self.x - segment[0] - self.size >= 0 and self.x - segment[0] - self.size < least_left_x:
                    least_left_x = self.x - segment[0] - self.size 
            
        return [least_left_x,least_right_x,least_up_y,least_down_y]

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
        collide = False
        for eachPart in self.body[:-1]:
            if eachPart[0]==self.x and eachPart[1]==self.y:
                collide =  True
        return collide

    def changedir(self,dirn):
        if self.body_direction == dirn and self.length>2:
            return
        elif dirn =="left":
            self.x_vel = -unit_velocity
            self.y_vel = 0
            self.body_direction = "right"
        elif dirn =="right":
            self.x_vel = unit_velocity
            self.y_vel = 0
            self.body_direction = "left"
        elif dirn =="up":
            self.x_vel = 0
            self.y_vel = -unit_velocity
            self.body_direction = "down"
        elif dirn =="down":
            self.x_vel = 0
            self.y_vel = unit_velocity
            self.body_direction = "up"

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
    stats = []
    Snake.totalSnakes = 0
    Fruits.totalFruits = 0
    

    Snake.totalSnakes = 0
    Fruits.totalFruits = 0
    score = 0
    
    # currNet = neat.nn.FeedForwardNetwork.create(genome,config)
    status = "No event"
        
    gameDisplay = pygame.display.set_mode((display_width,display_height)) #Commented for Fast
  
    gameLoop = True
    
    while True: # Ultra Game Loop
        score = 0
        Fruits.totalFruits = 0
        Snake.totalSnakes = 0
        for genome in genomes:
            net = neat.nn.FeedForwardNetwork.create(genome,config)
            nets.append(net)
            mySnakeHeads.append(Snake(random.randrange(0,display_width/2),
                                        random.randrange(0,display_height/2)))
            stats.append(snakeStats())
        currFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))     
        
        while gameLoop:
            gameDisplay.fill(white)
            clock.tick(FPS)
            scores = [i.score for i in stats]
            displayonScreen(gameDisplay,"Alive "+ str(len(mySnakeHeads)),30,black,(display_width/2-50-len("Alive :"+ str(len(mySnakeHeads))),40)) #Commented for Fast
            displayonScreen(gameDisplay,"Score:  "+ str(max(scores)),20,black,(display_width/2-50-len("Score"+ str(score)),10))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                # Close the game any way you want, or troll users who want to close your game.
                    raise SystemExit

            for x, mySnakeHead in enumerate(mySnakeHeads):
                currNet = nets[x]
                currMySnakeHead = mySnakeHeads[x]
                currStats = stats[x]    
                visionStats = currMySnakeHead.vision()
                netInput =(currFruit.x-currMySnakeHead.x,
                            currFruit.y-currMySnakeHead.y,
                            currMySnakeHead.x_vel,
                            currMySnakeHead.y_vel,
                            visionStats[0],
                            visionStats[1],
                            visionStats[2],
                            visionStats[3])
                output = currNet.activate(netInput)
                dirn = output.index(max(output))
                if dirn == 0 and output[dirn]>0.5:
                    currMySnakeHead.changedir("left")        
                elif dirn == 1 and output[dirn]>0.5:
                    currMySnakeHead.changedir("right") 
                elif dirn == 2 and output[dirn]>0.5:
                    currMySnakeHead.changedir("up") 
                elif dirn == 3 and output[dirn]>0.5:
                    currMySnakeHead.changedir("down") 

                # gameDisplay.fill(white)
                currFruit.draw(gameDisplay)
                currMySnakeHead.motion()
                currMySnakeHead.draw(gameDisplay)
                pygame.display.update()

                if currMySnakeHead.selfCollide() and toggle_selfcollition:
                    # gameLoop = False
                    status = "oops! AI Self Collided "
                    mySnakeHeads.remove(currMySnakeHead)
                    nets.remove(currNet)
                    stats.remove(currStats)
                elif checkCollition(currMySnakeHead,currFruit):
                    del currFruit
                    currFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))
                    currMySnakeHead.increase_length()
                    status = "nom nom fruit"
                    currStats.score+=1
                elif currMySnakeHead.x > display_width - currMySnakeHead.size or currMySnakeHead.x < 0 or currMySnakeHead.y > display_height - currMySnakeHead.size or currMySnakeHead.y<0: # Outside of game screen test
                    status = "oops! AI left the field"
                    mySnakeHeads.remove(currMySnakeHead)
                    nets.remove(currNet)
                    stats.remove(currStats)
            if (len(mySnakeHeads)<=0):
                gameLoop = False

        gameDisplay.fill(white)
        displayonScreen(gameDisplay,"Alive "+ str(len(mySnakeHeads)),30,black,(display_width/2-50-len("Alive :"+ str(len(mySnakeHeads))),40)) #Commented for Fast
        displayonScreen(gameDisplay,"Score:  "+ str(score),20,black,(display_width/2-50-len("Score"+ str(score)),10))
        currFruit.draw(gameDisplay)
        # currMySnakeHead.motion()
        currMySnakeHead.draw(gameDisplay)
        displayonScreen(gameDisplay,status,20,red,(display_width/2,display_height/2-30))
        displayonScreen(gameDisplay,"Press C to Continue or Press Q to Quit..",10,red,(display_width/2,display_height/2+40))
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
          

def run(genome,config_path):
    config = neat.config.Config(neat.DefaultGenome,neat.DefaultReproduction,
    neat.DefaultSpeciesSet,neat.DefaultStagnation,
    config_path)

    # p = neat.Population(config)
    # p.add_reporter(neat.StdOutReporter(True))
    # stats = neat.StatisticsReporter()
    # p.add_reporter(stats)
    playGame(genome,config)
    # winner = p.run(playGame,10000)     # Winner is genome object . Use pickle (import pickle) to save this winner genome. then unpickle and use wherever you want
    # print('\nBest genome:\n{!s}'.format(winner))
    # return winner

    

if __name__ == "__main__":
    genomes = []
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir,"config-feedforward.txt")
    genome_names = ["f1500p10000g500","f800p10000g100","myWinnerGenome100p10000","myWinnerGenome500p10000","myWinnerGenome500","myWinnerGenome10000p200"]
    for name in genome_names:
        mygenomefile = open(os.path.join(local_dir,"f1500p10000g500"),'rb')
        restore = pickle.load(mygenomefile)
        genomes.append(restore)  
    # print(restore)
    run(genomes,config_path)
    # myWinnerGenome = open(os.path.join(local_dir,"myWinnerGenome"),'xb')
    # pickle.dump(winner,myWinnerGenome)
    # myWinnerGenome.close()
