from Parameter import denavit_hartenberg
from math import cos, sin, pi, acos
from numpy import around, array, dot, hsplit, vsplit, vstack
from numpy.linalg import inv, norm



from numpy import sum

from pprint import pprint


#'Denavit-Hartenberg-Parameter laden'
d1, d2, d3, d4, d5, a1, a2, a3, a4, a5, \
alpha1, alpha2, alpha3, alpha4, alpha5 = denavit_hartenberg()

'''Funktion transformationsmatrix - 
Denavit-Hartenberg-Transformationsmatrix'''
def transformationsmatrix(theta, d, a, alpha):
    
    T = array([[cos(theta), -sin(theta)*cos(alpha), sin(theta)*sin(alpha), a*cos(theta)],   \
               [sin(theta), cos(theta)*cos(alpha), -cos(theta)*sin(alpha), a*sin(theta)],   \
               [0, sin(alpha), cos(alpha), d], [0, 0, 0, 1]])
    
    return T

#'Funktion A01 - Transformation von K0 in K1'
def A01(theta1):
    
    T01 = transformationsmatrix(theta1, d1, a1, alpha1)
    
    return T01

#'Funktion A02 - Transformation von K0 in K2'
def A02(theta1, theta2):
    
    T01 = A01(theta1)
    T12 = transformationsmatrix(theta2, d2, a2, alpha2)
    
    T02 = dot(T01, T12)
        
    return T02
    
#'Funktion A03 - Transformation von K0 in K3'
def A03(theta1, theta2, theta3):
    
    T02 = A02(theta1, theta2)
    T23 = transformationsmatrix(theta3, d3, a3, alpha3)
    
    T03 = dot(T02,T23)
    
    return T03
    
#'Funktion A04 - Transformation von K0 in K4'
def A04(theta1, theta2, theta3, theta4):
    
    T03 = A03(theta1, theta2, theta3)
    T34 = transformationsmatrix(theta4, d4, a4, alpha4)
        
    T04 = dot(T03,T34)
    
    return T04


#'Funktion A12 - Transformation von K1 in K2'
def A12(theta2):
     
    T12 = transformationsmatrix(theta2, d2, a2, alpha2)
    
    return T12
    
#'Funktion A13 - Transformation von K1 in K3'
def A13(theta2, theta3):
     
    T12 = A12(theta2)
    T23 = transformationsmatrix(theta3, d3, a3, alpha3)
    
    T13 = dot(T12, T23)
    
    return T13
    
#'Funktion A14 - Transformation von K1 in K4'
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

def kinematik_vor(theta1, theta2, theta3, theta4):
    #'Transformationsvorschrift zur Überführung von K0 in K5 (Format 4x4)'
    T04 = A04(theta1, theta2, theta3, theta4)
    
    T04 = around(T04, 5)
    
    #'Matrix in 4 Spalten teilen und den Vektoren (Format 4x1) zuordnen'
    x1, y1, z1, P01 = hsplit(T04, 4)
    
    #'Format der Vektoren von 4x1 auf 3x1 ändern'
    #Einheitsvektor von K4 in 0-Koordinaten: x4in0
    x, y, z, z4 = vsplit(x1, 4)
    x4in0 = vstack((x, y, z))
    #Einheitsvektor von K4 in 0-Koordinaten: y4in0
    x, y, z, z4 = vsplit(y1, 4)
    y4in0 = vstack((x, y, z))
    #Einheitsvektor von K4 in 0-Koordinaten: z4in0
    x, y, z, z4 = vsplit(z1, 4)
    z4in0 = vstack((x, y, z))
    #Verschiebung von K4 in Bezug auf K0 in 0-Koordinaten: P04in0
    x, y, z, z4 = vsplit(P01, 4)
    P04in0 = vstack((x, y, z))
    
    
    
    return x4in0, y4in0, z4in0, P04in0


winkelG1 = 90
winkelG2_standard = 180 
winkelG3_standard = 0
winkelG4_standard = 90
theta1 = (pi-(pi*winkelG1/180))
theta2 = ((winkelG2_standard)/180)*pi
theta3 = (-pi*(172/180) +pi*(winkelG3_standard/180))
theta4 = (-pi*(8/180)+ pi*(winkelG4_standard/180))

print (theta1)
print (theta2)
print (theta3)
print (theta4)
print("basdfklajsdflkasd")



a4in4 = array(([0], [0], [68], [0]))
ain0 = around(dot(A04(theta1, theta2, theta3, theta4),a4in4), 3)
x, y,z, zeile4 = vsplit(ain0, 4)
ain0_1 = vstack((x,y,z))


x1, y1, z1 ,p1 = kinematik_vor(theta1, theta2, theta3, theta4)


p1= p1 + ain0_1

print(p1)

winkelG1 = 90
winkelG2_standard = 180 
winkelG3_standard = 10
winkelG4_standard = 90

theta1 = (pi-(pi*winkelG1/180))
theta2 = ((winkelG2_standard)/180)*pi
theta3 = (-pi*(172/180)+pi*(winkelG3_standard/180))
theta4 = (-pi*(8/180)+pi*(winkelG4_standard/180))




a4in4 = array(([0], [0], [68], [0]))
ain0 = around(dot(A04(theta1, theta2, theta3, theta4),a4in4), 3)
x, y,z, zeile4 = vsplit(ain0, 4)



ain0_2 = vstack((x,y,z))



x2,y2,z2,p2 = kinematik_vor(theta1, theta2, theta3, theta4)

#p2 = p2 +ain0_2
#p1 = p1 +ain0_1

print(p2-p1)

x = p1[0]
y = p1[1]
z = p1[2]
o = [0]

p1 = array((x, y, z,o))


x = x1[0]
y = x1[1]
z = x1[2]
o = [0]
x2 = array((x, y,z,o))

x = y1[0]
y = y1[1]
z = y1[2]
o = [0]
y2 = array((x, y,z,o))

x = z1[0]
y = z1[1]
z = z1[2]
o = [0]
z2 = array((x, y,z,o))






def kinematik_inv(x4in0, y4in0, z4in0, P04):
    
    P04 = P04 - (z4in0 * 68)
    
    'Einheitsvektor x von K0 in 0-Koordinaten'
    x0in0 = array([[1], [0], [0], [0]]) 
    
    'Projektionsmatrix - Projektion auf x0, y0-Ebene'
    PrjAuf0 = array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]])
    
    'Berechnung von P34 in 0-Koordinaten'
    P34in0 = around(d4*z4in0, 16)
#    pprint(P35in0)
    'Berechnung von P03 in 0-Koordinaten'
    P03in0 = around(P04 - P34in0, 16) 
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
    P03in1 = around(dot(inv(A01), P03in0), 16)
    
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
    P34in3 = around(dot(inv(A03), P34in0), 16)


    'Hilfswinkel berechnen - Skalarprodukt'
    zahl = norm(P34in3)

        
    beta4 = acos(sum(P34in3*y3in3)/zahl)

    'Brechnung von Theta4'
    #Fallunterscheidung
    if P34in3[0] >= 0:
        theta4 = pi - beta4
        
    elif P34in3[0] < 0:
        theta4 = -(pi - beta4)
   
    
    

    return theta1, theta2, theta3, theta4



t1,t2,t3,t4 =kinematik_inv(x2,y2,z2, p1)

print(t1)
print(t2)
print(t3)
print(t4)
