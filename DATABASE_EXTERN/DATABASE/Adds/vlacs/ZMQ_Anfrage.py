# -*- coding: utf-8 -*-
"""
Created on Wed Aug 30 12:57:01 2017

@author: Christian Plesker
"""
import os
import sys


"""

Den aktuellen Dateipfad dem Systempfad hinzufügen um eventuelle Problem, beim Finden der Datein, vorzubeugen

"""
aktueller_pfad = os.path.abspath(os.path.dirname(__file__))
uebergeordneter_pfad = os.path.abspath(os.path.join(aktueller_pfad, os.pardir))#os.pardor Funktion zum kombinieren der pfad --> einz drüber

if uebergeordneter_pfad not in sys.path:
	sys.path.insert(0, uebergeordneter_pfad)                                    #in die sys.pfad liste einfügen für extern start


from configuration import config
from module import module

"""
Anfrage über ZMQ in der Verwaltungsschale zu kommunizieren
über die dritte Varaible wird die Anfrage spezialisiert (anfrage)
-Nachricht Senden                           = senden
-Nachricht empfange/warten auf eine Anwort  = empfangen
-Nachrichten senden + empfangen/warten      = senden_empfangen

"""
#Hauptfunktion des Prgramms
def zmq_senden_VLACS(adresse, inhalt):

    #Instanzierung eines zmq socket
    vlacs = module('VLACS', config)     #


    """
    Funktion zum verschicken einer Nachricht mit ZMQ
    """
    anfrage_2 = vlacs.create_message(TO = adresse,CORE = inhalt)#Funktion ist in module.py 
    vlacs.send(anfrage_2)                                               # Erstellen einer Message 
                                                                        # anfrage_2 da anfrage für anfragen von extern reserviert ist
    print("Vlacs hat gesendet:"+str(anfrage_2))
    

def zmq_empfangen_VLACS():
    
    #Instanzierung eines zmq socket
    vlacs = module('VLACS', config)     #

    """ 
    Auf eine Anwort warten.
    """
    nachricht_2 = vlacs.receive()                                       #Warten auf ein Antwort / Kann eventuell darauf verzichtet werden
    kern_2 = vlacs.extract_core(nachricht_2)                            #auspacken der message
    nachricht_2 = kern_2['response']                                    #Wert der Antwort raus ziehen

    return nachricht_2

    

