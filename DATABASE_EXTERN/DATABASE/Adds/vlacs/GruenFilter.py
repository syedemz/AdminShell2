# -*- coding: utf-8 -*-
"""
Created on Fri May  5 15:15:37 2017

@author: Christian Plesker

Programm zum Filtern von Störsignalen und herausfiltern von grüner Farbe
"""

import cv2
from numpy import array


def gruen_filtern(Bild):
    
    #Filter auf das Bild anwednen um Rauschen reduzieren
    median = cv2.medianBlur(Bild,5)
    
    
    #Farbe von BGR zu HSV Spektrum konvertieren
    hsv = cv2.cvtColor(median, cv2.COLOR_BGR2HSV)
    
     #Farbebereich eingrenzen (RGB [128,255,0]) grün
     #Untere Farbgrenze ([35,60,60])
    unteres_gruen = array([25,60,0])
    
    #Obere Farbgrenze([70,255,180])
    oberes_gruen = array([90,255,255])
    
    #Pixel bestimmen die in den Grenzen des Farbbereiches liegen
    mask = cv2.inRange(hsv, unteres_gruen, oberes_gruen)
    
    #Den Pixel, welche im Bereich liegen(mask = mask), werden die Farbe des Bildes übergeben
    #Die Pixel, welche nicht im Bereich liegen, bleiben schwarz
    gruen = cv2.bitwise_and(Bild, Bild, mask = mask)
    
    #Rückgabe des Bildes
    return gruen