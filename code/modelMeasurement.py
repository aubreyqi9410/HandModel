from __future__ import division
import math
from klampt import *
from klampt import vectorops, so3
from klampt import visualization as vis
from klampt.glrobotprogram import *
import numpy as np 
import os
import sys
import json

class GLIKTest(GLRealtimeProgram):
	def __init__(self, world):
		GLRealtimeProgram.__init__(self, "GLIKTest")
		self.world = world
		robot = self.world.robot(0)
		robot.link(8).setParentTransform(robot.link(8).getParentTransform()[0], [1,1,2])
	
	def display(self):
		self.world.drawGL()
	
		print 'measurements: ', self.measureLinks()
	
	def measureLinks(self):
		robot = self.world.robot(0)
		meas = {}
		meas['palm_index'] = self.distBetwLinks(6,8)
		meas['index_p'] = self.distBetwLinks(8,9)
		meas['index_m'] = self.distBetwLinks(9,10)
		meas['little_p'] = self.distBetwLinks(12,13)
		meas['little_m'] = self.distBetwLinks(13,14)
		meas['middle_p'] = self.distBetwLinks(16,17)
		meas['middle_m'] = self.distBetwLinks(17,18)
		meas['ring_p'] = self.distBetwLinks(20,21)
		meas['ring_m'] = self.distBetwLinks(21,22)
		meas['thumb_p'] = self.distBetwLinks(24,25)
		meas['thumb_m'] = self.distBetwLinks(25,26)
		self.writeToFile(meas)
		return meas
	def distBetwLinks(self, index1, index2):
		'''
		returns the distance between 2 links in centimeters
		'''
		robot = self.world.robot(0)
		link1 = robot.link(index1).getWorldPosition((0,0,0))
		link2 = robot.link(index2).getWorldPosition((0,0,0))
		return vectorops.distance(link1, link2) * 100
	
	def writeToFile(self, data):
		with open('../data/hand.json', 'w') as f:
			json.dump(data, f)
				
	def idle(self):
		pass			
if __name__ == "__main__":
	world = WorldModel()
	res = world.readFile("../worldfiles/test.xml")
	if not res: raise RuntimeError("Unable to load world file")
	GLIKTest(world).run()
