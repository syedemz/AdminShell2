# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 15:37:53 2017

@author: Christian Plesker
"""


from math import atan, acos, degrees
from numpy import sqrt
from vlacs.Punkte_sortieren import sortieren

"""
Funktion zum Bestimmen der Lage eines Quadrates mit der Länge 5mmx5mm

"""

def glyphen_winkel(objektpunkte):

    """
    Objektpunkte in der selben Reohnfolge sortieren

    """

    #objektpunkte in die selbe Reihnfolge sortieren
    punkte = sortieren(objektpunkte)
    

    Eckpunkt_rechts_oben = punkte[2]
    Eckpunkt_links_oben = punkte[3]
    Eckpunkt_links_unten = punkte[0]
    Eckpunkt_rechts_unten = punkte[1]
    
    """
    Bestimmung der Rotation der Glyphe:
        -Berechnung der linken und rechten Seite --die größere Seite bestimmen
        -Berechnung der unteren und oberen Seite --den Wert der beiden Seiten mitteln
        -Das Verhältnis von der gemittelten horizontalen Länge zur längsten vertikalen Seite
        -Winkel mittels arcosinus(Verhältnis) berechnen 
        -Winkel umrechnen in Grad und wiedergeben
        
    """
    
    
    linke_vertikale_Kante = sqrt(((Eckpunkt_links_oben[0] - Eckpunkt_links_unten[0] )**2)+((Eckpunkt_links_oben[1] - Eckpunkt_links_unten[1])**2))
    rechte_vertikale_Kante = sqrt(((Eckpunkt_rechts_oben[0] - Eckpunkt_rechts_unten[0] )**2)+((Eckpunkt_rechts_oben[1] - Eckpunkt_rechts_unten[1])**2))
    
    max_vertikale_Kante = max(linke_vertikale_Kante, rechte_vertikale_Kante)
    
    untere_Kante = sqrt(((Eckpunkt_links_unten[0] - Eckpunkt_rechts_unten[0] )**2)+((Eckpunkt_links_unten[1] - Eckpunkt_rechts_unten[1])**2))
    obere_Kante = sqrt(((Eckpunkt_rechts_oben[0] - Eckpunkt_links_oben[0] )**2)+((Eckpunkt_rechts_oben[1] - Eckpunkt_links_oben[1])**2))
    
    gemittelte_horizontale_Kante = (untere_Kante + obere_Kante)/2
    
    verhältnis_kanten = round((gemittelte_horizontale_Kante / max_vertikale_Kante),3)
    
    #Den Grenzfall ausschließen, dass durch Abweichungen in der Erkennung der Eckpunkte die Horizontalkante größer ist, als die vertikale Kante
    if verhältnis_kanten >= 1:
            verhältnis_kanten = 1

    #Winkel in rad berechnen
    winkel = acos(verhältnis_kanten)
    
    
    #umrechnung in Grad
    winkel = degrees(winkel)
    
    
    return winkel




"""
Lage der Glyhe in x-Richtung im Bild bestimmen 
    -Mittelpunkt (x-Koordinate) der Glyphe bestimmen
    -Mittelpunkt des Bildes bestimmen
    -Verschiebung der Glyphe berechnen

"""

def lagebestimmung(Objektpunkte, Bild):
    
        #Punkte sortieren
        punkte = sortieren(Objektpunkte)
    
        #Punkte einzelnd hinterlegen
        eckpunkt_rechts_oben = punkte[2]
        eckpunkt_links_oben = punkte[3]
        eckpunkt_links_unten = punkte[0]
        eckpunkt_rechts_unten = punkte[1]
        
        #Mittelpunkt der oberen und unteren Kante berechnen (nur die x-Koordinaten)
        mittelpunkt_x_oben = (eckpunkt_links_oben[0] + eckpunkt_rechts_oben[0])/2
        mittelpunkt_x_unten = (eckpunkt_links_unten[0] - eckpunkt_rechts_unten[0])/2
        
        #Mittelpunkt der Glyphe (x-Koordinate)
        gemittelt_x_position = (mittelpunkt_x_oben + mittelpunkt_x_unten)/2
        
        #Mittelpunkte des Bildes
        mittelpunkt_x = Bild.shape[1]/2
        
        #Verschiebung der Glyphe zum Mittelpunkt
        verschiebung_x = gemittelt_x_position - mittelpunkt_x
        
        
        #Mittelpunkt y-Koordinate des Bildes bestimmen
        mittelpunkt_y = Bild.shape[0]/2
        
        #Winkel des Translationsvektor zur Glyphe auf der x-z-Ebene
        winkel_h = atan(verschiebung_x/mittelpunkt_y)
        
        return winkel_h
    