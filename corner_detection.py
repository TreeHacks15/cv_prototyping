import numpy as np
import cv2

class CornerDetector(object):
    """
        Find corners of largest plane in image
    """ 

    def __init__(self, hough_thresh=70, angle_thresh=.2):
        self.hough_thresh = hough_thresh
        self.angle_thresh = angle_thresh

    def fit(self, data):
        return self
        
    def transform(self, img):
        img = self.preprocess(img)
        lines, points = self.hough(img)
        pairs = self.find_pairs(lines)
        areas = self.pairwise_area(img, points, pairs)
        corners = self.largest_plane(areas, points, pairs)
        return corners

    def preprocess(self, img):
        img = img.copy()
        img = cv2.bilateralFilter(img, 11, 17, 17)
        img = cv2.Canny(img, 30, 200)
        return img

    def hough(self, img):
        """
            Perform Hough Transform on img
        """
        lines = cv2.HoughLines(img,1,np.pi/180,self.hough_thresh)[0]
        return lines, self.find_points(lines)

    def find_pairs(self, lines):
        """
            Group nearly parallel lines
        """
        near_lines = []
        for l in lines:
            near = []
            for i in xrange(len(lines)):
                if abs(l[1]-lines[i][1]) < self.angle_thresh:
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
        return pairs

    def largest_plane(self, areas, points, pairs):
        """
            Given the pairwise areas return the corners of the largest plane
        """
        max_idx = np.argmax(areas)
        g1, g2 = np.unravel_index(max_idx,areas.shape)

        return self.find_corners(points[pairs[g1]["min"]], points[pairs[g1]["max"]],
                               points[pairs[g2]["min"]], points[pairs[g2]["max"]])

    def pairwise_area(self, img, points, pairs):
        """
            Calculate the areas of the quads given by any two elements of pairs
        """
        height, width = img.shape
        num_pairs = len(pairs)
        areas = np.zeros((num_pairs, num_pairs))
        for i in xrange(num_pairs):
           for j in xrange(num_pairs):
                if i == j:
                    continue
                corners = self.find_corners(points[pairs[i]["min"]], points[pairs[i]["max"]],
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
                areas[i,j] = self.find_area(corners)
        return areas

    def find_intersection(self, p0, p1, p2, p3):
        """
            find the intersection of the line given by p0,p1 and p2,p3
            Note: Stolen from StackOverFlow
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

    def find_corners(self, l1, l2, l3, l4):
        """
            Find the four corners of the quad given by l1, l2, l3, l4
        """
        return [self.find_intersection(l1[0], l1[1], l3[0], l3[1]),
                self.find_intersection(l1[0], l1[1], l4[0], l4[1]),
                self.find_intersection(l2[0], l2[1], l4[0], l4[1]),
                self.find_intersection(l2[0], l2[1], l3[0], l3[1])]

    def find_area(self, corners):
        """
            Find the area of the parallelogram given by corners
        """
        area = 0.0
        for i in xrange(0,4):
            j = (i+1)%4
            area += corners[i][0] * corners[j][1] - corners[j][0] * corners[i][1]
        return np.abs(area/2.0)

    def find_points(self, lines):
        """
            Convert the lines to pairs of Cartesian coordinates
        """
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
        return points
