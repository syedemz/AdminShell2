# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 16:35:12 2017

@author: Christian Plesker


Programm zum Erkennen der Gestalt des Objektes, Prüfung ob ein bestimmtes Muster vorhanden kontrollieren des Musters.
"""

import cv2
from vlacs.Mustererkennung import glyphmuster_erkennen
from vlacs.Glyphdatenbank import musterabgleich



def glyphmuster(Bild):
    
    
    
    #Ob die Glyphe gefunden wurde 
    gefunden = False
    
    #Das Bild grau konvertieren
    grau = cv2.cvtColor(Bild, cv2.COLOR_BGR2GRAY)

    #Kanten im Bild bestimmen
    kanten = cv2.Canny(Bild, 35, 125)
    
    #Kontouren finden
    _, konturen , _ = cv2.findContours(kanten, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
   
    #Konturen sortieren größte Kontur zu erst
    konturen = sorted(konturen, key=cv2.contourArea, reverse=True)[:10]
    
    #Schleife zur Suche in den Konturen nach einer Glyphe
    for kontur in konturen:
        
            # Form des Objektes prüfen
            #arcLength(linie, geschlossen) gibt an ob, die From geschlossen ist
            umfang = cv2.arcLength(kontur, True)

            #cv2.approxPolyDP(Linie, Wie weit darf die Linie von dem Orginal weg sein, ist sie geschlossen)
            annaeherung = cv2.approxPolyDP(kontur, 0.01*umfang, True)
            
            
            #Abfrage ob das die Kontur 4 Ecken besitzt
            if len(annaeherung) == 4:
                
                #Glyphmuster auslesen
                glyphmuster = glyphmuster_erkennen(grau, annaeherung.reshape(4,2))
           
                
                gefunden = musterabgleich(glyphmuster)
                #Abgleich mit der Datenbank, ob die Glyphe der gesuchten Glyphe entspricht
                
                if gefunden != False:
                   
                    
                    #Gibt den Namen des Gefunden Roboters zurück
                    return True, gefunden, annaeherung.reshape(4,2)
                
                else: 
                
                    return False, False, "keine Glyphe"
    return False, False, "keine Glyphe"