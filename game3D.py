import pygame
import pygame.locals as pylocals

import threading
import sys
import random
import time

from core.cube_3d import Cube3D
import numpy as np

import OpenGL.GL as gl
import OpenGL.GLU as glu

pygame.init()
window_name = '.'.join(sys.argv[0].split('.')[:-1])
pygame.display.set_caption(window_name if window_name != '' else 'pygame')
pygame.display.gl_set_attribute(pylocals.GL_MULTISAMPLEBUFFERS, 1)
pygame.display.gl_set_attribute(pylocals.GL_MULTISAMPLESAMPLES, 4)
SCREEN = pygame.display.set_mode((800, 600), pylocals.DOUBLEBUF|pylocals.OPENGL)
done = False
clock = pygame.time.Clock()
FRAME_RATE = 120

gl.glEnable(gl.GL_DEPTH_TEST)
gl.glClearColor(54 / 255.0, 54 / 255.0, 54 / 255.0, 0)

glu.gluPerspective(45, 4/3.0, 0.1, 12.0)

gl.glTranslatef(0.0, 0.0, -8.0)

#----------------------------------------------------------------------

faces = {}
side = ["top", "bottom", "left", "right", "front", "back"]
colors = [(1, 1, 1), (1, 1, 0), (0, 1, 0), (0, 0, 1), (1, 0, 0), (1, 0.647, 0)]
for i in range(6):
	faces[side[i]] = np.array([[colors[i] for j in range(3)] for k in range(3)])
cube = Cube3D(faces)
def draw():
	cube.render()

#----------------------------------------------------------------------
def movie():
	global done
	orientations = ["clockwise", "counterClockwise"]
	sides = ["right", "top", "left", "bottom", "front", "back"]
	while not done:
		buff = []
		for _ in range(20):
			buff.append((random.randrange(2), random.randrange(6)))
			cube.rotate3D(orientations[buff[_][0]], sides[buff[_][1]])
			time.sleep(0.3)
		for orientation, side in buff[::-1]:
			cube.rotate3D(orientations[1 - orientation], sides[side])
			time.sleep(0.3)

def terminal():
	global done
	buff = ""
	print("Commands to be in the format \"orientation, side\". \"exit\" to exit", end = '')
	while not done:
		print(buff)
		command = input("\n>>> ", end = '')

		if command == "exit":
			done = True
		elif command == "movie":
			movie()
		elif command == '':
			pass
		else:
			arguments = tuple(command.split(', '))
			buff = cube.rotate3D(*arguments)

try:
	thread = threading.Thread(target=terminal)
	thread.start()
except:
	print("Error: unable to start thread")

# gl.glRotatef(100, 300, 200, 0)

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True	
	gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)
	gl.glRotatef(1, 3, 1, 0)
	draw()
	pygame.display.flip()
	clock.tick(FRAME_RATE)
