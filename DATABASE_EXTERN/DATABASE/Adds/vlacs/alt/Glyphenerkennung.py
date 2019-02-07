# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:35:45 2017

@author: SMP II

Programm zum Erkennen derGestalt des Objektes, Prüfung ob ein bestimmtes Muster vorhanden ist und Rückgabe der Eckpunkte.
"""

import cv2
from Mustererkennung import *
from Glyphdatenbank import *



def glyphe_erkennen(Bild):
    
    
    
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
                
                
                glyphmuster = glyphmuster_erkennen(grau, annaeherung.reshape(4,2))
                
                #Ausgabe
                print("Es hat 4 Ecken")
                #Ausgabe des Musters
                print(glyphmuster)
                
                
                
                gefunden = musterabgleich(glyphmuster)
                #Abgleich mit der Datenbank, ob die Glyphe der gesuchten Glyphe entspricht
                
                if gefunden == True:
                    
                    print("gefunden")
                   
                    #Gibt die 4 Eckpunkte wieder
                    return (True, annaeherung.reshape(4,2))
                   
                    #Schleife wird unterbrochen
                    break
                
            return (False, [[1,1],[1,1]])