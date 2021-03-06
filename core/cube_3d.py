import numpy as np
from .legacy_cube import Cube

class Cube3D(Cube):
	"""Cube class with the 3d functions"""
	def __init__(self, faces):
		super().__init__(faces)
		self.inRotation = False
		self.rotatingSide = ""
		self.rotatingOrientation = ""
		self.positions = np.array([[[[-j, k, -i] for i in range(-1, 2)] for j in range(-1, 2)] for k in range(-1, 2)], dtype = np.float64)
		self.angle = 0

	def render(self):
		positions = self.positions.copy()

		if self.inRotation:
			self.angle += 0.4 * (-1 if self.rotatingOrientation == "clockwise" else 1)
			if self.angle >= np.pi / 2 or self.angle <= -np.pi / 2:
				self.inRotation = False
				self.angle = 0
				self.rotate(self.rotatingOrientation, self.rotatingSide)

			angle = self.angle
			side = self.rotatingSide
			if side in ("bottom", "left", "back"):
				angle *= -1
			if side in ("right", "left"):
				R = np.array([[1, 0, 0], [0, np.cos(angle), -np.sin(angle)], [0, np.sin(angle), np.cos(angle)]])
			if side in ("top", "bottom"):
				R = np.array([[np.cos(angle), 0, np.sin(angle)], [0, 1, 0], [-np.sin(angle), 0, np.cos(angle)]])
			if side in ("front", "back"):
				R = np.array([[np.cos(angle), -np.sin(angle), 0], [np.sin(angle), np.cos(angle), 0], [0, 0, 1]])

			for row in self.cube[self.slices[self.rotatingSide]]:
				for piece in row:
					piece.setRotationMatrix(R)

			positions[self.slices[self.rotatingSide]] = np.array([(R @ row.transpose()).transpose() for row in positions[self.slices[self.rotatingSide]]])

		for i in range(3):
			for j in range(3):
				for k in range(3):
					self.cube[i, j, k].render(positions[i, j, k], 0.48, self.inRotation)

	def rotate3D(self, orientation, side):
		if not self.inRotation:
			self.rotatingOrientation = orientation
			self.rotatingSide = side
			self.inRotation = True
