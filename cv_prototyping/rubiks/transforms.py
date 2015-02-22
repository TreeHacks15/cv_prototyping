import numpy as np
import scipy as sp
import cv2


class Crop_T(object):
	def __init__(self, crop=(100,200)):
		self.crop = crop

	def fit(self, data):
		return self

	def transform(self, data):
		image = data
		return image[self.crop[0]:-self.crop[0], self.crop[1]:-self.crop[1]]


class Gray_T(object):
	def __init__(self):
		pass

	def fit(self, data):
		return self

	def transform(self, data):
		img = data
		return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)


class CannyEdge_T(object):
	def __init__(self, threshold1=20, threshold2=200, dilation=4):
		self.threshold1 = threshold1
		self.threshold2 = threshold2
		self.dilation = dilation

	def fit(self, data):
		return self 

	def transform(self, data):
		gray = data
		gray = cv2.bilateralFilter(gray, 11, 17, 17)
		canny = cv2.Canny(gray, self.threshold1, self.threshold2)
		canny = cv2.dilate(canny, np.ones((self.dilation,self.dilation)))
		return canny



class Contours_T(object):
	def __init__(self, min_length=30, max_length=100):
		self.min_length = 30
		self.max_length = 100

	def fit(self, data):
		return self

	def transform(self, data):
		canny = data
		contours, hierarchy = cv2.findContours(canny,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		contours = [c for c in contours if (len(c) > 40 and len(c) < 200)]
		return contours