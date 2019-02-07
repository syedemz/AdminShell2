# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Christian Plesker
"""


"""

Funktion zur Kommunikation mittels eines Socket severs
Verwendet wird ZMQ

"""
import os
import sys
"""

Den aktuellen Dateipfad dem Systempfad hinzufügen um eventuelle Problem, beim Finden der Datein, vorzubeugen

"""
aktueller_pfad = os.path.abspath(os.path.dirname(__file__))
uebergeordneter_pfad = os.path.abspath(os.path.join(aktueller_pfad, os.pardir))#os.pardor Funktion zum kombinieren der pfad --> einz drüber

if uebergeordneter_pfad not in sys.path:
	sys.path.insert(0, uebergeordneter_pfad) 



"""

Hauptprogramm start

"""
import cv2
from math import pi, sqrt
from vlacs.Glyphe_erkennen import glyphe_erkennen
from vlacs.Glyphenwinkel import winkel_bestimmen
from vlacs.Glyphmittelpunkt import finde_glypmittelpunkt
from vlacs.Berechnungen_Glyphposition import kinematik_vor, kinematik_inv
from numpy import array
from vlacs.Kamerakalibrierung import kamera_kalibrieren


def main():
    
    from configuration import config
    from module import module
    
    """
    Anfrage über ZMQ in der Verwaltungsschale zu kommunizieren
    über die dritte Varaible wird die Anfrage spezialisiert (anfrage)
    -Nachricht Senden                           = senden
    -Nachricht empfange/warten auf eine Anwort  = empfangen
    -Nachrichten senden + empfangen/warten      = senden_empfangen
    
    """

    #Instanzierung eines zmq socket
    vlacs = module('VLACS', config)     #
    Arbeitszustand = True
    
    
    #Schleife zum überprüfen obeine Anfrage von der Benutzeroberfläche kam und dann die Anweisung ausführen
    while True:
        
        #Nachricht empfangen und die Anweisungen extrahieren
        MESSAGE = vlacs.receive()
        CORE =vlacs.extract_core(MESSAGE)
        befehl = CORE['anweisung']


        #Standard Antowrt --> wird überschrieben am Ende jedes Programmes
        inhalt ={"antwort": "kein Programm ausgeführt"}
    
        """
        ////////////// Kalibrierung der Kameraparameter zum Kalibrieren der Kamera/////////////////////////////
        
        """
        
        if befehl == "kalibrieren":
            #Funktion zum Kalibrieren
            antwort = kamera_kalibrieren();
            
            #Anwort für die Webseite
            inhalt ={"antwort": antwort}
            
        """
        ////////////// Erste Funktion zum Finden einerGlyphe //////////////////////////
        
        """
        
        if befehl == "glyphe_finden":
            
            #startet programm Programm zum Erkennen von Glyphen
            antwort = glyphe_erkennen()
               
            #Anwort für die Webseite
            inhalt ={"antwort": antwort}
            
        """
        ////////////// Zweite Funktion um den Roboter grade zudrehen //////////////////////////
        
        """    
            
            
        if befehl == "voreinstellung":
            
            """
            Um Anweisungen an andere Apps zuschicken müssen folgende DAten übergeben werden:
            ip_adress = Die Ip_Adresse des empfaengers
            request = GET oder POST Anfrage
            path = pfad der Verwaltungsschale beim Empfaenger um die zugewiesene App anzusteuern + der dienst der Applikation <module_id>/<resource_id>
            """
            
            #Roboter starten
            daten = {'befehl': "20 01 000 000 000 000 000 000 "}
            ip_adresse = "http://192.168.0.101:5000"
            pfad = '/vlacs_empfaenger/weiterleiten'         
            inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
            anfrage_2 = vlacs.create_message(TO = "HTTPOUT",CORE = inhalt)      #Funktion ist in module.py 
            vlacs.send(anfrage_2)

            #Rückmeldung von vlacs_empfaenger abwarten
            rueckmeldung = vlacs.poll(20000)
            kern_rueckmeldung =vlacs.extract_core(rueckmeldung)
            kern= kern_rueckmeldung['json_data']
            rueckmeldung_nachricht= kern['response']
            if rueckmeldung_nachricht == "response-timeout":
                                       
                    inhalt = {"antwort": "keine Verbindung"}
                    antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)
                    vlacs.send(antwort)
                    continue

            #Roboter starten
            daten = {'befehl': "empfangen"}
            ip_adresse = "http://192.168.0.101:5000"
            pfad = '/vlacs_empfaenger/empfangen'         
            inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
            anfrage_2 = vlacs.create_message(TO = rueckmeldung,CORE = inhalt)      #Funktion ist in module.py 
            vlacs.send(anfrage_2)
            

             #Zeit um aufdie Anfrage zu reagieren
            
            
            #Wenn die Antwort von VLACS_EMPFAENGER empfangen wurde dann:
            if rueckmeldung_nachricht == "weitergeleitet" and Arbeitszustand == True:
                                
                #startet programmzum Bestimmen des Verdrehungswinkels
                winkel, befehl = winkel_bestimmen()    #Der Winkel ist gleich der Winke
                
                """
                Winkel runden und in einen ganze Zahl wandeln
                
                Standarwinkel abziehen
                in ein dreistelliges Format vor dem Komma anpassen
                
                """
                neuer_winkel = int(round(winkel,0))

                neuer_winkel = 90 - winkel
                if neuer_winkel < 0:
                    neuer_winkel = 0
                    
                elif neuer_winkel > 180:
                    neuer_winkel = 180
                neuer_winkel = str("%0.3u"% (neuer_winkel))
                

                """
                Verdrehwinkel ausbessern
                """  
                inhalt ={"antwort": "error"}
                if befehl == "Winkel wird angepasst" and Arbeitszustand == True:
                    
                    #Neue Position mit angepassten Winkel vom Motor G1 in eine Nachricht packen und verschicken
                    anweisung = "18 02 "+ str(neuer_winkel)+" 180 000 090 090 000 "
                    daten = {'befehl': anweisung}
                    ip_adresse = "http://192.168.0.101:5000"
                    pfad = '/vlacs_empfaenger/weiterleiten'         
                    inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                    anfrage_2 = vlacs.create_message(TO = "HTTPOUT",CORE = inhalt)      #Funktion ist in module.py 
                    vlacs.send(anfrage_2)

                    #Abfangen der Rückmeldung von vlacs_empfaenger
                    rueckmeldung = vlacs.poll(20000)
                    kern_rueckmeldung =vlacs.extract_core(rueckmeldung)
                    kern= kern_rueckmeldung['json_data']
                    rueckmeldung_nachricht = ''
                    rueckmeldung_nachricht= kern['response']
                    if rueckmeldung_nachricht == "response-timeout":

                            inhalt = {"antwort": "keine Verbindung"}
                            antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)
                            vlacs.send(antwort)
                            continue
                        
                    anweisung = "empfangen"
                    daten = {'befehl': anweisung}
                    ip_adresse = "http://192.168.0.101:5000"
                    pfad = '/vlacs_empfaenger/empfangen'         
                    inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                    anfrage_2 = vlacs.create_message(TO = rueckmeldung,CORE = inhalt)      #Funktion ist in module.py 
                    vlacs.send(anfrage_2)
                    

                    
                    #Antwort verfassen für die Webseit auf error setzten
                    inhalt ={"antwort": "error"}    
                    
                    #Fals die Rückmeldung von vlacs_empfaenger erfolgreich war, soll die Anwort für die Webseit überschrieben werden
                    if rueckmeldung_nachricht == "weitergeleitet" and Arbeitszustand == True:
                        
                            inhalt ={"antwort": "Voreinstellung erfolgreich"}    
                    
                    if Arbeitszustand == False:
                            inhalt ={"antwort": "Abgebrochen"}  
                    
                    
        """
        ////////////// Dritte Funktion um die Motoren des Roboters zu testen //////////////////////////
        
        """    
                     
        if befehl == "start2":
            
            """
            //////////////////////////////////Roboter Fernwartungsanfrage///////////////////////////////////////////////////////
            """
            if Arbeitszustand == True:
                #Roboter starten: Fernwartungsanfrage fals nicht schon vorher erledigt

                daten = {'befehl': "20 01 000 000 000 000 000 000 "}
                ip_adresse = "http://192.168.0.101:5000"
                pfad = '/vlacs_empfaenger/weiterleiten'         
                inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                anfrage_2 = vlacs.create_message(TO = "HTTPOUT",CORE = inhalt)      #Funktion ist in module.py 
                vlacs.send(anfrage_2)

    
                #Rückmeldung durch vlacs_empfaenger auffangen
                rueckmeldung = vlacs.poll(20000)
                kern_rueckmeldung =vlacs.extract_core(rueckmeldung)
                kern= kern_rueckmeldung['json_data']
                rueckmeldung_nachricht= kern['response']

                if rueckmeldung_nachricht == "response-timeout":
                            inhalt = {"antwort": "keine Verbindung zu Vlacs_Empfaenger", "abweichung_x": "0", "abweichung_y": "0", "abweichung_gesamt": "0","antwort": "keine Verbindung"}
                            antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)
                            vlacs.send(antwort)
                            continue
                        
                daten = {'befehl': "empfangen"}
                ip_adresse = "http://192.168.0.101:5000"
                pfad = '/vlacs_empfaenger/empfangen'         
                inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                anfrage_2 = vlacs.create_message(TO = rueckmeldung,CORE = inhalt)      #Funktion ist in module.py 
                vlacs.send(anfrage_2)
                

            """
            //////////////////////////////////Bestimmung des Startpunktes im Bild///////////////////////////////////////////////////////
            """
            if Arbeitszustand == True:
                """
                Glyphenmittelpunkt1 aus dem Bild und den Berechnungen bestimmen
                
                """
                gefunden, glyphmittelpunkt_x1, glyphmittelpunkt_y1, hoehe_glyphe = finde_glypmittelpunkt()
         
            
            """
            //////////////////////////////////Roboter neue Position zuweisen ///////////////////////////////////////////////////////
            """
            if Arbeitszustand == True:
                #Anweisungen aus der Nachricht auslesen --> Welche Motoren sollen angschaltet werden: 0 = aus / 1 = an
                anweisungG2 = int(CORE['motorG2'])
                anweisungG3 = int(CORE['motorG3'])
                anweisungG4 = int(CORE['motorG4'])
                
                #Winkel um den die Motoren bewegt werden sollen
                winkelG1 = int(neuer_winkel)
                winkelG2 = int(CORE['winkelG2'])
                winkelG3 = int(CORE['winkelG3'])
                winkelG4 = int(CORE['winkelG4'])
                
                winkelG2 = anweisungG2*winkelG2
                winkelG3 = anweisungG3*winkelG3
                winkelG4 = anweisungG4*winkelG4
                
         
                #Neue winkel in das Format mit 3 stellen ohne Komma bringen
                G2 = str("%0.3u"% (int(round(180-winkelG2))))
                G3 = str("%0.3u"% (int(round(0+winkelG3))))
                G4 = str("%0.3u"% (int(round(90+winkelG4))))
         
            if Arbeitszustand == True:
                #Neue Positionswinkel dem Roboter übergeben
                anweisung = "18 02 " + str(neuer_winkel) +" "+ G2 +" "+ G3 +" "+ G4 +" 090 000 "    #Grundposition + winkeländerung
                daten = {'befehl': anweisung}
                ip_adresse = "http://192.168.0.101:5000"
                pfad = '/vlacs_empfaenger/weiterleiten'         
                inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                anfrage_2 = vlacs.create_message(TO = "HTTPOUT",CORE = inhalt)      #Funktion ist in module.py 
                vlacs.send(anfrage_2)

                
                #Rückmeldung von vlacs_empfaenger auffangen
                rueckmeldung = vlacs.poll(20000)
                kern_rueckmeldung =vlacs.extract_core(rueckmeldung)
                kern= kern_rueckmeldung['json_data']
                rueckmeldung_nachricht= kern['response']
              
                if rueckmeldung_nachricht == "response-timeout":
                        inhalt = {"antwort": "keine Verbindung zu Vlacs_Empfaenger", "abweichung_x": "0", "abweichung_y": "0", "abweichung_gesamt": "0","antwort": "keine Verbindung"}
                        antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)
                        vlacs.send(antwort)
                        continue
                    
                daten = {'befehl': "empfangen"}
                ip_adresse = "http://192.168.0.101:5000"
                pfad = '/vlacs_empfaenger/empfangen'         
                inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                anfrage_2 = vlacs.create_message(TO = rueckmeldung,CORE = inhalt)      #Funktion ist in module.py 
                vlacs.send(anfrage_2)

                
                """
                //////////////////////////////////Endpunkt im Bild bestimmen///////////////////////////////////////////////////////
                """      
            
            """
            Glyphenmittelpunkt2 aus dem Bild und den Berechnungen bestimmen
            
            """
            if Arbeitszustand == True:
                #Im Bild den Glyphmittelpunkt bestimmen
                gefunden, glyphmittelpunkt2_x2, glyphmittelpunkt2_y2, hoehe_glyphe = finde_glypmittelpunkt()
       
            
            """
            //////////////////////////////////Start und Endpunkt im Berechnungsmodel berechnen///////////////////////////////////////////////////////
            """
            """
            Startpunkt: Vektor bestimmen
            """
            if Arbeitszustand == True:
                #Standartpositon in Winkeln festhalten
                #winkelG1_standard = 90 # eventuell schon geändert --> neuer Winkel = winkelG1
                winkelG2_standard = 180 
                winkelG3_standard = 0
                winkelG4_standard = 90
                
                #Winkel in neuen winkeln festhalten
                theta1 = (pi-(pi*winkelG1/180))
                theta2 = ((winkelG2_standard)/180)*pi
                theta3 = (-pi*(172/180) +pi*(winkelG3_standard/180))
                theta4 = (-pi*(8/180)+ pi*(winkelG4_standard/180))

                
                #Endpunkt vektor bestimmen
                x2, y2, z2, P02 = kinematik_vor(theta1, theta2, theta3, theta4)
                
                
            """
            //////////////////////////////////Berechnung der Abweichung///////////////////////////////////////////////////////
            """
            if Arbeitszustand == True:

                
                #Verschiebung der Bildkoordinaten in pixel
                verschiebung_bild_x = glyphmittelpunkt2_x2 - glyphmittelpunkt_x1
                verschiebung_bild_y = glyphmittelpunkt2_y2 - glyphmittelpunkt_y1

                
    
                #Umrechnung in mm
                verschiebung2_bild_x = (verschiebung_bild_x/hoehe_glyphe)*50
                verschiebung2_bild_y = (verschiebung_bild_y/hoehe_glyphe)*50

        
            
            """
            //////////////////////////////////Abweichung der Motorwinkel///////////////////////////////////////////////////////
            """  
            if Arbeitszustand == True:
                        #Bestimmen des Verktors und der Ausrichtungsverktoren
                o = [0]
                x = x2[0]
                y = x2[1]
                z = x2[2]
                x4in0 = array((x, y,z,o))
                
                x = y2[0]
                y = y2[1]
                z = y2[2]
                y4in0 = array((x, y,z,o))
                
                x = z2[0]
                y = z2[1]
                z = z2[2]
                z4in0 = array((x, y,z,o))

                #Addieren des visuell bestimmten Verfahrensweges
                P04 = array((P02[0], P02[1]+ verschiebung2_bild_x, P02[2] + verschiebung2_bild_y,o))

                #Rückrechnung auf die Motorwinkel
                theta1, theta2, theta3, theta4 = kinematik_inv(x4in0, y4in0, z4in0, P04)
                
                #Winkel in Grad umrechnenen
                winkelG2_1 = (theta2/ pi)*180
                winkelG3_1 = ((theta3 +pi*(172/180))/pi)*180                     
                winkelG4_1 = ((theta4 +pi*(8/180))/pi)*180
                
                #Differenz des vorgegeben Winkels und des ausgerechneten Winkels
                winkelG2_abweichung = round(winkelG2_1 - (winkelG2+winkelG2_standard))
                winkelG3_abweichung = round(winkelG3_1 - (winkelG3+winkelG3_standard))
                winkelG4_abweichung = round(winkelG4_1 - (winkelG4+winkelG4_standard))

            """
            //////////////////////////////////Übergabe Parameter für die Webseit bestimmen///////////////////////////////////////////////////////
            """
            

            if Arbeitszustand == True:
                
                """
                Abweichungen der Winkel, welche übergeben werden.
                """
                abweichung_x_str = str(winkelG2_abweichung)
                abweichung_y_str = str(winkelG3_abweichung)
                abweichung_gesamt_str = str(winkelG4_abweichung)

                #Antowrt verfassen
                inhalt ={"antwort": "alles klar", "abweichung_x": abweichung_x_str, "abweichung_y": abweichung_y_str, "abweichung_gesamt": abweichung_gesamt_str}
             
            if Arbeitszustand == False:
                #Antowrt verfassen
                inhalt = {"antwort": "abgebrochen", "abweichung_x": "0", "abweichung_y": "0", "abweichung_gesamt": "0",}
            
            
            
            
            
        """
        //////////////////////////////////Programm zum Überprüfen der Verfahrenswege///////////////////////////////////////////////////////
        """
            
        if befehl == "start1":
            
            """
            //////////////////////////////////Roboter Fernwartungsanfrage///////////////////////////////////////////////////////
            """
            if Arbeitszustand == True:
                
                #Roboter starten: Fernwartungsanfrage fals nicht schon vorher erledigt
                daten = {'befehl': "20 01 000 000 000 000 000 000 "}
                ip_adresse = "http://192.168.0.101:5000"
                pfad = '/vlacs_empfaenger/weiterleiten'         
                inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                anfrage_2 = vlacs.create_message(TO = "HTTPOUT",CORE = inhalt)      #Funktion ist in module.py 
                vlacs.send(anfrage_2)                

    
                #Rückmeldung durch Vlacs_Empfaenger auffangen
                rueckmeldung = vlacs.poll(20000)
                kern_rueckmeldung =vlacs.extract_core(rueckmeldung)
                kern= kern_rueckmeldung['json_data']
                rueckmeldung_nachricht= kern['response']
                
                if rueckmeldung_nachricht == "response-timeout":
                        inhalt = {"antwort": "keine Verbindung zu Vlacs_Empfaenger", "abweichung_x": "0", "abweichung_y": "0", "abweichung_gesamt": "0"}
                        antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)
                        vlacs.send(antwort)
                        continue
                    
                daten = {'befehl': "empfangen"}
                ip_adresse = "http://192.168.0.101:5000"
                pfad = '/vlacs_empfaenger/empfangen'         
                inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                anfrage_2 = vlacs.create_message(TO = rueckmeldung,CORE = inhalt)      #Funktion ist in module.py 
                vlacs.send(anfrage_2)
                

                
                if Arbeitszustand == True:
                    
                    #Roboter starten: Fernwartungsanfrage fals nicht schon vorher erledigt
                    anweisung = "18 02 " + str(neuer_winkel) +" 180 000 090 090 000 " 
                    daten = {'befehl': anweisung}
                    ip_adresse = "http://192.168.0.101:5000"
                    pfad = '/vlacs_empfaenger/weiterleiten'         
                    inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                    anfrage_2 = vlacs.create_message(TO = "HTTPOUT",CORE = inhalt)      #Funktion ist in module.py                     
                    vlacs.send(anfrage_2)
        
                    #Rückmeldung durch Vlacs_Empfaenger abwarten
                    rueckmeldung = vlacs.poll(20000)
                    kern_rueckmeldung =vlacs.extract_core(rueckmeldung)
                    kern= kern_rueckmeldung['json_data']
                    rueckmeldung_nachricht= kern['response']
                    
                    if rueckmeldung_nachricht == "response-timeout":
                            inhalt = {"antwort": "keine Verbindung zu Vlacs_Empfaenger", "abweichung_x": "0", "abweichung_y": "0", "abweichung_gesamt": "0"}
                            antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)
                            vlacs.send(antwort)
                            continue
                        
                    daten = {'befehl': "empfangen"}
                    ip_adresse = "http://192.168.0.101:5000"
                    pfad = '/vlacs_empfaenger/empfangen'         
                    inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                    anfrage_2 = vlacs.create_message(TO = rueckmeldung,CORE = inhalt)      #Funktion ist in module.py 
                    vlacs.send(anfrage_2)
                    

                    
            """
            //////////////////////////////////Bestimmung des Startpunktes im Bild///////////////////////////////////////////////////////
            """
                        
            """
            Glyphenmittelpunkt1 aus dem Bild und den Berechnungen bestimmen
            
            """
            if Arbeitszustand == True:
                
                gefunden, glyphmittelpunkt_x1, glyphmittelpunkt_y1, hoehe_glyphe = finde_glypmittelpunkt()
     
            
            """
            //////////////////////////////////Roboter neue Position zuweisen ///////////////////////////////////////////////////////
            """
            if Arbeitszustand == True:

                
                ###########################Ausrichtungsvektoren bestimmen ############################
                
                #Standartpositon in Winkeln festhalten
                #winkelG1_standard = 90 # eventuell schon geändert --> neuer Winkel = winkelG1
                winkelG1 = int(neuer_winkel)
                winkelG2_standard = 180 
                winkelG3_standard = 0
                winkelG4_standard = 90
    
                #Winkel in neuen winkeln festhalten
            
                theta1 = (pi-(pi*winkelG1/180))
                theta2 = ((winkelG2_standard)/180)*pi
                theta3 = (-pi*(172/180) +pi*(winkelG3_standard/180))
                theta4 = (-pi*(8/180)+ pi*(winkelG4_standard/180))
                
                x1, y1, z1, P01 = kinematik_vor(theta1, theta2, theta3, theta4)
        
            if Arbeitszustand == True:
                
                #Anweisungen wo der Roboter hinbewegt werden soll
                #mmx = int(CORE['mmx'])
                mmy = int(CORE['mmy'])
                mmz = int(CORE['mmz'])
                #Bestimmen des Verktors und der Ausrichtungsverktoren
                o = [0]
                x = x1[0]
                y = x1[1]
                z = x1[2]
                x4in0 = array((x, y,z,o))
                
                x2 = y1[0]
                y2 = y1[1]
                z2 = y1[2]
                y4in0 = array((x2, y2,z2,o))
                
                x3= z1[0]
                y3 = z1[1]
                z3 = z1[2]
                z4in0 = array((x3, y3,z3,o))
  
                x4 = P01[0]
                y4 = P01[1]
                z4 = P01[2]
                P04 = array((x4,y4+ mmy, z4+mmz, o))

                #Berechnung der Winkel 
                theta1, theta2, theta3, theta4 = kinematik_inv(x4in0, y4in0, z4in0, P04)
            
            if Arbeitszustand == True:
                #Umrechnung in Grad
                winkelG2 = (theta2/ pi)*180
                winkelG3 = ((theta3 +pi*(172/180))/pi)*180 
                winkelG4 = ((theta4 +pi*(8/180))/pi)*180
                
                #Neue winkel in das Format mit 3 stellen ohne Komma bringen
                G2 = str("%0.3u"% (int(round(winkelG2))))
                G3 = str("%0.3u"% (int(round(winkelG3))))
                G4 = str("%0.3u"% (int(round(winkelG4))))
                
                
                #Neue Positionswinkel dem Roboter übergeben
                anweisung = "18 02 " + str(neuer_winkel) +" "+ G2 +" "+ G3 +" "+ G4 +" 090 000 "    #Grundposition + winkeländerung
                daten = {'befehl': anweisung}
                ip_adresse = "http://192.168.0.101:5000"
                pfad = '/vlacs_empfaenger/weiterleiten'         
                inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                anfrage_2 = vlacs.create_message(TO = "HTTPOUT",CORE = inhalt)      #Funktion ist in module.py                 
                vlacs.send(anfrage_2)
                
                #Rückmeldung von HTTPOUT auffangen
                rueckmeldung = vlacs.poll(20000)
                kern_rueckmeldung =vlacs.extract_core(rueckmeldung)
                kern= kern_rueckmeldung['json_data']
                rueckmeldung_nachricht= kern['response']
              
                if rueckmeldung_nachricht == "response-timeout":
                        
                        inhalt = {"antwort": "keine Verbindung zu Vlacs_Empfaenger", "abweichung_x": "0", "abweichung_y": "0", "abweichung_gesamt": "0"}
                        antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)
                        vlacs.send(antwort)
                        continue
                    
                daten = {'befehl': "empfangen"}
                ip_adresse = "http://192.168.0.101:5000"
                pfad = '/vlacs_empfaenger/empfangen'         
                inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
                anfrage_2 = vlacs.create_message(TO = rueckmeldung,CORE = inhalt)      #Funktion ist in module.py 
                vlacs.send(anfrage_2)
                

                
                """
                //////////////////////////////////Endpunkt im Bild bestimmen///////////////////////////////////////////////////////
                """
                
                #Warten, dass der Roboter die Nachricht empfangne und ausgeführt hat.
                
            
            """
            Glyphenmittelpunkt2 aus dem Bild und den Berechnungen bestimmen
            
            """
            if Arbeitszustand == True:
                #Im Bild den Glyphmittelpunkt bestimmen
                gefunden, glyphmittelpunkt2_x2, glyphmittelpunkt2_y2, hoehe_glyphe = finde_glypmittelpunkt()

            
            
            """
            //////////////////////////////////Berechnung der Abweichung///////////////////////////////////////////////////////
            """
            if Arbeitszustand == True:
                #Verktoren der beiden Punkte abziehen um die Verschiebung zu erhalten
                #Verschiebung der Vektoren 1 und 2 nach der Vorgabe in mm y = x und z = y
                verschiebung_vektor_x = verschiebung2_vektor_y = int(mmy)
                verschiebung_vektor_y = verschiebung2_vektor_z = int(mmz)
    
                
                #Verschiebung der Bildkoordinaten in pixel
                verschiebung_bild_x = abs(glyphmittelpunkt2_x2 - glyphmittelpunkt_x1)
                verschiebung_bild_y = abs(glyphmittelpunkt2_y2 - glyphmittelpunkt_y1)
            
                
                #Umrechnung in mm
                verschiebung2_bild_x = (verschiebung_bild_x/hoehe_glyphe)*50
                verschiebung2_bild_y = (verschiebung_bild_y/hoehe_glyphe)*50
                
                #Abweichung der beiden Vektoren in mm
                abweichung_x = int(verschiebung2_bild_x - verschiebung_vektor_x)
                abweichung_y = int(verschiebung2_bild_y - verschiebung_vektor_y)
                
                #Gesamtabweichung in x,y in mm
                x= abweichung_x*abweichung_x
                y= abweichung_y*abweichung_y
                abweichung_gesamt = int(sqrt((x+y)))
                
                
            """
            //////////////////////////////////Übergabe Parameter für die Webseit bestimmen///////////////////////////////////////////////////////
            """
            
            """
            x und y Koordinaten der Bildpunkte im Verhaeltnis zur groeße des canvas der Webseite bestimmen zum Zeichnen
            
            """
            if Arbeitszustand == True:
                
                abweichung_x_str = str(round(abweichung_x))
                abweichung_y_str = str(round(abweichung_y))
                abweichung_gesamt_str = str(round(abweichung_gesamt))

        
            inhalt ={"antwort": "alles klar", "abweichung_x": abweichung_x_str, "abweichung_y": abweichung_y_str, "abweichung_gesamt": abweichung_gesamt_str}
 
            if Arbeitszustand == False:
                
                inhalt = {"antwort": "abgebrochen", "abweichung_x": "0", "abweichung_y": "0", "abweichung_gesamt": "0",}
            
    
        """
        //////////////////////////////////Roboter Fernwartungsanfrage///////////////////////////////////////////////////////
        """
    
        if befehl == "speichern":
            
            abweichung_x = str(int(CORE['abweichung_x']))
            abweichung_y = str(int(CORE['abweichung_y']))
            gesamtabweichung = str(int(CORE['gesamtabweichung']))
                    

            anweisung = abweichung_x + " " + abweichung_y + " " + gesamtabweichung
            daten = {'befehl': anweisung}
            ip_adresse = "http://192.168.0.101:5000"
            pfad = '/vlacs_empfaenger/speichern'         
            inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
            anfrage_2 = vlacs.create_message(TO = "HTTPOUT",CORE = inhalt)      #Funktion ist in module.py 
            vlacs.send(anfrage_2)
            
            #Rückmeldung von HTTPOUT auffangen
            rueckmeldung = vlacs.poll(20000)
            kern_rueckmeldung =vlacs.extract_core(rueckmeldung)
            kern= kern_rueckmeldung['json_data']
            rueckmeldung_nachricht= kern['response']
       
            if rueckmeldung_nachricht == "response-timeout":
                        inhalt = {"antwort": "keine Verbindung zu Vlacs_Empfaenger"}
                        antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)
                        vlacs.send(antwort)
                        continue
            daten = {'befehl': "empfangen"}
            ip_adresse = "http://192.168.0.101:5000"
            pfad = '/vlacs_empfaenger/empfangen'         
            inhalt = {'request': "POST", 'json_data': daten, 'ip_address': ip_adresse, 'path': pfad}
            anfrage_2 = vlacs.create_message(TO = rueckmeldung,CORE = inhalt)      #Funktion ist in module.py 
            vlacs.send(anfrage_2)
 
            inhalt = {"antwort": "gespeichert"}

        """
        //////////////////////////////////Roboter Fernwartungsanfrage///////////////////////////////////////////////////////
        """
    
        if befehl == "stop":
            
            Arbeitszustand = False
            break
            
            inhalt = {"antwort": "abgebrochen"}
        
        antwort = vlacs.create_message(TO = MESSAGE, CORE = inhalt)    
        vlacs.send(antwort)
            

        
            
