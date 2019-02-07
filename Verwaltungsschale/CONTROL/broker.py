# Broker - Class for CONTROL of the AAS.
# Author: Vladimir Kutscher
# Author: Syed Emad

"""
The broker is the class for the CONTROL function of the Asset Administration
Shell. The main function of the broker is to forward incoming messages to the
proper receiver.
"""

################################################################################
## Imports
################################################################################
import sys
import zmq
import logging
import json
from os import path, pardir

################################################################################
## Operations
################################################################################
class broker():

    def __init__(self, config):

        ## Initialising of a ZeroMQ-Socket
        self.context = zmq.Context()
        self.config = config
        curdir = path.abspath(path.dirname(__file__))
        filename = path.abspath(path.join(curdir, pardir, 'FUNCTIONALITY',
                                'log', 'control.log'))
        logging.basicConfig(format='%(asctime)s %(message)s', filename=filename,
                                level=logging.INFO)

        #Start of HTTPIN
        self.url_HTTPIN = self.config['HTTPIN']['url']
        self.socket_HTTPIN = self.context.socket(zmq.ROUTER)
        self.config['HTTPIN']['socket'] = self.socket_HTTPIN
        self.socket_HTTPIN.bind(self.url_HTTPIN)

        #Start of all Sockets
        for module in self.config:
            if module != 'HTTPIN':
                exec('self.url_' + module + '=' + 'self.config[module][\'url\']')
                exec('self.socket_' + module + '=' + 'self.context.socket(zmq.DEALER)')
                exec('self.config[module][\'socket\']' + '=' + 'self.socket_' + module)
                exec('self.socket_' + module + '.bind' + '(self.url_' + module + ')' )

        self.poller = zmq.Poller()
        for module in self.config:
            exec('self.poller.register(self.socket_' + module + ', zmq.POLLIN)')
            self.sysout('established socket', meta=self.config[module])

    def mediate(self):
        loop = 0
        while True:
            try:
                items = dict(self.poller.poll())

            except KeyboardInterrupt:
                break

            for module in self.config:

                if items.get(self.config[module]['socket']) == zmq.POLLIN:

                    MESSAGE = self.config[module]['socket'].recv_multipart()
                    self.sysout('received message',
                                current_socket=self.config[module]['socket'],
                                meta = MESSAGE)

                    TO = MESSAGE[-3]

            if TO == b'restart':
                print("In the restart-loop of the Broker")

                CORE = self.extract_core(MESSAGE)

                if CORE['Anweisung'] == 'NEU':
                    DATA = CORE['DATA']

                    for new in DATA:
                        DATA[new]['identity'] = DATA[new]['identity'].encode('ascii')

                    #Write the new Data in the broker-configuration
                    self.config = {**self.config, **DATA}

                    new_module = next (iter (DATA.keys()))

                    """The next part opens a new socket in the broker if a
                    new app is installed"""

                    exec('self.url_' + new_module + '=' + 'self.config[new_module][\'url\']')
                    exec('self.socket_' + new_module + '=' + 'self.context.socket(zmq.DEALER)')
                    exec('self.config[new_module][\'socket\']' + '=' + 'self.socket_' + new_module)
                    exec('self.socket_' + new_module + '.bind' + '(self.url_' + new_module + ')' )
                    exec('self.poller.register(self.socket_' + new_module + ', zmq.POLLIN)')
                    self.sysout('established socket', meta=self.config[new_module])

                if CORE['Anweisung'] == "LÖSCHE":

                    DATA = CORE['DATA']
                    try:
                        exec('self.socket_' + DATA['module'] + '.close()')
                        exec('self.poller.unregister(self.socket_' + DATA['module'] + ')')
                        self.sysout('closed socket', meta=self.config[DATA['module']])

                        del self.config[DATA['module']]
                    except AttributeError:
                        self.sysout('ERROR',  meta = 'Deinstallation momentan nicht möglich bitte neustarten!')
                        continue

            for module in self.config:
                if TO == self.config[module]['identity']:
                    print('CONTROL: Preparing to send the message to: '+str(module))
                    self.config[module]['socket'].send_multipart(MESSAGE)
                    self.sysout('send message',
                                current_socket=self.config[module]['socket'],
                                meta = MESSAGE)

            loop += 1
            self.sysout('completed loop', meta= loop)

    def sysout(self, action, current_socket=False, meta=False):

        if len(str(meta)) > 200:
            ## Truncating works only if the length of the string (boolean False
            ## included) exceeds 200
            sys.stdout.write('<> CONTROL   #'+(str(action)+'{}'.format('\n'+'['+str(current_socket)+']' if current_socket else '')+'\n'+'{}'.format(str(meta)[0:200]+' ...'+'\n' if meta else '')+'</>'+'\n'))
        else:
            sys.stdout.write('<> CONTROL   #'+(str(action)+'{}'.format('\n'+'['+str(current_socket)+']' if current_socket else '')+'\n'+'{}'.format(str(meta)+'\n' if meta else '')+'</>'+'\n'))

        sys.stdout.flush()

        if len(str(meta)) > 200:
            logging.info('\n<> CONTROL   #{}\n   [{}]\n   {}\n</>'.format(str(action), str(current_socket) if current_socket else '', str(meta)[0:200]+' ...' if meta else ''))
        else:
            logging.info('\n<> CONTROL   #{}\n   [{}]\n   {}\n</>'.format(str(action), str(current_socket) if current_socket else '', str(meta) if meta else ''))

    def destroy(self):

        for module in self.config:
            exec('self.socket_' + module + '.close()')
            self.sysout('closed socket', meta=self.config[module])

        self.sysout('Control closed')

        self.context.destroy()

    def extract_core(self, MESSAGE):
        CORE = MESSAGE[-1]
        CORE_json = CORE.decode('ascii')
        CORE_pyobj = json.loads(CORE_json)
        return CORE_pyobj
