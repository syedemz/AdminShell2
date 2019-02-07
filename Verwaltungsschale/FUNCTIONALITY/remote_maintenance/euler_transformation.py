'Module importieren'
from math import acos, asin, cos, pi, sin
from numpy import around, array, dot, hsplit, vsplit

'''Funktion robot_control - Euler Transformation gamma = (psi, theta, phi) um
z0, x1, z2'''
def robot_control(x1, y1, z1, x4, y4, z4, a1, a2, a3, b1, c1, grab_position):
    
    #Transformationsmatrizen
    T01 = array([[cos(b1), sin(b1), 0], [-sin(b1), cos(b1), 0], [0, 0, 1]])
    T12 = array([[1, 0, 0], [0, cos(a1), -sin(a1)], [0, sin(a1), cos(a1)]])
    T23 = array([[1, 0, 0], [0, cos(a1-a2), sin(a1-a2)], 
                 [0, -sin(a1-a2), cos(a1-a2)]])
    T34 = array([[1, 0, 0], [0, cos(a2-a3), sin(a2-a3)], 
                 [0, -sin(a2-a3), cos(a2-a3)]])
    T45 = array([[cos(c1), 0, sin(c1)], [0, 1, 0], [-sin(c1), 0, cos(c1)]])
    
    T02 = dot(T01, T12)
    T03 = dot(T02, T23)
    T04 = dot(T03, T34)
    T05 = dot(T04, T45)
    print(around(T05, 3))

    'Eintrag T05_33 = cos(theta)'
    zeilen = vsplit(T05, 3)
    spalten = hsplit(zeilen[2], 3)
    T05_33 = float(spalten[2])
    
    theta = round(acos(T05_33), 6)
    
    'Singularität'
    if theta == 0 and b1 == 0:
        psi = 0
        theta = 0
        phi = 0
        
    elif theta == 0 and b1 != 0:
        psi = b1
        theta = 0
        phi = 0
        
    else: 
        
        'Python kann nicht rechnen'
        sinus_theta = round(sin(theta), 6)
        if sinus_theta > 1: sinus_theta = 1
        elif sinus_theta < -1: sinus_theta = -1
    
        'Eintrag T05_31 = sin(theta)*sin(phi) und T05_32 = sin(theta)*cos(phi)'
        T05_31 = float(spalten[0])
        T05_32 = float(spalten[1])
        phi11 = round(asin(T05_31/sinus_theta), 6)
        phi12 = round(pi - phi11, 6)        
        phi21 = round(acos(T05_32/sinus_theta), 6)
        phi22 = -phi21
        print(phi11, phi12, phi21, phi22)
        if phi11 == phi21 or phi11 == phi22:
            phi = phi11
            print('hu')
        elif phi12 == phi21 or phi12 == phi22:
            phi = phi12
            print('huhu')
        elif phi11 == 0 and phi12 == round(pi, 6):
            phi = 0
            print('huhuhuhuhu')
        
        'Eintrag T05_13 = sin(psi)*sin(theta) und T05_23 = -cos(psi)*sin(theta)'
        spalten = hsplit(zeilen[0], 3)
        T05_13 = float(spalten[2])
        spalten = hsplit(zeilen[1], 3)
        T05_23 = float(spalten[2])
        psi11 = round(asin(T05_13/sinus_theta), 5)  
        psi12 = round(pi - psi11, 5)
        psi21 = round(acos(-T05_23/sinus_theta), 5)
        psi22 = -psi21
        
        if psi11 == psi21 or psi11 == psi22:
            psi = psi11
        elif psi12 == psi21 or psi12 == psi22:
            psi = psi12
        elif psi11 == 0 and psi12 == round(pi, 4):
            psi = 0
    
    'Tool Center Point'
    tcp = array([[x4 - x1], [y4 - y1], [z4 - z1]])
    
    'Euler Winkel'
    euler_rad = array([[psi, theta, phi]])
    euler_grad = around(euler_rad*180/pi, 3)
    
    'Greiferzustand'
    grab_position = array([[grab_position]])

    return tcp, euler_rad, euler_grad, grab_position
    
    
'Testaufruf'
tcp, euler_rad, euler_grad, grab_position = \
robot_control(0, 0, 0, 100, 100, 100, a1 = pi/2, a2 = pi/2, a3 = 0, 
              b1 = pi/2, c1 = pi, grab_position = 1)
print(tcp)
print(euler_rad, euler_grad)
print(grab_position)