'''
Autor: Thomas Dasbach
Datum: 03.04.2017

Modulbeschreibung: Dieses Modul dient als Empfänger für die GUI für Nachrichten
aus der Schale. Es wird als QThread von "server.py" gestartet und läuft permanent
im Hintergrund.

'''

'Module importieren'
from PyQt4.QtCore import QObject
from PyQt4.QtCore import Signal
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
import os
import sys
import struct

###sys.path.append(os.path.abspath('../../'))

import json
###from structure import module
###from structure import configuration


'Klasse Server'
class Server_empfaenger(QObject):
    
    'Signale definieren'

    #Nachricht empfangen und an Server weiterleiten
    nachricht_empfangen = Signal(str, str, list)
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QObject'

        super(Server_empfaenger, self).__init__(parent)

    'Methode server_starten'
    def server_starten(self): 

                
        'Verbindungssocket instanziieren'
        #IPv4-Protokoll und TCP
        self.verb = socket(AF_INET, SOCK_STREAM)
        self.verb.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        'Verbindungssocket an eine IP-Adresse und einen Port binden'
        self.verb.bind(('127.0.0.1', 60111))
        print("Weihnachsmann: "  + str(self.verb))
        'Verbindungssocket auf Anfragen horchen lassen'
        #maximale Anzahl: 5
        self.verb.listen(5)
        
        'Information ausgeben'
        print('Server Empfaenger (Robotcontrol interface) läuft und hört zu...')
   
        while True:    
                
            '''Verbindungsanfrage akzeptieren. Es werden der 
            Kommunikationssocket und das Adressobjekt des
            Verbindungspartners zurückgegeben.'''
            self.komm, addr = self.verb.accept()
                
            'Daten vom Client empfangen'
            # Datentyp von data: bytes
            data = self.recv_msg(self.komm)
            MESSAGE = data.split(b'&')

            # the sender of the message is aquiered from the message
            sender_cod = MESSAGE[1]
            self.sender_e = str(sender_cod.decode('ascii'))

            # the message is aquired
            self.nachricht_kompl_e = MESSAGE[2].decode('ascii')
            # the messag is sended with the help of an Signal to the Server
            self.nachricht_empfangen.emit(self.sender_e, self.nachricht_kompl_e, MESSAGE)
                    
            
    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        self.sock.sendall(msg)
    
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
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
            
