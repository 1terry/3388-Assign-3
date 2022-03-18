# Terrence Ju
# Created for CS 3388
# Assignment 3, March 18, 2022
# Light source class

import numpy as np
from matrix import matrix

class lightSource:

    # Construcor Inits the class variables, takes in parameters of a position matrix, a colour tuple, and an intensity tuple
    def __init__(self,position=matrix(np.zeros((4,1))),color=(0,0,0),intensity=(1.0,1.0,1.0)):
        self.__position = position
        self.__color = color
        self.__intensity = intensity

    # Getter method returns position value
    def getPosition(self):
        return self.__position

    # Getter method returns color value
    def getColor(self):
        return self.__color

    # Getter method returns intensity value
    def getIntensity(self):
        return self.__intensity

    # Setter method sets position value to a given value
    def setPosition(self,position):
        self.__position = position

    # Setter method sets colour to a given value
    def setColor(self,color):
        self.__color = color

    # Setter method sets intensity to a given value
    def setIntensity(self,intensity):
        self.__intensity = intensity