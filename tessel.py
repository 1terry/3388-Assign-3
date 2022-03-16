from sys import ps1
import numpy as np
from matrix import matrix
import cameraMatrix
# import point

class tessel:

    def __init__(self,objectList,camera,light):
    	EPSILON = 0.001
		self.__faceList = [] 	
		pointList = []
		camera.worldToViewingCoordinates(light.getPosition())
		self.__intensity = light.getIntensity()

        #Create an empty list of faces. This is an instance variable for this class
        #Create an empty list for the points forming a face
		#Transform the position of the light into viewing coordinates (use method worldToViewingCoordinates from class cameraMatrix)
		#Get light intensity values
		
		for i in objectList:
			objColor = i.getColor()	
			u = i.getURange()[0]
			#For each object in objectList:
			#Get the object color
			#u becomes the start value of the u-parameter range for the object
			#While u + the delta u of the object is smaller than the final value of the u-parameter range + EPSILON:
			#'''	v become the start value of the v-parameter range for the object'''
	    	while u + (i.getUVDelta()[0]) < u + EPSILON:
				v = i.getVRange()[0]
				
				while v + (i.getUVDelta()[1]) < v + EPSILON:
					
					#While v + the delta v of the object is smaller than the final value of the v-parameter range + EPSILON:
					#Collect surface points transformed into viewing coordinates in the following way:
					p1 = matrix(u, v) 
					p2 = matrix(u, v + (i.getUVDelta()[0]))
					p3 = matrix(u + (i.getUVDelta()[0]), v + (i.getUVDelta()[1]))
					p4 = matrix(u + (i.getUVDelta()[0]), v)
					tMatrix = i.getT()	#Gets transformation matrix to multiply with

					# Applies transformation matrix
					p1 = p1.__mul__(tMatrix)
					p2 = p2.__mul__(tMatrix)
					p3 = p3.__mul__(tMatrix)
					p4 = p4.__mul__(tMatrix)

					# Transforms matrix to viewing coordinates
					p1 = camera.worldToViewingCoordinates(p1)
					p2 = camera.worldToViewingCoordinates(p2)
					p3 = camera.worldToViewingCoordinates(p3)
					p4 = camera.worldToViewingCoordinates(p4)
					
					# Appends to position
					self.__pointList.append(p1)
					self.__pointList.append(p2)
					self.__pointList.append(p3)
					self.__pointList.append(p4)
					
					#Get object point at (u,v), (u, v + delta v), (u + delta u, v + delta v), and (u + delta u, v)
					#Transform these points with the transformation matrix of the object
					#Transform these points from world to viewing coordinates	
					#Append these points (respecting the order) to the list of face points

                    #Make sure we don't render any face with one or more points behind the near plane in the following way:
					minPos = self.__minCoordinates(pointList, 2)

					if minPos <= -camera.getNP():
						centroid = self.__centroid(pointList)
						normalVec = self.__vectorNormal(pointList)
					#Compute the minimum Z-coordinate from the face points
					#If this minimum Z-value is not greater than -(Near Plane) (so the face is not behind the near plane):
					#Compute the centroid point of the face points
					#Compute the normal vector of the face, normalized
					#Compute face shading, excluding back faces (normal vector pointing away from camera) in the following way:
					#'''	if not backFace(centroid, face normal):'''
						if not self.__backFace(centroid, normalVec):
							S = self.__vectorToLightSource()
							R = self.__vectorSpecular()
							V = self.__vectorToEye()

						#S is the vector from face centroid to light source, normalized
						#R is the vector of specular reflection
						#V is the vector from the face centroid to the origin of viewing coordinates
																				

					#Compute color index
					#Obtain face color (in the RGB 3-color channels, integer values) as a tuple:
					#(object color (red channel) * light intensity (red channel) * index,
					# object color (green channel) * light intensity (green channel) * index,
					# object color (blue channel) * light intensity (blue channel) * index)
					#For each face point:
					#Transform point into 2D pixel coordinates and append to a pixel face point list
					#Add all face attributes to the list of faces in the following manner:
					#transform the face centroid from viewing to pixel coordinates
					#append pixel Z-coordinate of face centroid, the pixel face point list, and the face color
					#Re-initialize the list of face points to empty
					#v become v + delta v
					#u becomes u + delta u
      
	def __minCoordinate(self,facePoints,coord): 
		#Computes the minimum X, Y, or Z coordinate from a list of 3D points
		#Coord = 0 indicates minimum X coord, 1 indicates minimum Y coord, 2 indicates minimum Z coord.
        min = facePoints[0].get(coord,0)
        for point in facePoints:
            if point.get(coord,0) < min:
                min = point.get(coord,0)
        return min

    def __backFace(self,C,N):
		#Computes if a face is a back face with using the dot product of the face centroid with the face normal vector
        return C.dotProduct(N) > 0.0

    def __centroid(self,facePoints):
		#Computes the centroid point of a face by averaging the points of the face
        sum = matrix(np.zeros((4,1)))
        for point in facePoints:
            sum += point
        return sum.scalarMultiply(1.0/float(len(facePoints)))

    def __vectorNormal(self,facePoints):
		#Computes the normalized vector normal to a face with the cross product
        U = (facePoints[3] - facePoints[1]).removeRow(3).normalize()
        V = (facePoints[2] - facePoints[0]).removeRow(3).normalize()
        return U.crossProduct(V).normalize().insertRow(3,0.0)

    def __vectorToLightSource(self,L,C):
        return (L.removeRow(3) - C.removeRow(3)).normalize().insertRow(3,0.0)

    def __vectorSpecular(self,S,N):
        return  S.scalarMultiply(-1.0) + N.scalarMultiply(2.0*(S.dotProduct(N)))

    def __vectorToEye(self,C):
        return C.removeRow(3).scalarMultiply(-1.0).normalize().insertRow(3,0.0)

    def __colorIndex(self,object,N,S,R,V):
		#Computes local components of shading
        Id = max(N.dotProduct(S),0.0)
        Is = max(R.dotProduct(V),0.0)
        r = object.getReflectance()
        index = r[0] + r[1]*Id + r[2]*Is**r[3]
        return index

    def getFaceList(self):
        return self.__faceList