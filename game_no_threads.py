import pygame
import sys
from core.cube_class import Cube
import numpy as np

pygame.init()
window_name = '.'.join(sys.argv[0].split('.')[:-1])
pygame.display.set_caption(window_name if window_name != '' else 'pygame')
SCREEN = pygame.display.set_mode((600, 500))
done = False
clock = pygame.time.Clock()
FRAME_RATE = 60
FILL_CURRENT = (255, 255, 255)
FONT = pygame.font.Font('fonts/Consola.ttf', 22)

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
sides = {"top" : [150, 50], "bottom" : [150, 250], "front" : [150, 150], "back" : [350, 150], "right" : [250, 150], "left" : [50, 150]}
for i in range(6):
	faces[list(sides.keys())[i]] = i * np.ones((3, 3))
cube = Cube(faces)
colors = [(255, 255, 255), (255,255,0), (0,255,0), (0,0,255), (255,0,0), (255,128,0), (0, 0, 0)]

def draw():
	background(0)

	for side in list(sides.keys()):
		i = 0
		face = cube.getFace(side)
		if side == "top":
			face = np.rot90(face, 2)
		if side == "bottom":
			face = face[::-1]
		if side == "front":
			face = np.rot90(face, 1)
			face = face[:, ::-1]
		if side == "back":
			face = np.rot90(face, -1)
		if side == "right":
			face = np.rot90(face, -1)
		if side == "left":
			face = np.rot90(face, 1)
			face = face[:, ::-1]

		for row in face:
			j = 0
			for color in row:
				fill(*colors[int(color)])
				rect(sides[side][0] + i * 33, sides[side][1] + j * 33, 33, 33)
				j += 1
			i += 1

#----------------------------------------------------------------------
def interpreter(command):

	global done

	if command == "exit":
		done = True
	else:
		arguments = tuple(command.split(', '))
		try:
			buff = cube.rotate(*arguments)
		except:
			print("Invalid command")

buff = '>>> '

while not done:
	draw()
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.KEYDOWN:
			key = pygame.key.name(event.key)
			if key == 'return':
				interpreter(buff[4:])
				buff = '>>> '
			elif key == 'backspace':
				if len(buff) > 4:
					buff = buff[:-1]
			elif key == 'space':
				buff += ' '
			elif len(key) == 1:
				if event.mod and (pygame.KMOD_LSHIFT or pygame.KMOD_RSHIFT):
					buff += key.upper()
				else: buff += key

	text = FONT.render(buff, True, (255, 255, 255))
	SCREEN.blit(text, (10, 400))

	pygame.display.flip()
	clock.tick(FRAME_RATE)
