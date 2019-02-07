'''
Autor: Martin Schinnerl
Datum: 25.09.2016
Modifikation: Thomas Dasbach
Datum: 02.01.2016

Modulbeschreibung:
Das Modul steuerung enthält die Klasse Motor. Die Klasse wird im Sinne
der parallelen Programmierung von der Klasse QObject abgeleitet. Beim
Instanziieren eines Objektes ist der COM-Port (im Geräte-Manager
nachsehen) als String zu übergeben. Weiter werden die beiden Signale 
finished und start_akt definiert. Das erste Signal dient dem Beenden
eines Threads. Da der Start-Button während der Ausführung eines 
Programmes deaktiviert ist, dient das zweite Signal dem Aktivieren des
Buttons am Ende eines Programmes. Im Code-Block der Methode __init__ 
werden neben der Vererbung der Attribute und Methoden der Basisklasse
QObject, ein Attribut zur Unterbrechung der Ausführschleife der Methode 
servo_start definiert, die Offset-Werte der Motoren festgelegt, der
COM-Port zugewiesen, die minimal und maximal zulässigen PWM-Signale 
sowie die Grenzwinkel (Denavit-Hartenberg-Parameter) festgelegt. 
Weitere Methoden der Klasse Motor sind device_verbinden, fernsteuerung,
modulation, nachricht_senden, position_abfragen, programm_laden, 
servo_kalibrieren, servo_stop, servo_start, steuerung_fern und 
steuerung_synchron.
'''

'Module importieren'
from math import pi, sqrt, asin
from numpy import array, hsplit, hstack, load, vsplit, vstack
from os import getcwd, path
from PyQt4.QtCore import QObject, Signal
#from serial import Serial
from time import sleep
from berechnung.transformationen import Eulertransformation, kinematik_inv, kinematik_vor

import socket
#import sys



'TESTZWECKE'
from pprint import pprint

'Klasse Motor'
class Motor(QObject):
    
    'Signale definieren'
    finished = Signal()
    start_akt = Signal()
    
    'Methode __init__'
    def __init__(self, port, parent = None):
        
        'Vererbung aller Attribute und Methoden von QObject'
        super(Motor, self).__init__(parent)
        
        'Attribut zum Beenden der Ausführschleife definieren'
        self.exiting = False
        
        'Offset Werte der Servomotoren festlegen'
        #Achse1 - Kanal0
        self.offset1 = 15
        #Achse2 - Kanal1
        self.offset2 = 2
        #Achse3 - Kanal8
        self.offset3 = -65
        #Achse4 - Kanal16
        self.offset4 = 55
        #Achse5 - Kanal24
        self.offset5 = 0
        #Achse6 - Kanal25
        self.offset6 = 0
        
        'Attribut COM-Port definieren'
        self.port = port
        
        'Minimal und Maximal zulässige PWM-Signale in [ms] festlegen'
        'UNNÖTIG - 09.01.2017'
        #Achse1 - Kanal0
        self.pwm1_min = 905
        self.pwm1_max = 2095
        #Achse2 - Kanal1
        self.pwm2_min = 920
        self.pwm2_max = 2080
        #Achse3 - Kanal8
        self.pwm3_min = 900
        self.pwm3_max = 2100
        #Achse4 - Kanal16
        self.pwm4_min = 935
        self.pwm4_max = 2065
        #Achse5 - Kanal24
        self.pwm5_min = 700
        self.pwm5_max = 2300
        #Achse6 - Kanal25
        self.pwm6_min = 900
        self.pwm6_max = 1650
        
        'Grenzwinkel (Denavit-Hartenberg-Parameter) festlegen'
        #Achse1 - Kanal0
        self.theta1_min = 0 #-1
        self.theta1_max = pi #+1
        #Achse2 - Kanal1
        self.theta2_min = 0 #vorne +1
        self.theta2_max = pi #hinten -1
        #Achse3 - Kanal8
        self.theta3_min = -(pi - 8*pi/180) #zu -1
        self.theta3_max = 0 #auf +1
        #Achse4 - Kanal16
        self.theta4_min = -8*pi/180 #oben +1
        self.theta4_max = pi - 8*pi/180 #unten -1
        #Achse5 - Kanal24
        self.theta5_min = 0 #links -1
        self.theta5_max = pi #rechts +1
        
        'Grenzradien des Greifers festlegen'
        #Achse6 - Kanal25
        self.r6_min = 100 #zu -1
        self.r6_max = 200 #auf +1
        
        'Vorrangegangene Winkel'
        self.alteWinkel = [0,0,0,0,0,0,0]
        
        self.Geschwindigkeiten = [0,0,0,0,0,0,0]
        
        self.stable_Ver = [000, 110, 120]
        
        
    '''Methode device_verbinden - Die Methode dient dem 
    Instanziieren eines Serial-Objektes.
    '''
    def device_verbinden(self):
        
#       'Serial-Objekt instanziieren'
        

        ip = "127.0.0.1"
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

        self.s.connect((ip, 60110))

            
                
#        self.s.listen(5)
        
#        self.device = Serial(self.port, 9600, timeout = None)
#        'Port festlegen'
#        self.device.port = self.port
#        'Baudrate festlegen'
#        self.device.baudrate = 115200  
#        'Timeout festlegen'
#        self.device.timeout = 1
        sleep(1/100)
        
    def device_schliessen(self):
        
        self.s.close()
        sleep(1/10)        
        
        
        
    '''Methode fernsteuerung - Die Methode ermöglicht die Fernsteuerung
    des Roboters. Voraussetzung ist das Laden der Fernsteuerungsparameter
    mit der Methode steuerung_fern und der Aufruf der Methode steuerung_
    synchron. Ein Parameter pro Achse ermöglicht die unabhängige Steuerung
    der Servomotoren. Nach dem Erzeugen eines Serial-Objektes wird die
    aktuelle Position in Form von PWM-Signalen ausgelesen. Die Signale
    werden in die Winkel (Denavit-Hartenberg-Parameter) und den Öffnungs-
    radius des Greifers transformiert. Weiter werden die Winkel und der 
    Radius entsprechend den Fernsteuerungsparameten verändert. Am Ende 
    werden diese der Methode servo_start übergeben.'''
    def fernsteuerung(self):
        
        'Methode device_verbinden aufrufen'
#        self.device_verbinden()
        
        'Position abfragen'
        pwm1, pwm2, pwm3, pwm4, pwm5, pwm6 = self.position_abfragen()
        
        'Transformation der PWM-Signale in Winkel'
        theta1 = - (pwm1 - self.pwm1_max)/(self.pwm1_max - \
        self.pwm1_min)*pi
        theta2 = (pwm2 - self.pwm2_min)/(self.pwm2_max - \
        self.pwm2_min)*pi
        theta3 = (pwm3 - self.pwm3_max)/(self.pwm3_max - \
        self.pwm3_min)*pi
        theta4 = (pwm4 - self.pwm4_min)/(self.pwm4_max - \
        self.pwm4_min)*pi
        theta5 = - (pwm5 - self.pwm5_max)/(self.pwm5_max - \
        self.pwm5_min)*pi
        
        'Transformation des PWM-Signals in den Öffnungsradius'
        r6 = 200 - (pwm6 - self.pwm6_min)/(self.pwm6_max - \
        self.pwm6_min)*(200 - 100)
        
        'Winkel zuordnen'
        if self.p1 == 1:
            theta1 = self.theta1_max
        elif self.p1 == -1:
            theta1 = self.theta1_min
        
        if self.p2 == 1:
            theta2 = self.theta2_min
        elif self.p2 == -1:
            theta2 = self.theta2_max
        
        if self.p3 == 1:
            theta3 = self.theta3_max
        elif self.p3 == -1:
            theta3 = self.theta3_min
            
        if self.p4 == 1:
            theta4 = self.theta4_max
        elif self.p4 == -1:
            theta4 = self.theta4_min
            
        if self.p5 == 1:
            theta5 = self.theta5_max
        elif self.p5 == -1:
            theta5 = self.theta5_min
        
        'Öffnungsradius des Greifers zuordnen'
        if self.p6 == 1:
            r6 = self.r6_max
        elif self.p6 == -1:
            r6 = self.r6_min
        
        'Winkel-Matrix erstellen'
        self.winkel = array([[theta1, theta2, theta3, theta4, theta5]])
        'Greifer-Matrix erstellen'        
        self.greifer = array([[r6]])        
        
        'Aufruf der Methode servo_start'
        self.servo_start()
        
    '''Methode modulation - Die Methode transformiert die Winkel 
    (Denavit-Hartenberg-Parameter) und den Öffnungsradius des Greifers 
    in pulsweitenmodulierte Signale (PWM-Signale).'''
    'Methode ist deaktiviert - 09.01.2017'
    def modulation(self):
       '''
        'Format der Winkel-Matrix abfragen'
        #Format: nx5 mit n-Zeilen
        zeilenzahl, spaltenzahl = self.winkel.shape
        
        'Matrix in Zeilen teilen'
        zeilen = vsplit(self.winkel, zeilenzahl)
        
        'Matrix zeilenweise durchlaufen'
        for i in range(0, zeilenzahl):
            
            'Zeile_i auswählen'
            zeile = zeilen[i]
            
            'Zeile_i in Spalten teilen und die Einträge den Winkeln zuordnen'
            theta1, theta2, theta3, theta4, theta5 = \
            hsplit(zeile, spaltenzahl)
            
            'Datentyp array in float konvertieren'
            theta1 = float(theta1)
            theta2 = float(theta2)
            theta3 = float(theta3)
            theta4 = float(theta4)
            theta5 = float(theta5)
            
            'Transformation der Winkeln in PWM-Signale'
            pwm1 = int(self.pwm1_max - (self.pwm1_max - \
            self.pwm1_min)/pi*theta1)
            pwm2 = int(self.pwm2_min + (self.pwm2_max - \
            self.pwm2_min)/pi*theta2)
            pwm3 = int(self.pwm3_max + (self.pwm3_max - \
            self.pwm3_min)/pi*theta3)
            pwm4 = int(self.pwm4_min + (self.pwm4_max - \
            self.pwm4_min)/pi*theta4)
            pwm5 = int(self.pwm5_max - (self.pwm5_max - \
            self.pwm5_min)/pi*theta5)
            
            'PWM-Signale der Winkel zu einer Matrix zusammensetzen'
            #1.Zeile - neue Matrix erstellen
            if i == 0:
                pwm15 = array([[pwm1, pwm2, pwm3, pwm4, pwm5]])
            #2.Zeile bis n-te Zeile - Zeilen hinzufügen
            elif i >= 1:
                pwm15_neu = array([[pwm1, pwm2, pwm3, pwm4, pwm5]])
                
                pwm15 = vstack((pwm15, pwm15_neu))
                
        'Format der Greifer-Matrix abfragen'
        #Format: nx1 mit n-Zeilen
        zeilenzahl, spaltenzahl = self.greifer.shape
        
        'Matrix in Zeilen teilen'
        zeilen = vsplit(self.greifer, zeilenzahl)
        
        'Matrix zeilenweise durchlaufen'
        for i in range(0, zeilenzahl):
            
            'Zeile_i auswählen'
            zeile = zeilen[i]
            
            'Datentyp array in float konvertieren'
            r6 = float(zeile)
            
            'Transformation des Öffnungsradius in PWM-Signale'
            pwm6 = int(self.pwm6_min - (self.pwm6_max - \
            self.pwm6_min)/(200 - 100)*(r6 - 200))
            
            'PWM-Signale des Radius zu einer Matrix zusammensetzen'
            #1.Zeile - neue Matrix erstellen
            if i == 0:
                pwm68 = array([[pwm6]])
            #2.Zeile bis n-te Zeile - Zeilen hinzufügen
            elif i >= 1:
                pwm68_neu = array([[pwm6]])
                
                pwm68 = vstack((pwm68, pwm68_neu))
        
        'PWM-Signale zu einer Gesamtmatrix zusammensetzen'
        #Format nx6 mit n-Zeilen
        self.pwm = hstack((pwm15, pwm68))
       '''
       
    '''Methode ingrad - Die Methode transformiert die Winkel 
    (Denavit-Hartenberg-Parameter) und den Öffnungsradius des Greifers 
    von Bogenmaß in Grad.'''
    def ingrad(self):
       
        'Format der Winkel-Matrix abfragen'
        #Format: nx5 mit n-Zeilen
        zeilenzahl, spaltenzahl = self.winkel.shape
        
        'Matrix in Zeilen teilen'
        zeilen = vsplit(self.winkel, zeilenzahl)
        
        'Matrix zeilenweise durchlaufen'
        for i in range(0, zeilenzahl):
            
            'Zeile_i auswählen'
            zeile = zeilen[i]
        
            
            'Zeile_i in Spalten teilen und die Einträge den Winkeln zuordnen'
            theta1, theta2, theta3, theta4, theta5 = \
            hsplit(zeile, spaltenzahl)
            
            'Datentyp array in float konvertieren'
            theta1 = float(theta1)
            theta2 = float(theta2)
            theta3 = float(theta3)
            theta4 = float(theta4)
            theta5 = float(theta5)
            
            'Transformation der Winkeln in Grad'
            pwm1 = 180-int(theta1/pi*180)
            pwm2 = int(theta2/pi*180)
            pwm3 = 180+int(theta3/pi*180)-8
            pwm4 = int(theta4/pi*180)+9
            pwm5 = int(theta5/pi*180)
            
            if pwm4 < 0:
                pwm4 = 0
            if pwm5 > 180:
                pwm5 = 180
            
            'PWM-Signale der Winkel zu einer Matrix zusammensetzen'
            #1.Zeile - neue Matrix erstellen
            if i == 0:
                pwm15 = array([[pwm1, pwm2, pwm3, pwm4, pwm5]])
            #2.Zeile bis n-te Zeile - Zeilen hinzufügen
            elif i >= 1:
                pwm15_neu = array([[pwm1, pwm2, pwm3, pwm4, pwm5]])
                
                pwm15 = vstack((pwm15, pwm15_neu))
                
        'Format der Greifer-Matrix abfragen'
        #Format: nx1 mit n-Zeilen
        zeilenzahl, spaltenzahl = self.greifer.shape
        
        'Matrix in Zeilen teilen'
        zeilen = vsplit(self.greifer, zeilenzahl)
        
        'Matrix zeilenweise durchlaufen'
        for i in range(0, zeilenzahl):
            
            'Zeile_i auswählen'
            zeile = zeilen[i]
            
            'Datentyp array in float konvertieren'
            r6 = float(zeile)
            
            'Transformation des Öffnungsradius in PWM-Signale'
            #pwm6 = int(900 - (1650 - 900)/(200 - 100)*(r6 - 200))
            
            pwm6 = int(0 - (112 / (200-100) * (r6-200)))
            if pwm6 < 0 : pwm6 == 0
                
            #/pi*180
            'ZU TESTZWECKEN'
            #pwm6 = 90
            
            'PWM-Signale des Radius zu einer Matrix zusammensetzen'
            #1.Zeile - neue Matrix erstellen
            if i == 0:
                pwm68 = array([[pwm6]])
            #2.Zeile bis n-te Zeile - Zeilen hinzufügen
            elif i >= 1:
                pwm68_neu = array([[pwm6]])
                
                pwm68 = vstack((pwm68, pwm68_neu))
        
        'PWM-Signale zu einer Gesamtmatrix zusammensetzen'
        #Format nx6 mit n-Zeilen
        self.pwm = hstack((pwm15, pwm68))

    '''Methode ingrad_Echtzeit - Die Methode transformiert die Winkel 
    (Denavit-Hartenberg-Parameter) und den Öffnungsradius des Greifers 
    von Bogenmaß in Grad.'''
    def ingrad_Echtzeit(self,theta1_if, theta2_if, theta3_if, theta4_if, theta5_if, r6):
       

        'Datentyp array in float konvertieren'
        theta1_i = float(theta1_if)
        theta2_i = float(theta2_if)
        theta3_i = float(theta3_if)
        theta4_i = float(theta4_if)
        theta5_i = float(theta5_if)

        
        'Transformation der Winkeln in Grad'
        pwm1 = 180-int(round(theta1_i/pi*180,0))
        pwm2 = int(round(theta2_i/pi*180,0))
        pwm3 = 180+int(round(theta3_i/pi*180,0))-8
        pwm4 = int(round(theta4_i/pi*180,0))+9
        pwm5 = int(round(theta5_i/pi*180,0))
        
        if pwm3 < 0:
            pwm3 = 0
        if pwm4 < 0:
            pwm4 = 0
        if pwm5 > 180:
            pwm5 = 180
        
        pwm6 = int(r6)     
        if pwm6 < 40 : pwm6 == 40
        if pwm6 > 140 : pwm6 == 140
        return pwm1, pwm2, pwm3, pwm4, pwm5, pwm6


        
    '''
    Methode nachrichten_erstellen - Die Methode baut aus 6 Winkelangeben einen
    String der Form XX XXX XX.XX XXX XX.XX ... . Vor der Methode müssen die
    Winkel in Grad umgewandelt werden.
    '''
    def nachricht_erstellen(self, P1, P2, P3, P4, P5, P6, \
    S1, S2, S3, S4, S5, S6):
        
        
        
        self.Winkel = [0,P1,P2,P3,P4,P5,P6]
        self.speed = [0, S1, S2, S3, S4, S5, S6]
        
        nachricht = ''
        tho_i = 1
        nachricht += '00'
        for tho_i in range(1,7):
            self.akt_winkel = float(self.Winkel[tho_i])
            nachricht += ' '
            if self.akt_winkel < 0:
                print('Winkel ', tho_i, ' ist negativ'
                )
            if self.akt_winkel == 0 or self.akt_winkel < 0:
                nachricht += '000'
            elif self.akt_winkel < 100:
                if self.akt_winkel < 10:
                    nachricht += '00' + str(int(round(self.akt_winkel,0)))
                if int(self.Winkel[tho_i]) > 9:
                    nachricht += '0' + str(int(round(self.akt_winkel, 0)))
                #print(nachricht)
            elif int(self.Winkel[tho_i]) > 99:
                if int(self.Winkel[tho_i]) > 180:
                    nachricht += "180"
                else:
                    nachricht += str(int(round(self.akt_winkel,0)))
                #print(nachricht)
                
            nachricht += ' '
            
            self.speed_a = float(self.speed[tho_i])   
            if int(self.speed[tho_i]) == 0 or int(self.speed[tho_i]) < 0:
                nachricht += '00.0'
            elif int(self.speed[tho_i]) < 10:
                nachricht += '0' + \
                str("{0:.1f}".format(round(self.speed_a,1)))
                #print(nachricht)
            elif int(self.speed[tho_i]) >= 10:
                if int(self.speed[tho_i]) >= 30:
                    nachricht += "30.0"
                else:
                    nachricht += str("{0:.1f}".format(round(self.speed_a,1)))
                #print(nachricht)
        return nachricht

    def Geschwindigkeiten_ermitteln(self, P1, P2, P3, P4, P5, P6, Spd_m):
        
        if Spd_m > 10:
            print('Maximaler Speed überschrieben. Gewählt war: ', Spd_m)
            Spd_m = 10
        if Spd_m < 0:
            print('Mindest Speed überschrieben. Gewählt war: ', Spd_m)
            Spd_m = 1
            
        tho_i = 1
        self.angle = array([[0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0],[0,P1,P2,P3,P4,P5,P6]])
        self.winkel_dif = [0,0,0,0,0,0,0]
        self.speed = array([[0,0,0,0,0,0,0],\
        [0,0,0,0,0,0,0],[0.0,0.0,0.0,0.0,0.0,0.0,0.0]])
        self.Gesch_cor = [0,0,0,0,0,0,0]
        for tho_i in range(1,7):
            self.winkel_dif[tho_i] = abs((self.alteWinkel[tho_i]\
            -self.angle[2][tho_i]))
#            print("Winkel: ", tho_i, " Differenz: ", self.winkel_dif[tho_i])
        
        self.m_winkel_dif = (max(self.winkel_dif))        

        
        if self.m_winkel_dif == 0: self.m_winkel_dif = 1
#        print(self.m_winkel_dif)
        for tho_i in range(1,7):    
            
            self.speed[2][tho_i] = float(self.winkel_dif[tho_i]/\
            self.m_winkel_dif * Spd_m)
#            print(self.Geschwindigkeiten[tho_i])
            

            
#            self.Geschwindigkeiten[tho_i] = abs((self.alteWinkel[tho_i]\
#            -self.Winkel[tho_i])*40/255)
        
#            if self.speed[2][tho_i] < 1 \
#            and self.winkel_dif[tho_i] > 0:
#                self.Gesch_cor[tho_i] = 1 - self.speed[2][tho_i]
#                self.speed[2][tho_i] = 1
#        
#        for tho_i in range(1,7):
#            
#            self.speed[0][tho_i] = self.speed[2][tho_i]
#            self.speed[1][tho_i] = self.speed[2][tho_i]
            
#        '''  Die überkreuz multiplikation ist deshalb vorhanden, da die 
#        eigentliche If Bedingung jeweils die Winkel Dif / den Speed wäre, 
#        allerdings kann der Speed null sein.'''
#        if self.winkel_dif[2]*self.speed[2][3] < \
#        self.winkel_dif[3]*self.speed[2][2]:
##            print("Dif 3 größer")
#            if self.speed[2][2] == 0:
#                self.t1 = 0                
#            else:    
#                self.t1 = self.winkel_dif[2] / 36 / self.speed[2][2] * 10
##                print("Testpunkt 1")
#            if self.speed[2][3] == 0:
#                self.t2 = 0
#            else:
#                self.t2 = self.winkel_dif[3] / 36 / self.speed[2][3] * 10
#            
#            self.speed[0][4] += self.Gesch_cor[2] + self.Gesch_cor[3]
#            self.speed[1][4] += self.Gesch_cor[3]
#            
#        else:
##            print("dif 2 größer")            
#            if self.speed[2][2] == 0:
#                self.t2 = 0                
#            else:    
#                self.t2 = self.winkel_dif[2] / 36 / self.speed[2][2] * 10
#            if self.speed[2][3] == 0:
#                self.t1 = 0
#            else:
#                self.t1 = self.winkel_dif[3] / 36 / self.speed[2][3] * 10
#            self.speed[0][4] += self.Gesch_cor[2] + self.Gesch_cor[3]
#            self.speed[1][4] += self.Gesch_cor[2]
        
        self.t = self.m_winkel_dif / 3.3 / Spd_m
        
#        self.t3= max(self.t1, self.t2, self.t-self.t2)
#        
#        for tho_i in range(1,7):
#            self.angle[0][tho_i] = self.alteWinkel[tho_i] + \
#            (self.angle[2][tho_i] - self.alteWinkel[tho_i]) * self.t1 /self.t3
#            self.angle[1][tho_i] = self.alteWinkel[tho_i] + \
#            (self.angle[2][tho_i] - self.alteWinkel[tho_i]) * self.t2 /self.t3
        self.alteWinkel = self.angle[2] 
        
        
#        if self.winkel_dif[2]*self.speed[2][3] < \
#        self.winkel_dif[3]*self.speed[2][2]:
##            print("Dif 3 größer")
#            self.angle[0][2] = self.angle[2][2]
#            self.angle[1][2] = self.angle[2][2]
#            
#            self.angle[1][3] = self.angle[2][3]
#            
#        else:
#            self.angle[0][3] = self.angle[2][3]
#            self.angle[1][3] = self.angle[2][3]
#            
#            self.angle[1][2] = self.angle[2][2]
            
            
        return
        
        
        '''t basiert auf 180 Grad bei 5 in 9,6 Sekunden'''
            
    '''Methode nachricht_senden - Die Methode übermittelt Signale mit den 
    Methoden des Serial-Objektes in Form von Nachrichten (Datentyp: str) 
    an den Servocontroller. Vor dem Aufruf der Methode muss ein Serial-
    Objekt erzeugt werden (Methode device_verbinden).'''
    def nachricht_senden(self, nachricht):

        'serielle Schnittstelle öffnen'
#        self.device.open()
        
        'Information ausgeben'
        print(nachricht)        
        
        'Nachricht an den Servocontroller senden'
        self.s.send(nachricht.encode('ascii'))
        'Schnittstelle schließen'
#        self.device.close()


        
    '''Methode nachricht_senden - Die Methode übermittelt Signale mit den 
    Methoden des Serial-Objektes in Form von Nachrichten (Datentyp: str) 
    an den Servocontroller. Vor dem Aufruf der Methode muss ein Serial-
    Objekt erzeugt werden (Methode device_verbinden).'''
    def nachricht_senden_a(self, nachricht):

        'serielle Schnittstelle öffnen'
#        self.device.open()
        
        'Information ausgeben'
        print('An Arduino: ', nachricht)        
        
        'Nachricht an den Servocontroller senden'
        self.s.send(nachricht.encode('ascii'))
        'Schnittstelle schließen'
#        self.device.close()

        

    
    def notaus(self):
        
        
        
        'Nachricht mit der Halteposition erstellen'
        nachricht = \
        '12 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an den Servocontroller senden'
        self.nachricht_senden(nachricht)
        
    '''Methode position_abfragen - Die Methode gibt die aktuelle Position
    der Servomotoren in Form von PWM-Signalen zurück. Die Signale werden
    vom Servocontroller ausgelesen.'''
    'Funktion deaktiviert - 09.01.2017'
    def position_abfragen(self):
        '''
        'leere Liste zum Speichern der Halteposition erstellen'
        antwort = []    
        
        'serielle Schnittstelle öffnen'
#        self.device.open()
        
        'in einer Schleife die aktuelle Position der Motoren abfragen'
        for kanal in [0, 1, 8, 16, 24, 25]:
            
            'Nachricht zur Positionsabfrage erstellen'
            nachricht = 'QP' + str(kanal) + '\r'
            
            'Nachricht an den Servocontroller senden'
#            self.device.write(nachricht.encode('ascii'))
            
            'Antwort mit der aktuellen Position (Halteposition) empfangen'
            #Datentyp: bytes
#            antwort_kanal = self.device.read(1)
            
            'Antwort in PWM-Signal konvertieren und der Liste hinzufügen'
#            antwort += [antwort_kanal[0]*10]
            
        antwort = (1499,2080,953,1449,1499,1275)
        'Halteposition als neue Position senden'
        P1st, P2st, P3st, P4st, P5st, P6st = antwort
        
        'Datentyp ändern'
        P1st = int(P1st)
        P2st = int(P2st)
        P3st = int(P3st)
        P4st = int(P4st)
        P5st = int(P5st)
        P6st = int(P6st)
        
        return P1st, P2st, P3st, P4st, P5st, P6st
        '''
        
        return 90, 90, 90, 90, 90, 90
        
    '''Methode programm_laden - Die Methode lädt die Sollwinkel und den
    Öffnungsradius des Greifers in Form eines Arrays. Das Format der Winkel-
    Matrix ist nx5 und das der Greifer-Matrix ist nx1 mit n-Zeilen, wobei 
    jede Zeile einer neuen Position entspricht. Die Methode ist vor dem 
    Start der Motoren mit der Methode servo_start aufzurufen.'''
    def programm_laden(self, speichername):
        
        'Arbeitsverzeichnis abfragen'
        workdir = getcwd()
        
        'Dateiname der Winkel-Matrix'
        dateiname = speichername + '_winkel.npy'
        
        'Pfad der Winkel-Matrix'
        dir = path.join(workdir, 'speicher', 'programmspeicher', \
        dateiname)
        
        'Winkel-Matrix laden und zuweisen'
        self.winkel = load(dir)
        
        'Dateiname der Greifer-Matrix'
        dateiname = speichername + '_greifer.npy'
        
        'Pfad der Greifer-Matrix'
        dir = path.join(workdir, 'speicher', 'programmspeicher', \
        dateiname)
       
        'Greifer-Matrix laden und zuweisen'
        self.greifer = load(dir)
        
        'alte Winkel mit Starposition gleichsetzen'
        self.alteWinkel = [0, 90, 180, 0, 90, 90, 90]
        if speichername == 'programmFortsetzen':
            self.alteWinkel = [180, 0, 0, 180, 180, 0, 0]
        
    '''Methode servo_kalibrieren - Die Methode sendet die
    festgelegten Offset-Werte an den Servo-Controller. Die
    Methode wird beim Einschalten des Roboters ausgeführt.'''
    'Methode ist deaktiviert - 09.01.2017'
    def servo_kalibrieren(self):
        '''
        'Offset-Werte in eine Nachricht schreiben'
        nachricht = \
        '#0' + ' PO' + str(self.offset1) + \
        ' #1' + ' PO' + str(self.offset2) + \
        ' #8' + ' PO' + str(self.offset3) + \
        ' #16' + ' PO' + str(self.offset4) + \
        ' #24' + ' PO' + str(self.offset5) + \
        ' #25' + ' PO' + str(self.offset6) + ' \r'
        
        'Nachricht an den Servocontroller senden'
        self.nachricht_senden(nachricht)
        '''
        
        
    '''Methode servo_stop - Die Methode bringt die Servomotoren des
    Roboters zum Stillstand. Im ersten Schritt wird die Ausführschleife
    der Methode servo_start abgebrochen und so das Senden einer neuen
    Position verhindert. Nach dem Abbruch würde der Roboter bis zum Ende 
    der letzten an den Servocontroller gesendeten Position fahren. Um den 
    Roboter zwischen den Positionen anzuhalten, werden die aktuellen Winkel-
    positionen der Servomotoren in einer Schleife abgefragt und als 
    neue Position übermittelt. In Folge bleibt der Roboter stehen.'''
    def servo_stop(self):
        
        'Ausführschleife der Methode servo_start abbrechen'
        self.exiting = True
        
        'Halteposition abfragen'
#        P1st, P2st, P3st, P4st, P5st, P6st = self.position_abfragen()
                  
        'Nachricht mit der Halteposition erstellen'
        nachricht = \
        '20 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an den Servocontroller senden'
        self.nachricht_senden(nachricht)
        
        'Information ausgeben'
#        print(nachricht)


        
    '''Methode servo_start - Die Methode startet die Servomotoren
    des Roboters. Voraussetzung sind das Laden eines Programmes und 
    der Aufruf der Methode steuerung_synchron. Innerhalb der Methode 
    servo_start werden die Methode device_verbinden sowie die Methode 
    modulation aufgerufen. Danach werden die vom Roboter anzufahrenden 
    Positionen der Reihe nach an den Servocontroller übermittelt. Die 
    Funktion kann durch Aufruf der Methode servo_stop beendet werden.'''
    def servo_start(self): 
                
        
        'Methode device_verbinden aufrufen'
        self.device_verbinden()
        
        'Ausführschleife wird durchlaufen'
        self.exiting = False  
        
        
        'Shield aktivieren'
        self.shield_start()
        
#        'Shield deaktivieren'
#        if self.speichername == 'programmAus':
#            self.shield_abschalten()
            
#        pprint(self.winkel)    
        'Methode modulation aufrufen'
        self.ingrad()
        'Zählvariable definieren'
        nr = 0
        
        'TEST'
        sleep(self.t/12)
        
              
        
        'Ausführschleife zum Durchlaufen der PWM-Matrix'
        while not self.exiting:
            
            'Format der PWM-Matrix abfragen'
            #Format: nx6 mit n-Zeilen
            zeilenzahl, spaltenzahl = self.pwm.shape
            
            'Matrix in Zeilen teilen'
            zeilen = vsplit(self.pwm, zeilenzahl)
            
            'Zeile_nr auswählen'
            zeile = zeilen[nr]
            
            'Spalteneinträge der Zeile den Kanälen zuordnen'
            P1, P2, P3, P4, P5, P6 = hsplit(zeile, spaltenzahl)
            
            'Ermittlung der nötigen Geschwindigkeiten'            
            
            self.Geschwindigkeiten_ermitteln(P1, P2, P3, P4, P5, P6, 10)
            
            self.speed_split = vsplit(self.speed, 3)
            line = self.speed_split[2]
            
            junk, S1, S2, S3, S4, S5, S6 = hsplit(line, 7) 
            
            'Nachricht mit den PWM-Signalen erstellen'
            nachricht = self.nachricht_erstellen(P1, P2, P3, P4, P5, P6, \
            S1, S2, S3, S4, S5, S6)

            'Nachricht an den Servocontroller senden'
            self.nachricht_senden(nachricht)          
            
#            lines, rows = self.angle.shape  
#            self.angle_split = vsplit(self.angle, lines)   
#            lines, rows = self.speed.shape  
#            self.speed_split = vsplit(self.speed, lines) 
#            
#            for tho_j in range(0,3):
#                line = self.angle_split[tho_j]
#                junk, P1, P2, P3, P4, P5, P6 = hsplit(line, 7)
#                line = self.speed_split[tho_j]
#                junk, S1, S2, S3, S4, S5, S6 = hsplit(line, 7) 
#                nachricht = self.nachricht_erstellen(P1, P2, P3, P4, P5, P6, \
#                S1, S2, S3, S4, S5, S6)
#                
#                'Nachricht an den Servocontroller senden'
#                self.nachricht_senden(nachricht)
#                
##                sleep(1) 
#                if tho_j == 0: sleep(self.t1)
##                TEST abs entfernen!!!!!!!!!!!!!!!!!!!!!    
#                if tho_j == 1: sleep(abs(self.t2-self.t1))                
#                if tho_j == 2:
#                    if self.t > self.t2:
#                        sleep(self.t)
            
#            print('Zeilenanzahl gesamt: ', zeilenzahl)
#            print('nr: ', nr)

            'nächstes Signal mit der gewählten Verzögerung senden'
            sleep(self.t)

            'Zählvariable um Eins erhöhen'
            nr += 1
            
            'Ausführschleife nach der letzten Position beenden'
            if nr == zeilenzahl:
                print('beende Thread')
                'Abbruchbedingung auf True setzen'
#                self.device.close()
                
                'Shield abschalten'
                self.shield_abschalten()
                
                'Verbindung beenden'
                self.device_schliessen()
               
                self.exiting = True
               
                'Signale finished und start_akt versenden'
                
                self.start_akt.emit()
                self.finished.emit()
                

    '''Methode - Aktiviert das Shield indem eine 11 ... Nachricht übertragen 
    wird'''
    def shield_start(self):
        
        'Ausführschleife der Methode servo_start abbrechen'
#        self.exiting = True
        
        'Halteposition abfragen'
#        P1st, P2st, P3st, P4st, P5st, P6st = self.position_abfragen()

        'Nachricht mit der Halteposition erstellen'
        nachricht = \
        '50 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an den Servocontroller senden'
        self.nachricht_senden(nachricht)   
        
        
        self.data = self.s.recv(26)
        self.antwort = self.data.decode('ascii')


        'Überprüfen, ob die Arduino Version aktzeptabel ist'
        self.Versionsnummer = int(self.antwort[:3])
        
        
        if self.Versionsnummer in self.stable_Ver:
            if self.Versionsnummer == self.stable_Ver[-1]:
                print('Arduino Version ist aktuell')
            elif self.Versionsnummer == 000:
                print
                print('-----Achtung-----')
                print
                print('Kein Arduino verbunden  ->  Nutze Testmodus')
            else:
                print('-----Achtung-----')                
                print('Arduino Version nicht aktuell')
                print('Bitte demnächst updaten')
                
            'Nachricht mit der Halteposition erstellen'
            nachricht = \
            '11 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
            
            'Nachricht an den Servocontroller senden'
            self.nachricht_senden(nachricht)
            
            sleep(1)
        else:
            print('-----WARNUNG-----')
            print("Version Arduino nicht kompatibel!")
            print()
            print('Kontaktieren Sie den Support')
            self.device_schliessen()
           
            self.exiting = True
           
            'Signale finished und start_akt versenden' 
            self.start_akt.emit()
            self.finished.emit()
        
        'Information ausgeben'
#        print(nachricht)


    '''Methode - Deaktiviert das Shield indem eine 12 ... Nachricht übertragen 
    wird'''        
    def shield_abschalten(self):
        
        'Ausführschleife der Methode servo_start abbrechen'
#        self.exiting = True
        
        'Halteposition abfragen'
#        P1st, P2st, P3st, P4st, P5st, P6st = self.position_abfragen()
        self.device_verbinden()       
        'Nachricht mit der Halteposition erstellen'
        nachricht = \
        '12 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an den Servocontroller senden'
        self.nachricht_senden(nachricht)
        
        sleep(1)
        
        'Information ausgeben'
#        print(nachricht)
                
    '''Methode steuerung_fern - Die Methode legt die Fernsteuerungs-
    parameter fest. Außerdem aktiviert sie die Fernsteuerung initial.'''
    def steuerung_fern(self):
        print("Fernsteuerung aktiv")
        
        
        'Methode device_verbinden aufrufen'
        self.device_verbinden()
        
        'Shield aktivieren'
        self.shield_start()
        
        'Ermittlung der x,y,z Kordinaten des Greifers in Ruheposition'
        self.x_end = 0
        self.y_end = 213.37
        self.z_end = 27.25
        
#        print('Antwort x = ')
#        pprint(self.x_end)
#        print('Antwort y = ')
#        pprint(self.y_end)
#        print('Antwort z = ')
#        pprint(self.z_end)
#        if self.x_end == 0: self.a_end = 3.1415
#        else: self.a_urs = atan((self.y_end/self.x_end)*3.1415)
#        self.a_end = asin(-self.y_end/sqrt(self.x_end*self.x_end+self.y_end*self.y_end))+pi
        self.a_end = asin(-self.x_end/sqrt(self.x_end*self.x_end+self.y_end*self.y_end))
        self.b_end = asin((self.z_end-27.25)/sqrt(self.z_end*self.z_end+self.y_end*self.y_end+self.x_end*self.x_end))-pi/2
#        self.g_end = 3.1415/2
        self.g_end = 0
        self.greif_end = 3.1415 / 2
        
        self.alteWinkel = [0, 90, 180, 0, 90, 90, 56]
        self.Spd_m = 2
        
        self.antwort = '0'

    '''Methode steuerung_fern_aus - Deaktiviert das Shield und zerstört den
    Motorthread.'''
    def steuerung_fern_aus(self):
        
        self.shield_abschalten()

        self.start_akt.emit()
        self.finished.emit()
        
    '''Methode steuerung_fern_vektor -
    p1, p2, p3, ist die Verschiebung im 3D Raum (x,y,z), sie bezieht sich auf
    das ursprunglische Kordinatensystem.
    p4 beeinflusst die Geschwindigkeit mit der verfahren wird.
    p5 kippt den Greifer relativ
    p6 öffnet oder schließt den Greifer    
    Methode steuerung_fern muss vorher ausgerührt werden.'''
    def steuerung_fern_vektor(self, x_ver, y_ver, z_ver, Spd_ver, b_ver, greif_ver, ):
#        print("Ankommender Vektor")
        
        self.zustand_anfragen()
        
        try:
#            print('Antwort verarbeitet')
#            print('Antwort: \t', self.antwort)
            p1, p2, p3, p4, p5, p6, junk = \
            self.antwort.split(' ')
            
            self.theta1_a = float((180 - int(p1)) * pi / 180)
            self.theta2_a = float(int(p2) * pi /180)
            self.theta3_a = float((int(p3) - 180 + 8) / 180 * pi)
            self.theta4_a = float((int(p4)-9) / 180 * pi)
            self.theta5_a = float(int(p5) * pi / 180)
#            print('Antwort Theta1: ', self.theta1_a)
#            print('Antwort Theta2: ', self.theta2_a)
#            print('Antwort Theta3: ', self.theta3_a)
#            print('Antwort Theta4: ', self.theta4_a)
#            print('Antwort Theta5: ', self.theta5_a)
            self.greif_urs = int(p6)
            
            
            self.alteWinkel = [0,int(p1),int(p2),int(p3),int(p4),int(p5),int(p6)]
            
            
            self.x5in0, self.y5in0, self.z5in0, self.P05in0 = kinematik_vor\
            (self.theta1_a, self.theta2_a, self.theta3_a, self.theta4_a, self.theta5_a)
#            self.x5in0 = vstack(self.x5in0, 0)
#            self.y5in0 = vstack(self.y5in0, 0)
#            self.z5in0 = vstack(self.z5in0, 0)
#            self.P05in0 = vstack(self.P05in0, 0)
#            theta1, theta2, theta3, theta4, theta5 = kinematik_inv(self.x5in0, self.y5in0, self.z5in0, self.P05in0)
#            
#            print('Antwort Theta1: ', theta1)
#            print('Antwort Theta2: ', theta2)
#            print('Antwort Theta3: ', theta3)
#            print('Antwort Theta4: ', theta4)
#            print('Antwort Theta5: ', theta5)
            
            
            self.x_urs = float(self.P05in0[0])
            self.y_urs = float(self.P05in0[1])
            self.z_urs = float(self.P05in0[2])         
            self.b_urs = asin(self.z5in0[2]/sqrt(self.x_urs*self.x_urs+self.y_urs*self.y_urs+self.z_urs*self.z_urs))-pi/2
#            print('Zwischen 0 und 3.1415: ', -asin(self.z5in0[2]))
#            print('Antwort x = ')
#            pprint(self.x5in0)
#            print('Antwort y = ')
#            pprint(self.y5in0)
#            print('Antwort z = ')
#            pprint(self.z5in0)
#            print('Antwort P = ')
#            pprint(self.P05in0)
            
        
        except ValueError:
            print('Antwort von Arduino ignoriert')            
            self.x_urs = self.x_end_n
            self.y_urs = self.y_end_n
            self.z_urs = self.z_end_n
            self.a_urs = self.a_end_n
            self.b_urs = self.b_end_n
    
#            Nicht nötig, da nicht verändert.
#            self.g_urs = self.g_end
            self.greif_urs = self.greif_end
            
            
        self.amplifier = 4
        
        self.x_end_n = self.x_urs + x_ver * self.amplifier
        self.y_end_n = self.y_urs + y_ver * self.amplifier
        self.z_end_n = self.z_urs + z_ver * self.amplifier
        
                
        if self.z_end_n < 45 and not 213 < self.y_end_n < 214:
            self.z_end_n = 45
        if self.y_end_n < 0:
            self.y_end_n = 0
        
        self.entfernung = sqrt(self.x_end_n * self.x_end_n + self.y_end_n * self.y_end_n + self.z_end_n * self.z_end_n)
        
        if self.entfernung > 530:
            self.x_end_n = self.x_end_n * 530 / self.entfernung
            self.y_end_n = self.y_end_n * 530 / self.entfernung            
            self.z_end_n = self.z_end_n * 530 / self.entfernung            
            
#        print('X_end: ', self.x_end)
#        print('Y_end: ', self.y_end)
#        print('Z_end: ', self.z_end)
        
#        if self.x_end == 0: self.a_end = 3.1415
#        else:

#        self.a_end = (asin(-self.y_end/sqrt(self.x_end*self.x_end+self.y_end*self.y_end)))+pi
        self.a_end_n = -(asin(self.x_end_n/sqrt(self.x_end_n*self.x_end_n+self.y_end_n*self.y_end_n)))
            
#        if self.x_end == 0: self.a_end = 3.1415
#        else: self.a_end = atan((self.y_end/self.x_end)*3.1415)
#        print('a_end: ',self.a_end)
            
        self.b_end_n = self.b_urs + b_ver / 180 * 3.1415
        
#        self.b_end = atan(around((self.z_end-31)/sqrt(self.y_end * self.y_end+\
#        self.x_end * self.x_end) * 3.1415 , 5)) \
#        + 3.1415/2
#        print('b_end: ', self.b_end)
        
#        Wird schon in Start initialisiert
#        self.g_end = self.g_urs
        
        self.Spd_m = self.Spd_m + Spd_ver
        
        self.greif_end = self.greif_urs + greif_ver * 1
        if self.greif_end < 10:
            self.greif_end = 10
        if self.greif_end > 140:
            self.greif_end = 140
        
        self.x5in0_n, self.y5in0_n, self.z5in0_n = \
        Eulertransformation(self.a_end_n, self.b_end_n, self.g_end)
#        print('Rechnet x = ')
#        pprint(self.x5in0_n)
#        print('Rechnet y = ')
#        pprint(self.y5in0_n)
#        print('Rechnet z = ')
#        pprint(self.z5in0_n)    

#        
        
#        print('x5in0:')
#        print(around(x5in0,3))
#        print('y5in0:')
#        print(around(y5in0,3))
#        print('z5in0:')
#        print(around(z5in0,3))
        self.P05_n = array([[self.x_end_n],[self.y_end_n],[self.z_end_n],[0]])
#        print('Rechnet P = ')
#        pprint(self.P05_n)
        
       
        self.theta1_n, self.theta2_n, self.theta3_n, self.theta4_n, self.theta5_n = kinematik_inv\
        (self.x5in0_n, self.y5in0_n, self.z5in0_n, self.P05_n )
        
#        print('Errechn Theta1: ',self.theta1_n)
#        print('Errechn Theta2: ',self.theta2_n)
#        print('Errechn Theta3: ',self.theta3_n)
#        print('Errechn Theta4: ',self.theta4_n)
#        print('Errechn Theta5: ',self.theta5_n)
        
        P1, P2, P3, P4, P5, P6 = self.ingrad_Echtzeit\
        (self.theta1_n, self.theta2_n, self.theta3_n, self.theta4_n, self.theta5_n, self.greif_end)        
        
        self.Geschwindigkeiten_ermitteln(P1, P2, P3, P4, P5, P6, self.Spd_m)
        
        self.speed_split = vsplit(self.speed, 3)
        line = self.speed_split[2]
        
        junk, S1, S2, S3, S4, S5, S6 = hsplit(line, 7) 
        
        S6 = 20
        
        'Nachricht mit den PWM-Signalen erstellen'
        nachricht = self.nachricht_erstellen(P1, P2, P3, P4, P5, P6, \
        S1, S2, S3, S4, S5, S6)
        
        self.nachricht_senden(nachricht)

        
    '''Methode steuerung_fern - Die Methode legt die Fernsteuerungs-
    parameter fest. Außerdem aktiviert sie die Fernsteuerung initial.'''
    def steuerung_fern_abs(self):
        print("Fernsteuerung aktiv")
        
        
        'Methode device_verbinden aufrufen'
        self.device_verbinden()
        
        'Shield aktivieren'
        self.shield_start()
        
        self.alteWinkel = [0, 90, 180, 0, 90, 90, 56]

    


    '''Methode steuerung_fern_vektor -
    Hierbei werden die Ziel-Motorwinkel übergeben.'''
    def steuerung_fern_abs_vektor(self, P1, P2, P3, P4, P5, P6):

        self.zustand_anfragen()
        
#        print('Antwort: \t', self.antwort)
        p1, p2, p3, p4, p5, p6, junk = \
        self.antwort.split(' ')
        
        self.Geschwindigkeiten_ermitteln(P1, P2, P3, P4, P5, P6, 10)
        
        self.speed_split = vsplit(self.speed, 3)
        line = self.speed_split[2]
        
        junk, S1, S2, S3, S4, S5, S6 = hsplit(line, 7)
        
        nachricht = self.nachricht_erstellen(P1, P2, P3, P4, P5, P6, \
        S1, S2, S3, S4, S5, S6)
        
        self.nachricht_senden(nachricht)        
        
        
    '''Methode steuerung_synchron - Die Methode legt die Zeit, die der 
    Roboter für die Bewegung zwischen zwei Punkten benötigt, fest. Die 
    Servomotoren werden synchron (alle Motoren werden gleichzeitig ge-
    startet und erreichen gleichzeitig das Ziel) bewegt. In Folge hängen 
    die Winkelgeschwindigkeiten der einzelnen Motoren vom Drehwinkel ab. 
    Die Zeit muss in jedem Fall über 1500ms liegen. Die Methode ist vor 
    dem Start der Motoren mit Methode servo_start aufzurufen.'''
    def steuerung_synchron(self, t):
        
        'Zeit in [ms]'
        self.t = t
        
        'TESTFUNKTION'
        self.t = 6
                
        
    '''G-Codes'''
    def steuerung_fern_g_code(self):
        'Methode device_verbinden aufrufen'
        self.device_verbinden()      
        'Shield aktivieren'
        self.shield_start()
        
        'Ermittlung der x,y,z Kordinaten des Greifers in Ruheposition'
        self.x_end = 0
        self.y_end = 213.37
        self.z_end = 27.25
        
        self.a_end = asin(-self.x_end/sqrt(self.x_end*self.x_end+self.y_end*self.y_end))
        self.b_end = asin((self.z_end-27.25)/sqrt(self.z_end*self.z_end+self.y_end*self.y_end+self.x_end*self.x_end))-pi/2

        self.g_end = 0
        self.greif_end = 3.1415 / 2
        
        self.alteWinkel = [0, 90, 180, 0, 90, 90, 56]
        self.Spd_m = 10
                    
        self.amplifier = 1
        
        self.antwort = '0'
        
    def steuerung_fern_g_code_off(self):
        self.shield_abschalten()
        'Terminierung des Threads'
        self.start_akt.emit()
        self.finished.emit()

    def steuerung_fern_g_code_move(self, x, y, z, spd):
#        print("Ankommender Vektor")
        
        self.zustand_anfragen()
        
        try:
#            print('Antwort verarbeitet')
#            print('Antwort: \t', self.antwort)
            p1, p2, p3, p4, p5, p6, junk = \
            self.antwort.split(' ')
            
            self.theta1_a = float((180 - int(p1)) * pi / 180)
            self.theta2_a = float(int(p2) * pi /180)
            self.theta3_a = float((int(p3) - 180 + 8) / 180 * pi)
            self.theta4_a = float((int(p4)-9) / 180 * pi)
            self.theta5_a = float(int(p5) * pi / 180)
            
            self.greif_urs = int(p6)
            
            
            self.alteWinkel = [0,int(p1),int(p2),int(p3),int(p4),int(p5),int(p6)]
            self.x5in0, self.y5in0, self.z5in0, self.P05in0 = kinematik_vor\
            (self.theta1_a, self.theta2_a, self.theta3_a, self.theta4_a, self.theta5_a)
            
            
            self.x_urs = float(self.P05in0[0])
            self.y_urs = float(self.P05in0[1])
            self.z_urs = float(self.P05in0[2])         
            self.b_urs = asin(self.z5in0[2]/sqrt(self.x_urs*self.x_urs+self.y_urs*self.y_urs+self.z_urs*self.z_urs))-pi/2
            
        
        except ValueError:
            print('Antwort ignoriert')            
            self.x_urs = self.x_end_n
            self.y_urs = self.y_end_n
            self.z_urs = self.z_end_n
            self.a_urs = self.a_end_n
            self.b_urs = self.b_end_n
    
            self.greif_urs = self.greif_end
            
        
        self.x_end_n = x * self.amplifier
        self.y_end_n = y * self.amplifier
        self.z_end_n = z * self.amplifier
        
                
        if(self.z_end_n)<0:
            self.z_end_n = 0
            
        self.a_end_n = -(asin(self.x_end_n/sqrt(self.x_end_n*self.x_end_n+self.y_end_n*self.y_end_n)))
            
            
        self.b_end_n = self.b_urs
        


        
        self.x5in0_n, self.y5in0_n, self.z5in0_n = \
        Eulertransformation(self.a_end_n, self.b_end_n, self.g_end)
#        print('Rechnet x = ')
#        pprint(self.x5in0_n)
#        print('Rechnet y = ')
#        pprint(self.y5in0_n)
#        print('Rechnet z = ')
#        pprint(self.z5in0_n)    


        self.P05_n = array([[self.x_end_n],[self.y_end_n],[self.z_end_n],[0]])
        print('Rechnet P = ')
        pprint(self.P05_n)
        
       
        self.theta1_n, self.theta2_n, self.theta3_n, self.theta4_n, self.theta5_n = kinematik_inv\
        (self.x5in0_n, self.y5in0_n, self.z5in0_n, self.P05_n )
        
        
        P1, P2, P3, P4, P5, P6 = self.ingrad_Echtzeit\
        (self.theta1_n, self.theta2_n, self.theta3_n, self.theta4_n, self.theta5_n, self.greif_end)        
        
        self.Geschwindigkeiten_ermitteln(P1, P2, P3, P4, P5, P6, spd)
        
        self.speed_split = vsplit(self.speed, 3)
        line = self.speed_split[2]
        
        junk, S1, S2, S3, S4, S5, S6 = hsplit(line, 7) 
        
        S6 = 20
        
        'Nachricht mit den PWM-Signalen erstellen'
        nachricht = self.nachricht_erstellen(P1, P2, P3, P4, P5, P6, \
        S1, S2, S3, S4, S5, S6)
        
        self.nachricht_senden(nachricht)
        
        
    def steuerung_fern_g_code_pause(self, t_pause):
        print(t_pause/1000)
        sleep(abs(t_pause/1000))
        
    def steuerung_fern_g_code_switch_inch(self):
        self.amplifier = 25.4
        
    def steuerung_fern_g_code_switch_mm(self):
        self.amplifier = 1
        
    def steuerung_fern_g_code_notaus(self):
        self.servo_stop()
        
    def steuerung_fern_g_code_aus(self):
        'Shield abschalten'
        self.shield_abschalten()
        
        'Verbindung beenden'
        self.device_schliessen()
       
        self.exiting = True
       
        'Signale finished und start_akt versenden'
        
        self.start_akt.emit()
        self.finished.emit()
        
    def steuerung_fern_g_code_start_programm(self, progwahl):
        
        self.programm_laden(progwahl)
        
        self.servo_start()
        
    def steuerung_fern_g_code_stop_programm(self):
        self.servo_stop()
        
        
    '''Frage die aktuellen Winkelposition des Arduino ab.'''                
    def zustand_anfragen(self):
        
        'Nachricht mit der Halteposition erstellen'
        nachricht = \
        '30 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an den Servocontroller senden'
        self.nachricht_senden(nachricht)
        
        
#        self.s.listen(antwort.encode('ascii'))
        self.data = self.s.recv(26)
        self.antwort = self.data.decode('ascii')
        return self.antwort