'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul parameter enthält die Funktion denavit_hartenberg. Zur
Beschreibung der Roboterkinematik werden nach den Vorgaben der
Denavit-Hartenberg-Konvention ein Inertialsystem und vier weitere
körperfeste Koordinatensysteme festgelegt. Die Denavit-Hartenberg-
Transformationsmatrix überführt ein Koordinatensystem K_i-1 in ein 
System K_i. Die Matrix ist eine Funktion von vier Parametern. Es 
handelt sich um zwei Translationsparameter (d_i und a_i) sowie um 
zwei Rotationsparameter (theta_i und alpha_i). Im Fall von Rot-
ationsgelenken sind die drei Parameter d_i, a_i und alpha_i 
konstant sowie der vierte Parameter theta_i variabel. Nach dem 
Aufruf der Funktion werden die Parameter zurückgegeben. 
'''

'Modul importieren'
from math import pi

'Funktion denavit_hartenberg'
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