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

sys.path.append(os.path.abspath('../../../'))

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
        self.socket = False
        self.message_lenght = 1024
        server_con = module.module('ROBOTER_GUI', configuration.config)
        if self.socket == True:

            'Verbindungssocket instanziieren'
            #IPv4-Protokoll und TCP
            self.verb = socket(AF_INET, SOCK_STREAM)

            'Verbindungssocket an eine IP-Adresse und einen Port binden'
            #lokale IP-Adresse und Port 60000
            self.verb.bind(('localhost', 60100))

            'Verbindungssocket auf Anfragen horchen lassen'
            #maximale Anzahl: 5
            self.verb.listen(5)

        'Information ausgeben'
        print('Server läuft und hört zu...')


        while True:

            '''Verbindungsanfrage akzeptieren. Es werden der
            Kommunikationssocket und das Adressobjekt des
            Verbindungspartners zurückgegeben.'''
            if self.socket == True:
                self.komm, addr = self.verb.accept()




#                request = CORE_pyobj["request"]
#                response = data[request].to_dict()
#                for key in response:
#                    response = str(response)

            'Daten vom Client empfangen'
            #Datentyp von data: bytes
            if self.socket == True:
                data = self.komm.recv(self.message_lenght)

            MESSAGE = server_con.receive()
#            print(MESSAGE)

            CORE_pyobj = server_con.extract_core(MESSAGE)

            sender_cod = MESSAGE[1]

            self.sender_e = str(sender_cod.decode('ascii'))

            if self.socket == True:
                self.sender_e = "Socket-Server"
                '''Wenn keine Daten ankommen, wird der
                Kommunikationssocket geschlossen.'''
                if not data:
                    self.komm.close()
                    break

            'Nachricht vom Client'

            self.nachricht_kompl_e = CORE_pyobj

            self.nachricht_empfangen.emit(self.sender_e, self.nachricht_kompl_e, MESSAGE)
