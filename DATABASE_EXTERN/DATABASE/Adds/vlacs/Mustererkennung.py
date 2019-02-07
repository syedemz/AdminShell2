# -*- coding: utf-8 -*-
"""
Created on Tue May 16 14:54:47 2017

@author: Christian Plesker

Funktion zum erkennen des Musters der Glyphe
"""

import cv2
from numpy import sqrt, array
from vlacs.Punkte_sortieren import sortieren

#Funktion zum erkennen der Glyphe
def glyphmuster_erkennen(bild, bild_eckpunkte):
    
    """
    Bestimmung der Eckpunkte, die maximale Breite und die Höhe
    der Glyphe
    
    """
        
    #Ort der bestehenden Bildeckpunkte bestimmen
    bild_eckpunkte_sortiert = sortieren(bild_eckpunkte)

    #Trennen der einzelnen Punkte
    links_oben = bild_eckpunkte_sortiert[0]
    rechts_oben = bild_eckpunkte_sortiert[1]
    rechts_unten = bild_eckpunkte_sortiert[2]
    links_unten = bild_eckpunkte_sortiert[3]

    #Maximale Breite und Höhe bestimmen
    breite_oben = sqrt( ((rechts_oben[0] - links_oben[0])**2) + ((rechts_oben[1] - links_oben[1])**2) )      #Breite oben bestimmen
    breite_unten = sqrt( ((rechts_unten[0] - links_unten[0])**2) + ((rechts_unten[1] - links_unten[1])**2) ) #Breite unten bestimmen
    max_breite = max(int(breite_oben), int(breite_unten))     #Maximale erkannte Breite der Glyphenfläche
    
    höhe_rechts = sqrt( ((rechts_oben[0] - rechts_unten[0])**2) + ((rechts_oben[1] - rechts_unten[1])**2))   #Höhe rechts bestimmen
    höhe_links = sqrt( ((links_oben[0] - links_unten[0])**2) + ((links_oben[1] - links_unten[1])**2) )    #Höhe links bestimmen
    max_höhe = max(int(höhe_rechts), int(höhe_links))     #Maximale erkannte Höhe der Glyphenfläche
    
    #Neue Eckpunkte mit den Maximalwerten bestimmen
    neue_punkte = array([[0, 0], [max_breite, 0], [max_breite, max_höhe], [0 , max_höhe]], dtype="float32") #Maximale Punkte bestimmen
    
    
    """
    Transformation der verdrehten Glyphe auf eine Ebene
    
    """
    #Glyphe auf eine Ebene projezieren, Verdrehungen aufheben

    transformationsmatrix = cv2.getPerspectiveTransform(bild_eckpunkte_sortiert, neue_punkte) #Transformationsmatrix von den Orignaleckpunkten zu den Maximaleckpunkte berechnen
    transformierte_glyphe = cv2.warpPerspective(bild, transformationsmatrix, (max_breite, max_höhe))
    
    """
    Unterteilung der Raster
    Glyphenfläche wird in 100x100 Pixel umgewandelt
    
    """
    #Die transformierte Glyphenfläche in 100x100 Pixel unterteilen (Raster)
    
    neue_pixelanzahl = 100 # neue Anzahl an Pixeln
    x , y = transformierte_glyphe.shape
    
    transformierte_glyphe = cv2.resize(transformierte_glyphe, (int(neue_pixelanzahl), int(neue_pixelanzahl)))

    """
    Bestimmung des Glyphenmusters
    
    """
    #Die Glyphe in ein 3x3 Raster unterteilen, da die Glyphe 3x3 Punkte enthält
    Glyphmuster = [] # Eine leeres Raster erstellen
    
    
    
    
    #Mittelpunte der 3x3 Punkte in das Raster einfügen
    #Zeile 1
    Glyphmuster.append(transformierte_glyphe[20,20])
    Glyphmuster.append(transformierte_glyphe[20,50])
    Glyphmuster.append(transformierte_glyphe[20,80])
    #Zeile 2
    Glyphmuster.append(transformierte_glyphe[50,20])
    Glyphmuster.append(transformierte_glyphe[50,50])
    Glyphmuster.append(transformierte_glyphe[50,80])
    #Zeile 3
    Glyphmuster.append(transformierte_glyphe[80,20])
    Glyphmuster.append(transformierte_glyphe[80,50])
    Glyphmuster.append(transformierte_glyphe[80,80])
    
    #Bestimmen eines Farbgrenzwertesab dem das Muster 1 wird
    farbgrenzwert = 20
    print(Glyphmuster)
    
    #Durchlaufen der Rasterpunkte 
    #Wenn der Farbgrenzwert überschritten wird, wird der Rasterpunkt auf 1 gesetzt
    #Fals nicht 0
    for punkt in range(0,9):
        
        if Glyphmuster[punkt] >= farbgrenzwert:
            Glyphmuster[punkt]=1
        
        else:
            Glyphmuster[punkt]=0
        
        
    return Glyphmuster