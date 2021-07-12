import numpy as np
import cv2 

from skimage.measure import ransac 
from skimage.transform import FundamentalMatrixTransform, EssentialMatrixTransform


def FeatureExtractor(img):
	#using orb here 
	Orb = cv2.ORB_create()
	#Detection better points are detected using goodfeaturestotrack
	points = cv2.goodFeaturesToTrack(np.mean(img, axis=2).astype(np.uint8), 3000, qualityLevel=0.01, minDistance=7)
	
	#we extract the keypoints from each point we detected
	kpts = [cv2.KeyPoint(x=f[0][0], y=f[0][1], _size=20) for f in points]

	#compute 
	kpts, des = Orb.compute(img, kpts)

	#return kpts, des
	return np.array([(p.pt[0],p.pt[1]) for p in kpts]), des
	
	
class Frame_create(object):
	def __init__(self, img, frames):
		if img is not None:
			self.w, self.h = img.shape[0],img.shape[1]
			self.kpts, self.des = FeatureExtractor(img)
			self.id = len(frames)
			frames.append(self)
  
  			
def frames_matcher(frame1, frame2):			
	bf = cv2.BFMatcher(cv2.NORM_HAMMING)
	matches = bf.knnMatch(frame1.des,frame2.des, k=2)
	
	#Lowe's ratio test
	ret, idx1, idx2 = [], [], []

	for m,n in matches:
		if m.distance < 0.75*n.distance:
			matched_points1 = frame1.kpts[m.queryIdx]	
			matched_points2 = frame2.kpts[m.trainIdx]	
			#matched_points1 = frame1.kpts[m.queryIdx].pt	
			#matched_points2 = frame2.kpts[m.trainIdx].pt	
			
			if m.distance < 32:
				if m.queryIdx not in idx1 and m.trainIdx not in idx2:
					idx1.append(m.queryIdx)
					idx2.append(m.trainIdx)
					ret.append((matched_points1,matched_points2))	
	
	# no duplicates
	assert(len(set(idx1)) == len(idx1))
	assert(len(set(idx2)) == len(idx2))

	assert len(ret) >= 8
	ret = np.array(ret)
	idx1 = np.array(idx1)
	idx2 = np.array(idx2)

	# fit matrix
	model, inliers = ransac((ret[:, 0], ret[:, 1]),
		                  #EssentialMatrixTransform,
		                  #FundamentalMatrixTransform,
		                  EssentialMatrixTransform,
		                  min_samples=8,
		                  residual_threshold=1,
		                  max_trials=100)
	#print("Matches:  %d -> %d -> %d -> %d" % (len(f1.des), len(matches), len(inliers), sum(inliers)))
	print(len(matches), len(ret), len(ret[inliers]) )
	#print(len(ret[inliers]))
	return ret[inliers]

