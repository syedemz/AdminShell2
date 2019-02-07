'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul server enthält die Klasse Server, die im Sinne der parallelen
Programmierung von der Klasse QObject abgeleitet wird. Die Klasse enthält 
den Programmcode eines Socket-Servers zur Kommunikation mit einem externen 
Client. Ein Objekt der Klasse wird parallel zur grafischen Benutzungsober-
fläche in einem Thread gestartet. Zahlreiche Signale ermöglichen die Komm-
unikation mit der Benutzungsoberfläche. Die Statusabfrage und die Bedienung 
der Oberfläche sowie die Fernsteuerung des Roboters von extern sind möglich.
'''

'Module importieren'
from PyQt4.QtCore import QObject, Signal
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
      
'Klasse Server'
class Server(QObject):
    
    #Beenden des Threads
    finished = Signal()
    
    #Name der anfragenden App
    server_anfrage = Signal(str)
    #Name der App und gesendete Informationen
    server_daten = Signal(str, str)
    
    #Fernsteuerung des Roboters aktivieren
    fernsteuerung_ein = Signal()
    #Steuersignale
    fernsteuerung = Signal(int, int, int, int, int, int)
    #Fernsteuerung des Roboters deaktivieren
    fernsteuerung_aus = Signal()
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QObject'

        super(Server, self).__init__(parent)

    'Methode server_starten'
    def server_starten(self):
    
        'Verbindungssocket instanziieren'
        #IPv4-Protokoll und TCP
        self.verb = socket(AF_INET, SOCK_STREAM)
        self.verb.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    
        'Verbindungssocket an eine IP-Adresse und einen Port binden'
        #lokale IP-Adresse und Port 60111
        self.verb.bind(('localhost', 60111))
        print(self.verb)
    
        'Verbindungssocket auf Anfragen horchen lassen'
        #maximale Anzahl: 5
        self.verb.listen(5)
        
        'Information ausgeben'
        print('Server läuft und hört zu...')
        
        try:
            while True:
                '''Verbindungsanfrage akzeptieren. Es werden der 
                Kommunikationssocket und das Adressobjekt des
                Verbindungspartners zurückgegeben.'''
                self.komm, addr = self.verb.accept()
    
                while True:
                    'Daten vom Client empfangen'
                    #Datentyp von data: bytes
                    data = self.komm.recv(1024)
    
                    '''Wenn keine Daten ankommen, wird der
                    Kommunikationssocket geschlossen. '''
                    if not data:
                        self.komm.close()
                        break
    
                    'Nachricht vom Client'
                    #Daten in str konvertieren 
                    data = data.decode()
                    
                    '''Nachricht: Sender & codierte Nachricht'''
                    data = data.split('&')                  
                    sender = data[1]
                    nachricht_kompl = data[2]
                    nachricht = nachricht_kompl.split(' ')
                                        
                    if nachricht[0] == '20':
                        
                        'Namen der anfragenden App an GUI senden'
                        self.server_anfrage.emit(sender)
                        'Appnamen und gesendete Informationen an GUI senden'
                        self.server_daten.emit(sender, nachricht_kompl)

                    elif (nachricht[0] == '18' and 
                    sender == self.verbindungspartner):
                        
                        'Informationen an GUI senden'
                        self.server_daten.emit(sender, nachricht_kompl)
                        
                        'Fernsteuerung aktivieren/deaktivieren - Fernsteuerung'
                        #Fernsteuerung aktivieren
                        if nachricht[1] == '01':
                            
                            'Signal fernsteuerung_ein an GUI senden'
                            self.fernsteuerung_ein.emit()
                        
                        #Roboter fernsteuern
                        elif nachricht[1] == '02':
                            
                            p1 = int(nachricht[2])
                            p2 = int(nachricht[3])
                            p3 = int(nachricht[4])
                            Spd_ver = int(nachricht[5])
                            p5 = int(nachricht[6])
                            p6 = int(nachricht[7])
                            
                            'Steuerinformationen an GUI senden'
                            self.fernsteuerung.emit(p1, p2, p3, \
                            Spd_ver, p5, p6)
                        
                        #Fernsteuerung deaktivieren
                        elif nachricht[1] == '03':
                            
                            'Signal fernsteuerung_aus an GUI senden'
                            self.fernsteuerung_aus.emit()
        
        finally:
            'Verbindungssocket schließen'
            self.verb.close()
    
            'Signal finished senden'
            self.finished.emit()
    
    '''Methode verbindung_anmelden - auf der GUI ausgwählten Verbindungspartner
    zur Kommunikation zulassen'''
    def verbindung_anmelden(self, partner):
        
        self.verbindungspartner = partner
        
    '''Methode verbindung_abmelden - Verbindungspartber abmelden'''
    def verbindung_abmelden(self, bool):
        
        if True: self.verbindungspartner = None