# Broker - Class for CONTROL of the AAS.
# Author: Sebastian Mack
# Author: Vladimir Kutscher
# Author: Syed Emad

"""
The module class is contain the basic functionality which is required by
every module within the AAS. The main purpose is thereby the establishing
of the ZeroMQ Communication, Receiving, Creating and Sending of the messages
"""

################################################################################
## Imports
################################################################################

import sys
import zmq
import logging
import json
from os import path, getcwd
from flask import Flask, render_template
#from jinja2 import Template, Environment, FileSystemLoader, select_autoescape

################################################################################
## Operations
################################################################################

class module():
    """A module - class  which determine the functionality of all modules
    derived from this class"""

    def __init__(self, mod_name, config):
        """Definition of the parameter of an module derived from this class.
        """
        self.context = zmq.Context()
        self.config = config

        ## Finding the relative path to module.log for every instantiated module
        ## at the moment the modueles are instantiated at three levels, for that
        ## reason three levels are checked
        self.curdir = getcwd()
        self.topdir = path.dirname(self.curdir)
        self.toptopdir = path.dirname(self.topdir)
        ## separating folder - name from folder-path
        self.curdir_name = path.basename(self.curdir)
        self.topdir_name = path.basename(self.topdir)
        self.toptopdir_name = path.basename(self.toptopdir)
        ## checking which one is the right level (='Verwaltungsschale')
        if self.curdir_name == 'Verwaltungsschale':
            self.log_path = path.join(self.curdir, 'FUNCTIONALITY', 'log', 'module.log')

        elif self.topdir_name == 'Verwaltungsschale':
            self.log_path = path.join(self.topdir, 'FUNCTIONALITY', 'log', 'module.log')

        elif self.toptopdir_name == 'Verwaltungsschale':
            self.log_path = path.join(self.toptopdir, 'FUNCTIONALITY', 'log', 'module.log')

        else:
            pass

        ## level = logging.INFO -> all logging will be saved in module.log
        ## level = logging.DEBUG -> each run has an own logging
        logging.basicConfig(format='%(asctime)s %(message)s',
                            filename=self.log_path,
                            level=logging.DEBUG)


        self.name = mod_name
        ## identity of the module. Mostly same as module name in uppercase
        self.identity = self.config[mod_name]['identity']
        ## URL:Port of the module, which is defined in  congiguration.py
        self.url = self.config[mod_name]['url']
        ## generating of an socket with the help of the DEALER: a special kind
        ## of an socket in zeroMQ
        self.socket = self.context.socket(zmq.DEALER)
        ## connecting the socket with a timeout. This timeout works just for the
        ## first time after establishing a socket and can be used, e.g. to close
        ## sockets, which dont recieve messages
        self.establish_connection()


        # app = Flask(__name__)
        # ## WorkingDirectory = CurrentDirectory, which is the level of
        # ## module_start.py
        # self.TEMPLATES_DIR =  path.join(self.curdir, 'FUNCTIONALITY')
        # ## JINJA2 - SETTING AN ENVIRONMENT - JINJA2 SUPPORT MULTIPLE PATHS
        # self.env = Environment(
        # loader = FileSystemLoader(self.TEMPLATES_DIR),
        # # autoescape = select_autoescape(['html', 'xml'])
        # )

    def establish_connection(self):
        ## setting a timeout for the socket.
        self.socket.connect(self.url)
        ## every socket gets an poller, which can check for incoming messages
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.sysout('established connection')

    def send(self, MESSAGE):
        """Seinding of any kind of messages
        """
        self.socket.send_multipart(MESSAGE)
        self.sysout('send message', MESSAGE)

    def poll(self, timeout):
        """Polling for messages is "checking" for messages. The poller accepts
        an timeout. If no timeout is set, it will wait infinitely. If a message
        is available, it can be received.
        """
        self.msg = dict(self.poller.poll(timeout))
        if len(self.msg) > 0:
            self.msg = 0
            ## if there is something to receive
            MESSAGE = self.socket.recv_multipart()
            self.sysout('receive message (with poller)', MESSAGE)
            return MESSAGE
        else:
            """If there is no response within the timeout-time, a
            timeout-message is returned and the connection is renewed (otherwise
            the timeout is not working anymore).
            """
            self.sysout('No response within the timeout-time of: '+str(timeout)+' milliseconds')

            ## the socket has to be renewed, because the timeout seems to work
            ## just for the first time after connecting a socket
            self.socket.close()
            self.socket = self.context.socket(zmq.DEALER)
            self.establish_connection()

            ## generate a 'timeout' - MESSAGE
            CORE = json.dumps({'response':'response-timeout in: '+self.name,
                                'request': 'request-timeout in: '+self.name,
                                'json_data': {'response': "response-timeout"}})
            CORE_bytes = [CORE.encode('ascii')]
            MESSAGE = ['TO']+['FROM']+CORE_bytes

            return MESSAGE

    def receive(self):
        """Receiving messages. This function ist not checking (polling) if there
        is actually something to recieve but blocks until something is received.
        """
        MESSAGE = self.socket.recv_multipart()
        self.sysout('receive message', MESSAGE)
        return MESSAGE

    def create_message(self, TO = 'X', CORE = "no input"):
        """Function for creating of an message with the receiver X (TO)
        """

        if type(TO) is str:
            """In case of an single receiver
            """
            ## the sender (FROM) takes his own identity out of the config
            FROM = [self.identity]
            ## generating a string out of an object.
            CORE_json = json.dumps(CORE)
            ## encoding of the string with ascii
            CORE_bytes = [CORE_json.encode('ascii')]
            ## the adress is empty in case of single receiver
            ADDRESS = []
            TO = [self.config[TO]['identity']]

        elif type(TO) is list:
            """In case of multiple receiver
            """
            MESSAGE_received = TO
            FROM = [self.identity]
            CORE_json = json.dumps(CORE)
            CORE_bytes = [CORE_json.encode('ascii')]
            MESSAGE_received.pop()
            TO = [MESSAGE_received.pop()]
            MESSAGE_received.pop()
            ADDRESS = MESSAGE_received

        MESSAGE = ADDRESS + TO + FROM + CORE_bytes
        return MESSAGE

    def extract_core(self, MESSAGE):
        """A function for extracting the CORE out of the MESSAGE.
        """
        CORE = MESSAGE[-1]
        CORE_json = CORE.decode('ascii')
        CORE_pyobj = json.loads(CORE_json)
        return CORE_pyobj

    def sysout(self, action, meta=False):
        """Meta is limited to 200 chars at the moment - see string truncating
        [0:200] - part.
        """

        if len(str(meta)) > 200:
            ## Truncating works only if the length of the string (boolean False
            ## included) exceeds 200
            sys.stdout.write('\n'+'<> {}   #'.format(self.name)+str(action)+'\n'+'['+str(self.socket)+']'+'\n'+'{}'.format(str(meta)[0:200]+' ...'+'\n' if meta else '')+'</>'+'\n')
        else:
            sys.stdout.write('\n'+'<> {}   #'.format(self.name)+str(action)+'\n'+'['+str(self.socket)+']'+'\n'+'{}'.format(str(meta)+'\n' if meta else '')+'</>'+'\n')

        sys.stdout.flush()

        if len(str(meta)) > 200:
            logging.info('\n<> {}   #{}\n   [{}]\n   {}\n</>'.format(self.name, str(action), str(self.socket),     str(meta)[0:200]+' ...' if meta else ''))
        else:
            logging.info('\n<> {}   #{}\n   [{}]\n   {}\n</>'.format(self.name, str(action), str(self.socket),     str(meta) if meta else ''))

    def destroy(self):
        """Closing of the connection
        """
        ## the has to be closed first
        self.socket.close()
        self.context.destroy()

    # def create_template(self, html_to_render, variables):
    #     """ A function for rendering the template which has to be
    #     sended from the Module to HTTPIN via the ZeroMQ-Socket
    #     """
    #     ## loading of a template
    #     self.template = self.env.get_template(html_to_render)
    #     ## rendering of the template
    #     print('VARIABLES: '+str(variables))
    #     self.rendered_template = self.template.render(variables=variables)
    #     return self.rendered_template
