# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 15:55:16 2017

@author: Christian Plesker

Programm zum Bestimmen der Glyphenmittelpunkte aus einem Bild
"""


#Laden der benötien Bibliotheken
import cv2
import numpy as np
import time
from vlacs.Kamera import Kamera
from vlacs.GruenFilter import gruen_filtern
from vlacs.Glyphmuster import glyphmuster
from vlacs.Punkte_sortieren import sortieren



def finde_glypmittelpunkt():
        
    """
    Eingabe der Grundparameter
    -Abreitszustand (Kontrollwert ob, ein abbruch vorliegt)
    -Kammeranummer (0 = default, 1,2,3....je nach dem welche benutz werden soll, fals mehrere angeschlossen sind)
    """
   
    #Der Arbeitszustand zurücksetzten
    arbeitszustand = True
        
    #Festlegen der Kamera:
    # 0 - Standartkamera, 1/2/3... - zusätzlich, angeschlossene Kameras 
    kameranummer= 0
    
    #Messungen, wie oft nach einer Glyphe gesucht werden soll
    messungen = 50

    """
    Start des Programmes 
    -Kamera starten 
    
    """
    #Wiederholungen auf 0 setzten
    wiederholung1 = 0
    #Objekt Kamera instanzieren
    #kamera = Kamera(kameranummer)
    
    #Kamera starten
    
    #kamera.start()

    kamera = cv2.VideoCapture(0)

    while wiederholung1 <= messungen:

        
                
        #Bild schießen und hinter Bild hinterlegen
        #bild = kamera.aktuelles_bild_erhalten()
        _, bild = kamera.read()
        

        
                    #Ließt die Kameraparameter aus
        from vlacs.Kalibrierungsparameter import Parameter
        
        parameter = Parameter['kamera']
        
        Kameramatrix = parameter['mtx']
        Verzerrungsmatrix = parameter['dist']
            
        h,  w = bild.shape[:2]
        neuekameramatrix, roi=cv2.getOptimalNewCameraMatrix(Kameramatrix, Verzerrungsmatrix, (w,h), 1, (w,h))
            
        # undistort
        bild = cv2.undistort(bild, Kameramatrix, Verzerrungsmatrix, None, neuekameramatrix)
        
        # Bild zurecht schneiden
        x, y, w, h = roi
        bild = bild[y:y+h, x:x+w]
        
        
        #Bild filtern und grüne Farbe heraussuchen
        gruen = gruen_filtern(bild)
        

        #Anzahl der Wiederholungen auf 0 setzten
        wiederholung2 = 0       
        
        #Wenn kein Gruen in dem Bild gefunden wird
        if gruen.any() == False:
                  
                    
            #Erneute Bildaufnahme-Schleife bis etwas grünes gefunden wird oder Abbruch der Schleife durch zu viele Wiederholungen(50+)
            while wiederholung2 <= 50:
                
                k = cv2.waitKey(100) # Drücke Esc zum verlassen
                if k == 27 or arbeitszustand == False:
                    arbeitszustand = False
                    
                    break 
                
                print("Bild enthält kein gruen")
                
                 #Bild schießen und hinter Bild hinterlegen
                #bild = kamera.aktuelles_bild_erhalten()
                time.sleep(0.5)
                _, bild = kamera.read()


        
                            #Ließt die Kameraparameter aus
                from vlacs.Kalibrierungsparameter import Parameter
                    
                parameter = Parameter['kamera']
                
                Kameramatrix = parameter['mtx']
                Verzerrungsmatrix = parameter['dist']
                
                h,  w = bild.shape[:2]
                neuekameramatrix, roi=cv2.getOptimalNewCameraMatrix(Kameramatrix, Verzerrungsmatrix, (w,h), 1, (w,h))
                    
                # undistort
                bild = cv2.undistort(bild, Kameramatrix, Verzerrungsmatrix, None, neuekameramatrix)
                
                # Bild zurecht schneiden
                x, y, w, h = roi
                bild = bild[y:y+h, x:x+w]
                
                
                #Bild filtern und grüne Farbe heraussuchen
                gruen = gruen_filtern(bild)
                
                #Abbruchbedinung fals gruen gefunden wird
                if gruen.any() == True:
                    break
                
                #Die Wiederholung um 1 weiterzählen
                wiederholung2 = wiederholung2 + 1
        
        if wiederholung2 >= 50:
            arbeitszustand = False        
        #Finden von Glyphen, Abgleich des Glyphenmusters, Wiedergabe der Kontur, welche die richtige Glyhe ist
        if arbeitszustand == True:
            
            gefunden , robotername, objektpunkte = glyphmuster(gruen)

        
                
        if gefunden == True:
            print("Muster stimmt")
            
            punkte = sortieren(objektpunkte)
            
            Eckpunkt_rechts_oben = punkte[2]
            Eckpunkt_links_oben = punkte[3]
            Eckpunkt_links_unten = punkte[0]
            Eckpunkt_rechts_unten = punkte[1]
            
            
            glyphmittelpunkt_x = (Eckpunkt_rechts_oben[0]+Eckpunkt_links_oben[0]+Eckpunkt_links_unten[0]+Eckpunkt_rechts_unten[0])/4
            glyphmittelpunkt_y = (Eckpunkt_rechts_oben[1]+Eckpunkt_links_oben[1]+Eckpunkt_links_unten[1]+Eckpunkt_rechts_unten[1])/4
            
            #Länge der rechten und linken vertikalen Kante in Pixel
            rechte_kante_vertikal = np.sqrt(((Eckpunkt_rechts_oben[0] - Eckpunkt_rechts_unten[0] )**2)+((Eckpunkt_rechts_oben[1] - Eckpunkt_rechts_unten[1])**2))
            linke_kante_vertikal = np.sqrt(((Eckpunkt_links_oben[0] - Eckpunkt_links_unten[0] )**2)+((Eckpunkt_links_oben[1] - Eckpunkt_links_unten[1])**2))
            
            #Hoehe der Glyhpe mitteln mit den beiden im Bild bestimmten Kanten
            gemittelte_hoehe_glyphe= (rechte_kante_vertikal + linke_kante_vertikal)/2

            
            break
            
                
        if arbeitszustand == False:
            print("abbruch")
            break
            
        wiederholung1 = wiederholung1+1
        time.sleep(1)
        print("grün, aber keine Glyphe")
    
    #kamera.stop()
    kamera.release()
     
    if gefunden == True:

        return  gefunden, glyphmittelpunkt_x, glyphmittelpunkt_y, gemittelte_hoehe_glyphe
    
    elif wiederholung1 >= 50:
        
        return "keine Glpyhe, bitte überprüfen, ob die Glyphe im Sichfeld ist", False, False, False
                
    elif arbeitszustand == False:

        return "Abbruch", False, False, False
    
    else:
        return  "error", False, False, False
