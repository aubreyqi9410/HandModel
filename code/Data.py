from __future__ import division
import math
from klampt import *
from klampt import resource
import sys
sys.path.append("../../VICON")
import utils, ViconMarker
from ViconFrame import ViconFrameData, SingleFrameMarker
'''
Takes 2 files and assembles an data object
'''
class Data():
	def __init__(self, configFile, viconFile):
		self._viconFile = viconFile
		self._configFile = configFile
		self._viconMarkers = utils.parseCSVToMarkers(viconFile)
		configfn = configFile.split('/')[-1]
		configDir = '/'.join(configFile.split('/')[:-1])
		self._gloveConfigs = resource.get(configfn, directory=configDir)
		self.data = self._makeData()
	'''
	def _makeData(self):
		data = []
		for i in range(0, len(self._gloveConfigs)):
			gloveData = self._gloveConfigs[i]
			viconMarkers = self._getMatchingViconFrame(i)
			dat = Datum(gloveData, viconMarkers)
			data.append(dat)
		return data
	'''
	def _makeData(self):
		data = []
		viconFrameLen = len(self._viconMarkers[0].pos)
		for frameIdx in range(0, viconFrameLen):
			viconMarkers = ViconFrameData(self._assembleFrameData(frameIdx))
			gloveData = self._gloveConfigs[self._getGloveIdx(frameIdx)]
			dat = Datum(gloveData, viconMarkers)
			data.append(dat)
		return data

	def getMarkerPosAtFrame(self, frameIdx, markerIdx):
		return self.getFrame(frameIdx).viconMarkers.getMarker(markerIdx).markerFramePos
	
	def _getGloveIdx(self, viconIdx):
		n = len(self._gloveConfigs)/len(self._viconMarkers[0].pos)
		return int(viconIdx * n)
	'''	
	def _getMatchingViconFrame(self, gloveFrameIdx):
		#Find matching vicon frame given idx of data glove frame
		viconFrameIdx = gloveFrameIdx * self.gloveFR
		if not utils.isCompleteFrame(viconFrameIdx, self._viconMarkers):
			# max percent of markers missing is 50%
			minMarkers = len(self._viconMarkers)
			while(minMarkers >= len(self._viconMarkers)/2): 
				viconFrameIdx = utils.findClosestCompleteFrame(viconFrameIdx, self._viconMarkers, self.gloveFR, minMarkers)
				if viconFrameIdx == -1: minMarkers -= 1
				else:break
		frameData = self._assembleFrameData(viconFrameIdx)
		return ViconFrameData(frameData)
	'''
	def _assembleFrameData(self, frameIdx):
		markersData = []
		if frameIdx != -1:
			for marker in self._viconMarkers:
				markerFrameData = (marker.name, marker.pos[frameIdx])
				markersData.append(markerFrameData)
		return markersData

	def getFrame(self, frameIdx):
		return self.data[frameIdx]

	def fillMissing(self):
		pass
	

class Datum():
	def __init__(self, gloveData, viconMarkers):
		self.gloveData = gloveData
		self.viconMarkers = viconMarkers

