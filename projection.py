import numpy as np
import scipy as sp
import skimage
from skimage import draw
from scipy.linalg import pinv

std_rect = np.array([
                [0, 0], #bottom left
                [1, 0], #top left
                [1, 1], #top right
                [0, 1] #bottom right
]).astype(np.float64)

def to_projective(v):
    """
        Given a 2x4 set of vertices, returns a set 
        of points in projective space on the quad
    """
    vout = np.zeros((8, 3))
    vout[:, 2] = 1
    vout[0:4, 0:2] = v
    vout[4, 0:2] = (v[1,:] + v[0,:])/2.0
    vout[5, 0:2] = (v[3,:] + v[2,:])/2.0
    vout[6, 0:2] = (v[2,:] + v[0,:])/2.0
    vout[7, 0:2] = (v[3,:] + v[1,:])/2.0
    return vout


 def get_projection(vout):
    """
        finds projection matrix M mapping vin to vout
    """
    #=====[ Step 1: put in projective space ]=====
    vin = std_rect
    p, P = to_projective(vin), to_projective(vout)
    
    #=====[ Step 2: get matrix A ]===== 
    num_points = p.shape[0]
    A = zeros((num_points*2, 6 + 2))
    for i in range(num_points):
        i_start = i*2
        for j in range(2):
            j_start = 3*j;
            A[i_start+j, j_start:j_start+3] = p[i,:]

    for i in range(num_points):
        start = i*2
        A[start, 6] = -(P[i,0] * p[i,0])
        A[start, 7] = -(P[i,0] * p[i,1])
        A[start+1, 6] = -(P[i,1] * p[i,0])
        A[start+1, 7] = -(P[i,1] * p[i,1])

    #=====[ Step 3: get B ]=====
    B = P[:, :2].flatten()
    
    #=====[ Step 4: get M ]=====
    m = np.dot(pinv(A), B)
    M = np.zeros((3, 3))
    M[0,:] = m[0:3]
    M[1,:] = m[3:6]
    M[2,:2] = m[6:8]
    M[2,2] = 1
    return M


def projective_transform(M, vin):
    """
        transforms point in flat plane to book plane
    """
    vin = to_projective(vin)
    vout = (M.dot(vin.T).T)
    return ((vout.T / vout[:, 2].T).T)[:4, 0:2]


def draw_quad(img, vx, value=255):
    """draws a quadrilateral on img"""
    x = vx[:,0]
    y = vx[:,1]
    rr, cc = draw.polygon(y, x)
    img[rr,cc] = value
    return img


def draw_info(M, img, info_img, rel_coords):
	"""
		given coordinates of the info_img, relative to the unit square, 
		this will draw it on the screen
	"""
	#=====[ iterate over in 	]=====



