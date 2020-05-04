#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:55:09 2020

@author: srivenkat
"""
from core.cube3D_class import cubeProjection
from core.wireframe import Wireframe
import numpy as np

colors = [(255, 255, 255), (255,255,0), (0,255,0), (0,0,255), (255,0,0), (255,128,0), (0, 0, 0)]
faces = []
for i in range(6):
	side = np.loadtxt("temp/side{}.txt".format(i))
	faces.append(np.uint8(side))

new_faces = [None,None,None,None,None,None]
for i in range(len(faces)):
    j = faces[i][1][1]
    new_faces[j] = faces[i]

cube_nodes = [(x,y,z) for x in range(-3,4,2) for y in range(-3,4,2) for z in range(-3,4,2)]

cube = Wireframe()
cube.initNodeList(cube_nodes)
cube.initFaces(new_faces)

cp = cubeProjection(1000,1000)
cp.addWireframe('cube',cube)
cp.run()
