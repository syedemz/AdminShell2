"""
Moduledescription: This Module is a substitution for the robotcontrol. Useful
in the case that the robotcontrol respectively the raspberry
of the robotarm is not connected. The output of this module is just the
input of the imaginary robotcontrol interface.
ATTENTION: This module is started like other modules from the module_start.py
but it doesn't derive from module. The consequence is that it doesn't appear
in the terminal like the other modules.
"""

from socket import AF_INET, SOCK_STREAM, socket, SOL_SOCKET, SO_REUSEADDR
import os
import sys
import struct

## relative path definition
curdir = os.path.abspath(os.path.dirname(__file__))
topdir = os.path.abspath(os.path.join(curdir, os.pardir))
if topdir not in sys.path:
	sys.path.insert(0, topdir)

from configuration import config
from module import module

def recv_msg(sock):
    # Read message length and unpack it into an integer
    raw_msglen = recvall(sock, 4)
    if not raw_msglen:
        return None
    msglen = struct.unpack('>I', raw_msglen)[0]
    # Read the message data
    return recvall(sock, msglen)

def recvall(sock, n):
    # Helper function to recv n bytes or return None if EOF is hit
    data = b''
    while len(data) < n:
        packet = sock.recv(n - len(data))
        if not packet:
            return None
        data += packet
    return data

def main():
    """Creating a socket s and bindging it to an port.
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind(('127.0.0.1', 60111))
    s.listen(10)
    print("Listening on socket:"+str(s))

    while True:
        ''' Accept incoming messages and print the content.
        '''
        komm, addr = s.accept()
        #print('Connected to: ' + addr[0] + ':' + str(addr[1]))
        'Daten vom Client empfangen'
        data = recv_msg(komm)
        data_split = data.split(b'&')
        MESSAGE = data_split
        antwort = str(data_split[2])
        print("ROBOTARM_DUMMY received data: "+antwort)

if __name__ == '__main__':
    main()
