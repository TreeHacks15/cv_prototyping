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


class ProjectiveTransformer():
	"""
		Class: ProjectiveTransformer
		----------------------------
		finds transformation from info_space -> book_space
	"""
	def __init__(self):
		#=====[ Step 1: initialize std rect in info space	]=====
		self.std_rect = np.array([
	                [0, 0], #bottom left
	                [1, 0], #top left
	                [1, 1], #top right
	                [0, 1] #bottom right
		]).astype(np.float64)

		self.M = tf.ProjectiveTransform()		#transform: image_space -> info_space


	def fit(self, dst):
		"""
			finds self.M from book_corners 
		"""
		#=====[ Step 1: assertions on size	]=====
		assert dst.shape == (4, 2)

		#=====[ Step 2: find transform	]=====
		src = np.array((
					    	(0, 0),
					    	(0, 100),
					    	(100, 100),
					    	(100, 0)
						))
		self.M = tf.ProjectiveTransform()
		self.M.estimate(src, dst)


	def grab_surface(self, image):
		"""
			grabs a square image representing the surface 
		"""
		return tf.warp(image, self.M, output_shape=(100,100))


	def project(self, image, info_image, coords):
		"""
			projects 'info_image' onto image according to coords 
		"""
		
		return tf.warp(info_image, self.M.inverse, output_shape=image.shape)





