# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 12:55:54 2017

@author: Thomas
"""


import socket
from sys import exit

from time import sleep
#import os
#from numpy import around
from serial import Serial, SerialException


'''Socketserver zur GUI wird erstellt und wartet auf ankommende Verbindungen'''

ip = '127.0.0.1'
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
    s.bind((ip, 60110)) 
    s.listen(40)
except OSError:
    print('Already running, terminating')
    exit()

steve_msg = ''

com_ports = ['COM2','COM3','COM4','COM5','COM6']


''' Initialisierung'''
''' Festlegen welche Ports genutzt werden sollen. '''

arduino = True
stev = False

con_ard_enable = False

#
#operating_system = os.name
#
#if os.name == 'nt': laptop == True
#if os.name == '': raspberry == True

'''AKtivieren der gewählten Ports'''

if stev:
    steve = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    steve.bind(('localhost', 60120))
    steve.listen(5) 
    
print('----- Welcome to the Raspberry Distributor -----')
print()
print('Chosen Settings')
print('Connect to Arduino:\t', arduino)
print('Connect to Steve:\t', stev)
print()
print('Trying to activate all possible Connections:')

if arduino:
    com_ports_red = com_ports[:-1]
    for i, val in enumerate(com_ports_red):
        if not con_ard_enable:
            try:
                'Serial-Objekt instanziieren'
                device = Serial()
                'Port festlegen'
                device.port = com_ports[i]
                'Baudrate festlegen'
                device.baudrate = 115200
                'Timeout festlegen'
                device.timeout = 1
                
                device.open()
                
                con_ard_enable = True
                print('Connected to Arduino by', com_ports[i],'.')
            except SerialException:
                print('Connection to Arduino by ',com_ports[i],' not possible, trying ',com_ports[i+1],'.')
    
    if not con_ard_enable:
        try:
            i=i+1           
            'Serial-Objekt instanziieren'
            device = Serial()
            'Port festlegen'
            device.port = com_ports[i]
            'Baudrate festlegen'
            device.baudrate = 115200
            'Timeout festlegen'
            device.timeout = 1
            
            device.open()
            con_ard_enable = True
            print('Connected to Arduino by ', com_ports[i],'.')
            
        except SerialException:
            print('Connection to Arduino by ', com_ports[i],' not possible, trying ttyACM0.')
            
    if not con_ard_enable:
        try:
            'Serial-Objekt instanziieren'
            device = Serial()
            'Port festlegen'
            device.port = '/dev/ttyACM0'
            'Baudrate festlegen'
            device.baudrate = 115200
            'Timeout festlegen'
            device.timeout = 1
            
            device.open()
            con_ard_enable = True
            print('Connected to Arduino by ttyACM0')
            
        except SerialException:
            print('Connection to Arduino by ttyAMC0 not possible, conntact Support.')


print()  
print('--- Server Running ---')
print()

''' Main '''

#v_time = around(time.clock(), 5)
#a_time = around(time.clock(), 5)


''' Verbindung zu Steve herstellen '''
if stev:
    steve_com, steve_addr = steve.accept()
    print('Connection to Steve established')


while True:
        
    try: 
                
        while True:
            
            ''' Verbindungen von der GUI akzeptieren '''
            komm, addr = s.accept()
            print('Connection to GUI established')
            
            while True:
                '''Empfangen der Daten von der GUI'''
                data = komm.recv(56)
    
                if not data: 
                    komm.close()
                    break
                
#                a_time = around(time.clock(), 5)
#                   print(a_time - v_time , ' ' , data)#
#                v_time = around(a_time - v_time, 5)
                
                nachricht = data.decode('ascii')
                
                
                print('Nachricht: ', nachricht)
#                print(nachricht)
                
                '''Durchrouten an Steve'''
                '''Nachricht wird für Steve codiert'''
                if stev:
                    steve_msg_p = nachricht.split(' ')
                    for i in range (1,11):
                        steve_msg += steve_msg_p[i]
                        
                    steve_msg += '00'   
                    steve_com.send(steve_msg.encode('ascii'))
                    print('Steve: \t', steve_msg)
                    steve_msg = ''
                
                '''Nachricht wird über den Laptopport geroutet'''
                if arduino:
                                        
                    wiederversuch = True                   
                    while wiederversuch:
                        try:
                            device.write(nachricht.encode('ascii'))
                            print('Laptop: \t', nachricht)
        #                    print(nachricht[0])
        #                    print(nachricht[1])
        #                    print(nachricht[2])
                            '''Wenn die GUI Anfrage mit 30 beginnt, Antwort vom
                            Arduino abwarten und an die GUI leiten'''
                            if nachricht[0] == '1':
                                sleep(2)
                            if nachricht[0] == '3' and nachricht [1] == '0':
        #                        print('warte auf Antwort')
                                sleep(1/200)                                
                                antwort_raw = device.readline()
        #                        antwort = antwort_raw.decode()
                                antwort = str(antwort_raw[:-2].decode())
                                antwort += ' '
                                antwort = '{0:{1}<26}'.format(antwort, '0')
                            
        #                        antwort += ' '
        #                        for i in range(len(antwort), 29):
        #                            antwort += '0'
        #                        antwort.ljust(100, '0')
                                print('Antwort: \t', antwort)
                                
#                                device.flushInput()
                                
                                komm.send(antwort.encode('ascii'))
                            if nachricht[0] == '5':
#                                if arduino == False:
#                                    antwort = '000'
#                                    komm.send(antwort.encode('ascii'))
#                                    print(antwort)
#                                else:
                                print('warte auf Antwort')
                                sleep(1/50)                                
                                antwort_raw = device.readline()
        #                        antwort = antwort_raw.decode()
                                antwort = str(antwort_raw[:-2].decode())
#                                antwort = '110'
                                antwort += ' '
                                antwort = '{0:{1}<26}'.format(antwort, '0')
                            
        #                        antwort += ' '
        #                        for i in range(len(antwort), 29):
        #                            antwort += '0'
        #                        antwort.ljust(100, '0')
                                print('Antwort: \t', antwort)
                                
#                                device.flushInput()
                                
                                komm.send(antwort.encode('ascii'))
                            wiederversuch = False
                        except:
                            wiederversuch = True
                            print('Falsche Antwort')
#                            device.flushInput()

                if not arduino:
                    if nachricht[0] == '5':
                        antwort = '000 '
                        antwort = '{0:{1}<26}'.format(antwort, '0')
                    
                        print('Antwort: \t', antwort)

                        
                        komm.send(antwort.encode('ascii'))
                        
                        
#                '''Nachricht über den Raspberry Port routen'''                
#                if raspberry:
#                    device.write(nachricht.encode('ascii'))
#                    print('Laptop: \t', nachricht)
##                    print(nachricht[0])
##                    print(nachricht[1])
##                    print(nachricht[2])
#                    if nachricht[0] == '3' and nachricht [1] == '0':
##                        print('warte auf Antwort')
#                        antwort_raw = device.readline()
##                        antwort = antwort_raw.decode()
#                        antwort = str(antwort_raw[:-2].decode())
#                        antwort += ' '
#                        antwort = '{0:{1}<26}'.format(antwort, '0')
#                    
##                        antwort += ' '
##                        for i in range(len(antwort), 29):
##                            antwort += '0'
##                        antwort.ljust(100, '0')
#                        print('Antwort: \t', antwort)
#                        
#                        komm.send(antwort.encode('ascii'))
                print()
    
                '''Fehler abgreifen und Steve zurücksetzen, es wird davon 
                ausgegangen, dass die GUI neu gestartet wurde. '''
    except ConnectionAbortedError:
        print('Connection aborted.')
        if stev:               
            steve_msg = '09090.000018090.000000090.000009090.000009090.000000'   
            steve_com.send(steve_msg.encode('ascii'))
            print('Steve wurde resettet')
            steve_msg = ''
    except ConnectionResetError:
        print('Connection to GUI lost')
        if stev:               
            steve_msg = '09090.000018090.000000090.000009090.000009090.000000'   
            steve_com.send(steve_msg.encode('ascii'))
            print('Steve wurde resettet')
            steve_msg = ''

print('---Server shutdown---')