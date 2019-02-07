# -*- coding: utf-8 -*-
"""
Created on Thu Apr 27 13:00:29 2017

@author: Christian Plesker

Hauptprogramm zum Erkennen von Glyphen, Rotation und Distanzbestimmung

Das Programm bestimmt Mittelwerte der Distanz und Winkel aus 25 Messungen

"""

#Laden der benötien Bibliotheken
import cv2
import numpy as np
from Kamera import Kamera
from GruenFilter import *
from Glyphenerkennung import *
from Winkelberechnung import *
from Distanzbestimmung import *

def glyphe_lokalisieren():
        
    """
    Eingabe der Grundparameter
    -Anzahl der Messungen
    -Abreitszustand (Kontrollwert ob, ein abbruch vorliegt)
    -Kammeranummer (0 = default, 1,2,3....je nach dem welche benutz werden soll, fals mehrere angeschlossen sind)
    """
    #Anzahl der Messungen aus denen gemittelt wird
    messungen = 25
    
    #Erstellen eines Arrays in dem später die Messwerte gespeichert werden
    position=np.zeros((messungen +1,7),np.float32)   
     
    #Der Arbeitszustand zurücksetzten
    arbeitszustand = True
        
    #Festlegen der Kamera:
    # 0 - Standartkamera, 1/2/3... - zusätzlich, angeschlossene Kameras 
    kameranummer= 0
    

    """
    Start des Programmes 
    -Kamera starten 
    
    """
    #Objekt Kamera instanzieren
    kamera = Kamera(kameranummer)
    
    #Kamera starten
    kamera.start()
    
    
    
    #Anzahl der Wiederholungen1 zurücksetzten
    wiederholung1 = 0
    
    #Schlefe für die Messungen/Berechnungen
    
    while wiederholung1 <= messungen:
    
        
        k = cv2.waitKey(100) # Drücke Esc zum verlassen
        if k == 27 or arbeitszustand == False:
                arbeitszustand = False
                break     
    
        
        while True:
            
            k = cv2.waitKey(100) # Drücke Esc zum verlassen
            if k == 27 or arbeitszustand == False:
                arbeitszustand = False
                break        
            
            #Bild schießen und hinter Bild hinterlegen
            bild = kamera.aktuelles_bild_erhalten()
            
            #Bild filtern und grüne Farbe heraussuchen
            gruen = gruen_filtern(bild)
            
            #Anzahl der Wiederholungen2 zurücksetzten
            wiederholung2 = 0
            #Wenn kein Gruen in dem Bild gefunden wird
            if gruen.any() == False:
                
               
                
                #Erneute Bildaufnahme-Schleife bis etwas grünes gefunden wird oder Abbruch der Schleife durch zu viele Wiederholungen(50+)
                while wiederholung2 <= 50:
                    
                    k = cv2.waitKey(100) # Drücke Esc zum verlassen
                    if k == 27 or arbeitszustand == False or wiederholung2 >= 50:
                        arbeitszustand = False
                        
                        break    
                    
                    print("Bild enthält kein gruen")
                
                     #Bild schießen und hinter Bild hinterlegen
                    bild = kamera.aktuelles_bild_erhalten()
                    
                    #Bild filtern und grüne Farbe heraussuchen
                    gruen = gruen_filtern(bild)
                    
                    #cv2.waitKey(1000)
                    
                    #Abbruchbedinung fals gruen gefunden wird
                    if gruen.any() == True:
                        break
                    
                    #Die Wiederholung2 um 1 weiterzählen
                    wiederholung2 = wiederholung2 + 1
                    
                    
            k = cv2.waitKey(100) # Drücke Esc zum verlassen
            if k == 27 or arbeitszustand == False or wiederholung2 >= 50:
                arbeitszustand = False
                
                break    
            
            #cv2.waitKey(100)
            
            #Finden von Glyphen, Abgleich des Glyphenmusters, Wiedergabe der Kontur, welche die richtige Glyhe ist
            gefunden , glypheneckpunkte = glyphe_erkennen(gruen)
        
    
            
            if gefunden == True:
                print("funtioniert")
                
        
                break
            
        if arbeitszustand == False:
            break
        
        else:
            
            winkel_z = glyphen_winkel(glypheneckpunkte)
            winkel_h = lagebestimmung(glypheneckpunkte,bild)
    
            distanz= distanzbestimmung(bild,glypheneckpunkte)
            
                #Punkte sortieren
            punkte = sortieren(glypheneckpunkte)
            
            #Punkte einzeln hinterlegen
            Eckpunkt_rechts_oben = punkte[2]
            Eckpunkt_links_oben = punkte[3]
            Eckpunkt_links_unten = punkte[0]
            Eckpunkt_rechts_unten = punkte[1]
            
            #Mittelpunkkoordinaten bestimmen
            mittelpunkt_x = (Eckpunkt_rechts_oben[0] + Eckpunkt_links_oben[0] + Eckpunkt_links_unten[0] + Eckpunkt_rechts_unten[0])/4
            mittelpunkt_y = (Eckpunkt_rechts_oben[1] + Eckpunkt_links_oben[1] + Eckpunkt_links_unten[1] + Eckpunkt_rechts_unten[1])/4
            
            cv2.drawContours(bild, [glypheneckpunkte], 0, (0,255,0), 3)
            cv2.imshow('1', bild)
            
            #ablegen aller Variablen in einem array
            
            position[wiederholung1,0]= winkel_z
            position[wiederholung1,1]= winkel_h
            position[wiederholung1,2]= distanz
            position[wiederholung1,3]= mittelpunkt_x
            position[wiederholung1,4]= mittelpunkt_y

            
            #Wiederholungen der Messungen um 1 erweitern
            wiederholung1 = wiederholung1 + 1
    
    #kamera stoppen
    kamera.stop()  
    
    """
    Schleife zum auswerten des Mittelpunktes (gemittelt über die Messungen)
    """
    #Wiederholungen null setzen
    wiederholung3 = 0
    
    #Vorher den Mittelpunkt auf nullsetzen
    alle_mittelpunkte_x=0
    alle_mittelpunkte_y=0
    
    #Schleife zum Mitteln der Werte
    while wiederholung3 <= messungen:
        
        #Abbruchbedingung überprüfen
        k = cv2.waitKey(100) # Drücke Esc zum verlassen
        if k == 27 or arbeitszustand == False:
            arbeitszustand = False
            break    
            
        #Eckpunkte aus dem array holen
        Eckpunkt_rechts_oben = position[wiederholung3,3]
        Eckpunkt_links_oben = position[wiederholung3,4]
        Eckpunkt_links_unten = position[wiederholung3,5]
        Eckpunkt_rechts_unten = position[wiederholung3,6]
        

        
        #Alle Mittelpunkte in einer Summer zusammenrechnen
        alle_mittelpunkte_x = alle_mittelpunkte_x + mittelpunkt_x
        alle_mittelpunkte_y = alle_mittelpunkte_y + mittelpunkt_y
    
        wiederholung3 = wiederholung3 +1
    #Den gemittelten Wert bestimmen
    gemittelter_mittelpunkt_x = alle_mittelpunkte_x/(messungen+1)
    gemittelter_mittelpunkt_y = alle_mittelpunkte_y/(messungen+1)
    
    """
    Schleife zum auswerten des Winkels um die z-Achse (gemittelt über die Messungen/ winkel_y)
    """
    #Wiederholungen null setzen
    wiederholung4 = 0
    
    #Vorher den Mittelpunkt auf nullsetzen
    alle_winkel_z=0
   
    
    #Schleife zum Mitteln der Werte
    while wiederholung4 <= messungen:
        
        #Abbruchbedingung überprüfen
        k = cv2.waitKey(100) # Drücke Esc zum verlassen
        if k == 27 or arbeitszustand == False:
            arbeitszustand = False
            break    
            
        #winkel_z aus dem array holen
        winkel_z = position[wiederholung4,0]

        
        #Alle Mittelpunkte in einer Summer zusammenrechnen
        alle_winkel_z = alle_winkel_z + winkel_z
        wiederholung4 = wiederholung4 +1
    
    #Den gemittelten Wert bestimmen
    gemittelter_winkel_z = alle_winkel_z/(messungen+1)

    
    if arbeitszustand == False:
        print("Programm wurde abgebrochen")
        
    if wiederholung2 >= 50:
        print("Kein grüne Glyphe gefunden")
        arbeitszustand = False
                    
    if wiederholung1 >= 50:
        print("Berechnungen/Messungen abgeschlossen")
        arbeitszustand = False
        
    return gemittelter_mittelpunkt_x, gemittelter_mittelpunkt_y,gemittelter_winkel_z, arbeitszustand

       

