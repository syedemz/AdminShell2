# -*- coding: utf-8 -*-
"""
Created on Thu May 18 10:46:19 2017

@author: Chrisitan Plesker


Programm zum Sortieren von 4 Punkten nach ihrer Position im Bild
"""


import numpy as np

#Funktion zum sortieren von 4 Koordinatenpunkten
#Unterteilung der Punkte in links_unten, links_oben, rechts_oben und rechts_unten
       
def sortieren(Punkte):
    
     #Sortiert die Punkte nach dem ersten Eintrag aufsteigend   
    sortieren_nach_erstem_eintrag = sorted(Punkte, key=lambda tup: tup[0])                

    
    links = np.array([sortieren_nach_erstem_eintrag[0],sortieren_nach_erstem_eintrag[1]], dtype="float32")
    summe_links = links.sum(axis=1)
    
    rechts = np.array([sortieren_nach_erstem_eintrag[2],sortieren_nach_erstem_eintrag[3]], dtype="float32")
    summe_rechts = rechts.sum(axis=1)
    
    links_unten = links[np.argmin(summe_links)]        #Punkt lings unten
    links_oben = links[1-np.argmin(summe_links)]       #Punkt links oben
    rechts_oben = rechts[np.argmax(summe_rechts)]      #Punkt rechts oben
    rechts_unten = rechts[1-np.argmax(summe_rechts)]   #Punkt rechts unten
    
    #Hinterlegen der Punkte in einem Array in bestimmter Reihnfolge
    punkte_sortiert = np.array([links_unten, rechts_unten, rechts_oben, links_oben], dtype="float32")
 
    
    return punkte_sortiert


