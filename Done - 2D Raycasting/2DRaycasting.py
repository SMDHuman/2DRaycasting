from graphics import *
from random import randint
import time
from math import *
import keyboard

def clear_screen(win):
    for item in win.items[:]:
        item.undraw()

def mousePos():
    win1.bind('<Motion>', motion)
    return(pos)

pos = (0, 0)
def motion(event):
    global pos
    pos = (event.x, event.y)

class Wall():
	def __init__(self):
		self.posA = [randint(0, xwin1), randint(0, ywin1)]
		self.posB = [randint(0, xwin1), randint(0, ywin1)]

	def draw(self):
		l = Line(Point(self.posA[0], self.posA[1]), Point(self.posB[0], self.posB[1]))
		l.setFill("White")
		l.setWidth(3)
		l.draw(win1)

class Ray():
	def __init__(self, a):
		self.deg = a

	def cast(self, player, a):
		near = 100000000
		point = player.pos
		self.deg += a
		for wall in walls:
			x4, x3, x2, x1 = player.pos[0], player.pos[0] + cos(radians(self.deg)), wall.posA[0], wall.posB[0]
			y4, y3, y2, y1 = player.pos[1], player.pos[1] + sin(radians(self.deg)), wall.posA[1], wall.posB[1]

			den = (x1 - x2)*(y3 - y4) - (y1 - y2)*(x3 - x4)
			if(den != 0):
				t = ((x1 - x3)*(y3 - y4) - (y1 - y3)*(x3 - x4)) / den
				u = -((x2 - x1)*(y1 - y3) - (y2 - y1)*(x1 - x3)) / den

				if(t < 1 and t > 0 and u > 0):
					px = x1 + t*(x2 - x1)
					py = y1 + t*(y2 - y1)
					d = (player.pos[0] - px)**2 + (player.pos[1] - py)**2

					if(d < near):
						near = d
						point = [px, py]

		self.deg -= a
		l = Line(Point(player.pos[0], player.pos[1]), Point(point[0], point[1]))
		l.setFill("White")
		l.draw(win1)

		return(sqrt(near))

class Player():
	def __init__(self):
		self.pos = [xwin1 / 2, ywin1 / 2]
		self.ori = 0

	def update(self):
		d = self.pos[1] - cPos[1]
		if(d == 0): d = 0.01
		if(self.pos[1] - cPos[1] < 0):
			self.ori = -degrees(atan((self.pos[0] - cPos[0]) / d)) + 90 - fov / 2
		else:
			self.ori = -degrees(atan((self.pos[0] - cPos[0]) / d)) - 90 - fov / 2

		self.ori += fov / 2
		speed = 50
		if(keyboard.is_pressed("w")): 
			self.pos[0] += cos(radians(self.ori)) * dtime * speed
			self.pos[1] += sin(radians(self.ori)) * dtime * speed
		if(keyboard.is_pressed("s")): 
			self.pos[0] -= cos(radians(self.ori)) * dtime * speed
			self.pos[1] -= sin(radians(self.ori)) * dtime * speed
		if(keyboard.is_pressed("d")): 
			self.pos[0] += cos(radians(self.ori + 90)) * dtime * speed
			self.pos[1] += sin(radians(self.ori + 90)) * dtime * speed
		if(keyboard.is_pressed("a")): 
			self.pos[0] += cos(radians(self.ori - 90)) * dtime * speed
			self.pos[1] += sin(radians(self.ori - 90)) * dtime * speed
		self.ori -= fov / 2
		

	def draw(self):
		for i in range(rayNum):
			raysDist[i] = rays[i].cast(self, self.ori) * cos(radians( (fov / 2) - (i * fov / rayNum) ))

def drawCamera():
	clear_screen(win2)
	for i in range(rayNum):
		l = Line(Point(int(i * xwin2 / rayNum), (ywin2 - raysDist[i]) / 2), Point(int(i * xwin2 / rayNum), -(ywin2 - raysDist[i]) / 2))
		rgb = 255 - int(raysDist[i] * 0.7)
		if(rgb < 0): rgb = 0
		#rgb = 255
		l.setFill(color_rgb(rgb, rgb, rgb))
		l.setWidth(xwin2 / rayNum)
		l.draw(win2)
	win2.update()

win2 = GraphWin("Camera", 900, 600, autoflush = False)
win2.setBackground("Black")


win1 = GraphWin("Rays", 600, 600, autoflush = False)
win1.setBackground("Black")

xwin2 = int(win2.width)
ywin2 = int(win2.height)
xwin1 = int(win1.width)
ywin1 = int(win1.height)

win2.setCoords(0, -ywin2 / 2, xwin2, xwin2 / 2)
win1.setCoords(0, ywin1, xwin1, 0)

sPos = [0, 0]

border = 1
walls = []
wallNum = 5
for i in range(wallNum + 4 * border):
	walls.append(Wall()) 

wallNum += 4 * border
if(border):
	walls[0].posA = [0, 0]
	walls[0].posB = [0, ywin1]
	walls[1].posA = [0, ywin1]
	walls[1].posB = [xwin1, ywin1]
	walls[2].posA = [xwin1, ywin1]
	walls[2].posB = [xwin1, 0]
	walls[3].posA = [xwin1, 0]
	walls[3].posB = [0, 0]

rays = []
rayNum = 100
raysDist = [0] * rayNum
fov = 60
for i in range(rayNum):
	rays.append(Ray(i * fov / rayNum))

p1 = Player()

dtime = 0
while not(win1.checkMouse()):
	ctime = time.time()
	clear_screen(win1)
	for i in range(wallNum):
		walls[i].draw()

	cPos = mousePos()
	if(sPos[0] > xwin1): cPos[0] = xwin1
	if(sPos[1] > ywin1): cPos[1] = ywin1
	if(sPos[0] < 0): cPos[0] = 1
	if(sPos[1] < 0): cPos[1] = 1

	p1.update()
	p1.draw()

	drawCamera()
	
	win1.update()

	dtime = time.time() - ctime
