# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 11:30:11 2017

@author: SMP II

Programm zum Berechnen der Position der Glyphe
Aufbauend auf den Berechnungen von Martin Schinnerls Bachelor Thesis
Geändert in Berechnung von K0 in K4
"""



'Module importieren'
from Parameter import denavit_hartenberg
from math import cos, sin
from numpy import around, array, dot, hsplit, vsplit, vstack


'Denavit-Hartenberg-Parameter laden'
d1, d2, d3, d4, d5, a1, a2, a3, a4, a5, \
alpha1, alpha2, alpha3, alpha4, alpha5 = denavit_hartenberg()

'''Funktion transformationsmatrix - 
Denavit-Hartenberg-Transformationsmatrix'''
def transformationsmatrix(theta, d, a, alpha):
    
    T = array([[cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],   \
               [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],   \
               [0, sin(alpha), cos(alpha), d], [0, 0, 0, 1]])
    
    return T

'Funktion A01 - Transformation von K0 in K1'
def A01(theta1):
    
    T01 = transformationsmatrix(theta1, d1, a1, alpha1)
    
    return T01

'Funktion A02 - Transformation von K0 in K2'
def A02(theta1, theta2):
    
    T01 = A01(theta1)
    T12 = transformationsmatrix(theta2, d2, a2, alpha2)
    
    T02 = dot(T01, T12)
        
    return T02
    
'Funktion A03 - Transformation von K0 in K3'
def A03(theta1, theta2, theta3):
    
    T02 = A02(theta1, theta2)
    T23 = transformationsmatrix(theta3, d3, a3, alpha3)
    
    T03 = dot(T02,T23)
    
    return T03
    
'Funktion A04 - Transformation von K0 in K4'
def A04(theta1, theta2, theta3, theta4):
    
    T03 = A03(theta1, theta2, theta3)
    T34 = transformationsmatrix(theta4, d4, a4, alpha4)
        
    T04 = dot(T03,T34)
    
    return T04


'Funktion A12 - Transformation von K1 in K2'
def A12(theta2):
     
    T12 = transformationsmatrix(theta2, d2, a2, alpha2)
    
    return T12
    
'Funktion A13 - Transformation von K1 in K3'
def A13(theta2, theta3):
     
    T12 = A12(theta2)
    T23 = transformationsmatrix(theta3, d3, a3, alpha3)
    
    T13 = dot(T12, T23)
    
    return T13
    
'Funktion A14 - Transformation von K1 in K4'
def A14(theta2, theta3, theta4):

    T13 = A13(theta2, theta3)
    T34 = transformationsmatrix(theta4, d4, a4, alpha4)
    
    T14 = dot(T13, T34)
    
    return T14



'''Kinematische Vorwärtstransformation - Die Funktion berechnet aus den
Drehwinkeln theta_i die Transformationsvorschrift zur Überführung von 
K0 in K4. Die Spalten der Matrix (Format 4x4) entsprechen den Einheits-
vektoren von K4 sowie der Verschiebung von K4 in Bezug auf K0 in 0-Koord-
inaten (Lage und Orientierung von K4 in 0-Koordinaten). Abschließend werden 
die Spalten der Matrix den entsprechenden Vektoren zugeordnet, das Format 
der Vektoren auf 3x1 geändert und diese zurückgegeben.'''

def kinematik_vor(theta1, theta2, theta3, theta4, theta5):
    'Transformationsvorschrift zur Überführung von K0 in K5 (Format 4x4)'
    T04 = A04(theta1, theta2, theta3, theta4, theta5)
    T04 = around(T04, 5)
    
    'Matrix in 4 Spalten teilen und den Vektoren (Format 4x1) zuordnen'
    x4, y4, z4, P04 = hsplit(T04, 4)
    
    'Format der Vektoren von 4x1 auf 3x1 ändern'
    #Einheitsvektor von K4 in 0-Koordinaten: x4in0
    x, y, z, z4 = vsplit(x4, 4)
    x4in0 = vstack((x, y, z))
    #Einheitsvektor von K4 in 0-Koordinaten: y4in0
    x, y, z, z4 = vsplit(y4, 4)
    y4in0 = vstack((x, y, z))
    #Einheitsvektor von K4 in 0-Koordinaten: z4in0
    x, y, z, z4 = vsplit(z4, 4)
    z4in0 = vstack((x, y, z))
    #Verschiebung von K4 in Bezug auf K0 in 0-Koordinaten: P04in0
    x, y, z, z4 = vsplit(P04, 4)
    P04in0 = vstack((x, y, z))
    
    return x4in0, y4in0, z4in0, P04in0


