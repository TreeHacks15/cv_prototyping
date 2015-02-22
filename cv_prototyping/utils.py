import os
import numpy as np
import random
import cv2
import matplotlib.pyplot as plt


def get_data_dir():
    """
    returns data directory 
    """
    return os.path.join(os.getcwd(), '../data/')


def load_test_images(num_images=5, bw=True):
    """
    returns list of images
    """
    images_dir = os.path.join(get_data_dir(), 'image')
    image_paths = [os.path.join(images_dir, p) for p in os.listdir(images_dir) if p.endswith('.jpg')]
    random.shuffle(image_paths)
    return [cv2.imread(p) for p in image_paths[:num_images]]


def load_rubiks_video(data_dir='../data/', video=1, num_images=5, bw=False):
    """
    returns list of rubiks cubes
    """
    rubiks_dir = os.path.join(data_dir, 'rubiks/videos')
    video_dir = os.path.join(rubiks_dir, str(video))
    image_paths = [os.path.join(video_dir, p) for p in os.listdir(video_dir) if p.endswith('.jpg')]
    random.shuffle(image_paths)
    return [cv2.imread(p) for p in image_paths[:num_images]]


def show_images(images, n=4):
    """
    displays n images in a row
    """
    plt.rcParams['figure.figsize'] = 20, 50
    fig, axes = plt.subplots(nrows=1, ncols=min(n, 4))
    for i, img in enumerate(images[:n]):
        axes[i].imshow(img, cmap=plt.cm.gray)
        axes[i].set_xticks([])
        axes[i].set_yticks([])


def draw_quad(img, vx, value=255):
    """
    draws the quadilateral defined by vertices in vx
    on a copy of the image
    """
    x = vx[:,0]
    y = vx[:,1]
    rr, cc = draw.polygon(y, x)
    img = img.copy()
    img[rr,cc] = value
    return img
