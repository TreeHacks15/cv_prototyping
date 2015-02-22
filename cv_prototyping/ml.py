import os
import numpy as np 
import scipy as sp
import sklearn
from sklearn.pipeline import Pipeline

def get_frames_labels_paths(videos=[1]):
	"""
		iterates over all paths to frame, labels pairs
	"""
	rubiks_dir = os.path.join('../data/', 'rubiks/videos')
	video_dirs = [os.path.join(rubiks_dir, str(v)) for v in videos]
	paths = []
	for video_dir in video_dirs:
		for p in [os.path.join(video_dir, x) for x in os.listdir(video_dir)]:
			if p.endswith('jpg') and os.path.exists(p + '.labels.npy'):
				paths.append((p, p + '.labels.npy'))

	return paths


def featurize(image, contour, label):
	"""
	(image, contour) -> features 
	"""
	raise NotImplementedError


def gather_features():
	raise NotImplementedError