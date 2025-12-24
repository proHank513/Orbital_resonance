from vpython import*
import math
import random
import matplotlib.pyplot as plt
import statistics as stat

class obj:pass

class CAstroid:
        def __init__(self,m,size,r,v0,array):
                self.m=m
                self.size=size
                self.r=r
                self.v0=v0
                self.array=array

astroid=CAstroid(524,8E5,100E6,0,[])

G=6.6743E-11 #重力常數 #grav. constant

planet_m,moon_m = 5.6846E26,3.7493E19 #mass of saturn and mimas
planet_size,moon_size = 60268000,198200*10
moon_r = 185539000
ring_n=20
n=5000
dt=100
#t
t = 0

def Gravity(p1,p2):
        "定義重力施加在2上"
        #p1.a+=(-G*p2.m/(p1.pos-p2.pos).mag2 * (p1.pos-p2.pos).norm()) 
        
        p2.a+=(-G*p1.m/(p2.pos-p1.pos).mag2 * (p2.pos-p1.pos).norm()) #.mag2 means length sqr, norm(x) means unit vector

"""
scene=canvas(title="orbital resonance",width=750,height=750,
             center=vec(0,0,0),background=color.black)
planet=sphere(pos=vec(0,0,0),radius=planet_size,m=planet_m,
           color=vec(1,0.9,0),v=vec(0,0,0),a=vec(0,0,0),visible=True)
moon=sphere(pos=vec(moon_r,0,0),radius=moon_size,m=moon_m,
          color=vec(0,0,1),v=vec(0,sqrt(G*planet_m/moon_r),0),a=vec(0,0,0),visible=True)
"""

planet=obj()
moon=obj()

planet.pos, planet.m, planet.v, planet.a = vec(0,0,0), planet_m, vec(0,0,0), vec(0,0,0)
moon.pos, moon.m, moon.v, moon.a = vec(moon_r,0,0), moon_m, vec(0,sqrt(G*planet_m/moon_r),0), vec(0,0,0)


"""
def collision(p1,p2):
        if (p1.pos-p2.pos).mag<=astroid.size*2:
                """
u=0
for i in range(n):
        theta=random.random()*2*math.pi
        astroid.r=(random.random()*(140180000-92000000)) + 92E6 #b ring to f ring
        posx=astroid.r*math.cos(theta)
        posy=astroid.r*math.sin(theta)

        p=obj()
        p.pos, p.m, p.v, p.a = vec(posx,posy,0), astroid.m, vec(-sqrt(G*planet_m/astroid.r)*sin(theta),sqrt(G*planet_m/astroid.r)*cos(theta),0), vec(0,0,0)
        
        astroid.array.append(p)
"""
for i in range(ring_n):
    astroid.r=astroid.r+25E4*i
    for j in range(n*i):
        u+=1
        
        theta=j*2*math.pi/(n*i)
        posx=astroid.r*math.cos(theta)
        posy=astroid.r*math.sin(theta)
        p=sphere(pos=vec(posx,posy,0),radius=astroid.size,m=astroid.m,color=color.yellow
                 ,v=vec(-sqrt(G*sun_m/astroid.r)*sin(theta),sqrt(G*sun_m/astroid.r)*cos(theta),0),a=vec(0,0,0),visible=True)
        astroid.array.append(p)
"""
print(u)


#初始半徑分布
radii=[]
count=0
for i in range(n):
        radii.append(astroid.array[i].pos.mag)

                
plt.hist(radii,bins=50)
plt.xlabel('Distance(m)')
plt.ylabel('Density')
plt.title('Radii distribution')
plt.savefig('t='+ str(int(count*1E4)) +'.png')

print('moon orbital radius at t= ',count*1000,'=', moon.pos.mag)


count = 1 #等時間紀錄參數


while t < 500E4+100:
        rate(1000)
        #planet force
        Gravity(planet,moon)
        Gravity(moon,planet)
        for i in range(n):
                Gravity(planet,astroid.array[i])
                Gravity(astroid.array[i],planet)
                
        #moon force
        for i in range(n):
                Gravity(moon,astroid.array[i])
                Gravity(astroid.array[i],moon)
                
              
        #astroid force
        for i in range(n):
                for j in range(i+1,n):
                        u= astroid.array[i].pos-astroid.array[j].pos
                        if u.mag < 1E7:
                                Gravity(astroid.array[j],astroid.array[i])
                                
        
        #moon dt
        moon.v+=moon.a*dt
        moon.pos+=moon.v*dt
        moon.a=vec(0,0,0)  #a reset
        #astroid dt
        for i in range(n):
                astroid.array[i].v+=astroid.array[i].a*dt
                astroid.array[i].pos+=astroid.array[i].v*dt
                astroid.array[i].a=vec(0,0,0)  #a reset


        if t == count*1E3:

                radii=[]
                for i in range(n):
                        radii.append(astroid.array[i].pos.mag)

                plt.clf() #clear recent fig
                plt.hist(radii,bins=50)
                plt.xlabel('Distance(m)')
                plt.ylabel('Density')
                plt.title('Radii distribution')
                plt.savefig('t='+ str(int(count*1E3)) +'.png')

                print('moon orbital radius at t= ',count*1000,'=', moon.pos.mag)

                
                
                count += 1
                
        
        t += dt
        


print('moon orbital radius = ', moon.pos.mag)


#110E6~263E6每1E6公尺一個區間共153區間 bin size is 1e6m there will be 153 bins


