'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul client_extern enthält die Funktion send_message. Es handelt sich 
um einen Socket-Client, der zu Testzwecken erstellt wurde. Nach der Funktion
werden alle möglichen Funktionsaufrufe in alphabetischer Reihenfolge gezeigt.
'''

'Module importieren'
from socket import AF_INET, SOCK_STREAM, socket
from time import sleep
'Funktion send_message'
def open_message():
    global komm
    'Kommunikationssocket instanziieren'
    #IPv4-Protokoll und TCP
    komm = socket(AF_INET, SOCK_STREAM)
    'Verbindung herstellen'
    #lokale IP-Adresse und Port 60000
    komm.connect(('localhost', 60111))

#    try:
#        while True:

def send(nachricht):
    '''Nachricht in den Datentyp bytes konvertieren 
    und an den Server senden'''
    komm.send(nachricht.encode())
    'Daten vom Server empfangen'
    #Datentyp von data: bytes
#    data = komm.recv(1024)
    'Antwort vom Server'
    #Daten in str konvertieren
#    antwort = data.decode()
    'Bildschirmausgabe'
#    print(antwort)
#    return
#            
#    finally:
#        'Kommunikationssocket schließen'
#        komm.close
        
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

open_message()
sleep(5)
send('robo&robo&20')
sleep(5)
send('robo&robo&18 01 00 00 00 00 00 00')
sleep(5)
send('robo&robo&18 02 00 00 00 00 00 00')
