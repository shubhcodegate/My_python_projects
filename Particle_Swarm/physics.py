import random
import math
from multiprocessing import Pool
from multiprocessing.pool import ThreadPool

green = (0,155,0)
red = (255,0,0)
white = (255,255,255)
black = (0,0,0)
tomato = (255,99,71)

VISCOSITY = 0.05

class Vector2D:
    """ 
    This is a 2D vector with vector maths
    :param values: vector is [x-cordinate,y-cordinate] defaults to [0,0]
    :type values: list or tuple
    """
    def __init__(self,values=[0,0]):
        if type(values) is list:
            self.values = values
        elif type(values) is tuple:
            self.values = [values[0],values[1]]
    
    def __str__(self):
        return "Vector2D:({x}i, {y}j)".format(x=self.values[0], y=self.values[1])
    # For setting the value
    def __setitem__(self, index, value):
        self.values[index] = value

    # For getting the value from our custom_list
    def __getitem__(self, index):
        return self.values[index]
    
    def __add__(self,other):
        return Vector2D([i+j for i,j in zip(self.values,other.values)])
    def __sub__(self,other):
        if type(other) is list:
                return Vector2D([i-j for i,j in zip(self.values,other)])
        else:
            return Vector2D([i-j for i,j in zip(self.values,other.values)])
    def __eq__(self,other):
        return self.values == other.values
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
class Particle:
    """
    This a Physics Particle which follows physics.
    @param position
    @param mass
    @param radius
    @param velocity default [0,0]
    @param accel default [0,0]
    """
    particleCount = 0
    def __init__(self,position,mass,radius,velocity=[0,0],accel=[0,0]):
        Particle.particleCount+=1
        self.objtype = "Particle"
        self.position = Vector2D(position)
        self.velocity = Vector2D(velocity)
        self.accel = Vector2D(accel)
        self.mass = mass
        self.size = radius
        self.boundaryflag = False
        self.box = [[float('-inf'),float('-inf'),float('inf'),float('inf')]]

    def move(self):
        self.velocity += self.accel 
        self.position += self.velocity
        self.velocity*=(1-VISCOSITY)
        
        if self.boundaryflag:
            self.boundaryCondition()
        
    def enableBoundary(self,box):
        # Boundary Toggle default False
        #@param box [x_start,y_start,x_end,y_end]
        self.box = box
        self.boundaryflag = not self.boundaryflag
    def boundaryCondition(self):
        if self.position.values[0]>= self.box[2]-self.size:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = self.box[2]-self.size
        if self.position.values[0]<=self.box[0] + self.size:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] =self.box[0] + self.size
        if self.position.values[1]>=self.box[3]-self.size:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1] =self.box[3]-self.size
        if self.position.values[1]<=self.box[1] + self.size:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1] =self.box[1] + self.size
    def applyForce(self,force):
        # Force to be applied on Particle
        #@param force = physics.Vector2D()
        self.accel += force/self.mass
class BoxParticle(Particle):
    # Box Particle with 
    # @param dimension=[xlength,ylength]
    def __init__(self,position,mass,dimension=[50,50],velocity=[0,0],accel=[0,0]):
        super().__init__(position,mass,dimension,velocity,accel)
        self.objtype = "BoxParticle"

    def boundaryCondition(self):
        if self.position.values[0]>= self.box[2]-self.size[0]:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = self.box[2]-self.size[0]

        if self.position.values[0]<= self.box[0]:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = self.box[0]

        if self.position.values[1]>= self.box[3]-self.size[1]:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1] = self.box[3]-self.size[1]

        if self.position.values[1]<= self.box[1]:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1] = self.box[1]

    def meshify(self,interval=10):
        self.mesh = []
        x = [self.position.getx(),self.position.getx()+self.size[0]]
        y = [self.position.gety(),self.position.gety()+self.size[1]]
        for i in range(int(x[0]),int(x[1]),interval):
            for j in y:
                self.mesh.append([i,j])
        for i in range(int(y[0]),int(y[1]),interval):
            for j in x:
                self.mesh.append([j,i])
        return self.mesh
def collition(obj1,obj2):
    if (obj1.position-obj2.position).magnitude()<= obj1.size+obj2.size:
        # ------Collided---
        x1_x2 = obj1.position-obj2.position
        v1_v2 = obj1.velocity-obj2.velocity
        obj1.velocity -= x1_x2*((v1_v2).dot(x1_x2)/x1_x2.magnitude()**2)*((2*obj2.mass)/(obj1.mass+obj2.mass))
        obj2.velocity -= (-x1_x2)*((-v1_v2).dot(-x1_x2)/x1_x2.magnitude()**2)*((2*obj1.mass)/(obj1.mass+obj2.mass))
def perfectCollition(obj1,obj2,elastisity=0.3):
    """
    This is a custom implimentation of physics collider 
    @param obj1 physics particle
    @param obj2 physics particle
    @param elastisity defaults to 1
    """
    if obj1.objtype is "Particle" and obj2.objtype is "Particle":
        if obj1.position == obj2.position:
            randPos = Vector2D([random.randint(2,10),random.randint(2,10)])
            obj1.position = obj2.position + randPos
        elif (obj1.position-obj2.position).magnitude()<= obj1.size+obj2.size:
        # ------Collided---
            x1_x2 = obj1.position-obj2.position
            modx1_x2 = x1_x2.magnitude()
            v1_v2 = obj1.velocity-obj2.velocity
            obj1.velocity -= x1_x2*((v1_v2).dot(x1_x2)/modx1_x2**2)*((2*obj2.mass)/(obj1.mass+obj2.mass)) * elastisity
            obj2.velocity -= (-x1_x2)*((-v1_v2).dot(-x1_x2)/modx1_x2**2)*((2*obj1.mass)/(obj1.mass+obj2.mass)) * elastisity
            obj1.position,obj2.position = obj2.position + (x1_x2/modx1_x2)*(obj1.size+obj2.size)  ,obj1.position - (x1_x2/modx1_x2)*(obj1.size+obj2.size) 
    
    elif obj1.objtype is "Particle" and obj2.objtype is "BoxParticle" or obj2.objtype is "Particle" and obj1.objtype is "BoxParticle":
        if obj2.objtype is "Particle" and obj1.objtype is "BoxParticle":
            obj1,obj2 = obj2,obj1   
        meshes = obj2.meshify(obj1.size)
        for mesh in meshes:
            if (obj1.position-mesh).magnitude()<= obj1.size:
                #collided
                print("Box Collided !")
                x1_x2 = obj1.position-mesh
                modx1_x2 = x1_x2.magnitude()
                v1_v2 = obj1.velocity-obj2.velocity
                obj1.velocity -= x1_x2*((v1_v2).dot(x1_x2)/modx1_x2**2)*((2*obj2.mass)/(obj1.mass+obj2.mass)) * elastisity
                obj2.velocity -= (-x1_x2)*((-v1_v2).dot(-x1_x2)/modx1_x2**2)*((2*obj1.mass)/(obj1.mass+obj2.mass)) * elastisity
                obj1.position,obj2.position = obj2.position + (x1_x2/modx1_x2)*(obj1.size)  ,obj1.position - (x1_x2/modx1_x2)*(obj1.size) 
                break

def relativeDistance(vector1,vector2):
    """
    Find relative distance magnitude between two Vector2D
    @param vector1 Vector2D
    @param vector2 Vector2D
    """
    result = (vector1-vector2).magnitude()
    return result
def checkBoxCollition(item1,item2):
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
class SwarmParticle(Particle):
    def __init__(self,swarm,position,mass,radius,velocity=[0,0],accel=[0,0],w=0.8,c1=0.001,c2=0.05):
        Particle.__init__(self,position,mass,radius,velocity,accel)  
        self.w = w    #Self Momentum default was 0.8
        self.c1 = c1    #Social Parameter default was 0.4
        self.c2 = c2     #Cognitive Parameter default was 0.1
        self.myswarm = swarm
        self.pbest = self.position
        self.boundaryflag = False
        self.box = [float('-inf'),float('-inf'),float('inf'),float('inf')]
    def avoidEnemy(self):
        for hunter in self.myswarm.hunters:
            relative = self.position-hunter.position
            modRelative = relative.magnitude()
            Force = (relative/modRelative)*sigmoid(modRelative)*1000
            self.applyForce(Force)

    def move(self):
        self.accel = ( (self.pbest-self.position) * self.c1 + (self.myswarm.gbest - self.position) * self.c2)/((1-self.w)*self.mass )
        self.avoidEnemy()
        super().move()
        if type(self.myswarm.target) is Vector2D:
            if relativeDistance(self.pbest,self.myswarm.target) > relativeDistance(self.position,self.myswarm.target):
                self.pbest = self.position
        elif self.myswarm.target.objtype in ("Particle","BoxParticle"):
            if relativeDistance(self.pbest,self.myswarm.target.position) > relativeDistance(self.position,self.myswarm.target.position):
                self.pbest = self.position
        if self.boundaryflag:
            self.boundaryCondition()
        
    # def enableBoundary(self,box):
    #     self.box = box
    #     self.boundaryflag = not self.boundaryflag
    # def boundaryCondition(self):
    #     if self.position.values[0]>= self.box[2]-self.size:
    #         self.velocity.values[0] = -self.velocity.values[0]
    #     if self.position.values[0]<=self.box[0] + self.size:
    #         self.velocity.values[0] = -self.velocity.values[0]
    #     if self.position.values[1]>=self.box[3]-self.size:
    #         self.velocity.values[1] = -self.velocity.values[1]
    #     if self.position.values[1]<=self.box[1] + self.size:
    #         self.velocity.values[1] = -self.velocity.values[1]
    def explore(self):
        randForce = Vector2D([random.randint(10,150),random.randint(10,150)])
        self.applyForce(randForce)

class Swarm():
    """
    This is a swarm of particles with a target 
    @param n number of particles in this swarm
    @param target to optimize the distance
    @param collection  the particle list
    @param hunters HunterParticle
    """
    def __init__(self,n,target,collection=[],hunters = []):
        self.objtype = "Swarm"
        self.n = n
        self.gbest = Vector2D([0,0])
        self.collection = collection
        self.hunters = hunters
        self.target = target
        self.boundaryflag = False
        self.box = [float('-inf'),float('-inf'),float('inf'),float('inf')]
    def addHunters(self,hunters):
        self.hunters = hunters
    def addTarget(self,target):
        self.target = target
    def addCollection(self,collection):
        self.collection=collection
    def move(self):
        for i in self.collection:
            i.move()
            if type(self.target) is Vector2D:
                if relativeDistance(i.pbest,self.target) < relativeDistance(self.gbest,self.target):
                    self.gbest = i.pbest
            elif self.target.objtype in ("Particle","BoxParticle"):
                if relativeDistance(i.pbest,self.target.position) < relativeDistance(self.gbest,self.target.position):
                    self.gbest = i.pbest
            
    def enableBoundary(self,box = [float('-inf'),float('-inf'),float('inf'),float('inf')]):
        self.box = box
        for i in self.collection:
            i.enableBoundary(self.box)
    def explore(self):
        for i in range(10):
            random.choice(self.collection).explore()
class TargetParticle(Particle):
    def __init__(self,position,mass,radius,velocity=[0,0],accel=[0,0]):
        Particle.__init__(self,position,mass,radius,velocity,accel)  
        self.boundaryflag = False
        self.box = [float('-inf'),float('-inf'),float('inf'),float('inf')]
    def move(self):
        super().move()
        if self.boundaryflag:
            self.boundaryCondition()
    def enableBoundary(self,box):
        self.box = box
        self.boundaryflag = not self.boundaryflag
    def boundaryCondition(self):
        if self.position.values[0]>= self.box[2]-self.size:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = self.box[2]-self.size
        if self.position.values[0]<= self.box[0] + self.size:
            self.velocity.values[0] = -self.velocity.values[0]
            self.position.values[0] = self.box[0] + self.size
        if self.position.values[1]>= self.box[3]-self.size:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1] = self.box[3]-self.size
        if self.position.values[1]<= self.box[1] + self.size:
            self.velocity.values[1] = -self.velocity.values[1]
            self.position.values[1] = self.box[1] + self.size

class HunterParticle(Particle):
    def __init__(self,position,mass,radius,target=[],velocity=[0,0],accel=[0,0]):
        Particle.__init__(self,position,mass,radius,velocity,accel)
        self.target = target
    def addTarget(self,target):
        self.target = target
    def move(self):
        relative = self.target.position-self.position
        modRelative = relative.magnitude()
        Force = (relative/modRelative)*attacksigmoid(modRelative)*10
        self.applyForce(Force)
        super().move()
def sigmoid(x):
  return 1 / (1 + math.exp(0.2*x-10)) 
def attacksigmoid(x):
  return 1 / (1 + math.exp(-0.05*x+10))  

def createSwarm(n,target,particle_size=5,particle_mass=2):
    newSwarm = Swarm(n,target)
    collection = []
    for i in range(n):
        randPos = [random.randint(0,400),random.randint(0,400)]
        collection.append(SwarmParticle(newSwarm,randPos,particle_size,particle_mass))
    newSwarm.addCollection(collection)
    return newSwarm

def singleScene(myscene):
    for obj1,obj2 in myscene:
        perfectCollition(obj1,obj2,0.3) 


def multiScene(myscene):
    pool = ThreadPool(20)
    for obj1,obj2 in myscene:
        pool.apply_async(perfectCollition,(obj1,obj2,0.3))
    pool.close()
    pool.join()
