import numpy as np
from .piece_class import Piece

class Cube(object):
	"""Cube contains methods for rotations"""
	def __init__(self, faces):
		self.cube = np.array([Piece() for i in range(27)]).reshape((3, 3, 3))
		self.slices = {"bottom" : (0, slice(None), slice(None)),\
					 "right" : (slice(None), 0, slice(None)),\
					 "front" : (slice(None), slice(None), 0),\
					 "top" : (-1, slice(None), slice(None)),\
					 "left" : (slice(None), -1, slice(None)),\
					 "back" : (slice(None), slice(None), -1)}

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
			raise Exception("orientation can either be clockwise or counterClockwise"+orientation)

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
