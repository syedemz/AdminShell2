'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul client_extern enthält die Funktion send_message. Es handelt sich 
um einen Socket-Client, der zu Testzwecken erstellt wurde. Nach der Funktion
werden alle möglichen Funktionsaufrufe in alphabetischer Reihenfolge gezeigt.

Beispielbefehle:

12 01 000 000 000 000 000 000
12 02 120 120 120 120 120 120
12 02 000 010 000 000 000 000

16 01 000 000 000 000 000 000

16 02 1.571 3.142 -3.002 1.431 1.571 1

16 03 000 000 000 000 000 000

16 04 000 000 000 000 000 000
'''

'Module importieren'
from socket import AF_INET, SOCK_STREAM, socket
from time import sleep
from math import acos, cos, pi, sin
from numpy import around, array

#'Funktion send_message'
#def send_message(nachricht):

'Kommunikationssocket instanziieren'
'IPv4-Protokoll und TCP'
komm = socket(AF_INET, SOCK_STREAM)
'Verbindung herstellen'
#lokale IP-Adresse und Port 60000
komm.connect(('localhost', 60000))
aktiv = True

try:
    print('Willkommen beim externen Hilfprogramm')
    print('Wählen Sie zunächst den Modus')
    print('Modus 1: Senden von manuellen Befehlen')
    print('Modus 2: Senden eines Beispiel Programms (1000 Punkte)')
    mode = int(input('Modus:'))
    if (mode == 1):
            
        while aktiv:
            nachricht = input('Befehl: ')
            if nachricht == "end":
                aktiv = False            
            else:
                '''Nachricht in den Datentyp bytes konvertieren 
                und an den Server senden'''                
                komm.send(nachricht.encode('ascii'))
            'Daten vom Server empfangen'
            #Datentyp von data: bytes
            #data = komm.recv(1024)
            'Antwort vom Server'
            #Daten in str konvertieren
            #antwort = data.decode('ascii')
            'Bildschirmausgabe'
            #print(antwort)
        komm.close
    if (mode == 2):
        nachricht = '16 01'
        komm.send(nachricht.encode('ascii'))   
          
        winkel_start = array([1.571, 3.142, -3.002, 1.431, 0.8])
        winkel = winkel_start
        
        
        for i in range(0, 201):
           
            nachricht = ''
            nachricht += '16 02 '
            
#            modi = float((sin(3.1415 * i * 0.2) + 1)*0.95)
#            winkel[0] = float(3.1415 * modi/2)
#            nachricht += str(around(float(winkel[0]), 5))
#            nachricht += ' '
            nachricht += '1.571 '
#            
#            modi = float((cos(3.1415 * i * 0.2) + 1))
#            winkel[1] = float(3.1415 * modi/4 + 3.1415/2)
#            nachricht += str(around(float(winkel[1]), 5))
#            nachricht += ' '
#            
            nachricht += '3.142 '
            modi = float((cos(3.1415 * i * 0.02) + 1)*0.95)
            winkel[2] = float((-3.1415 * modi/2))
            nachricht += str(around(float(winkel[2]), 5))
            nachricht += ' '
#            nachricht += '-3.002 '
            
            nachricht += '1.431 1.571 0.978'
        #    print(nachricht)
            
            komm.send(nachricht.encode('ascii'))
            
            if i % 5 == 0:
                sleep(1/2)
                
                
        sleep(1)    
        nachricht = '16 03'
        komm.send(nachricht.encode('ascii'))
        print('Programm wurde erstellt.')
        komm.close
        
finally:
    'Kommunikationssocket schließen'
#    komm.close
        
'Übersicht über alle möglichen Anfragen'
#nachricht = 'Animation aktualisieren_' + \
#'0, 0, 1, 0, 1, 0, -1, 0, 0, -213.393, 0, 217.246, 150'
#send_message(nachricht)
#nachricht = 'Animation aktualisieren_' + \
#'-1, 0, 0, 0, 1, 0, 0, 0, -1, 338.744, 0, -25.181, 150'
#send_message(nachricht)
#nachricht = 'Animation aktualisieren_' + \
#'1, 0, 0, 0, 0, -1, 0, 1, 0, 0, 239.202, 323.708, 150'
#send_message(nachricht)

#send_message('Ansicht_abfragen')
#send_message('Ansicht_wechseln_0')
#send_message('Ansicht_wechseln_1')
#send_message('Ansicht_wechseln_2')

#send_message('Aufnahme_abbrechen')
#send_message('Aufnahme_beenden')
#send_message('Aufnahme_beginnen')
#send_message('Aufnahme_speichern_1')
#send_message('Aufnahme_speichern_2')
#send_message('Aufnahme_speichern_3')
#send_message('Aufnahme_speichern_4')
#send_message('Aufnahme_speichern_5')
#send_message('Aufnahme_zuruecksetzen')

#send_message('Bearbeiten schliessen')

#send_message('Greifer abfragen')
#send_message('Lage abfragen')
#send_message('Orientierung abfragen')

#send_message('Position_aendern')
#send_message('Position_anfang')
#send_message('Position_anzeigen_1')
#send_message('Position_einlesen')
#send_message('Position_ende')
#send_message('Position_nummer')
#send_message('Position_speichern')
#send_message('Position_vor')
#send_message('Position_zurueck')

#send_message('Programmauswahl_abfragen')
#send_message('Programmauswahl_aendern')

#send_message('Programm_bearbeiten')
#send_message('Programm_erstellen')
#send_message('Programm_ext_1_3000')
#send_message('Programm_fortsetzen')
#send_message('Programm_start')
#send_message('Programm_stop')
#send_message('Programm_waehlen_1')
#send_message('Programm_waehlen_2')
#send_message('Programm_waehlen_3')
#send_message('Programm_waehlen_4')
#send_message('Programm_waehlen_5')

#send_message('Roboter fernsteuern_0, 0, 0, 0, 0, 0, 3000')

#send_message('Tab abfragen')

#send_message('Wartung_beenden')
#send_message('Wartung_beginnen')
#send_message('Wartung_oeffnen')
#send_message('Wartung_schliessen')

#send_message('Winkel abfragen')