import pygame
import random
green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)

display_width = 900
display_height = 600
block_size = 20
fruit_block_size = 20
unit_velocity = 20
FPS = 5

pygame.init()
clock = pygame.time.Clock()
# pygame.display.set_caption("Snake Game")
# pygame.display.update()

class Snake:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.x_vel = 0
        self.y_vel = 0
        self.size = block_size
        self.rect = [self.x,self.y,self.size,self.size]
    def motion(self):
        self.x += self.x_vel
        self.y +=self.y_vel
        self.rect = [self.x,self.y,self.size,self.size]

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
        pygame.draw.rect(gameDisplay,green,self.rect)
    
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

def start():
    score = 0
    gameDisplay = pygame.display.set_mode((display_width,display_height))
    # gameExit = False
    gameLoop = True
    while True: # Ultra Game Loop
        
        mySnakeHead = Snake(200,200)
        snakeList = [mySnakeHead]
        myFruit =Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))     
        while gameLoop:
            clock.tick(FPS)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                # Close the game any way you want, or troll users who want to close your game.
                    raise SystemExit
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
            gameDisplay.fill(white)
            displayonScreen(gameDisplay,"Score"+ str(score),30,black,(display_width/2-50-len("Score"+ str(score)),10))
            myFruit.draw(gameDisplay)
            for eachSnake in snakeList:
                eachSnake.draw(gameDisplay)
            pygame.display.update()
            
            if checkCollition(mySnakeHead,myFruit):
                del myFruit
                myFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))
                score+=1
                snakeList.append(mySnakeHead)
                print("Yo ! I Collided")
            if mySnakeHead.x > display_width - mySnakeHead.size or mySnakeHead.x < 0 or mySnakeHead.y > display_height - mySnakeHead.size or mySnakeHead.y<0: # Outside of game screen test
                gameLoop = False
            
        gameDisplay.fill(white)
        displayonScreen(gameDisplay,"Game Over!",50,red,(display_width/2,display_height/2-30))
        displayonScreen(gameDisplay,"Press C to Continue or Press Q to Quit..",25,red,(display_width/2,display_height/2+40))
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
            


# pygame.quit()
# quit()


# input("Press Enter to continue...")
if __name__ == "__main__":
    start()