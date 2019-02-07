import sys
import zmq
import logging



class broker(object):


    def __init__(self, config):

        self.context = zmq.Context()
        self.config = config
        logging.basicConfig(format='%(asctime)s %(message)s', filename='log/control.log', level=logging.INFO)


        self.url_HTTPIN = self.config['HTTPIN']['url']
        self.socket_HTTPIN = self.context.socket(zmq.ROUTER)
        self.config['HTTPIN']['socket'] = self.socket_HTTPIN
        self.socket_HTTPIN.bind(self.url_HTTPIN)


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
                    self.sysout('received message', current_socket=self.config[module]['socket'], meta = MESSAGE)

                    TO = MESSAGE[-3]

                    for module in self.config:
                        if TO == self.config[module]['identity']:

                            self.config[module]['socket'].send_multipart(MESSAGE)
                            self.sysout('send message', current_socket=self.config[module]['socket'], meta = MESSAGE)
            loop += 1
            self.sysout('completed loop', meta= loop)



    def sysout(self, action, current_socket=False, meta=False):

        sys.stdout.write('<> CONTROL   #'+(str(action)+'{}'.format('\n'+'['+str(current_socket)+']' if current_socket else '')+'\n'+'{}'.format(str(meta)+'\n' if meta else '')+'</>'+'\n'))

        sys.stdout.flush()


        logging.info('\n<> CONTROL   #{}\n   [{}]\n   {}\n</>'.format(str(action), str(current_socket) if current_socket else '', str(meta) if meta else ''))


    def destroy(self):

        for module in self.config:
            exec('self.socket_' + module + '.close()')

        self.context.destroy()
