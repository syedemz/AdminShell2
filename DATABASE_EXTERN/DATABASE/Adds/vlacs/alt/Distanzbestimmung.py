# -*- coding: utf-8 -*-
"""
Created on Fri May 12 13:24:45 2017

@author: Christian Plesker
"""

import cv2
import numpy as np
import math
from Punkte_sortieren import *

"""
Funktion zur Bestimmung der Entfernung des Objektes zur Kamera

"""


def distanzbestimmung(Bild,Eckpunkte):
    
    #Punkte sortieren
    punkte = sortieren(Eckpunkte)
    
    #Punkte einzeln hinterlegen
    Eckpunkt_rechts_oben = punkte[2]
    Eckpunkt_links_oben = punkte[3]
    Eckpunkt_links_unten = punkte[0]
    Eckpunkt_rechts_unten = punkte[1]
    
    #Länge der rechten und linken vertikalen Kante in Pixel
    rechte_kante_vertikal = np.sqrt(((Eckpunkt_rechts_oben[0] - Eckpunkt_rechts_unten[0] )**2)+((Eckpunkt_rechts_oben[1] - Eckpunkt_rechts_unten[1])**2))
    linke_kante_vertikal = np.sqrt(((Eckpunkt_links_oben[0] - Eckpunkt_links_unten[0] )**2)+((Eckpunkt_links_oben[1] - Eckpunkt_links_unten[1])**2))
    
    #Hoehe der Glyhpe mitteln mit den beiden im Bild bestimmten Kanten
    gemittelte_hoehe_glyphe= (rechte_kante_vertikal + linke_kante_vertikal)/2
    
    #Breite der Glyphe(realer Wert) in cm
    objekt_breite = 5
    
    #Experimentell bestimmte focalLength
    focalLength = 806.33129883

    #Distanz berechnen in cm
    distanz = (objekt_breite*focalLength)/abs(gemittelte_hoehe_glyphe)
    
    #Beschriftung auf dem Bild mit der Distanz
    cv2.putText(Bild, "X = %.2fcm" % (distanz),(Bild.shape[1] - 600, Bild.shape[0] - 60), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    
    return(distanz)