# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 23:41:14 2017

@author: 
"""

import cv2
import numpy as np



#Anzahl an Pixel
Bildpixel = 100.0

#Grenzwert beim Erkennen des Glyphenmusters, ab dem die Farbe angenommen oder abgelehnt wird
Farbgrenzwert = 50

def punkte_sortieren(Punkte):
    
    p = Punkte.sum(axis=1)
    
    diff = np.diff(Punkte, axis=1)
    
     
    Punkte_geordnet = np.zeros((4,2), dtype="float32")
 
    Punkte_geordnet[0] = Punkte[np.argmin(p)]
    Punkte_geordnet[2] = Punkte[np.argmax(p)]
    Punkte_geordnet[1] = Punkte[np.argmin(diff)]
    Punkte_geordnet[3] = Punkte[np.argmax(diff)]
 
    
    return Punkte_geordnet



def max_width_height(Punkte):
 
    (tl, tr, br, bl) = Punkte
 
    top_width = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    bottom_width = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    max_width = max(int(top_width), int(bottom_width))
 
    left_height = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    right_height = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    max_height = max(int(left_height), int(right_height))
 
    return (max_width,max_height)
 
def topdown_points(max_width, max_height):
    return np.array([
        [0, 0],
        [max_width-1, 0],
        [max_width-1, max_height-1],
        [0, max_height-1]], dtype="float32")



def get_topdown_quad(image, src):
 
    # src and dst points
    src = punkte_sortieren(src)
 
    (max_width,max_height) = max_width_height(src)
    dst = topdown_points(max_width, max_height)
  
    # warp perspective
    matrix = cv2.getPerspectiveTransform(src, dst)
    warped = cv2.warpPerspective(image, matrix, max_width_height(src))
 
    # return top-down quad
    return warped

def resize_image(image, new_size):
    ratio = new_size / image.shape[1]
    return cv2.resize(image,(int(new_size),int(image.shape[0]*ratio)))

def get_glyph_pattern(image, black_threshold, white_threshold):
 
    # collect pixel from each cell (left to right, top to bottom)
    cells = []
     
    cell_half_width = int(round(image.shape[1] / 10.0))
    cell_half_height = int(round(image.shape[0] / 10.0))
    print(cell_half_width)
    print(cell_half_height)
    
 
    row1 = cell_half_height*3
    row2 = cell_half_height*5
    row3 = cell_half_height*7
    col1 = cell_half_width*3
    col2 = cell_half_width*5
    col3 = cell_half_width*7
 
    cells.append(image[row1, col1])
    cells.append(image[row1, col2])
    cells.append(image[row1, col3])
    cells.append(image[row2, col1])
    cells.append(image[row2, col2])
    cells.append(image[row2, col3])
    cells.append(image[row3, col1])
    cells.append(image[row3, col2])
    cells.append(image[row3, col3])
    
    
    for z in range(0,9):
        print(cells)
        if cells[z] >= 25:
            cells[z] = 1
                        
        else :
            cells[z] = 0
                        
    print (cells)
 
    return cells
 

def glyphmuster_erkennen(grau, annaeherung):
            #Dreht die erkannte Kontur grade zum Prüfen der Glyphe
            topdown_quad = get_topdown_quad(grau, annaeherung)
            
            # Unterteilt die Glyphe in 100x100 Pixel
            resized_shape = resize_image(topdown_quad, Bildpixel)


            # Benutzt das Glyphenbild und bestimmt das Muster
            glyph_pattern = get_glyph_pattern(resized_shape, Farbgrenzwert, Farbgrenzwert)
            
            return glyph_pattern