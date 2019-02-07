'''
Autor: Thomas Dasbach
Datum: 03.04.2017

Modulbeschreibung: Dieses Modul dient als Empfänger für die GUI für Nachrichten
aus der Schale. Es wird als QThread von "server.py" gestartet und läuft permanent
im Hintergrund.

'''

'Module importieren'
from PyQt4.QtCore import QObject, Signal
from socket import AF_INET, SOCK_STREAM, socket
import os
import sys
import struct

sys.path.append(os.path.abspath('../../'))

import json
from structure import module
from structure import configuration

#from pprint import pprint


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
        
        'Verbindungssocket an eine IP-Adresse und einen Port binden'
        #lokale IP-Adresse und Port 60000
        self.verb.bind(('localhost', 60111))
        print("schnittstelle empfaenger"  + str(self.verb))
        'Verbindungssocket auf Anfragen horchen lassen'
        #maximale Anzahl: 5
        self.verb.listen(5)
        
        'Information ausgeben'
        print('Server läuft und hört zu...')
                
        
        while True:    
                
            '''Verbindungsanfrage akzeptieren. Es werden der 
            Kommunikationssocket und das Adressobjekt des
            Verbindungspartners zurückgegeben.'''
            self.komm, addr = self.verb.accept()

#                request = CORE_pyobj["request"]
#                response = data[request].to_dict()
#                for key in response:
#                    response = str(response)
                
            'Daten vom Client empfangen'
            #Datentyp von data: bytes
            data = self.recv_msg(self.komm)
            print('gesendete Daten' + str(data))
            MESSAGE = data.split(b'&')
            

#            MESSAGE[0] = MESSAGE[0] + "'"
#            MESSAGE[1] = "b'" + MESSAGE[1] + "'"
#            MESSAGE[2] = MESSAGE[2][:-1]
#            print(MESSAGE[0])            
#            print(MESSAGE[1])
#            print(MESSAGE[2])
#            print(type(MESSAGE[0]))           
#            print(type(MESSAGE[1]))
#            print(type(MESSAGE[2]))
            
            
            sender_cod = MESSAGE[1]
            
            self.sender_e = str(sender_cod.decode('ascii'))

            
            self.nachricht_kompl_e = MESSAGE[2].decode('ascii')
            
            self.nachricht_empfangen.emit(self.sender_e, self.nachricht_kompl_e, MESSAGE)
            
            if not data:
                self.komm.close()           
            
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
            
