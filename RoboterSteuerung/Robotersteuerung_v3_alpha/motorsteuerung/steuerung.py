'''
Autor: Martin Schinnerl
Datum: 25.09.2016

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
from math import pi
from numpy import array, hsplit, hstack, load, vsplit, vstack
from os import getcwd, path
from PyQt4.QtCore import QObject, Signal
from serial import Serial
from time import sleep

'Klasse Motor'
class Motor(QObject):
    
    'Signale definieren'
    finished = Signal()
    start_akt = Signal()
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QObject'
        super(Motor, self).__init__(parent)
        
        'Attribut zum Beenden der Ausführschleife definieren'
        self.exiting = False
        
        'Vorrangegangene Winkel'
        self.winkel_nMinus1 = [0, 0, 0, 0, 0, 0, 0]
    
    '''Methode device_verbinden - Die Methode dient dem 
    Instanziieren eines Serial-Objektes.'''
    def device_verbinden(self):
        
        'Serial-Objekt instanziieren'
        self.device = Serial()
        'Port festlegen'
        self.device.port = '/dev/ttyACM0'
        'Baudrate festlegen'
        self.device.baudrate = 115200  
        'Timeout festlegen'
        self.device.timeout = 1
        'serielle Schnittstelle öffnen'
        self.device.open()
        
    '''Methode fortsetzen - Roboter auf Startposition fahren.'''
    def fortsetzen(self):
        
        'Ist-Motorwinkel abfragen'
        P1, P2, P3, P4, P5, P6 = self.motorwinkel_abfragen()
        
        'Ermittlung der nötigen Geschwindigkeiten' 
        S1, S2, S3, S4, S5, S6, t = self.geschwindigkeiten_ermitteln(P1, \
        P2, P3, P4, P5, P6, 10)
                
        'Nachricht mit den PWM-Signalen und Geschwindigkeiten erstellen'
        nachricht = self.nachricht_erstellen(P1, P2, P3, P4, P5, P6, \
        S1, S2, S3, S4, S5, S6)
        
        'Nachricht an Arduino senden'
        self.nachricht_senden(nachricht)
        
        'nächstes Signal mit der gewählten Verzögerung senden'
        sleep(t)
            
        'Shield ausschalten'
        self.shield_ausschalten()
        
        'Signale finished und start_akt versenden'
        self.finished.emit()                
        self.start_akt.emit()
        
    '''Methode geschwindigkeit ermitteln - Ermittelt jeweils die 
    Geschwindigkeit von einem alten Punkt zu einem neuen / übergebenen Punkt. 
    v_max gibt an, was die maximale Geschwindigkeit ist, welche angenommen 
    werden soll. Die Geschwindigkeiten werden so gewählt, dass alle Motoren 
    ihre Position nahezu gleichzeitig erreichen.'''
    def geschwindigkeiten_ermitteln(self, P1, P2, P3, P4, P5, P6, v_max):
        
        'Geschwindigkeitsbegrenzung zwischen 1 und 10 Zwetschgenknödel'
        if v_max > 10: v_max = 10
        if v_max < 0: v_max = 1
        
        'Variablen definieren'
        winkel_nMinus1 = self.winkel_nMinus1
        winkel_neu = array([0, P1, P2, P3, P4, P5, P6])
        
        'Winkeldifferenzen der Achsen berechnen'
        winkel_diff = abs(winkel_nMinus1 - winkel_neu)
        
        'Maximale Winkeldifferenz finden'
        max_winkel_diff = max(winkel_diff)
        if max_winkel_diff == 0: max_winkel_diff == 1
        
        'Variable aktualisieren'
        winkel_nMinus1 = winkel_neu
        
        'Geschwindigkeiten der Achsen berechnen'
        v = winkel_diff/max_winkel_diff*v_max
        S0, S1, S2, S3, S4, S5, S6 = hsplit(v, 7)
        
        'Datentyp ändern'
        S0 = float(S0)
        S1 = float(S1)
        S2 = float(S2)
        S3 = float(S3)
        S4 = float(S4)
        S5 = float(S5)
        S6 = float(S6)
        
        'Zeit nachdem das nächste Signal gesendet wird'
        t = max_winkel_diff / 3.3 / v_max

        return S1, S2, S3, S4, S5, S6, t
        
    '''Methode ingrad - Die Methode transformiert die Winkel 
    (Denavit-Hartenberg-Parameter) und den Öffnungsradius des Greifers 
    von rad in Grad.'''
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
            pwm1 = 180 - int(theta1/pi*180)
            pwm2 = int(theta2/pi*180)
            pwm3 = 180 + int(theta3/pi*180) - 8
            pwm4 = int(theta4/pi*180) + 9
            pwm5 = int(theta5/pi*180)
            
            if pwm4 < 0: pwm4 = 0
            if pwm5 > 180: pwm5 = 180
            
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
            pwm6 = int(0 - (112 / (200 - 100)*(r6 - 200)))
            if pwm6 < 0 : pwm6 == 0
                
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
    
    '''Methode motorwinkel_abfragen - Abfrage der Ist-Motorwinkel.
    Nachricht: 30 ...'''                
    def motorwinkel_abfragen(self):
        
        'Nachricht erstellen'
        nachricht = \
        '30 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an Arduino senden'
        self.nachricht_senden(nachricht)
        
        'Antwort vom Arduino lesen'
        antwort_raw = self.device.readline()
        motorwinkel_ist = str(antwort_raw[:-2].decode())
        P1, P2, P3, P4, P5, P6 = motorwinkel_ist.split(' ')

        'Datentyp str in float konvertieren'
        P1 = float(P1)
        P2 = float(P2)
        P3 = float(P3)
        P4 = float(P4)
        P5 = float(P5)
        P6 = float(P6)
        
#        P1, P2, P3, P4, P5, P6 = 100, 100, 100, 100, 100, 100 ###
        return P1, P2, P3, P4, P5, P6
        
    '''Methode nachrichten_erstellen - Die Methode baut aus 6 Winkelangaben 
    einen String der Form XX XXX XX.XX XXX XX.XX ... . Vor der Methode 
    müssen die Winkel in Grad umgewandelt werden.'''
    def nachricht_erstellen(self, P1, P2, P3, P4, P5, P6, \
    S1, S2, S3, S4, S5, S6):
        
        winkel = [0, P1, P2, P3, P4, P5, P6]
        speed = [0, S1, S2, S3, S4, S5, S6]
        
        nachricht = ''
        tho_i = 1
        nachricht += '00'
        
        for tho_i in range(1,7):
            
            akt_winkel = float(winkel[tho_i])
            nachricht += ' '
            
            if akt_winkel < 0:
                print('Winkel ', tho_i, ' ist negativ')
                
            if akt_winkel == 0 or akt_winkel < 0:
                nachricht += '000'
                
            elif akt_winkel < 100:
                
                if akt_winkel < 10:
                    nachricht += '00' + str(int(round(akt_winkel, 0)))
                    
                if int(winkel[tho_i]) > 9:
                    nachricht += '0' + str(int(round(akt_winkel, 0)))

            elif int(winkel[tho_i]) > 99:
                
                if int(winkel[tho_i]) > 180:
                    nachricht += '180'
                else:
                    nachricht += str(int(round(akt_winkel, 0)))
                
            nachricht += ' '
            
            speed_a = float(speed[tho_i]) 
            
            if int(speed[tho_i]) == 0 or int(speed[tho_i]) < 0:
                nachricht += '00.0'
                
            elif int(speed[tho_i]) < 10:
                nachricht += '0' + \
                str("{0:.1f}".format(round(speed_a, 1)))

            elif int(speed[tho_i]) >= 10:
                
                if int(speed[tho_i]) >= 30:
                    nachricht += '30.0'
                else:
                    nachricht += str("{0:.1f}".format(round(speed_a, 1)))

        return nachricht
        
    '''Methode nachricht_senden - Die Methode übermittelt Signale mit den 
    Methoden des Serial-Objektes in Form von Nachrichten (Datentyp: str) 
    an den Servocontroller. Vor dem Aufruf der Methode muss ein Serial-
    Objekt erzeugt werden (Methode device_verbinden).'''
    def nachricht_senden(self, nachricht):

        'Nachricht an den Servocontroller senden'
        self.device.write(nachricht.encode('ascii'))
        
        'Information ausgeben'
        print(nachricht)
        
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
                          
        'Nachricht mit der Halteposition erstellen'
        nachricht = \
        '20 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an den Servocontroller senden'
        self.nachricht_senden(nachricht)
        
    '''Methode servo_start - Die Methode startet die Servomotoren
    des Roboters. Voraussetzung sind das Laden eines Programmes und 
    der Aufruf der Methode steuerung_synchron. Innerhalb der Methode 
    servo_start werden die Methode device_verbinden sowie die Methode 
    modulation aufgerufen. Danach werden die vom Roboter anzufahrenden 
    Positionen der Reihe nach an den Servocontroller übermittelt. Die 
    Funktion kann durch Aufruf der Methode servo_stop beendet werden.'''
    def servo_start(self): 
        
        'serielle Verbindung herstellen'        
        self.device_verbinden()
        
        'Zählvariable definieren'
        nr = 0
        
        'Methode ingrad aufrufen'
        self.ingrad()
        
        'Shield aktivieren'
        self.shield_einschalten()
        
        'Ausführschleife zum Durchlaufen der PWM-Matrix'
        while not self.exiting:
            
            'Format der PWM-Matrix abfragen'
            #Format: nx6 mit n-Zeilen
            zeilenzahl, spaltenzahl = self.pwm.shape
            
            'Matrix in Zeilen teilen'
            zeilen = vsplit(self.pwm, zeilenzahl)
            
            'Zeile_nr auswählen'
            zeile = zeilen[nr]
            
            'Spalteneinträge den Kanälen zuordnen'
            P1, P2, P3, P4, P5, P6 = hsplit(zeile, spaltenzahl)
            
            'Ermittlung der nötigen Geschwindigkeiten'            
            S1, S2, S3, S4, S5, S6, t = self.geschwindigkeiten_ermitteln(P1, \
            P2, P3, P4, P5, P6, 10)
            
            'Nachricht mit den PWM-Signalen und Geschwindigkeiten erstellen'
            nachricht = self.nachricht_erstellen(P1, P2, P3, P4, P5, P6, \
            S1, S2, S3, S4, S5, S6)

            'Nachricht an Arduino senden'
            self.nachricht_senden(nachricht)
            
            'nächstes Signal mit der gewählten Verzögerung senden'
            sleep(t)

            'Zählvariable um Eins erhöhen'
            nr += 1
            
            'Ausführschleife nach der letzten Position beenden'
            if nr == zeilenzahl:
                
                'Shield abschalten'
                self.shield_ausschalten()
        
                'Abbruchbedingung auf True setzen'
                self.exiting = True
            
                'Signale finished und start_akt versenden'
                self.finished.emit()                
                self.start_akt.emit()
    
    '''Methode shield_ausschalten - Schaltet das Servoshield aus.
    Nachricht: 12 ... Ruheposition.'''
    def shield_ausschalten(self):
            
        'Nachricht mit der Halteposition erstellen'
        nachricht = \
        '12 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an Arduino senden'
        self.nachricht_senden(nachricht)
        
        'serielle Verbindung schließen'
        self.device.close()
        
    '''Methode shield_einschalten - Schalted das Servoshield ein.
    Nachricht: 11 ... Ruheposition.'''
    def shield_einschalten(self):
        
        'Nachricht mit der Halteposition erstellen'
        nachricht = \
        '11 090 00.0 090 00.0 090 00.0 090 00.0 110 00.0 130 00.0'
        
        'Nachricht an Arduino senden'
        self.nachricht_senden(nachricht)
        
    '''Methode steuerung_fern_abs_vektor - Übergabe der Ziel-Motorwinkel'''
    def steuerung_fern_abs_vektor(self, P1, P2, P3, P4, P5, P6):
        
        'serielle Schnittstelle öffnen'
        self.device_verbinden()
        
        'Shield einschalten'
        self.shield_einschalten()
        
        'Ist-Motorwinkel abfragen'
        P1, P2, P3, P4, P5, P6 = self.motorwinkel_abfragen()
        
        'Ermittlung der nötigen Geschwindigkeiten' 
        S1, S2, S3, S4, S5, S6, t = self.geschwindigkeiten_ermitteln(P1, \
        P2, P3, P4, P5, P6, 10)
                
        'Nachricht mit den PWM-Signalen und Geschwindigkeiten erstellen'
        nachricht = self.nachricht_erstellen(P1, P2, P3, P4, P5, P6, \
        S1, S2, S3, S4, S5, S6)
        
        'Nachricht an Arduino senden'
        self.nachricht_senden(nachricht)
    
    '''Methode steuerung_fern_aus'''
    def steuerung_fern_aus(self):
        
        'Shield abschalten'
        self.shield_ausschalten()
        
        'Signale finished und start_akt versenden'
        self.finished.emit()                
        self.start_akt.emit()
        
