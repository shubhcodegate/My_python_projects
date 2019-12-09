import pygame
import random
green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
Font = "comicsansms"

display_width = 600
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
        self.length = 10
        self.body = [self.rect]
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
        score = 0
        mySnakeHead = Snake(200,200)
        # snakeList = [mySnakeHead]
        myFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))     
        while gameLoop:
            clock.tick(FPS)
            print(mySnakeHead.vision())
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
            displayonScreen(gameDisplay,"Score:  "+ str(score),30,black,(display_width/2-50-len("Score"+ str(score)),10))
            myFruit.draw(gameDisplay)
            mySnakeHead.motion()
            mySnakeHead.draw(gameDisplay)
            pygame.display.update()
            mySnakeHead.selfCollide()
            if mySnakeHead.selfCollide():
                gameLoop = False
            if checkCollition(mySnakeHead,myFruit):
                del myFruit
                myFruit = Fruits(random.randint(0,display_width-fruit_block_size),random.randint(0,display_height-fruit_block_size))
                score+=1
                mySnakeHead.increase_length()
                # print("Yo ! I Collided")
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