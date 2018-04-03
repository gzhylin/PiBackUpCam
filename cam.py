#
#used as a reference http://www.pygame.org/docs/tut/CameraIntro.html 

#import Pygame files
import time
import os
import pygame
import pygame.camera
from pygame.locals import *
from gpiozero import DistanceSensor
from time import sleep

#set constans
DEVICE = '/dev/video0'
SIZE = (320,240)
BLACK = 0,0,0

#sensor reading
def readSensor(sensor):
	valueList = []            #init the list
	for i in range (0,10):
		valueList.append(sensor.distance*100)
		time.sleep(0.005)
	distance = sum(valueList)/len(valueList)
	return distance

#camera stream function
def cameraStream():
	#Initialize camera
	pygame.init()
	pygame.camera.init()

	#set window size
	display = pygame.display.set_mode((320,400),0)

	#get camera list and selet first camera
	cameraList = pygame.camera.list_cameras()
	if cameraList:
		camera = pygame.camera.Camera(cameraList[0],SIZE)

	#start the camera
	camera.start()

	sensor = DistanceSensor(echo=17, max_distance=3, trigger=4)

	#crate a surface to capture to
	screen = pygame.surface.Surface(SIZE, 0, display)
	
	working = True

	while working:
		display.fill(BLACK)
		#display image
		screen = camera.get_image(screen)
		#blit to the display surface
		display.blit(screen, (0,0))

		dist = readSensor(sensor)
		if  dist > 30:
			time = "MOVE"
		else:
			time = "STOP"

		font_big = pygame.font.Font(None, 50)           # font size
		text_surface = font_big.render('%d cm = %s'%(dist,time),True, (255,150,0))	
		
		rect = text_surface.get_rect(center=(160,350))  # position
		
		display.blit(text_surface, rect)

		pygame.display.flip()
		pygame.display.update()
		events = pygame.event.get()
		for e in events:
			if e.type == QUIT or (e.type == KEYDOWN and e.key == K_ESCAPE):
				#exit
				working = False
	camera.stop()
	pygame.quit()
	return

if __name__ == '__main__':
	cameraStream()
