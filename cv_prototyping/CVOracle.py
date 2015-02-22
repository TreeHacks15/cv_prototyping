import numpy as np 
import scipy as sp
import skimage
from sklearn.pipeline import Pipeline

#=====[ Transforms	]=====
from preprocessing import Preprocess_T
from corner_detection import CornerDetector_T
from projection import Projective_T
from ocr import OCR_T


class CVOracle():
	"""
		Class: CVOracle
		---------------
		Class responsible for interpreting images and returning results 
	"""
	def __init__(self):

		#=====[ image2contents:	]=====
		# input: image containing a rectangular surface
		# output: contents of that image
		image2contents = Pipeline 	([
										('preprocess', 		CVPreprocessor()),
										('get corners',  	CornerDetector()),
										('get contents', 	Projective_T())
									])

	def get_surface_contents(self, image):
		"""
		raw image -> image containing contents
		"""
		return image2contents.transform(image)


	def interpret_surface_contents(self, image):
		"""
		image of surface contents -> textual representation
		"""
		


	def update(self, image):
		"""
			image: raw image from Meta

			grabs the contents of the surface
		"""
		raise NotImplementedError