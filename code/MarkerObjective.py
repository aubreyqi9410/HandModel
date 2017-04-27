from klampt import vectorops, so3
from klampt import *
class MarkerObjective():
	def __init__(self, robot, linkIdx, localpos, markerIdx):
		self.linkIdx = linkIdx
		self.localpos = localpos
		self.globalpos = robot.link(linkIdx).getWorldPosition(localpos)
		self.markerIdx = markerIdx
	
	def updatePos(self, posChange):
		self.globalpos = vectorops(self.globalpos, posChange)
	
	def setLink(self, linkIdx):
		self.linkIdx = linkIdx
