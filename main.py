#!/usr/bin/env python

#Slam code for practice
# Imports
import numpy as np
import os
import cv2
import sys
from Display import DisplayImage
import time
from SLAM import SLAM_create
    

if __name__ == "__main__":
	
	#check if video input is provided
	if len(sys.argv) < 2:
		print("Missing input Video: %s <video.mp4>"% sys.argv[0])
		exit(-1)
		
		
	#video object
	video = cv2.VideoCapture(sys.argv[1])
	
	#get width and height
	H = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
	W = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
	#print(H,W)	
	
	#total frames
	total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
	
	#start video from a specific frame
	if os.getenv("StartFrame") is not None:
		video.set(cv2.CAP_PROP_POS_FRAMES, int(os.getenv("StartFrame")))		
		total_frames -= int(os.getenv("StartFrame"))+1
		
	#get focal lenght from command line and rescaling it
	F = int(os.getenv("F","525"))
	if os.getenv("DownScale") is not None:
		downscale = int(os.getenv("DownScale"))
		F *= 1/downscale
		W = W//downscale
		H = H//downscale

	print(F,H,W)
	
	# K matrix and its inverse
	K = np.array([[F,0,W//2],[0,F,H//2],[0,0,1]])	
	Kinv = np.linalg.inv(K)
	
	#all frames
	frames = list()
	#displaying frames
	Dispaly2D = DisplayImage(W,H)
	
	count = 0
	#start_time = time.time()

	slam = SLAM_create(W,H,K)
	
	while video.isOpened():
		ret, frame = video.read()
		count +=1
		print("\n-------Frame %d/%d-----------" %(count,total_frames))			
		if ret == True:
			frame = cv2.resize(frame,(W,H))
			frame = slam.process_frame(frame)	
			#print(len(frames))
		else:
			break
		

		if Dispaly2D is not None:
			Dispaly2D.showImage(frame)
			#Dispaly2D.show_frame_opencv(frame)
	
		
	#print("Time:     %.2f ms" % ((time.time()-start_time)*1000.0))
