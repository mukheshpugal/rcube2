import numpy as np
from .piece_3d import Piece3D

class Cube(object):
	"""Cube contains methods for rotations"""
	def __init__(self, faces):
		self.cube = np.array([Piece3D() for i in range(27)]).reshape((3, 3, 3))
		f = slice(None)
		self.slices = {"bottom" : (0, f, f), "right" : (f, 0, f), "front" : (f, f, 0), "top" : (-1, f, f), "left" : (f, -1, f), "back" : (f, f, -1)}

		for face in faces.keys():
			for i in range(3):
				for j in range(3):
					self.cube[self.slices[face]][i, j].addFace(face, faces[face][i, j])
		for layer in self.cube:
			for row in layer:
				for piece in row:
					piece.fillNullFaces()

	def rotate(self, orientation, side):
		cube = self.cube

		if orientation not in ("clockwise", "counterClockwise"):
			raise Exception("orientation can either be clockwise or counterClockwise")

		rotateDir = (orientation == "clockwise")

		if side in ("bottom", "left", "front"):
			rotateDir = not rotateDir

		cube[self.slices[side]] = np.rot90(cube[self.slices[side]], 1 if rotateDir else -1)

		try:
			for row in cube[self.slices[side]]:
				for piece in row:
					piece.rotate(orientation)(side)
		except KeyError:
			pass

		return "rotated " + side + " " + orientation

	def getFace(self, side):
		face = np.array([[piece.colorAt(side) for piece in row] for row in self.cube[self.slices[side]]])
		return face
