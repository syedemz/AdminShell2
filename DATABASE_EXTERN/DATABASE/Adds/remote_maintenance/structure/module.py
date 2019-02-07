import sys
import zmq
import logging
import json



class module(object):


    def __init__(self, mod_name, config):

        self.context = zmq.Context()
        self.config = config
        logging.basicConfig(format='%(asctime)s %(message)s', filename='log/module.log', level=logging.INFO)


        self.name = mod_name
        self.identity = self.config[mod_name]['identity']
        self.url = self.config[mod_name]['url']
        self.socket = self.context.socket(zmq.DEALER)
        self.establish_connection()


        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)


    def establish_connection(self):

        self.socket.connect(self.url)
        self.sysout('established connection')


    def send(self, MESSAGE):

        self.socket.send_multipart(MESSAGE)
        self.sysout('send message', MESSAGE)


    def receive(self):

        MESSAGE = self.socket.recv_multipart()
        self.sysout('receive message', MESSAGE)

        return MESSAGE


    def create_message(self, TO = 'X', CORE = "no input"):

        if type(TO) is str:
            FROM = [self.identity]
            CORE_json = json.dumps(CORE)
            CORE_bytes = [CORE_json.encode('ascii')]
            ADDRESS = []
            TO = [self.config[TO]['identity']]

        elif type(TO) is list:
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
        CORE = MESSAGE[-1]
        CORE_json = CORE.decode('ascii')
        CORE_pyobj = json.loads(CORE_json)
        return CORE_pyobj


    def sysout(self, action, meta=False):

        sys.stdout.write('\n'+'<> {}   #'.format(self.name)+str(action)+'\n'+'['+str(self.socket)+']'+'\n'+'{}'.format(str(meta)+'\n' if meta else '')+'</>'+'\n')


        sys.stdout.flush()


        logging.info('\n<> {}   #{}\n   [{}]\n   {}\n</>'.format(self.name, str(action), str(self.socket),     str(meta) if meta else ''))


    def destroy(self):
        self.socket.close()
        self.context.destroy()
