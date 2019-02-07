# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 16:10:07 2017

@author: SMP II
"""

from vlacs.Punkte_sortieren import *

def mittelpunkt_bestimmen(objektpunkte):
    
    #objektpunkte in die selbe Reihnfolge sortieren
    punkte = sortieren(objektpunkte)
    

    Eckpunkt_rechts_oben = punkte[2]
    Eckpunkt_links_oben = punkte[3]
    Eckpunkt_links_unten = punkte[0]
    Eckpunkt_rechts_unten = punkte[1]
    
    x_koordinate = (Eckpunkt_rechts_oben[0]+Eckpunkt_links_oben[0]+Eckpunkt_links_unten[0]+Eckpunkt_rechts_unten[0])/4
    y_koordinate = (Eckpunkt_rechts_oben[1]+Eckpunkt_links_oben[1]+Eckpunkt_links_unten[1]+Eckpunkt_rechts_unten[1])/4
    
    
    return x_koordinate, y_koordinate