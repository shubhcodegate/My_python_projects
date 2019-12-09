import random
import math

class Vector2D:
    def __init__(self,values=[0,0],randomGen=False,minMag = 0 ,maxMag=10):
        if randomGen:
            self.values = [random.randint(minMag,maxMag),random.randint(minMag,maxMag)]
        elif type(values) is list:
            self.values = values
    def __add__(self,other):
        return Vector2D([i+j for i,j in zip(self.values,other.values)])
    def __sub__(self,other):
        if type(other) is list:
                return Vector2D([i-j for i,j in zip(self.values,other)])
        else:
            return Vector2D([i-j for i,j in zip(self.values,other.values)])
    def __lt__(self, other):
        return self.magnitude()<other.magnitude()
    def __gt__(self,other):
        return self.magnitude()>other.magnitude()
    def __le__(self, other):
        return self.magnitude()<=other.magnitude()
    def __ge__(self,other):
        return self.magnitude()>= other.magnitude()
    def __mul__(self, other):
        if type(other) in (int, float):
            return Vector2D([i * other for i in self.values])
    def __truediv__(self,other):
        if type(other) in (int, float):
            return Vector2D([i/other for i in self.values])
    def __neg__(self):
        return Vector2D([-i for i in self.values])
    def dot(self,other):
        return sum([i*j for i,j in zip(self.values,other.values)])
    def getx(self):
        return self.values[0]
    def gety(self):
        return self.values[1]   
    def magnitude(self)-> float:
        return math.sqrt(sum([i**2 for i in self.values]))
    def relativeDist(self,other):
        self

def relativeDistance(vector1,vector2):
    result = (vector1-vector2).magnitude()
    return result
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

if __name__ == "__main__":
    x ,y = Vector2D(randomGen=True), Vector2D(randomGen=True)
    print(relativeDistance(x,y))