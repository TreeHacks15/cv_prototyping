import os
import numpy 
import scipy
from scipy.misc import imread
import skimage


def load_test_images(images_dir='./data/image', num_images=5):
	"""
		returns list of images
	"""
	image_paths = [os.path.join(images_dir, p) for p in os.listdir(images_dir) if p.endswith('.jpg')]
	return [imread(p) for p in image_paths[:num_images]]



