import os
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imresize
import cv2


def load_test_images(images_dir='./data/image', num_images=5, bw=True):
    """
        returns list of images
    """
    image_paths = [os.path.join(images_dir, p) for p in os.listdir(images_dir) if p.endswith('.jpg')]
    return [cv2.imread(p) for p in image_paths[:num_images]]


def preprocess_image(img):
    """
        scale, downsample, denoise
    """
    img = imresize(img, 0.1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    return edged

def find_book(img, hough_thresh=70, angle_thresh=.2):
    """
        return the four corners of the book
        `hough_thresh` is the HoughLines parameter
        `angle_thresh` determines how close to parallel pairs of lines must be
    """
    lines = cv2.HoughLines(img,1,np.pi/180,hough_thresh)[0]

    # Convert the lines to pairs of Cartesian coordinates
    points = []
    for l in lines:
        rho, theta = l
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        points.append([[x1,y1],[x2,y2]])

    # Group nearly parallel lines
    near_lines = []
    for l in lines:
        near = []
        for i in xrange(len(lines)):
            if abs(l[1]-lines[i][1]) < angle_thresh:
                near.append(i)
        near_lines.append(near)

    # Find maximally distant pairs of parallel lines
    pairs = {}
    for near in near_lines:
        if len(near) < 2:
            continue
        sl = sorted(near, key=lambda x: lines[x][0])
        pairs[len(pairs)] = {
            "min": sl[0],
            "max": sl[-1],
            "rho": (lines[sl[0]][0] + lines[sl[-1]][0])/2.0,
            "theta": (lines[sl[0]][1] + lines[sl[-1]][1])/2.0,
        }

    
    # Find the two pairs of lines which maximize area
    height, width = img.shape
    num_pairs = len(pairs)
    parea = np.zeros((num_pairs, num_pairs))
    for i in xrange(num_pairs):
       for j in xrange(num_pairs):
            if i == j:
                continue
            corners = find_corners(points[pairs[i]["min"]], points[pairs[i]["max"]],
                                   points[pairs[j]["min"]], points[pairs[j]["max"]])
            valid = True
            for c in corners:
                if c == None:
                    valid = False
                elif c[0] < -10 or c[0] > width+10:
                    valid = False
                elif c[1] < -10 or c[1] > height+10:
                    valid = False
            if not valid:
                continue
            parea[i,j] = find_area(corners)
    max_idx = np.argmax(parea)
    g1, g2 = np.unravel_index(max_idx,parea.shape)

    return find_corners(points[pairs[g1]["min"]], points[pairs[g1]["max"]],
                           points[pairs[g2]["min"]], points[pairs[g2]["max"]])

def find_intersection( p0, p1, p2, p3 ) :
    """
        find the intersection of the line given by p0,p1 and p2,p3
    """
    s10_x = p1[0] - p0[0]
    s10_y = p1[1] - p0[1]
    s32_x = p3[0] - p2[0]
    s32_y = p3[1] - p2[1]
    denom = s10_x * s32_y - s32_x * s10_y
    if denom == 0 : return None # collinear
    denom_is_positive = denom > 0
    s02_x = p0[0] - p2[0]
    s02_y = p0[1] - p2[1]
    s_numer = s10_x * s02_y - s10_y * s02_x
    if (s_numer < 0) == denom_is_positive : return None # no collision
    t_numer = s32_x * s02_y - s32_y * s02_x
    if (t_numer < 0) == denom_is_positive : return None # no collision
    if (s_numer > denom) == denom_is_positive or (t_numer > denom) == denom_is_positive : return None # no collision
    # collision detected
    t = 1.0 * t_numer / denom
    intersection_point = [ p0[0] + (t * s10_x), p0[1] + (t * s10_y) ]
    return intersection_point

def find_corners(l1, l2, l3, l4):
    """
        find the four corners of the quad given by l1, l2, l3, l4
    """
    return [find_intersection(l1[0], l1[1], l3[0], l3[1]),
             find_intersection(l1[0], l1[1], l4[0], l4[1]),
             find_intersection(l2[0], l2[1], l4[0], l4[1]),
             find_intersection(l2[0], l2[1], l3[0], l3[1])]

def find_area(corners):
    """
        find the area of the parallelogram given by corners
    """
    area = 0.0
    for i in xrange(0,4):
        j = (i+1)%4
        area += corners[i][0] * corners[j][1] - corners[j][0] * corners[i][1]
    return np.abs(area/2.0)

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

