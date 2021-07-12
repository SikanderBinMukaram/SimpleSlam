import pygame
from pygame.locals import DOUBLEBUF as DB
import cv2

class DisplayImage(object):
	def __init__(self, W,H): 
		pygame.init()
		self.screen = pygame.display.set_mode((W,H),DB)
		self.surface = pygame.Surface(self.screen.get_size()).convert()
		
	def showImage(self, img):
		#for RGB we swap channels
		pygame.surfarray.blit_array(self.surface,img.swapaxes(0,1)[:,:,[0,1,2]])
		self.screen.blit(self.surface, (0,0))
		pygame.display.flip()	
		
	def show_frame_opencv(self, img):
		cv2.imshow('image',img)
		cv2.waitKey(1)

