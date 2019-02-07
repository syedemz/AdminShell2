# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from pprint import pprint
from math import acos, cos, pi, sin, sqrt
from numpy import around, array
from math import acos, cos, pi, sin, atan, tan, asin
from numpy import around, array, dot, hsplit, sum, vsplit, vstack
from numpy.linalg import inv, norm
from pprint import pprint


def denavit_hartenberg():
    
    'Translation in Richtung z_i-1'
    #Angaben in [mm]
    d1 = 0
    d2 = 0
    d3 = 0
    d4 = 0
    d5 = 165
    
    'Translation in Richtung x_i-1 = x_i'
    #Angaben in [mm]
    a1 = 0
    a2 = 166
    a3 = 216.5
    a4 = 0
    a5 = 0
    
    'Rotation um x_i'
    #Angaben in [rad]
    alpha1 = pi/2
    alpha2 = 0
    alpha3 = 0
    alpha4 = pi/2
    alpha5 = 0
    
    return d1, d2, d3, d4, d5, a1, a2, a3, a4, a5, \
    alpha1, alpha2, alpha3, alpha4, alpha5
    
'Denavit-Hartenberg-Parameter laden'
d1, d2, d3, d4, d5, a1, a2, a3, a4, a5, \
alpha1, alpha2, alpha3, alpha4, alpha5 = denavit_hartenberg()

'''Funktion transformationsmatrix - 
Denavit-Hartenberg-Transformationsmatrix'''
def transformationsmatrix(theta, d, a, alpha):
    
    T = array([[cos(theta), -sin(theta)*cos(alpha), \
    sin(theta)*sin(alpha), a*cos(theta)], \
    [sin(theta), cos(theta)*cos(alpha), \
    -cos(theta)*sin(alpha), a*sin(theta)], \
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

'Funktion A05 - Transformation von K0 in K5'
def A05(theta1, theta2, theta3, theta4, theta5):
    
    T04 = A04(theta1, theta2, theta3, theta4)
    T45 = transformationsmatrix(theta5, d5, a5, alpha5)
    
    T05 = dot(T04,T45)
    
    return T05

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

'Funktion A15 - Transformation von K1 in K5'
def A15(theta2, theta3, theta4, theta5):
    
    T14 = A14(theta2, theta3, theta4)
    T45 = transformationsmatrix(theta5, d5, a5, alpha5)
    
    T15 = dot(T14, T45)
    
    return T15
    
'Funktion A45 - Transformation von K4 in K5'
def A45(theta5):
    
    T45 = transformationsmatrix(theta5, d5, a5, alpha5)
    
    return T45

'''Kinematische Vorwärtstransformation - Die Funktion berechnet aus den
Drehwinkeln theta_i die Transformationsvorschrift zur Überführung von 
K0 in K5. Die Spalten der Matrix (Format 4x4) entsprechen den Einheits-
vektoren von K5 sowie der Verschiebung von K5 in Bezug auf K0 in 0-Koord-
inaten (Lage und Orientierung von K5 in 0-Koordinaten). Abschließend werden 
die Spalten der Matrix den entsprechenden Vektoren zugeordnet, das Format 
der Vektoren auf 3x1 geändert und diese zurückgegeben.'''
def kinematik_vor(theta1, theta2, theta3, theta4, theta5):
    'Transformationsvorschrift zur Überführung von K0 in K5 (Format 4x4)'
    T05 = A05(theta1, theta2, theta3, theta4, theta5)
    T05 = around(T05, 5)
    
    'Matrix in 4 Spalten teilen und den Vektoren (Format 4x1) zuordnen'
    x5, y5, z5, P05 = hsplit(T05, 4)
    
    'Format der Vektoren von 4x1 auf 3x1 ändern'
    #Einheitsvektor von K5 in 0-Koordinaten: x5in0
    x, y, z, z4 = vsplit(x5, 4)
    x5in0 = vstack((x, y, z))
    #Einheitsvektor von K5 in 0-Koordinaten: y5in0
    x, y, z, z4 = vsplit(y5, 4)
    y5in0 = vstack((x, y, z))
    #Einheitsvektor von K5 in 0-Koordinaten: z5in0
    x, y, z, z4 = vsplit(z5, 4)
    z5in0 = vstack((x, y, z))
    #Verschiebung von K5 in Bezug auf K0 in 0-Koordinaten: P05in0
    x, y, z, z4 = vsplit(P05, 4)
    P05in0 = vstack((x, y, z))
    
    return x5in0, y5in0, z5in0, P05in0

'''Kinematische Rückwärtstransformation - Die Funktion berechnet 
aus den Einheitsvektoren von K5 sowie der Verschiebung von K5 in 
Bezug auf K0 in 0-Koordinaten (Format 4x1) (Lage und Orientierung
von K5 in 0-Koordinaten) die Drehwinkel theta_i und gibt diese 
zurück. Die Rückwärtstransformation erfolgt auf geometrischem Weg.'''
def kinematik_inv(x5in0, y5in0, z5in0, P05):
    
#    'Schritt 1 - Berechnung von Theta1'
#    print("x Wert:")
#    pprint(x5in0)
#    print("y Wert:")
#    pprint(y5in0)
#    print("z Wert:")
#    pprint(z5in0)
#    print("Drehung:")
#    pprint(P05)
    
    'Einheitsvektor x von K0 in 0-Koordinaten'
    x0in0 = array([[1], [0], [0], [0]]) 
    
    'Projektionsmatrix - Projektion auf x0, y0-Ebene'
    PrjAuf0 = array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
    
    'Berechnung von P35 in 0-Koordinaten'
    P35in0 = around(d5*z5in0, 5)
#    pprint(P35in0)
    
    'Berechnung von P03 in 0-Koordinaten'
    P03in0 = around(P05 - P35in0, 5) 
#    pprint(P03in0)
    'Projektion von P03 auf x0, y0-Ebene'
    P03PrjAuf0 = dot(PrjAuf0, P03in0)
    
    'Format anpassen'
    P03PrjAuf0[3] = 0
    
    'Berechnung von Theta1 - Skalarprodukt'
    theta1 = acos(sum(P03PrjAuf0*x0in0)/norm(P03PrjAuf0))
    
    'Schritt 2 - Berechnung von Theta2'
    
    'Einheitsvektor x von K1 in 1-Koordinaten'
    x1in1 = array([[1], [0], [0], [0]])
    
    'Transformationsmatrix A01 zur Überführung von K0 in K1'
    A01 = transformationsmatrix(theta1, d1, a1, alpha1)
    
    'Format anpassen'
    P03in0[3] = 1
    
    'Berechnung von P03 in 1-Koordinaten'
    P03in1 = around(dot(inv(A01), P03in0), 5)
    
    'Format anpassen'
    P03in1[3] = 0
    
    'Hilfswinkel berechnen - Cosinussatz'
    #Rundungsfehler korrigieren
    b = (a3**2 - a2**2 - norm(P03in1)**2)/(-2*a2*norm(P03in1))
    if b >= 1: b = 1
    elif b <= -1: b = -1
    #Hilfswinkel
    beta21 = acos(b)
    beta22 = acos(sum(P03in1*x1in1)/norm(P03in1))

    'Berechnung von Theta2'
    #Fallunterscheidung
    print(P03in1[0])
    print(P03in1[1])
    if P03in1[0] and P03in1[1] >= 0:
        theta2 = beta22 + beta21
    elif P03in1[0] >= 0 and P03in1[1] < 0:
        theta2 = beta22 - pi + beta21

    'Berechnung von Theta3'
    
    'Hilfswinkel berechnen - Cosinussatz'
    #Rundungsfehler korrigieren
    b = (norm(P03in1)**2 - a2**2 - a3**2)/(-2*a2*a3)
    if b >= 1: b = 1
    elif b <= -1: b = -1
    #Hilfswinkel
    beta3 = acos(b)
    
    'Berechnung von Theta3'
    theta3 = -(pi - beta3)
    
    'Berechnung von Theta4'
    
    'Einheitsvektor y von K3 in 3-Koordinaten'
    y3in3 = array([[0], [1], [0], [0]])
            
    'Transformationsmatrizen Aij zur Überführung von Ki in Kj'
    A12 = transformationsmatrix(theta2, d2, a2, alpha2)
    A23 = transformationsmatrix(theta3, d3, a3, alpha3)
    A02 = dot(A01, A12)
    A03 = dot(A02, A23)
    
    'Berechnung von P35 in 3-Koordinaten'
    P35in3 = around(dot(inv(A03), P35in0), 5)
    
    'Hilfswinkel berechnen - Skalarprodukt'
    beta4 = acos(sum(P35in3*y3in3)/norm(P35in3))
    
    'Brechnung von Theta4'
    #Fallunterscheidung
    if P35in3[0] >= 0:
        theta4 = pi - beta4
    elif P35in3[0] < 0:
        theta4 = -(pi - beta4)
    
    'Berechnung von Theta5'
    
    'Einheitsvektor x von K4 in 4-Koordinaten'
    x4in4 = array([[1], [0], [0], [0]])
    
    'Transformationsmatrizen Aij zur Überführung von Ki in Kj'
    A34 = transformationsmatrix(theta4, d4, a4, alpha4)
    A04 = dot(A03, A34)
    
    'Berechnung des Einheitsvektors x von K5 in 4-Koordinaten'
    x5in4 = around(dot(inv(A04), x5in0), 5)
        
    'Brechnung von Theta5 - Skalarprodukt'
    theta5 = acos(sum(x4in4*x5in4)/norm(x5in4))
    
    return theta1, theta2, theta3, theta4, theta5


'''Methode Eulertransformation - Als Eingabe werden drei Eulerwinkel erwartet.
Diese beschreiben die Rotation des Greifers im Raum. Die Transformation rechnet
die Eulerwinkel in drei Rotationswinkel, welche sich auf das raumfeste Koordsys
beziehen.'''
def Eulertransformation(a, b, g):
#    x5in0 = around(array([cos(x)*cos(z)-sin(x)*cos(y)*sin(z), \
#    sin(x)*cos(z)+cos(x)*cos(y)*cos(z), \
#    sin(x)*sin(y), 0]), 5)
#    y5in0 = around(array([sin(x)*cos(z)+cos(x)*cos(y)*sin(z), \
#    cos(x)*cos(y)*cos(z)-sin(x)*sin(z), \
#    -cos(x)*sin(y), 0]), 5)
#    z5in0 = around(array([sin(y)*sin(z), \
#    sin(y)*cos(z), \
#    cos(y), 0]), 5)
       
    
    'Berechnung x5in0'
    x5in0 = around(array([[cos(a)*cos(g)-sin(a)*cos(b)*sin(g)], \
    [sin(a)*cos(g)+cos(a)*cos(b)*sin(g)], \
    [sin(b)*sin(g)], [0]]), 5)
    
    'Berechnung y5in0'
    y5in0 = around(array([[-cos(a)*sin(g)-sin(a)*cos(b)*cos(g)], \
    [-sin(a)*sin(g)+cos(a)*cos(b)*cos(g)], \
    [sin(b)*cos(g)], [0]]), 5)
    
    'Berechnung z5in0'
    z5in0 = around(array([[sin(a)*sin(b)], \
    [-cos(a)*sin(b)], \
    [cos(b)], [0]]), 5)    
    
    return x5in0, y5in0, z5in0


    
'''Methode 
p1, p2, p3, ist die Verschiebung im 3D Raum (x,y,z)
p4, p5, p6 sind Eulerwinkel
Methode steuerung_fern muss vorher ausgerührt werden.'''
def steuerung_fern_vektor():
#        print("Ankommender Vektor")
        
    x_urs = 0
    y_urs = 48+165
    z_urs = 31
    if x_urs == 0: a_urs = 3.1415
    else: a_urs = atan((y_urs/x_urs)*3.1415)
    
    b_urs = atan((z_urs-31)/sqrt(y_urs^2+x_urs^2)*3.1415)+3.1415/2
    g_urs = 3.1415/2
    print('b_urs: ', b_urs)
    
    x_end = x_urs    
    y_end = y_urs+50
    z_end = z_urs+50
    
    if x_end == 0: a_end = 3.1415
    else: a_end = atan((y_end/x_end)*3.1415)
    b_end = atan((z_end-31)/sqrt(y_end^2+x_end^2)*3.1415)+3.1415/2
    g_end = g_urs
    
    x5in0, y5in0, z5in0 = \
    Eulertransformation(a_end, b_end, g_end)
    
    print('x5in0:')
    print(around(x5in0,3))
    print('y5in0:')
    print(around(y5in0,3))
    print('z5in0:')
    print(around(z5in0,3))
    P05 = array([[x_end],[y_end],[z_end],[0]])
    
    theta1, theta2, theta3, theta4, theta5 = kinematik_inv\
    (x5in0, y5in0, z5in0, P05 )

    pwm1, pwm2, pwm3, pwm4, pwm5, \
    pwm6 = ingrad_Echtzeit\
    (theta1, theta2, theta3, theta4, theta5)        
    
    print(pwm1, pwm2, pwm3, pwm4, pwm5, pwm6)
    
    
def ingrad_Echtzeit(theta1, theta2, theta3, theta4, theta5):
   

    'Datentyp array in float konvertieren'
    theta1 = float(theta1)
    theta2 = float(theta2)
    theta3 = float(theta3)
    theta4 = float(theta4)
    theta5 = float(theta5)
    
    'Transformation der Winkeln in Grad'
    pwm1 = 180-int(theta1/pi*180)
    pwm2 = int(theta2/pi*180)
    pwm3 = 180+int(theta3/pi*180)-8
    pwm4 = int(theta4/pi*180)+9
    pwm5 = int(theta5/pi*180)
    
    if pwm4 < 0:
        pwm4 = 0
    if pwm5 > 180:
        pwm5 = 180
    
    pwm6 = 90    
    return pwm1, pwm2, pwm3, pwm4, pwm5, pwm6

steuerung_fern_vektor()
    
    