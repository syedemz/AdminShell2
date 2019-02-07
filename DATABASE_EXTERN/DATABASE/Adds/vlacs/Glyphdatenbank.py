# -*- coding: utf-8 -*-
"""
Created on Thu May  4 18:36:15 2017

@author: Christian Plesker
"""

#Programm zum Abgleich des Glyphenmusters
#Die Funktion gleicht das Muster mit den Mustern in der Datenbank ab


#Gespeicherte Muster der Datenbank, Glyphe vom Roboterarm
Glyphmuster = [[1, 0, 1, 0, 1, 1, 1 ,0 ,0],[1, 0, 1, 0, 1, 0, 0 ,1 ,1],[0, 0, 1, 1, 1, 0, 1 ,0 ,1],[1, 1, 0, 0, 1, 0, 1 ,0 ,1]]


#Funktion zum Abgleich
def musterabgleich(Glyphe):
    
    #For-Schleife zählt die einzelnen Einträge der gespeicherten Glyphenliste durch
    for muster in Glyphmuster:
        
        #Default = Das Muster wurde nicht gefunden
        gefunden = False
        
        
        #Abgleich der Muster in der Datenbank mit dem gefunden Glyphenmuster
        if Glyphe == muster:
            
            #Fals gefunden wird der gefunden als Ture hinterlegt
            gefunden = True
            #Die Funktion wird abgebrochen und gibt die Variable gefunden aus
            return "Franconia Robotics 6 DOF ARM V4.0"

        
    #Fals das Muster nicht in der Datenbank zu finden ist, wird die Funktion beendet und die Variable gefunden ausgegeben
    return gefunden
        
        