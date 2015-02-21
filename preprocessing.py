from scipy.misc import imresize
import cv2

class Preprocess_T(object):
	""" 
		Transform: Preprocess_T
		-----------------------
		(color) image -> preprocessed image

		Steps:
		------
		- resize
		- covnert to grayscale
	"""
	def __init__(self, scale=.1):
		self.scale = scale

	def fit(self, data):
		return self
		
	def transform(self, data):
		img = data
		img = imresize(img, self.scale)
		img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		return img