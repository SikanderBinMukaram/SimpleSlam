import numpy as np
import cv2
from Frame_helper import Frame_create, frames_matcher



class SLAM_create(object):
	def __init__(self, W, H, K):
		self.frames = list()
		self.K, self.W, self.H = K, W, H
		
	def process_frame(self, img):		
		frame = Frame_create(img, self.frames)
		
		if len(self.frames) < 2:
			return img
			
		frame1 = self.frames[-2]
		frame2 = self.frames[-1]

		
		
		#idx1, idx2, Rt = frames_matcher(frame1, frame2)
		matches = frames_matcher(frame1, frame2)
		
		#checking matching
		for p1,p2 in matches:
			u1,v1 = map(lambda x: int(round(x)),p1)
			u2,v2 = map(lambda x: int(round(x)),p2)
			cv2.circle(img, (u1,v1), color = (0,255,0), radius =3)
			cv2.line(img, (u1,v1), (u2,v2), color = (255,0,0))
		
		
		# draw only keypoints location,not size and orientation
		#img2 = cv2.drawKeypoints(img, frame1.kpts, None, color=(0,255,0), flags=0)
		return img 
		#idx1, idx2, 
