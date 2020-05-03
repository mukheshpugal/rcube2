import numpy as np
from .piece_class import Piece

class Cube(object):
	"""Cube contains methods for rotations"""
	def __init__(self, faces):
		self.cube = np.array([Piece() for i in range(27)]).reshape((3, 3, 3))
		self.slices = {"top" : self.cube[0, :, :], "right" : self.cube[:, 0, :], "front" : self.cube[:, :, 0], "bottom" : self.cube[-1, :, :], "left" : self.cube[:, -1, :], "back" : self.cube[:, :, -1]}
		for face in faces.keys():
			for i in range(3):
				for j in range(3):
					self.slices[face][i, j].addFace(face, faces[face][i, j])
		for layer in self.cube:
			for row in layer:
				for piece in row:
					piece.fillNullFaces()

	def rotate(self, orientation, side):
		cube = self.cube

		if orientation not in ("clockwise", "counterClockwise"):
			raise Exception("orientation can either be clockwise or counterClockwise")

		if side == "top":
			cube[0, :, :] = np.rot90(cube[0, :, :], -1 if orientation=="clockwise" else 1)

		if side == "right":
			cube[:, 0, :] = np.rot90(cube[:, 0, :], -1 if orientation=="clockwise" else 1)

		if side == "front":
			cube[:, :, 0] = np.rot90(cube[:, :, 0], -1 if orientation=="clockwise" else 1)

		if side == "bottom":
			cube[-1, :, :] = np.rot90(cube[-1, :, :], 1 if orientation=="clockwise" else -1)

		if side == "left":
			cube[:, -1, :] = np.rot90(cube[:, -1, :], 1 if orientation=="clockwise" else -1)

		if side == "back":
			cube[:, :, -1] = np.rot90(cube[:, :, -1], 1 if orientation=="clockwise" else -1)

		try:
			for row in self.slices[side]:
				for piece in row:
					piece.rotate(orientation)(side)
		except KeyError:
			pass

	def getFace(self, side):
		face = np.array([[piece.colorAt(side) for piece in row] for row in self.slices[side]])
		return face
