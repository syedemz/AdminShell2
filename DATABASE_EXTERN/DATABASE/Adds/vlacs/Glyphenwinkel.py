
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 12:20:48 2017

@author: Christian Plesker

Programm zum erkennen einer Glyphe und auslesen des Glyphenmusters.

"""

#Laden der benötien Bibliotheken
import cv2
import time
from vlacs.Kamera import Kamera
from vlacs.GruenFilter import gruen_filtern
from vlacs.Glyphmuster import glyphmuster
from vlacs.Winkelberechnung import glyphen_winkel


def winkel_bestimmen():
        
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

    kamera = cv2.VideoCapture(0)
    #kamera = Kamera(kameranummer)
    #Kamera starten#
    #kamera.start()

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
            
            winkel = glyphen_winkel(objektpunkte)

            break
            
                
        if arbeitszustand == False:
            print("abbruch")
            break
            
        wiederholung1 = wiederholung1+1
        time.sleep(1)
        
    #kamera.stop()
    kamera.release()
    if gefunden == True:

        return winkel, "Winkel wird angepasst"
    
    elif wiederholung1 >= 50:

        return False, "keine Glpyhe, bitte überpruefen, ob die Glyphe im Sichfeld ist"
                
    elif arbeitszustand == False:

        return False, "Abbruch"
   
    else:

        print(gefunden)
        return  False, "error"
