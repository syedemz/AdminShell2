# -*- coding: utf-8 -*-
"""
Created on Wed May 24 18:37:44 2017

@author: Thomas
"""

'Module importieren'
from PyQt4.QtCore import QObject, pyqtSignal
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
class Server_sender(QObject):
    
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QObject'

        super(Server_sender, self).__init__(parent)
        self.identitaet = [configuration.config['ROBO_GUI']['identity']]
        
    def starten(self):
        self.server_starten()

    'Methode server_starten'
    def server_starten(self):
        self.message_lenght = 1024
        self.server_con = module.module('ROBO_GUI_SHADOW', configuration.config)
        'Verbindungs Socket aktivieren'
        try:
            self.verb = socket(AF_INET, SOCK_STREAM) 
            self.verb.bind(('localhost', 60112)) 
            self.verb.listen(5)
        except OSError:
            print('Already running, terminating')
            exit()
            
        
        'Information ausgeben'
        print('Ausgangsserver läuft und hört zu...')
                
        
        while True:    
            try:    
                
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
#                print(data)
                data_split = data.split(b'&')
                MESSAGE = data_split
                antwort = str(data_split[2])
                
                
    
                
                self.nachricht_kompl_e = MESSAGE[2].decode('ascii')
                
                MESSAGE = self.create_traitor(CORE_pyobj = antwort, MESSAGE_received = MESSAGE)
                self.server_con.send(MESSAGE)
                
                if not data:
                    self.komm.close()        
                
            except ConnectionRefusedError:
                print("Keine Robotersteuerung aktiv")                
            except ConnectionAbortedError:
                print('Connection aborted.')
            except ConnectionResetError:
                print('Connection to GUI lost')
                
    def create_traitor(self, TO = b'someone', CORE_pyobj = "no input", MESSAGE_received = False):

        ADDRESS = []
        TO = [TO]
        FROM = self.identitaet
        CORE_json = json.dumps(CORE_pyobj)
        CORE = [CORE_json.encode('ascii')]

        if MESSAGE_received:

            MESSAGE_received.pop()
            MESSAGE_received.pop()
            TO = [MESSAGE_received.pop()]
        
#        print('Adresse ', ADDRESS)
#        print('TO ',TO)
#        print('FROM ', FROM)
#        print('CORE ', CORE)
        MESSAGE = ADDRESS + TO + FROM + CORE
        return MESSAGE        
                
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