import math
import numpy as np
from klampt import vectorops,so3

def getVector(p1, p2):
	'''
	Get vector formed by two points
	'''
	return vectorops.sub(p1, p2)

def calcAngle(v1, v2):
	'''
	return angle between two vectors in degrees
	'''
	v1 = vectorops.unit(v1)
	v2 = vectorops.unit(v2)
	return math.degrees(math.acos(vectorops.dot(v1, v2)))


def calcJointAngle(P, M, I, D):

	PM = getVector(P, M)
	MI = getVector(M, I)
	ID = getVector(I, D)

	MCP = calcAngle(PM, MI)
	PIP = calcAngle(MI, ID)

	return (MCP, PIP)



	
P = (-64.9777, 481.5, 581.644)
M = (-60.7915, 472.194, 600.827)
I = (-60.8881, 464.243, 647.206)
D = (-28.7731, 453.828, 643.712)

print calcJointAngle(P, M, I,D)
