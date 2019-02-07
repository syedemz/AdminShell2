'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul winkelnormierung enthält die Funktion winkel_normieren.
Die Funktion normiert einen beim Funktionsaufruf übergebenen Winkel
auf das Intervall [0, 2*pi] und gibt den normierten Winkel zurück.
'''

'Modul importieren'
from math import pi

'Funktion winkel_normieren'
def winkel_normieren(phi):

    if phi < 0:
        phi = 2*pi + phi
    elif phi > 2*pi:
        phi = phi - 2*pi
        
    return phi