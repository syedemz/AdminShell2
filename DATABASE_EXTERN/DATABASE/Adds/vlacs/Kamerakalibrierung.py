#Ersteller: Christiain Plesker
#Email: Christian.Plesker@web.de

#Programm:
#1.Bestimmung der Kameraparameters
#2.Speichern die Parameter in einer npz Datei:
#   -Kamera Kalibrierungs Matrix (3x3) - gespeichert under: mtx
#   -Distortion MAtrix - gespeichert unter: dist
#   -Rotations Matrix (3x3) - gespeichert unter: rvecs
#   -Translation Matrix (3x1) - gespeicher unter: tvecs




import cv2
import numpy as np
import os
import time

def kamera_kalibrieren():

    # Erstellt die Objektpunkte, im Format: (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
    erwartete_objektpunkte = np.zeros((4*6,3), np.float32)
    erwartete_objektpunkte[:,:2] = np.mgrid[0:6,0:4].T.reshape(-1,2)
    
    #Erzeugung leerer Arrays zum späteren abspeichern der Objektpunkte und Bildpunkte
    Objektpunkte = []
    Bildpunkte = []
    
    
    Kriterien = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    anzahl_bilder = 0;
    #Die richtige Kamera auswählen
    #Festlegen der Kamera:
    # 0 - Standartkamera, 1/2/3... - zusätzlich, angeschlossene Kameras 
    kameranummer= 0
    #Kamera starten
    kam = 0
    kam = cv2.VideoCapture(kameranummer)  
    
    while anzahl_bilder < 40:
        print("1")
        #Bild schießen und hinter Bild hinterlegen
        unwichtig , bild = kam.read()
        time.sleep(1)
            
        #Bild zu Grau convertieren
        Grau = cv2.cvtColor(bild, cv2.COLOR_BGR2GRAY)
        
        #Schachbrettmuster finden
        Rückgabewert, Ecken = cv2.findChessboardCorners(Grau, (6,4), None)
        
        #Wenn ein Muster gefunden wurde, werden die Ecken den Objektpunkten angehangen
        if Rückgabewert == True:
            
            print("gefunden")
            #anhängen der objp in das Array Objektpunkte
            Objektpunkte.append(erwartete_objektpunkte)
            
            #Befehl zum präzisieren der Postion der Ecken
            #cv2.cornerSubPix(Bild, Position der Ecken, 
            #Hälfte des Suchfensters in dem nach den Ecken gesucht werden soll, 
            #Hälfte der Mitte die nicht betrachtet wird um Fehler zu vermeiden, Suchketerium)
            
            Bildecken = cv2.cornerSubPix(Grau, Ecken, (11,11), (-1,-1), Kriterien)
            Bildpunkte.append(Bildecken)
            
            anzahl_bilder = anzahl_bilder+1
            
            
    #Kamera stoppen
    #kam.release()
            
    #Kalibierung der Kamera
    #Abspeichern der Ausgabewerte
    Rueckgabewert, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(Objektpunkte, Bildpunkte, Grau.shape[::-1], None, None)
    

    from vlacs.Kalibrierungsparameter import Parameter
    #Dictionary ersetteln
    
    add_parameter = {'Rueckgabewert': Rueckgabewert, 'mtx': mtx, 'dist': dist, ' rvecs': rvecs, 'tvecs' : tvecs}
    #An die gewünschte Stelle setzten
    Parameter["kamera"] = add_parameter

    #Die Syntaxerstellen zum Abspeichern / array wird benötigt, da mtx und dist in numpy.arrays gespecihert werden. Beim Laden ohne numpy importiert gibt dies Probleme
    Parameter = 'from numpy import array \n' + 'Parameter = '+str(Parameter)

    
    # Den richtige Pfad finden und abspeichern 
    workdir = os.getcwd()
    pathToConfFile = os.path.join(workdir, 'FUNCTIONALITY','vlacs','Kalibrierungsparameter.py')
    file = open(pathToConfFile, "w")
    file.write(Parameter)
    file.close()
    
    #Antwort geben, dass alles geklappt hat.
    antwort = "Kalibriert"
    kam = 1
    return antwort
