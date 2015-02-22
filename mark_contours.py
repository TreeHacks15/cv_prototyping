from copy import deepcopy
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import sklearn
import pickle

from cv_prototyping import *
from cv_prototyping.rubiks import Cube

labels = []

def onclick(event):
    print 'button=%d, x=%d, y=%d, xdata=%f, ydata=%f'%(
    	event.button, event.x, event.y, event.xdata, event.ydata)
    


if __name__ == '__main__':

	#=====[ Step 1: initialization	]=====
	frames = load_rubiks_video(data_dir='./data')
	cube = Cube()

	#=====[ Step 1: load frames	]=====
	for frame in frames:
		contours = cube.get_contours(frame)
		labels = np.zeros((len(contours),)).astype(bool)

		contours_image = cube.draw_contours(frame, contours, labels)

		fig = plt.figure()
		ax = plt.gca()

		cid = fig.canvas.mpl_connect('button_press_event', onclick)
		plt.imshow(contours_image)
		plt.show()

			# key = cv2.waitKey(30)
			# if key in [27, ord('Q'), ord('q')]: 
				# break


