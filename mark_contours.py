from copy import deepcopy
import os
import cv2
import numpy as np
import sklearn
import pickle
from utils import *


if __name__ == '__main__':

	#=====[ Step 1: setup videocapture	]=====
	video_filename = '../data/videos/3.mov'

	#=====[ Step 4: initialize game 	]=====
	num_frames = 1
	while (num_frames < 507):
		frame_ic = get_next_frame (vc)
		if num_frames > 30 and num_frames < 100:
			disp_frame = board.draw_vertices (frame_ic)
		else:
			disp_frame = deepcopy(frame_ic)

		if num_frames >= 100 and num_frames < 200:
			disp_frame = board.draw_squares (frame_ic)
		else:
			disp_frame = deepcopy(frame_ic)

		# disp_frame = cv2.resize (disp_frame, (1260, 420))
		# cv2.imshow ('FRAME', disp_frame)
		# key = cv2.waitKey(5)
		num_frames += 1
	board.initialize_game (frame_ic)
	####[ DEBUG: display board with initial config	]#####
	# cv2.imshow ('INITIAL CONFIG', frame_ic)
	# key = 0
	# while not key in [27, ord('Q'), ord('q')]: 
	# 	key = cv2.waitKey (30)
	# cv2.destroyAllWindows ()


	# add_frames = [470, 516, 550, 589, 648, 709, 819, 878, 932] #1.mov
	add_frames = 		[	531, 566, 652, 689, 744, 801, 		#3.mov
							1005, 1069, 1501, 1558, 1610, 
							1642, 1673, 1695, 1922, 1963, 
							2050, 2211, 2359, 2768, 2812, 
							2972, 3219, 3290, 3484, 3576, 
							3781, 4000, 4502, 4933, 5377, 
							5645]
	while True:

		#=====[ Step 1: get/preprocess frame	]=====
		frame = get_next_frame (vc)

		#=====[ Step 2: display and wait indefinitely on key	]=====
		print "frame #: ", num_frames
		if num_frames > 531:
			disp_frame = board.draw_last_move (deepcopy(frame))
		else:
			disp_frame = frame
		disp_frame = cv2.resize (disp_frame, (1260, 420))

		cv2.imshow ('FRAME', disp_frame)

		#=====[ Case: space bar -> add frame	]=====
		if num_frames in add_frames:
			print "===[ ADDING FRAME #" + str(num_frames) + " ]==="
			board.add_move (frame)
			# board.display_movement_heatmaps ()			

		#=====[ Case: exit -> escape	]=====
		key = cv2.waitKey (2)
		if key in [27, ord('Q'), ord('q')]: 
			break

		num_frames += 1




