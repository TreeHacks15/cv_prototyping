import numpy as np 
import scipy as sp
import skimage
from sklearn import Pipeline

from preprocessing import CVPreprocessor
from projective_transform import ProjectiveTransform
from corner_detection import CornerDetector

class CVOracle():
	"""
		Class: CVOracle
		---------------
		Class responsible for interpreting images and returning results 
	"""
	def __init__(self):

		self.preprocessor = CVPreprocessor() # image -> preprocessed image
		self.corner_detector = CornerDetector() # image -> surface corners
		self.pt = ProjectiveTransform() # surface conrers -> surface contents


	def get_surface_contents(self, image):
		"""
		raw image -> image containing contents
		"""

		image = self.preprocessor.transform(image)
		image = self.corner_detecor.transform()



	def update(self, image):
		"""
			image: raw image from Meta

			grabs the contents of the surface
		"""
		image = 