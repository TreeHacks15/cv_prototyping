import numpy as np
import scipy as sp
import cv2

import requests
import json
import urllib

class ExtractStrokes_T(object):
	"""
		Transform: ExtractStrokes
		-------------------------
		image -> strokes (contours)
	"""
	def __init__(self):
		pass


	def fit(self):
		return self 


	def transform(self, data):
		"""
			image -> strokes (contours)
		"""
		image = data
		edges = cv2.Canny(img, 30,200)
		edges = cv2.GaussianBlur(edges,(11,11), .3)
		_ , edges = cv2.threshold(edges,0,255,0)
		contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		return contours


class StrokesOCR_T(object):
	"""
		Transform: StrokesOCR_T
		-----------------------
		strokes (contours) -> image
	"""
	def __init__(self):
		pass


	def fit(self, data):
		return self 


	def transform(self, data):
		"""
			strokes (contours) -> text 
		"""
		components = []
		for i in xrange(len(contours)):
		    xs = [int(p[0][0]) for p in contours[i]]
		    ys = [int(p[0][1]) for p in contours[i]]
		    if len(xs) < 10:
        		continue
		    components.append({"type": "stroke",
        	    		       "x": xs,
            	       		   "y": ys})
	    # plt.plot(xs,ys)
		# plt.imshow(edges, cmap="gray")

		api_key = "2007de54-d86a-4c4e-aed5-c9b442a95651"
		url = "http://webdemo.myscript.com/api/myscript/v2.0/equation/doSimpleRecognition.json"
		params = {
		    "apiKey": api_key,
		    "equationInput": json.dumps({
		        "resultTypes": ["LATEX"],
		        "components": components,
		        "switchToChildren": True
		    })
		}
		response = requests.post(url, params=params)
		result = json.loads(response.content)
		return result['result']['results'][0]['value']
