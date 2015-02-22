import numpy as np
import scipy as sp
from pytesser import *

class OCR_T(object):
	"""
		Transform: OCR
		--------------
		image -> contained text

		uses tesseract
	"""
	def __init__(self):
		pass


	def fit(self, data):
		return self


	def transform(self, data):
		"""
			image -> contained text 
		"""
		image = data
		raise NotImplementedError