###############
""" IMPORTE """
###############

import sys
import zmq
import logging
import json

##################################
"""DEFINITION ZMQ KOMMUNIKATION"""
##################################

class module(object):                   # eine Modul-Klasse, welche die Funktionalitaet aller Module (Database etc.) festlegt


    def __init__(self, mod_name, config): # Definition der Faehigkeiten und Parameter eines Moduls

        self.context = zmq.Context()    # erfolgt immer als erstes und in der Welt von ZeroMQ bedeutet es die Erstellung eines "Kontainers" für alle Sockets . Es wird ein Kontext pro Session erstellt.
        self.config = config
        logging.basicConfig(format='%(asctime)s %(message)s', filename='log/module.log', level=logging.INFO) # mitloggen der Geschehnisse


        self.name = mod_name            # Name des Moduls
        self.identity = self.config[mod_name]['identity'] # dem Modul wird zusaetzlich zum Namen noch einne Identitaet zugeordnet, welche meist das gleiche in Kleinbuchstaben ist
        self.url = self.config[mod_name]['url'] # die URL:Port zum Mudul, welche in der congiguration.py zu finden ist
        self.socket = self.context.socket(zmq.DEALER) # generierung eines Sockets mithilfe des DEALERs, einer speziellen Form eines Sockets von ZeroMQ  - über diesen Socket findet die Kommunikation statt
        self.establish_connection()     # an den erstellten Socket wird eine Verbindung unter der uebergebenen url angebunden


        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)


    def establish_connection(self):

        self.socket.connect(self.url)
        self.sysout('established connection')


    def send(self, MESSAGE): # Definition des Versenden einer beliebigen MESSAGE

        self.socket.send_multipart(MESSAGE)     # Versenden der Nachricht ueber den Socket
        self.sysout('send message', MESSAGE)    # die Ausgabe der Nachricht zur Info


    def receive(self):

        MESSAGE = self.socket.recv_multipart()  # Empfangen der Nachricht
        self.sysout('receive message', MESSAGE)

        return MESSAGE                          # Rueckgabe der Nachricht


    def create_message(self, TO = 'X', CORE = "no input"):  # Funktion zur Erstellung einer Nachricht mit dem Empfaenger X und der Nachricht "no input"

        if type(TO) is str:                             # bei einem einzelnen Adressat
            FROM = [self.identity]                      # Versender ist die eigenen Identität (aus config)
            CORE_json = json.dumps(CORE)                # Funktion von json zur Generierung eines Strings aus einem Objekt (z.B. wird ein String aus einer einfachen Liste genenriert: json.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}]) ---> '["foo", {"bar": ["baz", null, 1.0, 2]}]')
            CORE_bytes = [CORE_json.encode('ascii')]    # ascii Kodierung des generierten Strings
            ADDRESS = []
            TO = [self.config[TO]['identity']]

        elif type(TO) is list:                          # bei mehreren Adressaten
            MESSAGE_received = TO
            FROM = [self.identity]
            CORE_json = json.dumps(CORE)
            CORE_bytes = [CORE_json.encode('ascii')]
            MESSAGE_received.pop()
            TO = [MESSAGE_received.pop()]
            MESSAGE_received.pop()
            ADDRESS = MESSAGE_received

        MESSAGE = ADDRESS + TO + FROM + CORE_bytes      # Generierung der Nachricht
        return MESSAGE                                  # Rueckgabe der generierten Nachricht


    def extract_core(self, MESSAGE):
        CORE = MESSAGE[-1]
        CORE_json = CORE.decode('ascii')
        CORE_pyobj = json.loads(CORE_json)
        return CORE_pyobj


    def sysout(self, action, meta=False):

        sys.stdout.write('\n'+'<> {}   #'.format(self.name)+str(action)+'\n'+'['+str(self.socket)+']'+'\n'+'{}'.format(str(meta)+'\n' if meta else '')+'</>'+'\n')


        sys.stdout.flush()


        logging.info('\n<> {}   #{}\n   [{}]\n   {}\n</>'.format(self.name, str(action), str(self.socket),     str(meta) if meta else ''))


    def destroy(self):          # Beenden der Verbindung wenn sie nicht mehr gebraucht wird. Da Python dies automatisch erledingt, wird die Funktion eigentlich nicht gebraucht.
        self.socket.close()     # zuerst muss immer der Socket beednet werden, sonst wuerde destroy haengen
        self.context.destroy()
