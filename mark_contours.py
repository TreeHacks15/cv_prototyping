from copy import deepcopy
import os
import cv2
import cv
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import pickle

from cv_prototyping import *
from cv_prototyping.rubiks import Cube

def save_labels(image_path, labels):
	"""
		saves labels as a numpy array
	"""
	path = image_path + '.labels.npy'
	np.save(path, labels)


if __name__ == '__main__':

	cv2.namedWindow ('DISPLAY')

	#=====[ Step 1: initialization	]=====
	cube = Cube()

	#=====[ Step 1: load frames	]=====
	for path, frame in iter_rubiks_video(video=1, data_dir='./data/'):
		labels = []

		contours = cube.get_contours(frame)

		#==========[ Step 4: have user mark keypoints ]==========
		for contour in contours:
			cont_img = cube.draw_contour(frame, contour)
			cv2.imshow('DISPLAY', cont_img)

			while True:

				key = cv2.waitKey(30)
				if key == 97: #a
					print "NOT CUBE"
					labels.append(1)
					break
				elif key == 108:
					print "CUBE"
					labels.append(0)
					break

		print labels
		save_labels(path, labels)


