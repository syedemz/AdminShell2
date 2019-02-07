# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:37:04 2017

@author: Thomas
"""

'''
Autor: Thomas Dasbach
Datum: 03.04.2017

Modulbeschreibung: Dieses Modul dient als Empfänger für die GUI für Nachrichten
aus der Schale. Es wird als QThread von "server.py" gestartet und läuft permanent
im Hintergrund.

'''

'Module importieren'
from PyQt4.QtCore import QObject, pyqtSignal
from socket import AF_INET, SOCK_STREAM, socket
import os
import sys
import struct
from time import sleep

sys.path.append(os.path.abspath('../../'))

import json
from structure import module
from structure import configuration

#from pprint import pprint


'Klasse Server'
class Server_empfaenger(QObject):
    
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QObject'

        super(Server_empfaenger, self).__init__(parent)
        
    def starten(self):        
        self.server_starten()

    'Methode server_starten'
    def server_starten(self):
        
        self.message_lenght = 1024
        server_con = module.module('ROBO_GUI', configuration.config)

        'Verbindungssocket instanziieren'
        #IPv4-Protokoll und TCP
#        self.verb = socket(AF_INET, SOCK_STREAM)
#        verbinde = True
#        while verbinde == True:
#            try:                
#                self.verb.connect(('localhost', 60111))
#                verbinde = False
#            except ConnectionRefusedError:
#                sleep(1/10)
#            except OSError:
#                print("OSERROR")
        
        'Verbindungssocket an eine IP-Adresse und einen Port binden'
        #lokale IP-Adresse und Port 60000
        
            
        
        'Information ausgeben'
        print('Eingangsserver läuft und hört zu...')
                
        
        while True:    
            try:    
                '''Verbindungsanfrage akzeptieren. Es werden der 
                Kommunikationssocket und das Adressobjekt des
                Verbindungspartners zurückgegeben.'''
    
    #                request = CORE_pyobj["request"]
    #                response = data[request].to_dict()
    #                for key in response:
    #                    response = str(response)
                    
                'Daten vom Client empfangen'
                #Datentyp von data: bytes
                
                MESSAGE_list = server_con.receive()
    #            print(MESSAGE)            
#                print(type(MESSAGE_list[0]))
#                print(type(MESSAGE_list[1]))
#                print(type(MESSAGE_list[2]))
                MESSAGE_str = MESSAGE_list[0] + str('&').encode('ascii') + MESSAGE_list[1] + str('&').encode('ascii') + MESSAGE_list[2][1:-1]
#                print("Inhalt der Nachricht: ", MESSAGE_str)
                self.verb = socket(AF_INET, SOCK_STREAM)                
                self.verb.connect(('localhost', 60111))
                self.send_msg(self.verb, MESSAGE_str)
                print("Nachricht weitergeleitet: ", MESSAGE_str)
                self.verb.close()
                
            except ConnectionRefusedError:
                print("Keine Robotersteuerung aktiv")                
            except ConnectionAbortedError:
                print('Connection aborted.')
            except ConnectionResetError:
                print('Connection to GUI lost')
            except OSError:
                print("OSERROR Type 2")
                self.verb = socket(AF_INET, SOCK_STREAM)
                self.verb.connect(('localhost', 60111))
                
                
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
        data = b''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data