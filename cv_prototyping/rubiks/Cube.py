import numpy as np
import scipy as sp
import cv2
import sklearn
from sklearn.pipeline import Pipeline

#=====[ Transforms	]=====
from transforms import Crop_T
from transforms import Gray_T
from transforms import CannyEdge_T
from transforms import Contours_T

class Cube(object):
	"""
		Class: Cube
		-----------
		deals with the Rubik's Cube 
	"""
	def __init__(self):
		self.state = None


	def update(self, frame):
		"""
			updates self.state
		"""
		self.state = self.get_state(frame)
		raise NotImplementedError


	def get_state(self, frame):
		"""
			gets current state from frame 
		"""
		raise NotImplementedError


	def get_contours(self, frame):
		"""
			raw frame -> contours 
		"""
		get_contours = Pipeline([
									('crop', Crop_T()),
									('grayscale', Gray_T()),
									('edges', CannyEdge_T()),
									('contours', Contours_T())
								])
		return get_contours.transform(frame)


	def get_cropped(self, frame):
		"""
			raw frame -> cropped frame 
		"""
		return Contours_T().transform(frame)


	def draw_edges(self, frame):
		"""
			draws edges 
		"""
		get_edges =	Pipeline([
								('crop', Crop_T()),
								('grayscale', Gray_T()),
								('edges', CannyEdge_T()),
							])
		return get_edges.transform(frame)


	def draw_contours(self, frame, contours=None, labels=None):
		"""
			draws contours on the raw frame;
			red = negative example
			blue = positive example
		"""
		if contours is None:
			contours = self.get_contours(frame)

		cont_img = Crop_T().transform(frame.copy())
		if not labels is None:
			assert len(labels) == len(contours)
			contours = np.array(contours)
			contours_pos = [contours[i] for i in range(len(contours)) if labels[i]]
			contours_neg = [contours[i] for i in range(len(contours)) if not labels[i]]
			cv2.drawContours(cont_img, contours_pos, -1, (0, 255, 0), 3)
			cv2.drawContours(cont_img, contours_neg, -1, (255, 0, 0), 3)
		else:
			cv2.drawContours(cont_img, contours, -1, (255, 0, 0), 3)
		return cont_img
