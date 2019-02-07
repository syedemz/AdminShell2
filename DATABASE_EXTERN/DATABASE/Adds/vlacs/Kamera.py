#Ersteller: Christian Plesker
#Christian.Plesker@web.de 


#Program:
#   Dieser Code dient zur vereinfachung der Kamerabenutzung:
#   Der Code enthält:
#   1.Erstellung eines Objektes (Kamera)
#   2.Funktion zum Starten der Kamera
#   3.Funktion zum Aufnehmen eines Bildes
#   4.Funktion zum Stoppen der Kamera



import cv2 
from threading import Thread

class Kamera:
    
    #Funktion mit den Attributen der Klasse
    def __init__(self, Kameranummer):
        self.video_aufnahme = cv2.VideoCapture(Kameranummer)
        self.aktuelles_bild = self.video_aufnahme.read()[1]
        

       
        
    #Klassenoperation zum starten der Kamera
    #Erstellen eines eigenen Threads
    def start(self):
        Thread(target=self._update_bild, args=()).start()
        
        
    #Klassenoperation zum:
    #Bild schießen
    #Updaten des aktuellen Bildes   
    def _update_bild(self):
       while(True):
            self.aktuelles_bild= self.video_aufnahme.read()[1]
            
            
    #Klassenoperation zur Wiedergabe des aktuellen Bildes
    def aktuelles_bild_erhalten(self):
       return self.aktuelles_bild
    
    #Klassenoperation zum auschalten der Kamera
    def stop(self):
        self.video_aufnahme.release()
        
        
        