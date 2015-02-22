#!/bin/python2
import os
import numpy as np
from scipy.misc import imsave
import time

#=====[ Step 1: import/init depthsense ]=====
import DepthSense as ds
ds.initDepthSense()

#=====[ Step 2: setup video dir ]=====
title = str(time.time)
video_dir = os.path.join('../data/video', '%s.vid' % title)
os.mkdir(video_dir)
frames = []

#=====[ Step 3: Function to save frames ]=====
def save_frame(frame, index):
    path = os.path.join(video_dir, '%d.jpg' % index)
    imsave(path, frame)


#=====[ Main ]=====
if __name__ == '__main__':
   
    i = 0
    while True:
        time.sleep(0.5)
        frame = ds.getColourMap()
        save_frame(frame, index)
        i += 1