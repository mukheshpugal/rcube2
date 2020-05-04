#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 23:55:09 2020

@author: srivenkat
"""
from core.cube3D_class import cubeProjection
from core.wireframe import Wireframe
from core.cube_feature import featureExtract
import numpy as np 
import cv2

colors = [(255, 255, 255), (255,255,0), (0,255,0), (0,0,255), (255,0,0), (255,128,0), (0, 0, 0)]

face0 = cv2.imread("images/solved/image1.jpeg")
face1 = cv2.imread("images/solved/image2.jpeg")
face2 = cv2.imread("images/solved/image3.jpeg")
face3 = cv2.imread("images/solved/image4.jpeg")
face4 = cv2.imread("images/solved/image5.jpeg")
face5 = cv2.imread("images/solved/image6.jpeg")

cube_ext = featureExtract([face0,face1,face2,face3,face4,face5])
faces = cube_ext.face

#faces = [i*np.ones((3,3)) for i in range(6)]

cube_nodes = [(x,y,z) for x in range(-3,4,2) for y in range(-3,4,2) for z in range(-3,4,2)]

cube = Wireframe()
cube.initNodeList(cube_nodes)
cube.initFaces(faces)

cp = cubeProjection(1000,1000)
cp.addWireframe('cube',cube)
cp.run()
