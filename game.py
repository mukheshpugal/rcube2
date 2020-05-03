import pygame
import threading
import sys
from core.cube_class import Cube
import numpy as np

pygame.init()
window_name = '.'.join(sys.argv[0].split('.')[:-1])
pygame.display.set_caption(window_name if window_name != '' else 'pygame')
SCREEN = pygame.display.set_mode((600, 400))
done = False
clock = pygame.time.Clock()
FRAME_RATE = 60
FILL_CURRENT = (255, 255, 255)

def background(a):
	if not isinstance(a, tuple):
		a = (a, a, a)
	SCREEN.fill(a)

def fill(a, b = None, c = None):
	global FILL_CURRENT
	if b is None:
		FILL_CURRENT = (a, a, a)
	else:
		FILL_CURRENT = (a, b, c)

def rect(a, b, c, d):
	pygame.draw.rect(SCREEN, FILL_CURRENT, pygame.Rect((a, b), (c, d)))
#----------------------------------------------------------------------

faces = {}
sides = ("top", "bottom", "front", "back", "right", "left")
for i in range(6):
	faces[sides[i]] = i * np.ones((3, 3))
cube = Cube(faces)
colors = [(255, 255, 255), (255,255,0), (0,255,0), (0,0,255), (255,0,0), (255,128,0), (255, 255, 255)]

def draw():
	background(0)
	fill(255, 0, 0)
	i = 0
	for row in cube.getFace("front"):
		j = 0
		for color in row:
			fill(*colors[int(color)])
			rect(150 + i * 33, 150 + j * 33, 33, 33)
			j += 1
		i += 1
	i = 0
	for row in cube.getFace("top"):
		j = 0
		for color in row:
			fill(*colors[int(color)])
			rect(150 + i * 33, 50 + j * 33, 33, 33)
			j += 1
		i += 1
	i = 0
	for row in cube.getFace("bottom"):
		j = 0
		for color in row:
			fill(*colors[int(color)])
			rect(150 + i * 33, 250 + j * 33, 33, 33)
			j += 1
		i += 1
	i = 0
	for row in cube.getFace("left"):
		j = 0
		for color in row:
			fill(*colors[int(color)])
			rect(50 + i * 33, 150 + j * 33, 33, 33)
			j += 1
		i += 1
	i = 0
	for row in cube.getFace("right"):
		j = 0
		for color in row:
			fill(*colors[int(color)])
			rect(250 + i * 33, 150 + j * 33, 33, 33)
			j += 1
		i += 1
	i = 0
	for row in cube.getFace("back"):
		j = 0
		for color in row:
			fill(*colors[int(color)])
			rect(350 + i * 33, 150 + j * 33, 33, 33)
			j += 1
		i += 1

#----------------------------------------------------------------------
def process():
	global done
	while not done:
		draw()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True
		pygame.display.flip()
		clock.tick(FRAME_RATE)

try:
   threading.Thread(target=process).start()
except:
   print("Error: unable to start thread")