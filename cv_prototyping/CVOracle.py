import numpy as np 
import scipy as sp
import skimage
from sklearn.pipeline import Pipeline

#=====[ Transforms	]=====
from preprocessing import Preprocess_T
from corner_detection import CornerDetector_T
from projection import Projective_T
from ocr import ExtractStrokes_T
from ocr import StrokesOCR_T


class CVOracle(object):
	"""
		Class: CVOracle
		---------------
		Class responsible for interpreting images and returning results 
	"""
	def __init__(self):

		#=====[ image2contents:	]=====
		# input: image containing a rectangular surface
		# output: contents of that image
		self.image2contents = Pipeline 	([
											('preprocess', 		Preprocess_T()),
											('get corners',  	CornerDetector_T()),
											('get contents', 	Projective_T())
										])

		self.contents2text = Pipeline([
											('get contours', 	ExtractStrokes_T)
									])

	def get_surface_contents(self, image):
		"""
		raw image -> image containing contents
		"""
		return self.image2contents.transform(image)


	def interpret_surface_contents(self, image):
		"""
		image of surface contents -> textual representation
		"""
		pass
		

	def update(self, image):
		"""
			image: raw image from Meta

			grabs the contents of the surface
		"""
		raise NotImplementedError