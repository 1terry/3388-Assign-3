# Terrence Ju
# Created for CS 3388
# Assignment 3, March 18, 2022
# Tessel class

import numpy as np
from matrix import matrix

class tessel:

    # Constructor takes in a list of objects, a camera and a light
    def __init__(self,objectList,camera,light):
        # Inits Epsilon, face list and list of points on the face, as well as light intensity and position of light
        EPSILON = 0.001
        self.__faceList = [] 	
        pointList = []
        lightView = camera.worldToViewingCoordinates(light.getPosition())
        intensity = light.getIntensity()
        
        # For each object in object list, we will set object colour and initialize u to the lower bound of the range
        for i in objectList:
            objColor = i.getColor()	
            u = i.getURange()[0]
            uDelta = i.getUVDelta()[0]  #U and V delta values are also stored and calculated
            vDelta = i.getUVDelta()[1]

            # While u + the delta u of the object is smaller than the final value of the u-parameter range + EPSILON
            while (u + uDelta) < (i.getURange()[1] + EPSILON): 
                v = i.getVRange()[0]    #V becomes the start value of the v-param range of the object

                # While v + the delta v of the object is smaller than the final value of the v-parameter range + EPSILON
                while (v + vDelta) < (i.getVRange()[1] + EPSILON):
                    # Gets object points
                    p1 = i.getPoint(u, v)
                    p2 = i.getPoint(u, v + vDelta)
                    p3 = i.getPoint(u + uDelta, v + vDelta)
                    p4 = i.getPoint(u + uDelta, v)

                    tMatrix = i.getT()	#Gets transformation matrix to multiply with

                    # Multiplies points by transformation matrix
                    p1 = tMatrix * p1
                    p2 = tMatrix * p2
                    p3 = tMatrix * p3
                    p4 = tMatrix * p4

                    # Transforms points to viewing coordinates
                    p1 = camera.worldToViewingCoordinates(p1)
                    p2 = camera.worldToViewingCoordinates(p2)
                    p3 = camera.worldToViewingCoordinates(p3)
                    p4 = camera.worldToViewingCoordinates(p4)
                    
                    # Appends to position list
                    pointList.append(p1)
                    pointList.append(p2)
                    pointList.append(p3)
                    pointList.append(p4)

                    minPos = self.__minCoordinate(pointList, 2)     #Calculates the min z value of face points

                    # If min z pos < - near plane (so that the face is not behind the near plane)
                    if minPos <= -(camera.getNp()):
                        # Gets centroid and normalalized form of normal vector
                        centroid = self.__centroid(pointList)
                        normalVec = self.__vectorNormal(pointList)
                        normalVec = matrix.normalize(normalVec)
                
                        # Computes face shading, exluding back faces
                        if not self.__backFace(centroid, normalVec):
                            # Sets S, R, V and normalizes S
                            S = self.__vectorToLightSource(lightView, centroid)
                            S = matrix.normalize(S)
                            R = self.__vectorSpecular(S, normalVec)
                            V = self.__vectorToEye(centroid)
                
                            # Computes colour index and face colour, which is stored as a tuple
                            colorIndex = self.__colorIndex(i, normalVec, S, R, V)
                            faceColor = (int(objColor[0] * intensity[0] * colorIndex), int(objColor[1] * intensity[1] * colorIndex), 
                            int(objColor[2] * intensity[2] * colorIndex))
                            
                            # Creates face point list and appends the pixel coordinates of each point
                            facepointList = []
                            for x in pointList:
                                facepointList.append(camera.viewingToPixelCoordinates(x))
                                
                            # Converts centroid to pixel and appends z coord of centroid, pixel face point list and face color to the face list
                            centroid = camera.viewingToPixelCoordinates(centroid)
                            self.__faceList.append([(centroid.get(2,0)), facepointList, faceColor])

                    # Re-inits point list and updates u and v values
                    pointList = []
                    v = v + vDelta
                u = u + uDelta
      
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