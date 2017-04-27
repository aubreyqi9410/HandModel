from __future__ import division
import math
from klampt import *
from klampt import vectorops, so3
from klampt import visualization as vis
from klampt.glrobotprogram import *
import numpy as np 
import os
import sys
'''
Read markers from file and visualize them
'''
class GLIKTest(GLRealtimeProgram):
	def __init__(self, markers, startFrame, endFrame, numMarkers):
		GLRealtimeProgram.__init__(self, "GLIKTest")
		self.markers = markers
		self.startFrame = max(startFrame, 0)
		self.endFrame = min(endFrame, len(markers[0].pos))
		self.numMarkers = numMarkers
		self.markerNames = utils.getTopMarkers(self.markers, self.startFrame, self.endFrame, self.numMarkers)
		
	def check(self, markerName):
		for markers in self.markerNames:
			if markerName == markers[0]:
				return True
		return False

	def display(self):
		if self.startFrame != self.endFrame:
			idx = int(self.ttotal/0.01) + self.startFrame
		else:
			idx = self.startFrame
		#TODO: plot marker of single frame
		glDisable(GL_LIGHTING)
		glDisable(GL_DEPTH_TEST)
		glPointSize(5)
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		T = so3.from_axis_angle(([0,0,1], math.pi))
		count = 0
		for i in range(0, len(self.markers)):
			marker = self.markers[i]
			if self.check(marker.name):
				if marker.isCompleteFrame(idx):
					count += 1
					if count == self.numMarkers:
						print 'completeIdx: ', idx
				glColor3f(0,1,1)
				pos = marker.getPosAtFrame(idx)#so3.apply(T, marker.getPosAtFrame(idx))
				glVertex3fv(pos)
		glEnd()
		glEnable(GL_DEPTH_TEST)

if __name__ == "__main__":
	sys.path.append('../../VICON')
	import utils, ViconMarker
	fn = sys.argv[1]
	startFrame = int(sys.argv[2])
	endFrame = int(sys.argv[3])
	numMarkers = int(sys.argv[4])
	filename = '/home/ying/Klampt/VICON/data/' + fn
	markers = utils.parseCSVToMarkers(filename)
	GLIKTest(markers, startFrame, endFrame, numMarkers).run()
