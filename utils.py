import os
import cv2
import numpy as np
import matplotlib.pyplot as plt


def load_test_images(images_dir='./data/image', num_images=5, bw=True):
    """
        returns list of images
    """
    image_paths = [os.path.join(images_dir, p) for p in os.listdir(images_dir) if p.endswith('.jpg')]
    return [cv2.imread(p) for p in image_paths[:num_images]]

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
    return fig, axes

