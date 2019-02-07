'''
Autor: Thomas Dasbach
Date: 

Modulbeschreibung:
Das Modul client_extern enthält die Funktion send_message. Es handelt sich 
um einen Socket-Client, der zu Testzwecken erstellt wurde. Nach der Funktion
werden alle möglichen Funktionsaufrufe in alphabetischer Reihenfolge gezeigt.

Beispielbefehle:

12 01 000 000 000 000 000 000
12 02 120 120 120 120 120 120
12 02 000 000 004 000 000 000

16 01 000 000 000 000 000 000

16 02 1.571 3.142 -3.002 1.431 1.571 1

16 03 000 000 000 000 000 000

16 04 000 000 000 000 000 000

18 01 000 000 000 000 000 000
18 02 120 120 120 120 120 120
'''

'Module importieren'
from socket import AF_INET, SOCK_STREAM, socket
from time import sleep
from math import cos
from numpy import around, array
from PyQt4 import QtGui

import os
import pygame
import xbox_gui
import sys

import json


sys.path.append(os.path.abspath('../../../'))

from Verwaltungsschale.structure import module
from Verwaltungsschale.structure import configuration

class ExampleApp(QtGui.QMainWindow, xbox_gui.Ui_mainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        
        self.setupUi(self)        
        
        self.nutz_socket = False
        self.nutz_zeromq = True
        'kommunikationssocket instanziieren'
        'IPv4-Protokoll und TCP'
        if self.nutz_socket:
            self.komm = socket(AF_INET, SOCK_STREAM)
            'Verbindung herstellen'
            #lokale IP-Adresse und Port 60000
            self.komm.connect(('localhost', 60100))
#        if self.nutz_zeromq:
#            self.COM_module = module.entity('X_BOX', configuration.config)
            
        if self.nutz_zeromq:
            self.COM_module = module.module('X_BOX', configuration.config)
        
        self.aktiv = True
        self.mode3_init = False
        self.mode3 = 0
                


        
        '''Knoepfe verbinden'''
        
        self.programm_senden_1.clicked.connect(self.programm_senden_1_f)
        self.programm_senden_2.clicked.connect(self.programm_senden_2_f)
        
        self.drop_befehle_senden.clicked.connect(self.drop_befehle_senden_f)
        self.manuelle_befehle_senden.clicked.connect(self.manuelle_befehle_senden_f)
        
        self.modus_3_senden.clicked.connect(self.modus_3_senden_f)
        
        self.modus_1_start.clicked.connect(self.modus_1_start_f)
        self.modus_1_stop.clicked.connect(self.modus_1_stop_f)
        self.modus_2_start.clicked.connect(self.modus_2_start_f)
        self.modus_2_stop.clicked.connect(self.modus_2_stop_f)
        self.modus_3_start.clicked.connect(self.modus_3_start_f)
        self.modus_3_stop.clicked.connect(self.modus_3_stop_f)
        self.close.triggered.connect(self.schliessen_f)
        self.empfange_button.clicked.connect(self.empfangen)
        self.modus_3_anfrage.clicked.connect(self.modus_3_anfrage_f)
        
        self.test_button.clicked.connect(self.test_button_f)
        
        '''Moegliche Befehle fuer die Schnellauswahl'''
        self.beispiel_befehle = [\
        '12 01 000 000 000 000 000 000',\
        '12 02 120 120 120 120 120 120',\
        '12 02 000 000 004 000 000 000',\
        '18 01 000 000 000 000 000 000',\
        '18 02 120 120 120 120 120 120',\
        '18 02 0 170 90 50 120 120',\
        '18 02 120 120 120 120 120 120',\
        '19',\
        'N00 G00 X0 Y312 Z100',\
        'N00 G00 X0 Y412 Z300',\
        'N01 G01 X120 Y300 Z100',\
        'N01 G01 X0 Y400 Z300',\
        'N01 G01 X120 Y300 Z100',\
        'N66 ',\
        'N01 G01 X120 Y300 Z100',\
        'N01 G01 X120 Y300 Z100',\
        'N01 G01 X120 Y300 Z100',\
        'N01 G01 X120 Y300 Z100']        
        
        self.drop_befehle.addItems(self.beispiel_befehle)
        
        
        '''Ausgabefenster initial fuellen'''        
        self.ausgabe.append('---- Willkommen beim externen Hilfprogramm ----')
        self.ausgabe.append('Wählen Sie zunächst rechts einen Modus aus.')
        self.ausgabe.append('')      
        self.ausgabe.append('')
        
        self.apps_laden()
    

    def empfangen(self):
        
        MESSAGE = self.COM_module.receive()
        
        CORE_pyobj = self.COM_module.extract_core(MESSAGE)        
        
        self.ausgabe.append(CORE_pyobj)
    
    def modus_1_start_f(self):
        
        self.modus_1_start.setEnabled(False)
        self.modus_2_start.setEnabled(False)
        self.modus_3_start.setEnabled(False)
        
        self.modus_1_stop.setEnabled(True)
        self.drop_befehle_senden.setEnabled(True)
        self.manuelle_befehle_senden.setEnabled(True)
        
        self.drop_befehle.setEnabled(True)
        self.manuelle_befehle.setEnabled(True)
        
        self.Zustandsangabe_1.clear()
        self.Zustandsangabe_1.insertPlainText('Modus aktiviert.')
        
    def modus_1_stop_f(self):
        
        self.modus_1_start.setEnabled(True)
        self.modus_2_start.setEnabled(True)
        self.modus_3_start.setEnabled(True)
        
        self.modus_1_stop.setEnabled(False)
        self.drop_befehle_senden.setEnabled(False)
        self.manuelle_befehle_senden.setEnabled(False)
        
        self.drop_befehle.setEnabled(False)
        self.manuelle_befehle.setEnabled(False)
        
        self.Zustandsangabe_1.clear()
        self.Zustandsangabe_1.insertPlainText('Modus deaktiviert.')
        
    def modus_2_start_f(self):
        self.modus_1_start.setEnabled(False)
        self.modus_2_start.setEnabled(False)
        self.modus_3_start.setEnabled(False)
        
        self.modus_2_stop.setEnabled(True)
        self.programm_senden_1.setEnabled(True)
        
        self.Zustandsangabe_2.clear()
        self.Zustandsangabe_2.insertPlainText('Modus aktiviert.')
        
    def modus_2_stop_f(self):
        self.modus_1_start.setEnabled(True)
        self.modus_2_start.setEnabled(True)
        self.modus_3_start.setEnabled(True)
        
        self.modus_2_stop.setEnabled(False)
        self.programm_senden_1.setEnabled(False)
        self.programm_senden_2.setEnabled(False)   
        
        self.Zustandsangabe_2.clear()
        self.Zustandsangabe_2.insertPlainText('Modus deaktiviert.')        
        
    def modus_3_start_f(self):
        self.modus_1_start.setEnabled(False)
        self.modus_2_start.setEnabled(False)
        self.modus_3_start.setEnabled(False)
        
        self.modus_3_stop.setEnabled(True)
        self.modus_3_senden.setEnabled(True)
        self.modus_3_anfrage.setEnabled(True)
        
        self.Zustandsangabe_3.clear()
        self.Zustandsangabe_3.insertPlainText('Modus aktiviert.')
        
    def modus_3_stop_f(self):
        self.modus_1_start.setEnabled(True)
        self.modus_2_start.setEnabled(True)
        self.modus_3_start.setEnabled(True)
        
        self.modus_3_stop.setEnabled(False)
        self.modus_3_senden.setEnabled(False)
        self.modus_3_anfrage.setEnabled(False)
        
        self.Zustandsangabe_3.clear()
        self.Zustandsangabe_3.insertPlainText('Modus deaktiviert.')
        
    def programm_senden_1_f(self):
        self.programm_senden_2.setEnabled(True) 
        
    def programm_senden_2_f(self):
        
        nachricht = '16 01'
        self.senden(nachricht)
        
        winkel_start = array([1.571, 3.142, -3.002, 1.431, 0.8])
        winkel = winkel_start
        
        for i in range(0, 201):
           
            nachricht = ''
            nachricht += '16 02 '
            
#            modi = float((sin(3.1415 * i * 0.2) + 1)*0.95)
#            winkel[0] = float(3.1415 * modi/2)
#            nachricht += str(around(float(winkel[0]), 5))
#            nachricht += ' '
            nachricht += '1.571 '
#            
#            modi = float((cos(3.1415 * i * 0.2) + 1))
#            winkel[1] = float(3.1415 * modi/4 + 3.1415/2)
#            nachricht += str(around(float(winkel[1]), 5))
#            nachricht += ' '
#            
            nachricht += '3.142 '
            modi = float((cos(3.1415 * i * 0.02) + 1)*0.95)
            winkel[2] = float((-3.1415 * modi/2))
            nachricht += str(around(float(winkel[2]), 5))
            nachricht += ' '
#            nachricht += '-3.002 '
            
            nachricht += '1.431 1.571 0.978'

            self.senden(nachricht)
            
            if i % 5 == 0:
                sleep(1/2)
                
                
        sleep(1)    
        nachricht = '16 03'
        self.senden(nachricht)
        self.ausgabe.append('Programm wurde erstellt')  
        
        
    def drop_befehle_senden_f(self):
        self.senden(str(self.drop_befehle.currentText()))
        
    def manuelle_befehle_senden_f(self):
        self.senden(str(self.manuelle_befehle.text()))
        self.manuelle_befehle.clear()
        
    def modus_3_senden_f(self):
        self.modus_3_senden.setEnabled(False)
        #Loop until the user clicks the close button.
        self.done = False
        self.XBOX_port = None
        self.mode3_init = False      
        pygame.init()
    
      
        clock = pygame.time.Clock()
        
        pygame.joystick.init()
        
        if self.mode3_init == False:
            sleep(1)            
            print('Mode 3 aktiv.')
            print()
            
            joystick_count = pygame.joystick.get_count()
            for i in range(joystick_count):
                joystick = pygame.joystick.Joystick(i)
                joystick.init()
            
            
                # Get the name from the OS for the controller/joystick
                name = joystick.get_name()                
                if name == 'Controller (XBOX 360 For Windows)':
                    self.XBOX_port = i
                if name == 'Controller (Xbox 360 Wireless Receiver for Windows)':
                    self.XBOX_port = i
                if name == 'Controller (Xbox One For Windows)':
                    self.XBOX_port = i
                if name == 'Xbox 360 Wireless Receiver':
                    self.XBOX_port = i
                
            self.mode3_init = True
                
        if self.XBOX_port == None:
                
            self.done = True
            print('XBox Controller nicht gefunden')
            self.ausgabe.append('Hab echt gesucht, aber')
            self.ausgabe.append('habe wirklich keinen XBox')
            self.ausgabe.append('Controller gefunden :(')
                
        else:
            print('Control with XBox ready.')    
            print()
            print('X_box port: ', self.XBOX_port)                
                
        self.mode3 = 0
        while self.done == False:
            
            joystick = pygame.joystick.Joystick(self.XBOX_port)
            joystick.init()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.done=True
            
            self.button = joystick.get_button( 0 )
            '''Enable the continuous remote control'''
            if self.button == 1 and self.mode3 == 0: 
                self.mode3 = 1
                nachricht = '17 01 000 000 000 000 000 000'
                self.senden(nachricht)
                
            if self.mode3 == 1:
                
                nachricht = '17 02 00'           
                                    
                self.axis = joystick.get_axis( 0 )
                if abs(-self.axis)<0.5:
                    self.mod_axis=0
                else: self.mod_axis = (self.axis) / 2
                nachricht += str(int((self.mod_axis + 0.5) * 8))
                
                nachricht += ' 00'
                self.axis = joystick.get_axis( 1 )
                if abs(self.axis)<0.5:
                    self.mod_axis=0
                else: self.mod_axis = (-self.axis) / 2
                nachricht += str(int((self.mod_axis + 0.5) * 8))
                
                nachricht += ' 00'
                self.axis = joystick.get_axis( 4 )
                if abs(self.axis)<0.5:
                    self.mod_axis=0
                else: self.mod_axis = (-self.axis) / 2
                nachricht += str(int((self.mod_axis + 0.5) * 8))
                
    
                nachricht += ' 00'
                self.axis = joystick.get_axis( 2 )
                if abs(self.axis)<0.5:
                    self.mod_axis=0
                else: self.mod_axis = (-self.axis) / 2
                nachricht += str(int((self.mod_axis + 0.5) * 8))                
                
                nachricht += ' 00'
                self.axis = joystick.get_axis( 3 )
                if abs(self.axis)<0.5:
                    self.mod_axis=0
                else: self.mod_axis = (self.axis) / 2
                nachricht += str(int((self.mod_axis + 0.5) * 8))
    
    
                nachricht += ' 00'
                nachricht_erw = '4'                
                self.button = joystick.get_button( 3 )
                if self.button == 1:
                    nachricht_erw = '8'
                    
                self.button = joystick.get_button( 2 )
                if self.button == 1: 
                    nachricht_erw = '0'
                    
                nachricht += nachricht_erw  
                
                self.senden(nachricht)
                    
                print(nachricht)
            # Limit to 1 frames per second
                
                
            self.button = joystick.get_button( 1 )
            '''Disable the continuous remote control'''
            if self.button == 1 and self.mode3 == 1:
                
                self.modus_3_senden.setEnabled(True)
                nachricht = '17 03 000 000 000 000 000 000'
                
                self.senden(nachricht)
                self.mode3 = 0
                self.done = True
                
            clock.tick(5)    

    def modus_3_anfrage_f(self):
        nachricht = '20 01 000 000 000 000 000 000'
        self.senden(nachricht)
        
    def senden(self, nachricht):
        self.ausgabe.append(nachricht)
        if self.nutz_socket:
            self.komm.send(nachricht.encode('ascii'))
        if self.nutz_zeromq:
            MESSAGE = self.create_traitor(TO = configuration.config['ROBO_GUI']['identity'], CORE_pyobj = nachricht, FROM = configuration.config['X_BOX']['identity'])
            print(MESSAGE)
            self.COM_module.send(MESSAGE)
            
    def create_traitor(self, TO = b'someone', CORE_pyobj = "no input", MESSAGE_received = False, FROM = b'from'):

        ADDRESS = []
        TO = [TO]
        FROM = [FROM]
        CORE_json = json.dumps(CORE_pyobj)
        CORE = [CORE_json.encode('ascii')]

        if MESSAGE_received:

            MESSAGE_received.pop()
            TO = [MESSAGE_received.pop()]
            MESSAGE_received.pop()
            ADDRESS = MESSAGE_received

        MESSAGE = ADDRESS + TO + FROM + CORE
        return MESSAGE
            
    def schliessen_f(self):
        
        if self.mode3 == 1:
            nachricht = '17 03 000 000 000 000 000 000'
            self.senden(nachricht)
        
        pygame.quit ()
        self.close()
        
    def apps_laden(self):
        
        self.apps_alle = configuration.config
        for self.app_name in self.apps_alle:
            self.andere_apps.addItem(str(self.app_name))
            
#        self.andere_apps.paintEvent(self.app_name)
        
    def test_button_f(self):
        self.senden(self.andere_apps.currentItem().text())
        

def main():   

    app = QtGui.QApplication(sys.argv)  
    form = ExampleApp()                 
    form.show()                         
    app.exec_()
    
    pygame.quit()
               


if __name__ == '__main__':              
    main()                              
