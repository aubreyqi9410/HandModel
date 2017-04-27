from __future__ import division
import math
from klampt import *
from klampt import vectorops, so3
from klampt import visualization as vis
from klampt.glrobotprogram import *
import numpy as np 
import pandas as pd
import os
import sys
from MarkerObjective import MarkerObjective
from klampt import resource

configs = []
class GLIKTest(GLRealtimeProgram):
	def __init__(self, world, frames, markers):
		GLRealtimeProgram.__init__(self, "GLIKTest")
		self.world = world
		robot = self.world.robot(0)
		self.frames = frames
		self.markers = markers
		self.prev_i = -1
		self.objectives = self.initObjectives()
	def display(self):
		self.world.drawGL()
				
		robot = self.world.robot(0)
	
		glDisable(GL_LIGHTING)
		glDisable(GL_DEPTH_TEST)
		glPointSize(5)
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		for obj in self.objectives:
			
			glColor3f(0,0,1)
			glVertex3fv(obj.globalpos)
		glEnd()
		glEnable(GL_DEPTH_TEST)

	def solve_ik(self, robotlinks, localposs, worldposs, frameIdx):
		'''
		Solve IK given a list of IK objectives
		'''
		robot = robotlinks[0].robot()
		assert(len(robotlinks) == len(localposs))
		objectives = []
		for i in range(0, len(robotlinks)):
			obj = ik.objective(robotlinks[i], local=localposs[i], world=worldposs[i])		
			objectives.append(obj)
		
		s = ik.solver(objectives)
		#s.setActiveDofs([0,1, 2, 3, 4, 5, 6, 7, 8,9,10])

		maxIters = 100
		tol = 1e-3
		(res, iters) = s.solve(maxIters, tol)
		if not res: print "IK Failure"	
		return robot.getConfig()

	def setConfigFromGlove(self, configFile):
		startConfig = resource.load('Configs', configFile)
		handModel = self.world.robot(0)
		handModel.setConfig(startConfig)
	
	def idle(self):
		global configs
		i = int(self.ttotal/0.1)
	
		frameIdx = self.frames[i]
		if i != self.prev_i:
			self.updateAllObjectives(frameIdx)	
		self.prev_i = i
		links = []
		localpos = []
		globalpos = []
		robot = self.world.robot(0)
		for obj in self.objectives:
			links.append(robot.link(obj.linkIdx))
			localpos.append(obj.localpos)
			globalpos.append(obj.globalpos)
		q = self.solve_ik(links, localpos, globalpos, frameIdx)
		configs.append(q)
		resource.set('ik.configs', configs)
		robot.setConfig(q)	

	def getObjectivesFromFile(self, filename):
		df = pd.read_csv(filename, sep=',')
		markers = []
		for i in range(0, len(df)):
			link_idx = int(df.iloc[i, 0])
			x = df.iloc[i,1]
			y = df.iloc[i,2]
			z = df.iloc[i,3]
			localpos = (x,y,z)
			marker = (link_idx, localpos)
			markers.append(marker)
		return markers
	
	def initObjectives(self):
		robot = self.world.robot(0)
		markers = self.getObjectivesFromFile('../data/objectives.csv')
		objectives = []	
		for i in range(0, len(markers)):
			link_idx = markers[i][0]
			localpos = markers[i][1]
			obj = MarkerObjective(robot, link_idx, localpos, i)
			objectives.append(obj)
		
		return objectives

	def updateAllObjectives(self, idx):
		for i in range(0, len(self.objectives)):
			obj = self.objectives[i]
			pos = vectorops.add(obj.globalpos, self.markers[obj.markerIdx].getPosChange(self.frames)[idx])
			obj.globalpos = pos
				
if __name__ == "__main__":
	sys.path.append('../../VICON')
	import utils, ViconMarker
	filename = '/home/ying/Klampt/VICON/data/Ying_index Cal 08.csv'
	markers = utils.parseCSVToMarkers(filename, 2100, 4000)
	completeFrames = utils.getCompleteFrames(markers)
	world = WorldModel()
	res = world.readFile("../worldfiles/test.xml")
	if not res: raise RuntimeError("Unable to load world file")
	GLIKTest(world, completeFrames, markers).run()
