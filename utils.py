import os
import numpy 
import scipy
from scipy.misc import imread
import matplotlib.pyplot as plt
import skimage
from skimage.transform import resize
from skimage.restoration import denoise_bilateral


def load_test_images(images_dir='./data/image', num_images=5, bw=True):
	"""
		returns list of images
	"""
	image_paths = [os.path.join(images_dir, p) for p in os.listdir(images_dir) if p.endswith('.jpg')]
	return [imread(p, flatten=bw) for p in image_paths[:num_images]]

def preprocess_image(img):
	"""
		scale, downsample, denoise
	"""
	#=====[ Step 1: scale to 0-1	]=====
	img = img / 255.0

	#=====[ Step 2: downsample	]=====
	shape = img.shape
	new_shape = tuple([s/10 for s in img.shape])
	img = resize(img, new_shape)

	#=====[ Step 3: denoise	]=====
	denoised = denoise_bilateral(img, sigma_range=0.05, sigma_spatial=15)
	return denoised

def show_images(images, n=4):
    """
        displays n images in a row
    """
    plt.rcParams['figure.figsize'] = 20, 50
    fig, axes = plt.subplots(nrows=1, ncols=n)
    for i, img in enumerate(images[:n]):
        axes[i].imshow(img, cmap=plt.cm.gray)
        axes[i].set_xticks([])
        axes[i].set_yticks([])

