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

'''

'Module importieren'
from numpy import save, hsplit, vsplit, vstack
from PyQt4.QtCore import QObject, Signal, QThread
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR

import os
import sys
import struct
from time import sleep
from schnittstelle.server_empfaenger import Server_empfaenger


'Klasse Server'
class Server(QObject):
    
    'Signale definieren'
    #Animation aktualisieren
    animation_akt = Signal(float, float, float, float, float, float, \
    float, float, float, float, float, float, float)

    #Beenden des Threads
    finished = Signal()
    
    #Roboter fernsteuern
    roboter_fern = Signal()
    roboter_fern_vektor = Signal(int, int, int, int, int, int)
    roboter_fern_aus = Signal()

    roboter_fern_abs = Signal()
    roboter_fern_abs_vektor = Signal(int, int, int, int, int, int)
    roboter_fern_abs_aus = Signal()
    
    roboter_fern_anfrage = Signal(str)
 
    roboter_zustandsanfrage = Signal(str)
    roboter_zustandsaussage = Signal(str, str)
    server_protokoll = Signal(str, str)
        
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QObject'

        super(Server, self).__init__(parent)
        
        global akz_app
        
        akz_app = ''
        
    'Methode server_starten'
    def server_starten(self):
        
        self.mode = 0
        self.g_code_modus = False
        
        self.message_lenght = 1024
        self.verb = socket(AF_INET, SOCK_STREAM)
        self.verb.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        try:
            self.verb.bind(('127.0.0.1', 60112))
            print("Osterhase"+str(self.verb))
        except Exception as e:
            print(e)  
                
        self.thread_server_emp = QThread()
        'Server-Objekt instanziieren'
        self.server_emp = Server_empfaenger()
        'Server-Objekt an den Thread übergeben'
        self.server_emp.moveToThread(self.thread_server_emp)
        'Signale und Slots verbinden'
        self.thread_server_emp.started.connect(self.server_emp.server_starten)
        self.server_emp.nachricht_empfangen.connect(self.nachricht_empfangen)
        print("server_emp.nachricht_empfangen connected")
        self.thread_server_emp.finished.connect(self.thread_server_emp.deleteLater)
        'Methode start des Thread-Objektes aufrufen'
        self.thread_server_emp.start()
        'Methode exec des Thread-Objektes aufrufen'
        self.thread_server_emp.exec()
            
    def nachricht_empfangen(self, sender, nachricht_kompl, MESSAGE):
                
        self.sender = sender

        'Nachricht vom Client'
#        nachricht_kompl = data.decode()

        '''Die Nachricht entsprechend der Leerzeichen
        in Teile zerlegen.'''

        nachricht = nachricht_kompl.split(' ')
        print(nachricht)

        '''Im Weiteren wird die Nachricht des Client dem
        entsprechenden Fall zugeordnet, das Signal gesendet,
        die Antwort erstellt und dem Client übermittelt.
        Beispiele zeigen den jeweiligen Aufruf.'''
        
        if nachricht[0] == '18' and self.sender == self.akz_app:
            
            self.server_protokoll.emit(self.sender, nachricht_kompl)
            
            if nachricht[1] == '01':
                print("In der 18 01 drin")
                
                'Signal roboter_fern senden'
                self.roboter_fern_abs.emit()
                    
                'Antwort erstellen und an den Client senden'
                antwort = 'Remote control enabled'

                self.send_msg(self.verb, MESSAGE)

                self.message_lenght = 29
                
            elif nachricht[1] == '02':
                print("In der 18 02 drin")
                
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
                print("Nachticht an roboter_fern_abs_vektor: "+str(p1))

            elif nachricht[1] == '03':
                
                'Signal roboter_fern senden'
                self.roboter_fern_abs_aus.emit()
                    
                'Antwort erstellen und an den Client senden'
                antwort = 'Remote control disabled'

                self.send_msg(self.verb, MESSAGE)
       
                self.message_lenght = 29

        elif nachricht[0] == '20':
            
            self.server_protokoll.emit(self.sender, nachricht_kompl)
            self.roboter_fern_anfrage.emit(self.sender)
        
    def verbindung_anmelden(self, zul_app):
               
        self.akz_app = zul_app
        print("Akz_App im Server:"+str(self.akz_app))
        
    def zustandsaussage(self, antwort_gui, a_sender):
        pass
##        if akz_app != ' ':
##            antwort = akz_app + " " + antwort_gui
##        elif akz_app == ' ':
##            antwort = 'XX ' + antwort_gui

##        self.send_msg(self.verb, MESSAGE)
        
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