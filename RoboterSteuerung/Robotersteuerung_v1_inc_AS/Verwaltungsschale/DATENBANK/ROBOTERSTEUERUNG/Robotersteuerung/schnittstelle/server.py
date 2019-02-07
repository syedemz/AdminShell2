'''
Autor: Martin Schinnerl
Datum: 25.09.2016
Überarbeitung: Thomas Dasbach

Modulbeschreibung:
Das Modul server enthält die Klasse Server, die im Sinne der parallelen
Programmierung von der Klasse QObject abgeleitet wird. Die Klasse enthält 
den Programmcode eines Socket-Servers zur Kommunikation mit einem externen 
Client. Ein Objekt der Klasse wird parallel zur grafischen Benutzungsober-
fläche in einem Thread gestartet. Zahlreiche Signale ermöglichen die Komm-
unikation mit der Benutzungsoberfläche. Die Statusabfrage und die Bedienung 
der Oberfläche sowie die Fernsteuerung des Roboters von extern sind möglich.
Bekannte Befehle:
01: Animation aktualisieren
02: Gibt die aktuelle Perspektive auf den Roboter zurück
03: Wechselt die aktuelle Perspektive auf den Roboter
04: Aufnahme ...
04 01: ... abbrechen
04 02: ... beenden
04 03: ... beginnen
04 04: ... speichern
04 05: ... zuruecksetzen
05: Bearbeiten schliessen
06: Greifer abfragen
07: Lage abfragen
08: Orientierung abfragen
09: Position ...
09 01: ...aendern
09 02: ...anfang
09 03: ...anzeigen
09 04: ...einlesen
09 05: ...ende
09 06: ...nummer
09 07: ...speichern
09 08: ...vor
09 09: ...zurueck
10: Programmauswahl
10 01: ...abfragen
10 02: ...aendern
11: Programm ...
11 01: ...bearbeiten
11 02: ...erstellen
11 03: ...ext
11 04: ...fortsetzen
11 05: ...start
11 06: ...stop
11 07: ...waehlen
12: Roboter fernsteuern, Bewegungsvektor
13: Tab abfragen
14: Wartung...
14 01: ...beenden
14 02: ...beginnen
14 03: ...oeffnen
14 04: ...schliessen
15: Winkel abfragen
'''

'Module importieren'
from numpy import save, hsplit, vsplit, vstack
from PyQt4.QtCore import QObject, Signal, QThread
from socket import AF_INET, SOCK_STREAM, socket
import os
import sys
import struct
from time import sleep
from schnittstelle.server_empfaenger import Server_empfaenger

sys.path.append(os.path.abspath('../../'))

import json
from structure import module
from structure import configuration

#from pprint import pprint


'Klasse Server'
class Server(QObject):
    
    'Signale definieren'
    
    #Animation aktualisieren
    animation_akt = Signal(float, float, float, float, float, float, \
    float, float, float, float, float, float, float)

    #Ansicht abfragen
    ansicht_abf = Signal()
    #Ansicht wechseln
    ansicht_wec = Signal(int)
    
    #Aufnahme abbrechen
    aufnahme_abb = Signal()
    #Aufnahme beenden
    aufnahme_bee = Signal()
    #Aufnahme beginnen
    aufnahme_beg = Signal()
    #Aufnahme speichern
    aufnahme_spe = Signal(str)
    #Aufnahme zurücksetzen
    aufnahme_zur = Signal()
    
    #Bearbeiten schließen
    bearbeiten_sch = Signal()
    
    #Beenden des Threads
    finished = Signal()
    
    #Greifer abfragen
    greifer_abf = Signal()
    #Lage abfragen
    lage_abf = Signal()
    #Orientierung abfragen
    orientierung_abf = Signal()
    
    #Position ändern
    position_aen = Signal()
    #Position Anfang
    position_anf = Signal()
    #Position anzeigen
    position_anz = Signal(int)
    #Position einlesen
    position_ein = Signal()
    #Position Ende
    position_end = Signal()
    #Position Nummer
    position_num = Signal()
    #Position speichern
    position_spe = Signal()
    #Position vor
    position_vor = Signal()
    #Position zurück
    position_zur = Signal()
    
    #Programmauswahl abfragen
    programmauswahl_abf = Signal()
    #Programmauswahl ändern
    programmauswahl_aen = Signal()
    
    #Programm bearbeiten
    programm_bea = Signal()
    #Programm erstellen
    programm_ers = Signal()
    #Programm extern
    programm_ext = Signal(str, int)
    #Programm fortsetzen
    programm_for = Signal()
    #Programm starten
    programm_sta = Signal()
    #Programm stoppen
    programm_sto = Signal()
    #Programm wählen
    programm_wae = Signal(int)
    
    #Roboter fernsteuern
    roboter_fern = Signal()
    roboter_fern_vektor = Signal(int, int, int, int, int, int)
    roboter_fern_aus = Signal()

    roboter_fern_abs = Signal()
    roboter_fern_abs_vektor = Signal(int, int, int, int, int, int)
    roboter_fern_abs_aus = Signal()
    
    #Fernsteuerungsanfrage
    roboter_fern_anfrage = Signal(str)
    
    #G-Code Signale
    roboter_fern_g_code_on = Signal()
    roboter_fern_g_code_off = Signal()
    roboter_fern_g_code_move = Signal(int, int, int, int)
    roboter_fern_g_code_pause = Signal(int)
    roboter_fern_g_code_switch_inch = Signal()
    roboter_fern_g_code_switch_mm = Signal()
    roboter_fern_g_code_notaus = Signal()
    roboter_fern_g_code_aus = Signal()
    roboter_fern_g_code_start_programm = Signal(str)
    roboter_fern_g_code_stop_programm = Signal()
     
    roboter_zustandsanfrage = Signal(str)
    roboter_zustandsaussage = Signal(str, str)
    server_protokoll = Signal(str, str)
    
    fernsteuerung_mot = Signal(str)
    
    
    
    #Tab abfragen
    tab_abf = Signal()

    #Wartung beenden
    wartung_bee = Signal()
    #Wartung beginnen
    wartung_beg = Signal()
    #Wartung öffnen
    wartung_oef = Signal()
    #Wartung schließen
    wartung_sch = Signal()
    
    #Winkel abfragen
    winkel_abf = Signal()
    
    

    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QObject'

        super(Server, self).__init__(parent)
        
        global akz_app
        
        akz_app = ' '
        
#        akz_app = 'x-box'
        self.schnitt = True
        
        self.coord_g = [0,0,0,0,0,0,0]
        
        self.identitaet = [configuration.config['ROBO_GUI']['identity']]
        
        self.HOST, self.PORT = "localhost", 9999
        
    'Methode server_starten'
    def server_starten(self):
        
        self.mode = 0
        self.g_code_modus = False
        
        
        self.message_lenght = 1024
        
        if self.schnitt == False: 
            self.server_con = module.module('ROBO_GUI_SHADOW', configuration.config)
        else:
            self.verb = socket(AF_INET, SOCK_STREAM)
            verbinde = True
            while verbinde == True:
                try:                
                    self.verb.connect(('localhost', 60112))
                    verbinde = False
                except ConnectionRefusedError:
                    sleep(1/10)
                except OSError:
                    verbinde = False    
        
        
        self.thread_server_emp = QThread()
        
        'Server-Objekt instanziieren'
        self.server_emp = Server_empfaenger()
        
        'Server-Objekt an den Thread übergeben'
        self.server_emp.moveToThread(self.thread_server_emp)
        
        'Signale und Slots verbinden'
        self.thread_server_emp.started.connect(self.server_emp.server_starten)
        
        self.server_emp.nachricht_empfangen.connect( \
        self.nachricht_empfangen)
        
        self.thread_server_emp.finished.connect(self.thread_server_emp.deleteLater)

        'Methode start des Thread-Objektes aufrufen'
        self.thread_server_emp.start()
        'Methode exec des Thread-Objektes aufrufen'
        self.thread_server_emp.exec()
#        self.message_lenght = 1024
#        self.server_con = module.entity('ROBO_GUI', configuration.config)
        
        if self.socket == True:
            'Verbindungssocket instanziieren'
            'IPv4-Protokoll und TCP'
#            self.device = socket(AF_INET, SOCK_STREAM)
            
#            'Verbindungssocket an eine IP-Adresse und einen Port binden'
#            #lokale IP-Adresse und Port 60000
#            self.verb.bind(('localhost', 60100))
#            
#            'Verbindungssocket auf Anfragen horchen lassen'
#            #maximale Anzahl: 5
#            self.verb.listen(5)
        
        'Information ausgeben'
        print('Server läuft und hört zu...')
                
#        
#        while True:    
                
        '''Verbindungsanfrage akzeptieren. Es werden der 
        Kommunikationssocket und das Adressobjekt des
        Verbindungspartners zurückgegeben.'''
#                self.komm, addr = self.verb.accept()
            



#                request = CORE_pyobj["request"]
#                response = data[request].to_dict()
#                for key in response:
#                    response = str(response)
                
        'Daten vom Client empfangen'
            #Datentyp von data: bytes
#                    data = self.komm.recv(self.message_lenght) 
            
#            MESSAGE = self.server_con.receive()
#            CORE_pyobj = self.server_con.extract_core(MESSAGE)
#            
#            sender_cod = MESSAGE[1]
#            self.sender = str(sender_cod.decode('ascii'))
            
    def nachricht_empfangen(self, sender, nachricht_kompl, MESSAGE):
        
        
#            akz_app = self.fernsteuerung_mot
        self.sender = sender
#        print("sender: ", sender)
#        print("nachricht_kompl: ", nachricht_kompl)
#        print("MESSAGE: ", MESSAGE)
        
#        print('Aktueller Sender: ', self.sender)
#        print('Akzeptierte: ', akz_app)
#        if self.sender == akz_app:
#            print('Ist akzeptabel')
#        else:
#            print('Sender wird nicht akzeptiert.')
        
        
#        '''Wenn keine Daten ankommen, wird der
#        Kommunikationssocket geschlossen.'''
#        if not data:
#            self.komm.close()
#            break
        
        'Nachricht vom Client'
        #Daten in str konvertieren
#        nachricht_kompl = data.decode()
#        print(nachricht_kompl)
        
#        print(nachricht_kompl)
        '''Die Nachricht entsprechend der Leerzeichen
        in Teile zerlegen.'''
        
#        print('Nachricht_kompl: ', nachricht_kompl)
        nachricht = nachricht_kompl.split(' ')


        '''Im Weiteren wird die Nachricht des Client dem
        entsprechenden Fall zugeordnet, das Signal gesendet,
        die Antwort erstellt und dem Client übermittelt.
        Beispiele zeigen den jeweiligen Aufruf.'''
        
        if nachricht[0] == '01':
            print("Test")
#                        '''Aktualisiert den digitalen Roboter. Beim 
#                        Aufruf sind Lage und Orientierung des Werkzeug-
#                        koordinatensystems in 0-Koordinaten sowie der
#                        Öffnungsradius des Greifers zu übergeben.  
#                        Bsp.: 'Animation aktualisieren_' + \
#                        '0, 0, 1, 0, 1, 0, -1, 0, 0' + \
#                        '-213.393, 0, 217.246, 150'
#                        '''
#                        '''Lage und Orientierung in 0-Koordinaten
#                        sowie den Öffnungsradius des Greifers zuordnen'''
#                        xe1, ye1, ze1, xe2, ye2, ze2, xe3, ye3, ze3, \
#                        xP5, yP5, zP5, r6 = nachricht[1].split(', ')
#                        
#                        'Datentyp von str in float ändern'
#                        #Koordinaten des Einheitsvektors in x-Richtung                        
#                        xe1 = float(xe1)
#                        ye1 = float(ye1)
#                        ze1 = float(ze1)
#                        #Koordinaten des Einheitsvektors in y-Richtung
#                        xe2 = float(xe2)
#                        ye2 = float(ye2)
#                        ze2 = float(ze2)
#                        #Koordinaten des Einheitsvektors in z-Richtung
#                        xe3 = float(xe3)
#                        ye3 = float(ye3)
#                        ze3 = float(ze3)
#                        #Koordinaten des Verschiebungsvektors
#                        xP5 = float(xP5)
#                        yP5 = float(yP5)
#                        zP5 = float(zP5)
#                        #Öffnungsradius des Greifers
#                        r6 = float(r6)
#                        
#                        'Signal animation_akt senden'
#                        self.animation_akt.emit(xe1, ye1, ze1, xe2, ye2, \
#                        ze2, xe3, ye3, ze3, xP5, yP5, zP5, r6)
#                        
#                        'Antwort erstellen und an den Client senden'
#                        antwort = 'Animation aktualisieren'
#                        self.komm.send(antwort.encode())
#                            
#                    elif nachricht[0] == '02':
#                           
#                        if nachricht[1] == 'abfragen':
#                            '''Ansicht des digitalen Roboters abfragen.
#                            Bsp.: 'Ansicht_abfragen'    
#                            '''
#                            'Signal ansicht_abf senden'
#                            self.ansicht_abf.emit()
#                            
#                        elif nachricht[1] == '03':   
#                            '''Ansicht des digitalen Roboters wechseln. 
#                            Beim Aufruf ist der Index der Ansicht zu 
#                            übergeben.
#                            'Bsp.: 'Ansicht_wechseln_0'
#                            '''
#                            'Index der Ansicht'
#                            #Index 0 entspricht der Draufsicht
#                            #Index 1 entspricht der Seitenansicht
#                            #Index 2 entspricht der Greiferansicht
#                            ind = int(nachricht[2])   
#                            
#                            'Signal ansicht_wec senden'
#                            self.ansicht_wec.emit(ind)
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Ansicht wechseln'
#                            self.komm.send(antwort.encode())
#    
#                    elif nachricht[0] == '04':
#                        
#                        if nachricht[1] == '01':
#                            '''Aufnahme abbrechen.
#                            Bsp.: 'Aufnahme_abbrechen'
#                            '''
#                            'Signal aufnahme_abb senden'
#                            self.aufnahme_abb.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Aufnahme abbrechen'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '02':
#                            '''Aufnahme beenden.
#                            Bsp.: 'Aufnahme_beenden'
#                            '''
#                            'Signal aufnahme_bee senden'
#                            self.aufnahme_bee.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Aufnahme beenden'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '03':
#                            '''Aufnahme beginnen.
#                            Bsp.: 'Aufnahme_beginnen'
#                            '''
#                            'Signal aufnahme_beg senden'
#                            self.aufnahme_beg.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Aufnahme beginnen'
#                            self.komm.send(antwort.encode())    
#                            
#                        elif nachricht[1] == '04':
#                            '''Aufnahme speichern. Beim Aufruf ist der
#                            Speicherplatz zu übergeben.
#                            Bsp.: 'Aufnahme_speichern_1'
#                            '''
#                            'Speicherplatz'
#                            #Platz 1 bis 5 oder größer
#                            speicherplatz = nachricht[2]
#                            
#                            'Signal aufnahme_spe senden'
#                            self.aufnahme_spe.emit(speicherplatz)
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Aufnahme auf Platz ' + \
#                            speicherplatz + ' speichern'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '05':
#                            '''Aufnahme zurücksetzen.
#                            Bsp.: 'Aufnahme_zuruecksetzen'
#                            '''
#                            'Signal aufname_zur senden'
#                            self.aufnahme_zur.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Aufnahme zuruecksetzen'
#                            self.komm.send(antwort.encode())
#    
#                    elif nachricht[0] == '05':
#                        '''Bearbeiten schließen.
#                        Bsp.: 'Bearbeiten schliessen'
#                        '''
#                        'Signal bearbeiten_sch senden'
#                        self.bearbeiten_sch.emit()
#                        
#                        'Antwort erstellen und an den Client senden'
#                        antwort = 'Bearbeiten schliessen'
#                        self.komm.send(antwort.encode())
#                    
#                    elif nachricht[0] == '06':
#                        '''Abfrage des Öffnungsradius des Greifers.
#                        Bsp.: 'Greifer abfragen'
#                        '''
#                        'Signal greifer_abf senden'
#                        self.greifer_abf.emit()
#                        
#                    elif nachricht[0] == '07':
#                        '''Abfrage der Lage des Werkzeug-
#                        Koordinatensystems.
#                        Bsp.: 'Lage abfragen'
#                        '''
#                        'Signal lage_abf senden'
#                        self.lage_abf.emit()
#                            
#                    elif nachricht[0] == '08':
#                        '''Abfrage der Orientierung des Werkzeug-
#                        Koordinatensystems.
#                        Bsp.: 'Orientierung abfragen'
#                        '''
#                        'Signal orientierung_abf senden'
#                        self.orientierung_abf.emit()
#                        
#                    elif nachricht[0] == '09':
#                        
#                        if nachricht[1] == '01':
#                            '''Aufgerufene Position des Programmes
#                            in Bearbeitung ändern.
#                            Bsp. 'Position_aendern'
#                            '''
#                            'Signal position_aen senden'
#                            self.position_aen.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Position aendern'
#                            self.komm.send(antwort.encode())
#                        
#                        elif nachricht[1] == '02':
#                            '''Erste Position des Programmes in 
#                            Bearbeitung anzeigen.
#                            Bsp.: 'Position_anfang'
#                            '''
#                            'Signal position_anf senden'
#                            self.position_anf.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Erste Position anzeigen'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '03':
#                            '''Position x des Programmes in Bearbeitung
#                            anzeigen. Beim Aufruf ist die Nummer der
#                            anzuzeigenden Position zu übergeben.
#                            Bsp.: 'Position_anzeigen_1'
#                            '''
#                            'Positionsnummer'
#                            nr = int(nachricht[2])
#                            
#                            'Signal position_anz senden'
#                            self.position_anz.emit(nr)
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Position ' + nachricht[2] + ' anzeigen'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '04':
#                            '''Position einlesen.
#                            Bsp.: 'Position_einlesen'
#                            '''
#                            'Signal position_ein senden'
#                            self.position_ein.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Position einlesen'
#                            self.komm.send(antwort.encode())    
#                            
#                        elif nachricht[1] == '05':
#                            '''Letzte Position des Programmes in 
#                            Bearbeitung anzeigen.
#                            Bsp.: 'Position_ende'
#                            '''
#                            'Signal position_end senden'
#                            self.position_end.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Letzte Position anzeigen'
#                            self.komm.send(antwort.encode())    
#                        
#                        elif nachricht[1] == '06':
#                            '''Abfrage der angezeigten Position des
#                            Programmes in Bearbeitung.
#                            Bsp.: 'Position_abfragen'
#                            '''
#                            'Signal position_num senden'
#                            self.position_num.emit() 
#                            
#                        elif nachricht[1] == '07':
#                            '''Änderungen nach der Korrektur einer 
#                            Position speichern.
#                            Bsp.: 'Position_speichern'
#                            '''
#                            'Signal position_spe senden'
#                            self.position_spe.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Position speichern'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '08':
#                            '''Nächste Position des Programmes 
#                            in Bearbeitung anzeigen.
#                            Bsp.: 'Position_vor'
#                            '''
#                            'Signal position_vor senden'
#                            self.position_vor.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Position vor'
#                            self.komm.send(antwort.encode())
#                           
#                        elif nachricht[1] == '09':
#                            '''Vorhergehende Position des Programmes
#                            in Bearbeitung anzeigen.
#                            Bsp. 'Position_zurueck'
#                            '''
#                            'Signal position_zur senden'
#                            self.position_zur.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Position zurueck'
#                            self.komm.send(antwort.encode())   
#                        
#                    elif nachricht[0] == '10':
#                        
#                        if nachricht[1] == '01':
#                            '''Programmauswahl abfragen.
#                            Bsp.: 'Programmauswahl_abfragen'
#                            '''
#                            'Signal programmauswahl_abf senden'
#                            self.programmauswahl_abf.emit()        
#                    
#                        elif nachricht[1] == '02':
#                            '''Programmauswahl ändern.
#                            Bsp.: 'Programmauswahl_aendern'
#                            '''
#                            'Signal programmauswahl_aen senden'
#                            self.programmauswahl_aen.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Programmauswahl aendern'
#                            self.komm.send(antwort.encode())
#                    
#                    elif nachricht[0] == '11':
#                        
#                        if nachricht[1] == '01':
#                            '''Programm bearbeiten.
#                            Bsp.: 'Programm_bearbeiten'
#                            '''
#                            'Signal programm_bea senden'
#                            self.programm_bea.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Programm bearbeiten'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '02':
#                            '''Programm erstellen.
#                            Bsp.: 'Programm_erstellen'
#                            '''
#                            'Signal programm_ers senden'
#                            self.programm_ers.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Programm erstellen'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '03':
#                            '''Programm von extern ausführen. Beim Aufruf
#                            sind der Speicherplatz und die Zeit in [ms]
#                            zu übergeben.
#                            Bsp.: 'Programm_ext_1_3000'
#                            '''
#                            'Speicherplatz'
#                            speichername = 'programm' + nachricht[2]
#                            'Zeit'              
#                            t = int(nachricht[3])
#                            
#                            'Signal programm_ext senden'
#                            self.programm_ext.emit(speichername, t)
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Programm ' + nachricht[2] + ' starten'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '04':
#                            '''Programm fortsetzen.
#                            Bsp.: 'Programm_fortsetzen'
#                            '''
#                            'Signal programm_for senden'
#                            self.programm_for.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Programm fortsetzen'
#                            self.komm.send(antwort.encode())    
#                                                        
#                        elif nachricht[1] == '05':
#                            '''Programm starten.
#                            Bsp.: 'Programm_start'
#                            '''
#                            'Signal programm_sta senden'
#                            self.programm_sta.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Programm starten'
#                            self.komm.send(antwort.encode())
#                                
#                        elif nachricht[1] == '06':
#                            '''Programm unterbrechen.
#                            Bsp. 'Programm_stop'
#                            '''
#                            'Signal programm_sto senden'
#                            self.programm_sto.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Programm anhalten'
#                            self.komm.send(antwort.encode()) 
#                                                    
#                        elif nachricht[1] == '07':
#                            '''Programm wählen. Beim Aufruf ist die 
#                            Nummer des Programms zu übergeben.
#                            Bsp.: 'Programm_waehlen_1'
#                            '''
#                            'Programmnummer'
#                            #Nummer von 1 bis 5
#                            nr = int(nachricht[2])
#                            
#                            'Signal programm_wae senden'
#                            self.programm_wae.emit(nr)
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Programm ' + str(nr) + ' gewaehlt'
#                            self.komm.send(antwort.encode())
#                            
        elif nachricht[0] == '12' and self.sender == akz_app:
            self.server_protokoll.emit(self.sender, nachricht_kompl)
            if nachricht[1] == '01':
                '''Roboter Fernsteuerung aktivieren.
                Befehlsform
                XX YY 000 000 000 000 000 000
                XX = 12, Befehlsaufruf
                YY = 01, Befehlsaufruf
                '''
#                    print("Nachricht beginnt mit 12 01")
                'Signal roboter_fern senden'
                self.roboter_fern.emit()
                    
                'Antwort erstellen und an den Client senden'
                antwort = 'Fernsteuerung aktiv'
#                            self.komm.send(antwort.encode())
                
                MESSAGE = self.create_traitor(CORE_pyobj = antwort, MESSAGE_received = MESSAGE)
                
                if self.schnitt == True:
#                    self.verb.connect(('localhost', 60112))
                    self.send_msg(self.verb, MESSAGE)
#                    self.verb.close()
                else:
                    self.server_con.send(MESSAGE)
                
            elif nachricht[1] == '02':
                
                '''Roboter fernsteuern.
                Befehlsform
                XX YY 111 222 333 444 555 666
                XX = 12, Befehlsaufruf
                YY = 02, Befehlsaufruf
                111 = Verschiebung in x0
                222 = Verschiebung in y0
                333 = Verschiebung in z0
                444 = Drehung um x0
                555 = Drehung um y0
                666 = Drehung um z0
                '''
                '''Werte und Zeit zuordnen'''

#                            print("Nachricht beginnt mit 12 02")
                'Datentyp von str in int ändern'
                p1 = int(nachricht[2])
                p2 = int(nachricht[3])
                p3 = int(nachricht[4])
                p4 = int(nachricht[5])
                p5 = int(nachricht[6])
                p6 = int(nachricht[7])
                

                'Signal roboter_fern senden'
                self.roboter_fern_vektor.emit(p1, p2, p3, \
                p4, p5, p6)

            elif nachricht[1] == '03':
                
                '''Fernsteuerung abschalten'''


                'Signal roboter_fern senden'
                self.roboter_fern_aus.emit()
                
#                        
#                    elif nachricht[0] == '13':
#                        '''Abfrage der geöffneten Seite.
#                        Bsp. 'Tab abfragen'
#                        '''
#                        'Signal tab_abf senden'
#                        self.tab_abf.emit()
#                        
#                    elif nachricht[0] == '14':
#                    
#                        if nachricht[1] == '01':
#                            '''Wartung beenden.
#                            Bsp. 'Wartung_beenden'
#                            '''
#                            'Signal wartung_bee senden'
#                            self.wartung_bee.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Wartung beenden'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '02':
#                            '''Wartung beginnen.
#                            Bsp.: 'Wartung_beginnen'
#                            '''
#                            'Signal wartung_beg senden'
#                            self.wartung_beg.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Wartung beginnen'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '03':
#                            '''Wartung öffnen.
#                            Bsp.: 'Wartung_oeffnen'
#                            '''
#                            'Signal wartung_oef senden'
#                            self.wartung_oef.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Wartung oeffnen'
#                            self.komm.send(antwort.encode())
#                            
#                        elif nachricht[1] == '04':
#                            '''Wartung schließen.
#                            Bsp.: 'Wartung_schliessen'
#                            '''
#                            'Signal wartung_sch senden'
#                            self.wartung_sch.emit()
#                            
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Wartung schliessen'
#                            self.komm.send(antwort.encode())
#                    
#                    elif nachricht[0] == '15':
#                        '''Abfrage der Winkel (Denavit-Hartenberg-
#                        Parameter)
#                        Bsp.: 'Winkel abfragen'
#                        '''
#                        'Signal winkel_abf senden'
#                        self.winkel_abf.emit()
 
 
            '''Methode 16 dient dem Einspeisen von großen
            Datenmatrizen. Es gibt atuell (22.02.2017) keinen
            echten Anwendungsfall.'''
        
        
        elif nachricht[0] == '16' and self.sender == akz_app:
            self.server_protokoll.emit(self.sender, nachricht_kompl)
            if nachricht[1] == '01':
                self.mode = 16
                self.winkel = (1.571,  3.142, -3.002,  \
                1.431,  1.571)
                self.greifer = 0.978
                self.anz = 0
            elif nachricht[1] == '02':
                '''Programmübertragung starten.
                Befehlsform
                XX YY 111 222 333 444 555 666
                XX = 12, Befehlsaufruf
                YY = 02, Befehlsaufruf
                Die Tupel sind jeweils Theta 1 bis 5
                '''
                '''Werte und Zeit zuordnen'''
                if(self.mode == 16):
                    self.anz += 1
#                    print("Ankommender Vektor ", self.anz)
 
                    'Datentyp von str in int ändern'
                    p1 = float(nachricht[2])
                    p2 = float(nachricht[3])
                    p3 = float(nachricht[4])
                    p4 = float(nachricht[5])
                    p5 = float(nachricht[6])
                    p6 = float(nachricht[7])
                    
                    
                    
#                                self.P05 = array([[p1],[p2],[p3],[0]])
#                                
#                                self.x5in0, self.y5in0, self.z5in0 = \
#                                Eulertransformation(p4, p5, p6)
                    
                    self.winkel_neu = (p1, p2, p3, p4, p5)
                    'Position einfügen'
                    self.winkel = vstack((self.winkel, \
                    self.winkel_neu))
#                                pprint(self.winkel)
                    
                    self.greifer_neu = p6
                    self.greifer = vstack((self.greifer, \
                    self.greifer_neu))



            elif nachricht[1] == '03':
#                print('Array: ' , self.winkel.shape)  
                workdir = os.getcwd()
                dateiname = 'fernsteuerung' + \
                '_winkel.npy'
                dir = os.path.join(workdir, 'speicher', \
                'programmspeicher', dateiname)
#                            pprint(self.winkel)
                save(dir, self.winkel)
                
#                print('Array: ' , self.greifer.shape)  
                workdir = os.getcwd()
                dateiname = 'fernsteuerung' + \
                '_greifer.npy'
                dir = os.path.join(workdir, 'speicher', \
                'programmspeicher', dateiname)
#                            pprint(self.winkel)
                save(dir, self.greifer)
                

                self.mode = 0
                    
            elif nachricht[1] == '04':
                if self.mode == 0:
                    self.t = 1
                    self.programm_ext.emit(\
                    'fernsteuerung', self.t)
                    

        elif nachricht[0] == '17' and self.sender == akz_app:
            self.server_protokoll.emit(self.sender, nachricht_kompl)
            if nachricht[1] == '01':
                '''Roboter Fernsteuerung aktivieren.
                Befehlsform
                XX YY 000 000 000 000 000 000
                XX = 18, Befehlsaufruf
                YY = 01, Befehlsaufruf
                '''
#                            print("Nachricht beginnt mit 12 01")
                'Signal roboter_fern senden'
                self.roboter_fern.emit()
                    
                'Antwort erstellen und an den Client senden'
                antwort = 'Remote control enabled'
                MESSAGE = self.create_traitor(CORE_pyobj = antwort, MESSAGE_received = MESSAGE)
                if self.schnitt == True:
#                    self.verb.connect(('localhost', 60112))
                    self.send_msg(self.verb, MESSAGE)
#                    self.verb.close()
                else:
                    self.server_con.send(MESSAGE)
                self.message_lenght = 29
                
            elif nachricht[1] == '02':
                
                '''Roboter fernsteuern.
                Befehlsform
                XX YY 111 222 333 444 555 666
                XX = 18, Befehlsaufruf
                YY = 02, Befehlsaufruf
                111 = Verschiebung in x0
                222 = Verschiebung in y0
                333 = Verschiebung in z0
                444 = Drehung um x0
                555 = Drehung um y0
                666 = Drehung um z0
                '''
                '''Werte und Zeit zuordnen'''

                'Datentyp von str in int ändern'
                p1 = int(nachricht[2]) - 4
                p2 = int(nachricht[3]) - 4
                p3 = int(nachricht[4]) - 4
                Spd_ver = int(nachricht[5]) - 4
                p5 = int(nachricht[6]) - 4
                p6 = int(nachricht[7]) - 4
                

                'Signal roboter_fern senden'
                self.roboter_fern_vektor.emit(p1, p2, p3, \
                Spd_ver, p5, p6)
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Vektor gesendet'
#                            self.komm.send(antwort.encode())

#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Vektor gesendet'
#                            self.komm.send(antwort.encode())

            if nachricht[1] == '03':
                '''Roboter Fernsteuerung deaktivieren.
                Befehlsform
                XX YY 000 000 000 000 000 000
                XX = 18, Befehlsaufruf
                YY = 01, Befehlsaufruf
                '''
#                            print("Nachricht beginnt mit 12 01")
                'Signal roboter_fern senden'
                self.roboter_fern_aus.emit()
                    
                'Antwort erstellen und an den Client senden'
                antwort = 'Remote control disabled'
                MESSAGE = self.create_traitor(CORE_pyobj = antwort, MESSAGE_received = MESSAGE)
                if self.schnitt == True:
#                    self.verb.connect(('localhost', 60112))
                    self.send_msg(self.verb, MESSAGE)
#                    self.verb.close()
                else:
                    self.server_con.send(MESSAGE)
                self.message_lenght = 29

        elif nachricht[0] == '18' and self.sender == akz_app:
            self.server_protokoll.emit(self.sender, nachricht_kompl)
            if nachricht[1] == '01':
                '''Roboter Fernsteuerung aktivieren.
                Befehlsform
                XX YY 000 000 000 000 000 000
                XX = 12, Befehlsaufruf
                YY = 01, Befehlsaufruf
                '''
#                            print("Nachricht beginnt mit 12 01")
                'Signal roboter_fern senden'
                self.roboter_fern_abs.emit()
                    
                'Antwort erstellen und an den Client senden'
                antwort = 'Remote control enabled'
                MESSAGE = self.create_traitor(CORE_pyobj = antwort, MESSAGE_received = MESSAGE)
                if self.schnitt == True:
#                    self.verb.connect(('localhost', 60112))
                    self.send_msg(self.verb, MESSAGE)
#                    self.verb.close()
                else:
                    self.server_con.send(MESSAGE)
                self.message_lenght = 29
                
            elif nachricht[1] == '02':
                '''ANPASSEN'''                        
                '''Roboter fernsteuern.
                Befehlsform
                XX YY 111 222 333 444 555 666
                XX = 12, Befehlsaufruf
                YY = 02, Befehlsaufruf
                111 = Angabe des ersten Motorwinkel
                222 = Angabe des zweiten Motorwinkel
                333 = Angabe des dritten Motorwinkel
                444 = Angabe des vierten Motorwinkel
                555 = Angabe des fünften Motorwinkel
                666 = Angabe über Öfnnungswinkel des Greifers
                '''
                '''Werte und Zeit zuordnen'''

                'Datentyp von str in int ändern'

                
                p1 = int(nachricht[2])
                p2 = int(nachricht[3])
                p3 = int(nachricht[4])
                Spd_ver = int(nachricht[5])
                p5 = int(nachricht[6])
                p6 = int(nachricht[7])
                'Signal roboter_fern senden'
                self.roboter_fern_abs_vektor.emit(p1, p2, p3, \
                Spd_ver, p5, p6)
#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Vektor gesendet'
#                            self.komm.send(antwort.encode())

#                            'Antwort erstellen und an den Client senden'
#                            antwort = 'Vektor gesendet'
#                            self.komm.send(antwort.encode())

            if nachricht[1] == '03':
                '''Roboter Fernsteuerung deaktivieren.
                Befehlsform
                XX YY 000 000 000 000 000 000
                XX = 12, Befehlsaufruf
                YY = 01, Befehlsaufruf
                '''
#                            print("Nachricht beginnt mit 12 01")
                'Signal roboter_fern senden'
                self.roboter_fern_abs_aus.emit()
                    
                'Antwort erstellen und an den Client senden'
                antwort = 'Remote control disabled'
                MESSAGE = self.create_traitor(CORE_pyobj = antwort, MESSAGE_received = MESSAGE)
                if self.schnitt == True:
#                    self.verb.connect(('localhost', 60112))
                    self.send_msg(self.verb, MESSAGE)
#                    self.verb.close()
                else:
                    self.server_con.send(MESSAGE)
                

#                if self.socket == True: 
#               
#                    'Nachricht an den Servocontroller senden'
#                    self.device.sendto(antwort + "\n", (self.HOST, self.PORT))
#                    
                self.message_lenght = 29

            '''G-Code Schnittstelle - Als Erkennungszeichen wird die Zeilen-
            nummerierung verwendet. Jeder G-Code beginnt mit Angabe der Zeile.
            Diese beginnt mit einem N, direkt gefolgt von der Zeilennummer.
            Anschließend werden die verschiedenen Befehlstypen angegeben.
            Mögliche Befehle sind:

            Noch umzusetzen:
            G00 - Schnelllauf
            G01 - Gerade Bewegung
            G04 - Pause, Angabe in ms
            G09 - Kurzzeitiger Stopp
            G20 - Umstellen auf Inch
            G21 - Umstellen auf mm
            G61 - Schnellstopp
            G64 - Normaler Stoppmodus
            G66 - Ruft ein Macro auf
            G67 - Beendet den Macroaufruf von G66
            '''

        elif nachricht[0] == '19' and self.sender == akz_app:
            self.server_protokoll.emit(self.sender, nachricht_kompl)            
            if self.g_code_modus == False:
                self.g_code_modus = True
                self.roboter_fern_g_code_on.emit()
                antwort = 'G-Code Steuerung aktiviert.'
                MESSAGE = self.create_traitor(CORE_pyobj = antwort, MESSAGE_received = MESSAGE)
                
                if self.schnitt == True:
#                    self.verb.connect(('localhost', 60112))
                    self.send_msg(self.verb, MESSAGE)
#                    self.verb.close()
                else:
                    self.server_con.send(MESSAGE)
#                print(antwort)
                
            elif self.g_code_modus == True:
                self.g_code_modus = False
                self.roboter_fern_g_code_off.emit()   
                antwort = 'G-Code Steuerung deaktiviert.'
                MESSAGE = self.create_traitor(CORE_pyobj = antwort, MESSAGE_received = MESSAGE)
                
                if self.schnitt == True:
#                    self.verb.connect(('localhost', 60112))
                    self.send_msg(self.verb, MESSAGE)
#                    self.verb.close()
                else:
                    self.server_con.send(MESSAGE)
#                print(antwort)

        elif nachricht[0] == '20':
            self.server_protokoll.emit(self.sender, nachricht_kompl)
            self.roboter_fern_anfrage.emit(self.sender)
            
        elif nachricht[0] == '21':
            self.server_protokoll.emit(self.sender, nachricht_kompl)
            self.roboter_zustandsanfrage.emit(self.sender)                            
        
        if self.g_code_modus == True:
            self.g_code_index = nachricht[0]
            if self.g_code_index[0] == 'N' and self.sender == akz_app:
                
                self.server_protokoll.emit(self.sender, nachricht_kompl)
                
                self.g_code_com_kompl = nachricht[1]
                
                self.g_code_com = int(self.g_code_com_kompl[1:])
                
#                print('G-Code: ', self.g_code_com)
                
                if self.g_code_com == 0:
                    for i in range(2,5):
                        self.msg_spl = nachricht[i]        
                        self.coord_g[i] = int(self.msg_spl[1:])
#                        print('i: ', i, '  coord: ', self.coord_g[i])
                        
                    self.roboter_fern_g_code_move.emit(self.coord_g[2],self.coord_g[3],self.coord_g[4], 10)
                
                if self.g_code_com == 1:
                    for i in range(2,5):
                        self.msg_spl = nachricht[i]
                        
                        self.coord_g[i] = int(self.msg_spl[1:])
#                        print('i: ', i, '  coord: ', self.coord_g[i])
                        
                    self.roboter_fern_g_code_move.emit(self.coord_g[2],self.coord_g[3],self.coord_g[4], 5)
                
                if self.g_code_com == 4:
                    self.msg_spl_kompl = nachricht[2]
                    self.msg_spl = self.msg_spl_kompl[1:]
#                    print(int(self.msg_spl))
                    self.roboter_fern_g_code_pause.emit(int(self.msg_spl))
                    
                if self.g_code_com == 9:
                    self.roboter_fern_g_code_pause.emit(1000)
                    
                if self.g_code_com == 20:
                    self.roboter_fern_g_code_switch_inch.emit()
                    
                if self.g_code_com == 21:
                    self.roboter_fern_g_code_switch_mm.emit()
                    
                if self.g_code_com == 61:
                    self.roboter_fern_g_code_notaus.emit()
                    
                if self.g_code_com == 64:
                    self.roboter_fern_g_code_aus.emit()

                if self.g_code_com == 66:
                    self.msg_spl = nachricht[2]
                    self.roboter_fern_g_code_start_programm.emit(self.msg_spl)
                    
                if self.g_code_com == 67:
                    self.roboter_fern_g_code_stop_programm.emit()
                    
#        print(nachricht_kompl)
#        nachricht = []
        
#        finally:
#            
#           'Verbindungssocket schließen'
#           self.verb.close()
#           'Signal finished versenden'
#           self.finished.emit()
           
    '''Methode antwort_ansicht - Gibt die gewählte Ansicht
    des digitalen Roboters an den Client zurück.'''
    def antwort_ansicht(self, ind):
        
        'Antwort erstellen - Index der Ansicht zuordnen' 
        if ind == 0:
            antwort = 'Draufsicht'
        elif ind == 1:
            antwort = 'Seitenansicht'
        elif ind == 2:
            antwort = 'AnsichtGreifer'
        
        'Antwort an den Client senden'
        self.komm.send(antwort.encode())
    
    '''Methode matrixInString - Erstellt aus einer Matrix die Antwort
    als String.
    Bsp.: 0.0, 213.393, 30.131 '''
    def matrixInString(self, matrix):
        
        'Format der Matrix abfragen'
        zeilenzahl, spaltenzahl = matrix.shape
        'Matrix in Zeilen teilen'
        zeilen = vsplit(matrix, zeilenzahl)
        'leeren String erstellen'
        antwort = str()
        'Matrix zeilenweise durchlaufen'
        for i in range(0, zeilenzahl):
            'Matrix spaltenweise durchlaufen'
            for j in range(0, spaltenzahl):
                'Zeile in Spalten teilen'
                spalten = hsplit(zeilen[i], spaltenzahl)
                'Antwort zusammensetzen'
                antwort += str(float(spalten[j]))
                'Zeileneinträge mit Kommata trennen'
                if j < spaltenzahl-1:
                    antwort = antwort + ', '
            'mehrere Zeilen mit Backslash trennen'
            if i < zeilenzahl-1:
                antwort = antwort + ' / '
                
        return antwort 
        
    '''Methode antwort_greifer - Gibt den Öffnungsradius des Greifers 
    an den Client zurück.
    Bsp.: 150.0 '''
    def antwort_greifer(self, greifer):
        
        'Anwort erstellen und an den Client senden'
        antwort  = self.matrixInString(greifer)
        self.komm.send(antwort.encode())
        
    '''Methode antwort_lage - Gibt die Lage des Werkzeugkoordinatensystems
    (in 0-Koordinaten) an den Client zurück.
    Bsp.: 0.0, 213.393, 30.131 '''
    def antwort_lage(self, lage):
        
        'Antwort erstellen und an den Client senden'
        antwort = self.matrixInString(lage)
        self.komm.send(antwort.encode())
        
    '''Methode antwort_orientierung - Gibt die Orientierung des Werkzeug-
    koordinatensystems (in 0-Koordinaten) an den Client zurück.
    Bsp.: 1.0, -0.0, 0.0, 0.0, 0.0, -1.0, 0.0, 1.0, 0.0 '''
    def antwort_orientierung(self, orientierung):
        
        'Antwort erstellen und an den Client senden'
        antwort = self.matrixInString(orientierung)
        self.komm.send(antwort.encode())

    '''Methode antwort_positionsnummer - Gibt die angezeigte Position an
    den Client zurück.'''
    def antwort_positionsnummer(self, nr):
        
        'Antwort erstellen und an den Client senden'
        antwort = 'Position ' + str(nr) + ' gewaehlt'
        self.komm.send(antwort.encode())
       
    '''Methode antwort_programm - Gibt die Programmauswahl an den 
    Client zurück.'''
    def antwort_programm(self, nr):
        
        'Antwort erstellen'
        if nr == 0:
            antwort = 'kein Programm gewaehlt'
        elif nr != 0:
            antwort = 'Programm ' + str(nr) + ' gewaehlt'
            
        'Antwort an den Client senden'
        self.komm.send(antwort.encode())
    
    '''Methode antwort_tab - Gibt den angezeigten Tab an den Client
    zurück.'''
    def antwort_tab(self, ind):
        
        'Antwort erstellen - Index dem Tab zuordnen'
        if ind == 0:
            antwort = 'Programme'
        elif ind == 1:
            antwort = 'Programm_erstellen'
        elif ind == 2:
            antwort = 'Programm_bearbeiten'
        elif ind == 3:
            antwort = 'Wartung'
             
        'Antwort an den Client senden'
        self.komm.send(antwort.encode())   
       
    '''Methode antwort_winkel - Gibt die Winkel (Denavit-Hartenberg-
    Parameter) an den Client zurück.
    Bsp.: 1.571, 3.142, -3.002, 1.431, 1.571 '''
    def antwort_winkel(self, winkel):
        
        'Antwort erstellen und an den Client senden'
        antwort = self.matrixInString(winkel)
        self.komm.send(antwort.encode())


    def create_traitor(self, TO = b'someone', CORE_pyobj = "no input", MESSAGE_received = False):

        ADDRESS = []
        TO = [TO]
        FROM = self.identitaet
        CORE_json = json.dumps(CORE_pyobj)
        CORE = [CORE_json.encode('ascii')]

        if MESSAGE_received:

            MESSAGE_received.pop()
            TO = [MESSAGE_received.pop()]
            MESSAGE_received.pop()
            ADDRESS = MESSAGE_received
        
#            print('Adresse ', type(ADDRESS), ADDRESS)
#            print('TO ',type(TO), TO)
#            print('FROM ', type(FROM), FROM)
#            print('CORE ', type(CORE), CORE)
        if self.schnitt == False:
            MESSAGE = ADDRESS + TO + FROM + CORE
#            print("gesamte Message: ", MESSAGE)
        else:
#            print("Core: ", type(CORE[0]), CORE[0])
#            print("to: ", type(TO[0]), TO[0])
#            print("from: ", type(FROM[0]), FROM[0])
            MESSAGE = (bytes(TO[0]) + b'&' + bytes(FROM[0]) + b'&' + CORE[0])
#            print("Message: ", MESSAGE)
            
        return MESSAGE        
        
        
    def verbindung_zulassen(self, zul_app):
        global akz_app
        akz_app = str(zul_app)
#        print('Folgende App hat nun Zugriff: ', akz_app)
        antwort = 'Zugriff erteilt'      
        
        MESSAGE = self.create_traitor(TO = zul_app.encode('ascii'), CORE_pyobj = antwort)
        if self.schnitt == True:
#            self.verb.connect(('localhost', 60112))
            self.send_msg(self.verb, MESSAGE)
#            self.verb.close()
        else:
            self.server_con.send(MESSAGE)
#        if akz_app != ' ':
#            antwort = '20 01'
#            MESSAGE = self.server_con.create_message(TO = configuration.config[ant_app]['identity'], CORE_pyobj = antwort)
#            self.server_con.send(MESSAGE)
    
    def zustandsaussage(self, antwort_gui, a_sender):
        if akz_app != ' ':
            antwort = akz_app + " " + antwort_gui
        elif akz_app == ' ':
            antwort = 'XX ' + antwort_gui
        MESSAGE = self.create_traitor(TO = a_sender.encode('ascii'), CORE_pyobj = antwort)
        if self.schnitt == True:
#            self.verb.connect(('localhost', 60112))
            self.send_msg(self.verb, MESSAGE)
#            self.verb.close()
        else:
            self.server_con.send(MESSAGE)
        
    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)
    
    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)
    
    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        sock.connect(('localhost', 60112))
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
            sock.close()
        return data