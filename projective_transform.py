import numpy as np
import scipy as sp
import skimage 
import skimage.transform as tf
from skimage import draw

def draw_quad(img, vx, value=255):
    """draws a quadrilateral"""
    x = vx[:,0]
    y = vx[:,1]
    rr, cc = draw.polygon(y, x)
    img = img.copy()
    img[rr,cc] = value
    return img


class ProjectiveTransformer(object):
	"""
		Transform: ProjectiveTransformer
		--------------------------------
		(image, surface_corners) -> surface_contents 

		- std_rect: square in info_space
		- M: transform from info_space to surface_space
	"""
	def __init__(self):
		self.std_rect = np.array((
	                				(0, 0), #bottom left
					                (0, 100), #top left
	        				        (100, 100), #top right
					                (100, 0) 	#bottom right
		)).astype(np.float64)
		self.M = tf.ProjectiveTransform()
		return self


	def fit(self, image):
		pass


	def transform(self, data):
		"""
			data = (image, surface_corners)
			returns region in image bounded by surface_corners as a 100x100 
			numpy array 
		"""
		#=====[ Step 1: Input validation	]=====
		if not (type(data) == tuple) and (len(data) == 2):
			raise TypeError("Pass in (image, corners); you passed %s" % str(type(data)))
		(image, corners) = data
		if not (type(corners) == np.array) and (corners.shape == (4,2)):
			raise TypeError("corners must be a 4x2 numpy array")

		#=====[ Step 2: Find projective transform	]=====	
		self.M.estimate(self.std_rect, corners)

		#=====[ Step 3: grab surface	]=====
		return tf.warp(image, self.M, output_shape=(100,100))


