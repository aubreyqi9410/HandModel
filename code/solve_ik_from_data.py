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
from Data import Data
configs = []
class GLIKTest(GLRealtimeProgram):
	def __init__(self, world, data, objFile, frameIdx):
		GLRealtimeProgram.__init__(self, "GLIKTest")
		self.world = world
		robot = self.world.robot(0)
		self.data = data
		self.objectives = self.initObjectives(objFile)
		self.currentFrameIdx = 0
		self.frameIdx = frameIdx

	def display(self):
		self.world.drawGL()	
		robot = self.world.robot(0)
		glDisable(GL_LIGHTING)
		glDisable(GL_DEPTH_TEST)
		glPointSize(5)
		glEnable(GL_POINT_SMOOTH)
		glBegin(GL_POINTS)
		#TODO: plot VICON markers
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
	
	def idle(self):
		global configs
		if self.frameIdx == -1:
			i = int(self.ttotal/0.1)
			if i > self.currentFrameIdx:
				self.updateAllObjectives(i)	
			self.currentFrameIdx = i
		else:
			self.currentFrameIdx = frameIdx

		links = []
		localpos = []
		globalpos = []
		robot = self.world.robot(0)
		for obj in self.objectives:
			links.append(robot.link(obj.linkIdx))
			localpos.append(obj.localpos)
			globalpos.append(obj.globalpos)
		# set starting config using data from glove
		robot.setConfig(self.data.getFrame(self.currentFrameIdx).gloveData)
		# solve IK
		'''
		q = self.solve_ik(links, localpos, globalpos, self.currentFrameIdx)
		configs.append(q)
		resource.set('ik.configs', configs)
		robot.setConfig(q)	
		'''
	def getObjectivesFromFile(self, filename):
		df = pd.read_csv(filename, sep=',')
		markerObjectives = []
		for i in range(0, len(df)):
			link_idx = int(df.iloc[i, 0])
			x = df.iloc[i,1]
			y = df.iloc[i,2]
			z = df.iloc[i,3]
			localpos = (x,y,z)
			marker = (link_idx, localpos)
			markerObjectives.append(marker)
		return markerObjectives
	
	def initObjectives(self, objFile):
		robot = self.world.robot(0)
		markerObjectivesData = self.getObjectivesFromFile(objFile)
		objectives = []	
		for i in range(0, len(markerObjectivesData)):
			link_idx = markerObjectivesData[i][0]
			localpos = markerObjectivesData[i][1]
			obj = MarkerObjective(robot, link_idx, localpos, i)
			objectives.append(obj)
		return objectives

	def updateAllObjectives(self, frameIdx):	
		
		for i in range(0, len(self.objectives)):
			obj = self.objectives[i]
			
			frame1pos = self.data.getMarkerPosAtFrame(frameIdx-1, i)#self.data.getFrame(frameIdx-1).viconMarkers[i].markerFramePos
			frame2pos = self.data.getMarkerPosAtFrame(frameIdx, i)#self.data.getFrame(frameIdx).viconMarkers[i].markerFramePos
			posChange = utils.calcChangeBetwFrames(frame1pos, frame2pos)
			pos = vectorops.add(obj.globalpos, posChange)
			obj.globalpos = pos
				
if __name__ == "__main__":
	sys.path.append('../../VICON')
	import utils, ViconMarker
	configFile = sys.argv[1]
	viconFile = sys.argv[2]
	objFile = sys.argv[3]
	frameIdx = int(sys.argv[4])
	data = Data(configFile, viconFile)
	world = WorldModel()
	res = world.readFile("../worldfiles/test.xml")
	if not res: raise RuntimeError("Unable to load world file")
	GLIKTest(world, data, objFile, frameIdx).run()
