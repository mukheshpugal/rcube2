#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 18:40:28 2020

@author: srivenkat
"""
from .wireframe import Wireframe
import pygame
import numpy as np
from operator import itemgetter
pygame.init()

colors = [(255, 255, 255), (255,255,0), (0,255,0), (0,0,255), (255,0,0), (255,128,0), (0, 0, 0)]

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.transformall(x.rotateXMatrix(15))),
    pygame.K_RIGHT:  (lambda x: x.transformall(x.rotateXMatrix(-15))),
    pygame.K_DOWN:   (lambda x: x.transformall(x.rotateYMatrix(15))),
    pygame.K_UP:     (lambda x: x.transformall(x.rotateYMatrix(-15))),
    pygame.K_EQUALS: (lambda x: x.transformall(x.rotateZMatrix(15))),
    pygame.K_MINUS:  (lambda x: x.transformall(x.rotateZMatrix(-15)))}

class cubeProjection:
#Displays 3D objects on a Pygame screen
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption('Wireframe Display')
        self.background = (10,10,50)
        self.wireframes = {}
        self.displayNodes = True
        self.displayEdges = False
        self.displayColors = True
        self.nodeColour = (255,255,255)
        self.edgeColour = (200,200,200)
        self.nodeRadius = 4
        
    def addWireframe(self,name,frame):
        self.wireframes[name] = frame

    def rotateXMatrix(self,deg):
    # Return matrix for rotating about the x-axis by 'radians' radians
        radians = deg*3.14/180
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[1, 0, 0],
                         [0, c,-s],
                         [0, s, c]])
                         
    def rotateYMatrix(self,deg):
    # Return matrix for rotating about the y-axis by 'radians' radians """        
        radians = deg*3.14/180       
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[ c, 0, s],
                         [ 0, 1, 0],
                         [-s, 0, c]])

    def rotateZMatrix(self,deg):
    # Return matrix for rotating about the z-axis by 'radians' radians """        
        radians = deg*3.14/180      
        c = np.cos(radians)
        s = np.sin(radians)
        return np.array([[c,-s, 0],
                         [s, c, 0],
                         [0, 0, 1]])

    def scaleMatrix(self,sx=0, sy=0, sz=0):
    # Return matrix for scaling equally along all axes centred on the point (cx,cy,cz). """        
        return np.array([[sx, 0,  0],
                         [0,  sy, 0],
                         [0,  0,  sz]])

    def project(self,points):
        new = []
        for pt in points:
            factor = 500 / (15 + pt[2])
            x = (pt[0])*factor + self.width/2
            y = -(pt[1])*factor + self.height/2
            new.append([x,y,pt[2]])
        return new

    def display(self):
        """ Draw the wireframes on the screen. """
        self.screen.fill(self.background)
        for wireframe in self.wireframes.values():
            if self.displayEdges:
                for n1,n2 in wireframe.edges:
                    pygame.draw.aaline(self.screen, self.edgeColour, wireframe.nodes[n1][:2], wireframe.nodes[n2][:2], 1)
            if self.displayNodes:
                for node in wireframe.nodes:
                    pygame.draw.circle(self.screen, self.nodeColour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
            if self.displayColors:
                avg_z = []
                #i = 0
                for i in range(len(wireframe.surfaces)):
                    item = wireframe.surfaces[i]
                    mean = (item[0][2] +item[1][2] +item[2][2] +item[3][2])/4.0
                    avg_z.append((mean,i))
                for temp in sorted(avg_z,key=itemgetter(1),reverse=True):
                    surf = wireframe.surfaces[int(temp[1])]
                    surf[:4] = self.project(surf[:4])
                    bound = [tuple(surf[0])[:2],tuple(surf[1])[:2],tuple(surf[2])[:2],tuple(surf[3])[:2]]
                    pygame.draw.polygon(self.screen,colors[int(surf[4])],bound)                
                
    def transformall(self,matrix):
        """ Rotate all wireframe about their centre, along a given axis by a given angle. """
        for wireframe in self.wireframes.itervalues():
            wireframe.transform(matrix)
            
    def updateall(self):
        for wireframe in self.wireframes.itervalues():
            wireframe.updateFaces()
            
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False                

                elif event.type == pygame.KEYDOWN:
                    if event.key in key_to_function:
                        key_to_function[event.key](self)
                    
            self.updateall()
            self.screen.fill(self.background)
            self.display()
            pygame.display.flip()
            
        pygame.quit()

