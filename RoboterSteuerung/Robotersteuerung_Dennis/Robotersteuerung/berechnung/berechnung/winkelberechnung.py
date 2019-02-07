'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul winkelberechnung enthält die Funktion winkel_berechnen. 
Die Funktion berechnet den Winkel den ein Ortsvektor (x, y) mit
der x-Achse einschließt. In Abhängigkeit der x- und y-Koordinaten
wird der Vektor dem entsprechenden Quadranten zugeordnet und der 
zugehörige Winkel in den Intervallen [0, pi/2[ für den 1.Quadranten, 
[pi/2, pi[ für den 2.Quadranten, [pi, 3*pi/2[ für den 3.Quadranten 
und [3*pi/2, 2*pi[ für den 4.Quadranten berechnet und zurückgegeben. 
'''

'Modul importieren'
from math import atan, pi

'Funktion winkel_berechnen'
def winkel_berechnen(x, y):
    
    #Sonderfall 1
    if x == 0 and y >= 0:
        phi = pi/2
    #Sonderfall 2
    elif x == 0 and y < 0:
        phi = 3*pi/2
    #1.Quadrant
    elif x > 0 and y >= 0:
        phi = atan(y/x)
    #2.Quadrant
    elif x < 0 and y >= 0:
        phi = pi - atan(y/-x)
    #3.Quadrant
    elif x < 0 and y < 0:
        phi = pi + atan(-y/-x)
    #4.Quadrant
    elif x > 0 and y < 0:
        phi = 2*pi - atan(-y/x)
    
    return phi