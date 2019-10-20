import pygame, sys
import math, time

idb = 0
pygame.init()

G = 6.673*(10**-9)
size = height, width = 1000,1000

screen = pygame.display.set_mode(size)

def add_vec(vec1,vec2):
    x = vec1[0]*math.cos(vec1[1]) + vec2[0]*math.cos(vec2[1])
    y = vec1[0]*math.sin(vec1[1]) + vec2[0]*math.sin(vec2[1])
    return math.hypot(x,y), math.atan2(y , x)

class Ball:
    def __init__(self,mass,x,y,force,angle,raduis,idb):
        self.mass = mass
        self.force = force
        self.x = x
        self.y = y
        self.angle = angle
        self.idb = idb
        self.raduis = raduis
        self.color = (255,0,0)
        self.trail = []
        for i in range(5):
            self.trail.append((int(self.x),int(self.y)))
        self.trail_time = time.time()


    def show(self):
        if time.time() - self.trail_time > 0.1:
            self.trail_time = time.time()
            self.trail.pop(0)
            self.trail.append((int(self.x),int(self.y)))
        for i in self.trail:
            pygame.draw.circle(screen,(231,246,15),i,1)
        pygame.draw.circle(screen,self.color,(int(self.x),int(self.y)),int(self.raduis))

    def move(self):
        if not (0 < self.x < width and 0 < self.y < height):
            for i in balls:
                if i.idb == self.idb:
                    balls.remove(i)
        for i in balls:
            if i.idb != self.idb:
                force = G*((self.mass*i.mass)/math.hypot(self.x-i.x,self.y-i.y)**2)
                x = self.x - i.x
                y = self.y - i.y
                theta = math.atan2(y,x) - (1/2)*math.pi
                self.force, self.angle = add_vec((self.force,self.angle),(force,theta))
        self.x += (math.sin(self.angle) * self.force)/(0.001*self.mass)
        self.y -= (math.cos(self.angle) * self.force)/(0.001*self.mass)

earth = Ball(10**7, height/2, width/2, 0, 0, 50, idb)
earth.color = (60,17,201)
balls = [earth]

last_pressed = time.time()
mouse_pressed = 0
while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    if time.time()-last_pressed > 0.2:
        if mouse_pressed == 0 and pygame.mouse.get_pressed()[0] == 1:
            last_pressed = time.time()
            mouse_pressed = 1
            mouse_pos1 = pygame.mouse.get_pos()
        elif mouse_pressed == 1 and pygame.mouse.get_pressed()[0] == 1:
            mouse_pos2 = pygame.mouse.get_pos()
            idb += 1
            mouse_pressed = 0
            last_pressed = time.time()
            x = mouse_pos1[0]-mouse_pos2[0]
            y = mouse_pos1[1]-mouse_pos2[1]
            speed = 0.03*math.hypot(x,y)
            angle = math.atan2(y,x) + (1/2)*math.pi
            balls.append(Ball(10**4,mouse_pos1[0],mouse_pos1[1],speed,angle,10,idb))

    screen.fill((0, 0, 0))
    if mouse_pressed == 1:
        # print(f"star: {mouse_pos1} end: {pygame.mouse.get_pos()}")
        pygame.draw.line(screen, (255, 0, 0), mouse_pos1, pygame.mouse.get_pos())

    for i in balls:
        i.move()
        i.show()
    pygame.display.flip()
    pygame.display.update()