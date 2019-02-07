# -*- coding: utf-8 -*-
"""
Based on the Code of Thomas Dasbach (03.04.2017) and modified heavily by
Vladimir Kutscher (23.07.2017).Expanded by robterparameters to be able to
calibrate by Christian Plesker.

Moduledescription: This Module is a part of the interface (api_robotarm)
between the AS and the robotcontrol (Robotersteuerung) and serves as the
receiver of the messages from the AS. The received messages (zmq-socket)
get restructured and streamed (SOCK_STREAM) to the robotcontrol over an
standard socket (AF_INET)
For the communication from the robotcontrol to the shell has to be or is
in a separate module.

Changes:
- Qt Threads deleted
- not used code deleted
-
"""
from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
import os
import sys
import struct
from time import sleep

## relative path definition
curdir = os.path.abspath(os.path.dirname(__file__))
topdir = os.path.abspath(os.path.join(curdir, os.pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)

from configuration import config
from module import module

class ShellToRobotarmInterface():
    """The purpose of this class is to establish a connection between
    the shell and the robotarm.
    """

    def __init__(self):
        """ Class - Initialisation. Establishing an zmq-socket.
        """

        self.zmq_s = module('API_ROBOTARM', config)
        print('api_robotarm zmq-socket is running and awaits messages ... ')

    def connect_socket(self):
        """Connects to a Socket (AF_INET), which is established by the
        robotcontrol interface (or the robotarm_dummy).
        """
        self.s = socket(AF_INET, SOCK_STREAM)
        ## connecting to local port 60111
        self.s.connect(('127.0.0.1', 60111))
        return self.s

    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        self.msg = struct.pack('>I', len(msg)) + msg
        self.s.sendall(self.msg)

    def forward(self):
        """ Module start method
        """
        try:
            """ Waiting on the ZeroMQ - Socket for incoming messages,
            rebuild them in a way the robotcontrol can understand and
            sending the messages to the robotcontrol (Port: 60111)
            """
            MESSAGE_list = self.zmq_s.receive()

            #Extract the core of the message
            orders = self.zmq_s.extract_core(MESSAGE_list)

            #Split the core of the message in every order of every motor
            orders = orders.split()

            #Loading parameter which calibrate the robot
            from api_robotarm.Roboterparameter import Parameter

            #Start variable set
            i = 2
            m = 1

            #Loop to modifie the orders of every motor with the calibration parameters
            while i < 8:

                #extracting the offset and gradient of every motor
                motor = Parameter["Motor_" + str(m)]
                offset = motor["Offset"]
                gradient = motor["gradient"]

                #Saving the new order
                orders[i] = int(offset) + int(orders[i])*int(gradient)

                if orders[i] < 0:
                    orders[i] = 0
                elif orders[i] > 180:
                    orders[i] = 180

                orders[i] = str("%0.3u"% (orders[i]))
                i = i+1
                m = m+1

            #restructuring the order and create a new messagelist
            inhalt = orders[0] +" "+ orders[1] +" "+  orders[2] +" "+  orders[3] +" "+  orders[4] +" "+  orders[5] +" "+  orders[6] + ' ' + orders[7]
            MESSAGE_list = self.zmq_s.create_message(TO = "API_ROBOTARM",CORE = inhalt)

            ## restructuring of the message
            MESSAGE_str = MESSAGE_list[0] + str('&').encode('ascii') + MESSAGE_list[1] + str('&').encode('ascii') + MESSAGE_list[2][1:-1]
            ## building an standard socket
            self.s = self.connect_socket()
            ## sending the message
            self.send_msg(self.s, MESSAGE_str)
            ## closing the socket
            self.s.close()

        except ConnectionRefusedError:
            print("Connection refused. No robotcontrol-receiver on port 60111?")
        except ConnectionAbortedError:
            print('Connection aborted.')
        except ConnectionResetError:
            print('Connection to GUI lost')
        except OSError:
            print("OSERROR Type 2.")
            self.verb = socket(AF_INET, SOCK_STREAM)
            self.verb.connect(('127.0.0.1', 60111))
        except KeyboardInterrupt:
            try:
                """If an KeyboardInterrupt comes, the socket will be closed
                """
                self.verb.close()
                print("The socket (60111) and the api_robotarm will be closed...")
            except:
                print("api_robotarm will be closed...")

def main():
	""" Instantiating a zqm - socket to the shell on the one hand and
	establishing a connection to the robotcontrol (AF_INET - socket) and
	forwarding all messages coming from zmq to robotcontrol in a loop
	"""
	## instantiating the class
	receiver = ShellToRobotarmInterface()

	while True:
		""" Forwarding the messages in a loop.
		"""
		receiver.forward()

if __name__ == '__main__':
    main()
