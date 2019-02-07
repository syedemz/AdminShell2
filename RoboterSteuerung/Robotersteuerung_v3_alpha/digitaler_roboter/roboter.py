'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul roboter enthält die Klasse DigitalerRoboter. Bei dem digitalen
Roboter handelt es sich um ein vereinfachtes Abbild des Originals in drei 
Ansichten. Circle-Objekte stellen die Gelenke und Line 2D-Objekte die Teile
des Roboters sowie des Greifers dar. Der digitale Roboter kann bewegt werden.
Dazu werden die Objekte als Ansichten in eigene Klassen ausgelagert und mit
der Animation-Blit-Technik animiert. Die Klasse DigitalerRoboter wird von
der Klasse QWidget abgeleitet. Weiter werden die beiden Signale animation_
aktiv und koordinaten definiert. Das erste Signal wird beim Bewegen des 
digitalen Roboters gesendet. Das zweite Signal übermittelt veränderte 
Lagekoordinaten des Werkzeugkoordinatensystems. Im Code-Block der Methode 
__init__ werden neben der Vererbung der Attribute und Methoden der Basis-
klasse QWidget, drei Zeichenflächen mit Koordinatensystem instanziiert, 
die Mittelpunktkoordinaten der Circle-Objekte in der Ausgangsposition der
Roboters berechnet und die Methode zum Anzeigen des digitalen Roboters 
aufgerufen. Weitere Methoden der Klasse sind animation_aktivieren, 
animation_aktualisieren, animation_zuruecksetzen, ansicht_wechseln, 
bilder_aufnehmen, greifer_laden, koordinaten, koordinaten_draufsicht, 
koordinaten_greifer, koordiniaten_seitenansicht, koordinaten_abfragen, 
lage_berechnen, modellrechnung, orientierung_laden und lage_laden.
'''

'Module importieren'
from berechnung.parameter import denavit_hartenberg
from berechnung.transformationen import A01, A02, A03, A04, \
A05, A12, A13, A14, A15, A45, kinematik_inv, kinematik_vor
from grafische_benutzungsoberflaeche.grafikelemente import QPlotWidget
from math import cos, pi, sin
from numpy import around, array, dot, hstack, load, hsplit, vsplit, vstack
from os import getcwd, path
from PyQt4.QtCore import Signal
from PyQt4.QtGui import QHBoxLayout, QStackedWidget, QWidget
from digitaler_roboter.ansicht.draufsicht_roboter import DraufsichtRoboter
from digitaler_roboter.ansicht.seitenansicht_roboter import  \
SeitenansichtRoboter
from digitaler_roboter.ansicht.rueckansicht_greifer import RueckansichtGreifer

'Klasse DigitalerRoboter'
class DigitalerRoboter(QWidget):
    
    'Signale definieren'
    signal_animation_aktiv = Signal(bool)
    signal_koordinaten = Signal(int, int, int)
    
    'Methode __init__ '
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QWidget'
        super(DigitalerRoboter, self).__init__(parent)
        
        'Zeichenflächen mit Koordinatensystem instanziieren'        
        
        'Hintergrundfarbe der Zeichenflächen festlegen'
        farbe_zeichenflaeche = '#b5afb5'
        
        'Zeichenfläche mit Koordinatensystem instanziieren - Draufsicht'
        self.zeichenflaeche_draufsicht = QPlotWidget()
        
        #Hintergrundfarbe festlegen
        self.zeichenflaeche_draufsicht.figure.set_facecolor( \
        farbe_zeichenflaeche)
        
        #Koordinatensystem an die Zeichenfläche anpassen
        self.zeichenflaeche_draufsicht.figure.tight_layout()
        
        #gleiche Skalierung der Achsen des Koordinatensystems
        self.zeichenflaeche_draufsicht.axes.set_aspect('equal')
        
        #Grenzen des Koordinatensystems festlegen
        self.zeichenflaeche_draufsicht.axes.set_xlim([-650, 650])
        self.zeichenflaeche_draufsicht.axes.set_ylim([-225, 625]) 
        
        #Achsen des Koordinatensystems und Beschriftung ausblenden
        self.zeichenflaeche_draufsicht.axes.axis('off')
        
        #Zeichenfläche deaktivieren
        self.zeichenflaeche_draufsicht.setEnabled(False)
        
        'Zeichenfläche mit Koordinatensystem instanziieren - Seitenansicht'
        self.zeichenflaeche_seitenansicht = QPlotWidget()
        
        #Hintergrundfarbe festlegen
        self.zeichenflaeche_seitenansicht.figure.set_facecolor( \
        farbe_zeichenflaeche)
        
        #Koordinatensystem an die Zeichenfläche anpassen
        self.zeichenflaeche_seitenansicht.figure.tight_layout()
        
        #gleiche Skalierung der Achsen des Koordinatensystems
        self.zeichenflaeche_seitenansicht.axes.set_aspect('equal')
        
        #Grenzen des Koordinatensystems festlegen
        self.zeichenflaeche_seitenansicht.axes.set_xlim(-250, 650)
        self.zeichenflaeche_seitenansicht.axes.set_ylim([-225, 625])
        
        #Achsen des Koordinatensystems und Beschriftung ausblenden
        self.zeichenflaeche_seitenansicht.axes.axis('off')
        
        #Zeichenfläche deaktivieren
        self.zeichenflaeche_seitenansicht.setEnabled(False)
          
        'Zeichenfläche mit Koordinatensystem instanziieren - Greifer'
        self.zeichenflaeche_ansicht_greifer = QPlotWidget()
        
        #Hintergrundfarbe festlegen
        self.zeichenflaeche_ansicht_greifer.figure.set_facecolor( \
        farbe_zeichenflaeche)
        
        #Koordinatensystem an die Zeichenfläche anpassen
        self.zeichenflaeche_ansicht_greifer.figure.tight_layout()
        
        #gleiche Skalierung der Achsen des Koordinatensystems
        self.zeichenflaeche_ansicht_greifer.axes.set_aspect('equal')
        
        #Grenzen des Koordinatensystems festlegen
        self.zeichenflaeche_ansicht_greifer.axes.set_xlim([-350, 350])
        self.zeichenflaeche_ansicht_greifer.axes.set_ylim([-350, 350])
        
        #Achsen des Koordinatensystems und Beschriftung ausblenden
        self.zeichenflaeche_ansicht_greifer.axes.axis('off')
        
        #Zeichenfläche deaktivieren
        self.zeichenflaeche_ansicht_greifer.setEnabled(False)
        
        '''Die Zeichenflächen werden gestapelt, da immer nur eine
        Ansicht angezeigt werden kann.'''
        
        'QStackedWidget-Objekt instanziieren'
        self.ansicht = QStackedWidget()
        #Draufischt: CurrentIndex(0)
        self.ansicht.addWidget(self.zeichenflaeche_draufsicht)
        #Seitenansicht: CurrentIndex(1)
        self.ansicht.addWidget(self.zeichenflaeche_seitenansicht)
        #Greifer: CurrentIndex(2)
        self.ansicht.addWidget(self.zeichenflaeche_ansicht_greifer)
        
        'Layout festlegen'
        layout = QHBoxLayout()
        layout.addWidget(self.ansicht)
        self.setLayout(layout)
        
        '''Lage und Orientierung des Werkzeugkoordinatensystem sowie die
        Öffnungsradien des Greifers in Ausgangsposition laden'''
        
        'Denavit-Hartenberg-Parameter laden'
        (d1, d2, d3, d4, d5, a1, a2, a3, a4, a5, \
        alpha1, alpha2, alpha3, alpha4, alpha5) = denavit_hartenberg()
        self.a3 = a3
        
        'Orientierung des Werkzeugkoordinatensystems laden'
        self.x5in0, self.y5in0, self.z5in0 = \
        self.orientierung_laden('programmEin')
        
        'Lagevektor des Werkzeugkoordinatensystems laden'
        self.P05in0 = self.lage_laden('programmEin')
        
        'Öffnungsradien des Greifers laden'
        self.r6, self.r7 = self.greifer_laden('programmEin')
        
        'Mittelpunktkoordinaten der Punkte berechnen'
        self.modellrechnung()
      
        'Methode animation_anzeigen aufrufen'
        self.animation_anzeigen()
    
    '''Methode animation_anzeigen - Die Methode dient dem Instanziieren
    der drei Ansichten. Jeder Animation wird die entsprechenden Zeichen-
    fläche als Parent und die Mittelpunktkoordinaten der Circle-Objekte
    übergeben. Weiter werden die Signale mit den Slots verbunden.'''
    def animation_anzeigen(self):
        
        'DraufsichtRoboter-Objekt instanziieren'
        self.animation_draufsicht = DraufsichtRoboter( \
        self.zeichenflaeche_draufsicht, \
        self.xP1in0, self.yP1in0, self.xP2in0, self.yP2in0, \
        self.xP4in0, self.yP4in0, self.xP5in0, self.yP5in0)
        
        'Signal und Slot verbinden'
        self.animation_draufsicht.xy_neu.connect( \
        self.koordinaten_draufsicht)

        'SeitenansichtRoboter-Objekt instanziieren'
        self.animation_seitenansicht = SeitenansichtRoboter( \
        self.zeichenflaeche_seitenansicht, \
        self.xP1in1, self.yP1in1, self.xP2in1, self.yP2in1, self.xP3in1, \
        self.yP3in1, self.xP4in1, self.yP4in1, self.xP5in1, self.yP5in1)
        
        'Signal und Slot verbinden'
        self.animation_seitenansicht.xy_neu.connect( \
        self.koordinaten_seitenansicht)
        
        'RueckansichtGreifer-Objekt instanziieren'
        self.animation_greifer = RueckansichtGreifer( \
        self.zeichenflaeche_ansicht_greifer, \
        self.xP6in4z, self.yP6in4z, self.xP7in4z, self.yP7in4z)
        
        'Signal und Slot verbinden'
        self.animation_greifer.xy_neu.connect( \
        self.koordinaten_greifer)        
    
    '''Methode animation_aktivieren - Die Methode aktiviert die Zeichen-
    flächen. In Folge kann der digitale Roboter durch Verschieben der 
    Punkte bewegt werden. Die bewegbaren Punkte erscheinen in Farbe.'''
    def animation_aktivieren(self, b):
        
        'Zeichenflächen aktivieren'
        self.zeichenflaeche_draufsicht.setEnabled(b)
        self.zeichenflaeche_seitenansicht.setEnabled(b)
        self.zeichenflaeche_ansicht_greifer.setEnabled(b)
        
        'Einfärben der bewegbaren Punkte'
        self.animation_draufsicht.punkte_faerben(b)
        self.animation_seitenansicht.punkte_faerben(b)
        self.animation_greifer.punkte_faerben(b)

    '''Methode animation_aktualisieren - Die Methode ermöglicht das
    Aktualisieren des digitalen Roboters. Dabei sind die Lage (Zeilenvektor
    vom Format 1x3) und Orientierung (Zeilenvektor Format 1x9) des Werkzeug-
    koordinatensystems in 0-Koordinaten sowie der Öffnungsradius des Greifers 
    (Zeilenvektor vom Format 1x1) zu übergeben.'''
    def animation_aktualisieren(self, orientierung, lage, greifer): 
        
        'Orientierung des Werkzeugkoordinatensystems'
        
        'Einheitsvektoren zuordnen'
        x5in0, y5in0, z5in0 = hsplit(orientierung, 3) #Format 1x3
        
        'Format anpassen'
        x5in0 = x5in0.transpose() #Format 3x1
        self.x5in0 = vstack((x5in0, array([[0]]))) #Format 4x1
        y5in0 = y5in0.transpose() #Format 3x1
        self.y5in0 = vstack((y5in0, array([[0]]))) #Format 4x1
        z5in0 = z5in0.transpose() #Format 3x1
        self.z5in0 = vstack((z5in0, array([[0]]))) #Format 4x1
        
        'Lage des Werkzeugkoordinatensystems'
        
        'Lagevektor zuordnen und Format anpassen'
        P05in0 = lage #Format 1x3
        P05in0 = P05in0.transpose() #Format 3x1
        self.P05in0 = vstack((P05in0, array([[1]]))) #Format 4x1
        
        'Öffnungsradien des Greifers zuordnen und Datentyp ändern'
        self.r6 = float(greifer)
        self.r7 = self.r6

        'Mittelpunktkoordinaten der Circle-Objekte berechnen'
        self.modellrechnung()
        
        'Draufsicht aktualisieren'
        self.animation_draufsicht.ansicht_aktualisieren( \
        self.xP2in0, self.yP2in0, self.xP4in0, \
        self.yP4in0, self.xP5in0, self.yP5in0)
        
        'Seitenansicht aktualisieren'
        self.animation_seitenansicht.ansicht_aktualisieren(
        self.xP2in1, self.yP2in1, self.xP3in1, self.yP3in1, \
        self.xP4in1, self.yP4in1, self.xP5in1, self.yP5in1)
        
        'Greifer aktualisieren'
        self.animation_greifer.ansicht_aktualisieren( \
        self.xP6in4z, self.yP6in4z, self.xP7in4z, self.yP7in4z)
        
        'Lagekoordinaten des Werkzeugkoordinatensystems'
        x5in0 = int(self.xP5in0)
        y5in0 = int(self.yP5in0)
        z5in0 = int(self.zP5in0)
        
        'Signal zum Aktualisieren der Lagekoordinaten senden'
        self.signal_koordinaten.emit(x5in0, y5in0, z5in0)
        
    '''Methode animation_zuruecksetzen - Die Methode setzt den digitalen 
    Roboter auf die Ausgangsposition zurück. Weiter werden die Bewegungs-
    möglichkeit deaktiviert und die Punkte entfärbt.'''
    def animation_zuruecksetzen(self, b):
        
        if b == True:
            
            'Orientierung des Werkzeugkoordinatensystems laden'
            self.x5in0, self.y5in0, self.z5in0 = self.orientierung_laden( \
            'programmEin')
            
            'Lagevektor des Werkzeugkoordinatensystems laden'
            self.P05in0 = self.lage_laden('programmEin')
            
            'Öffnungsradien des Greifers laden'
            self.r6, self.r7 = self.greifer_laden('programmEin')
            
            'Mittelpunktkoordinaten der Punkte berechnen'
            self.modellrechnung()
            
            'Draufsicht aktualisieren'
            self.animation_draufsicht.ansicht_aktualisieren( \
            self.xP2in0, self.yP2in0, self.xP4in0, \
            self.yP4in0, self.xP5in0, self.yP5in0)
            
            'Seitenansicht aktualisieren'
            self.animation_seitenansicht.ansicht_aktualisieren(
            self.xP2in1, self.yP2in1, self.xP3in1, self.yP3in1, \
            self.xP4in1, self.yP4in1, self.xP5in1, self.yP5in1)
            
            'Greifer aktualisieren'
            self.animation_greifer.ansicht_aktualisieren( \
            self.xP6in4z, self.yP6in4z, self.xP7in4z, self.yP7in4z)
            
            'Geist ausblenden und Koordinaten aktualisieren'            
            self.geisterstunde(False)
            
            'Entfärben der bewegbaren Punkte'
            self.animation_draufsicht.punkte_faerben(False)
            self.animation_seitenansicht.punkte_faerben(False)
            self.animation_greifer.punkte_faerben(False)
            
            'Lagekoordinaten des Werkzeugkoordinatensystems'
            x5in0 = int(self.xP5in0)
            y5in0 = int(self.yP5in0)
            z5in0 = int(self.zP5in0)
            
            'Signal zum Aktualisieren der Lagekoordinaten senden'
            self.signal_koordinaten.emit(x5in0, y5in0, z5in0)

    '''Methode ansicht_wechseln - Die Methode ermöglicht den Wechsel 
    zwischen den drei Ansichten.'''
    def ansicht_wechseln(self, index):
        
        self.ansicht.setCurrentIndex(index)
        
    '''Methode bilder_aufnehmen - Die Methode ermöglicht die Aufnahme und
    das Abspeichern von Bildern der Drauf- und Seitenansicht.'''
    def bilder_aufnehmen(self):
        
        'Ansichten zentrieren'
        self.zeichenflaeche_draufsicht.axes.set_xlim([-625, 625])
        self.zeichenflaeche_draufsicht.axes.set_ylim([-325, 525])       
        self.zeichenflaeche_seitenansicht.axes.set_xlim(-525, 725)
        self.zeichenflaeche_seitenansicht.axes.set_ylim([-325, 525])
        
        'Arbeitsverzeichnis'
        workdir = getcwd()
        
        'Dateiname und Pfad'
        dateiname = 'bild_draufsicht.svg'
        dir = path.join(workdir, 'speicher', 'bildspeicher', dateiname)
        
        'Draufsicht als Bild speichern'
        self.zeichenflaeche_draufsicht.figure.savefig(dir, \
        dpi = 1200, facecolor = self.farbe_zeichenflaeche)
        
        'Dateiname und Pfad'
        dateiname = 'bild_seitenansicht.svg'
        dir = path.join(workdir, 'speicher', 'bildspeicher', dateiname)
        
        'Seitenansicht als Bild speichern'
        self.zeichenflaeche_seitenansicht.figure.savefig(dir, \
        dpi = 1200, facecolor = self.farbe_zeichenflaeche)
    
    '''Methode geisterstunde - Bei der Bewegung des digitalen Roboters wird
    die zuletzt gespeicherte Position als Schatten eingeblendet. Die Methode
    ermöglicht das Ein- oder Ausblenden des Geistes.'''
    def geisterstunde(self, b):
        
        self.animation_draufsicht.geisterstunde(b)
        self.animation_seitenansicht.geisterstunde(b)
        self.animation_greifer.geisterstunde(b)
        
    '''Methode greifer_laden - Die Methode lädt den Öffnungsradius des
    Greifers (Zeilenvektor vom Format 1x1) und gibt diesen als Gleit-
    kommazahl zurück. Da sich der Greifer synchron öffnet und schließt 
    sind die Radien von Punkt6 und Punkt 7 gleich.'''
    def greifer_laden(self, name):
        
        'Arbeitsverzeichnis'
        workdir = getcwd()
        
        'Dateiname und Pfad'
        dateiname = name + '_greifer.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', dateiname)
        
        'Öffnungsradius laden'
        greifer = load(dir)
        
        'Datentyp ändern'
        r6 = float(greifer)
        r7 = r6
        
        return r6, r7    
    
    '''Methode koordinaten - Die Methode zerlegt einen Spaltenvektor 
    in die Koordinaten und gibt diese als Gleitkommazahl zurück.'''
    def koordinaten(self, r):
        
        'Format des Vektors'
        zeilenzahl, spaltenzahl = r.shape
        
        'Vektor in Zeilen zerlegen'
        zeilen = vsplit(r, zeilenzahl)
        
        'Koordinaten zuordnen'
        x = float(zeilen[0])
        y = float(zeilen[1])
        z = float(zeilen[2])
        
        return x, y, z
    
    '''Methode koordinaten_draufsicht - Die Bewegung des digitalen 
    Roboters ändert die x0,y0-Koordinaten der Punkte 2, 4 und 5. Diese 
    werden der Methode übergeben. Die z0-Koordinaten der Punkte 2, 4 und 5, 
    die 1-Koordinaten der Punkte 2, 3, 4, und 5 sowie die die 4z-Koordinaten 
    der Punkte 6 und 7 bleiben unverändert. In Folge sind die x0,y0-Koord-
    inaten der drei Punkte und der Winkel theta1 zu aktualisieren sowie die 
    von theta1 abhängigen Transformationsvorschriften und die 0-Koordinaten 
    von Punkt3 neu zu berechnen.'''
    def koordinaten_draufsicht(self, xP2, yP2, xP4, yP4, xP5, yP5):
        
        'Mittelpunktkoordinaten aktualisieren'
        self.xP2in0 = xP2
        self.yP2in0 = yP2
        self.xP4in0 = xP4
        self.yP4in0 = yP4
        self.xP5in0 = xP5
        self.yP5in0 = yP5
        
        'Theta1 (Denavit-Hartenberg-Parameter) aktualisieren'
        self.theta1 = self.animation_draufsicht.theta1
        
        'Transformation = f(theta1)'
        
        'Neuberechnung der Transformtionsmatrizen Aij'
        self.A01 = A01(self.theta1)
        self.A02 = A02(self.theta1, self.theta2)
        self.A03 = A03(self.theta1, self.theta2, self.theta3)
        self.A04 = A04(self.theta1, self.theta2, self.theta3, self.theta4)
        self.A05 = A05(self.theta1, self.theta2, self.theta3, self.theta4, \
        self.theta5)
        
        'Neuberechnung der Mittelpunktkoordinaten'
        
        'Ortsvektor von Punkt3'
        #in 1-Koordinaten
        rP3in1 = array([[self.xP3in1], [self.yP3in1], [self.zP3in1], [1]])
        #in 0-Koordinaten
        rP3in0 = around(dot(self.A01, rP3in1), 3)

        'Koordinaten von Punkt3'
        #in 0-Koordinaten
        self.xP3in0, self.yP3in0, self.zP3in0 = self.koordinaten(rP3in0)

        'Lagekoordinaten des Werkzeugkoordinatensystems'
        x5in0 = int(self.xP5in0)
        y5in0 = int(self.yP5in0)
        z5in0 = int(self.zP5in0)
        
        'Signal zum Aktualisieren der Lagekoordinaten senden'
        self.signal_koordinaten.emit(x5in0, y5in0, z5in0)
        
        'Signal, das die Bewegung des digitalen Roboters signalisiert, senden'
        self.signal_animation_aktiv.emit(True)
    
    '''Methode koordinaten_greifer - Die Bewegung des Greifers ändert 
    die x4z,y4z-Koordinaten der Punkte 6 und 7. Diese werden der Methode 
    übergeben. Die 4z-Koordinaten der Punkte 6 und 7 bleiben unverändert. 
    In Folge sind die x4z,y4z-Koordinaten der beiden Punkte und der Winkel 
    theta5 zu aktualisieren sowie die von theta5 abhängigen Transformations-
    vorschriften neu zu berechnen.'''
    def koordinaten_greifer(self, xP6in4z, yP6in4z, xP7in4z, yP7in4z):
        
        'Mittelpunktkoordinaten aktualisieren'
        self.xP6in4z = xP6in4z
        self.yP6in4z = yP6in4z
        self.xP7in4z = xP7in4z
        self.yP7in4z = yP7in4z
        
        'Theta5 (Denavit-Hartenberg-Parameter) aktualisieren'
        self.theta5 = self.animation_greifer.theta5
        
        'Radien aktualisieren'
        self.r6 = self.animation_greifer.r6
        self.r7 = self.r6
        
        'Transformation = f(theta5)'
        
        'Neuberechnung der Transformtionsmatrizen Aij'
        self.A05 = A05(self.theta1, self.theta2, self.theta3, self.theta4, \
        self.theta5)
        
        self.A15 = A15(self.theta2, self.theta3, self.theta4, self.theta5)
        
        self.A45 = A45(self.theta5)

        'Signal, das die Bewegung des digitalen Roboters signalisiert, senden'
        self.signal_animation_aktiv.emit(True)
        
    '''Methode koordinaten_seitenansicht - Die Bewegung des digitalen 
    Roboters ändert die x1,y1-Koordinaten der Punkte 2, 3, 4, und 5. Diese 
    werden der Methode übergeben. Die z1-Koordinaten der Punkte 2, 3, 4 und
    5 und die 4z-Koordinaten der Punkte 6 und 7 bleiben erhalten. In Folge 
    sind die x1,y1-Koordinaten der vier Punkte und die Winkel theta2, theta3 
    und theta4 zu aktualisieren sowie die von den Winkeln abhängigen 
    Transformationsvorschriften und die 0-Koordinaten der vier Punkte neu
    zu berechnen.'''
    def koordinaten_seitenansicht(self, xP2in1, yP2in1, xP3in1, yP3in1, \
    xP4in1, yP4in1, xP5in1, yP5in1):
        
        'Mittelpunktkoordinaten aktualisieren'
        self.xP2in1 = xP2in1
        self.yP2in1 = yP2in1
        self.xP3in1 = xP3in1
        self.yP3in1 = yP3in1
        self.xP4in1 = xP4in1
        self.yP4in1 = yP4in1
        self.xP5in1 = xP5in1
        self.yP5in1 = yP5in1
        
        'Theta2, Theta3 und Theta4 (Denavit-Hartenberg-P.) aktualisieren'
        self.theta2 = self.animation_seitenansicht.theta2
        self.theta3 = self.animation_seitenansicht.theta3
        self.theta4 = self.animation_seitenansicht.theta4
        
        'Transformation = f(theta2, theta3, theta4)'        
        
        'Neuberechnung der Transformationsmatrizen Aij'
        self.A02 = A02(self.theta1, self.theta2)
        self.A03 = A03(self.theta1, self.theta2, self.theta3)
        self.A04 = A04(self.theta1, self.theta2, self.theta3, self.theta4)
        self.A05 = A05(self.theta1, self.theta2, self.theta3, self.theta4, \
        self.theta5)
        
        self.A12 = A12(self.theta2)
        self.A13 = A13(self.theta2, self.theta3)
        self.A14 = A14(self.theta2, self.theta3, self.theta4)
        self.A15 = A15(self.theta2, self.theta3, self.theta4, self.theta5)
        
        'Neuberechnung der Mittelpunktkoordinaten'
        
        'Ortsvektor von Punkt2' 
        #in 1-Koordinaten
        rP2in1 = array([[self.xP2in1], [self.yP2in1], [self.zP2in1], [1]])
        #in 0-Koordinaten
        rP2in0 = around(dot(self.A01, rP2in1), 3)
        
        'Ortsvektor von Punkt3'
        #in 1-Koordinaten
        rP3in1 = array([[self.xP3in1], [self.yP3in1], [self.zP3in1], [1]])
        #in 0-Koordinaten
        rP3in0 = around(dot(self.A01, rP3in1), 3)
        
        'Ortsvektor von Punkt4'
        #in 1-Koordinaten
        rP4in1 = array([[self.xP4in1], [self.yP4in1], [self.zP4in1], [1]])
        #in 0-Koordinaten
        rP4in0 = around(dot(self.A01, rP4in1), 3)
        
        'Ortsvektor von Punkt5'
        #in 1-Koordinaten
        rP5in1 = array([[self.xP5in1], [self.yP5in1], [self.zP5in1], [1]])
        #in 0-Koordinaten
        rP5in0 = around(dot(self.A01, rP5in1), 3)
        
        'Koordinaten von Punkt2'
        #in 0-Koordinaten
        self.xP2in0, self.yP2in0, self.zP2in0 = self.koordinaten(rP2in0)
        
        'Koordinaten von Punkt3'
        #in 0-Koordinaten
        self.xP3in0, self.yP3in0, self.zP3in0 = self.koordinaten(rP3in0)
        
        'Koordinaten von Punkt4'
        #in 0-Koordinaten
        self.xP4in0, self.yP4in0, self.zP4in0 = self.koordinaten(rP4in0)
        
        'Koordinaten von Punkt5'
        #in 0-Koordinaten
        self.xP5in0, self.yP5in0, self.zP5in0 = self.koordinaten(rP5in0)

        'Bewegungen des digitalen Roboters synchronisieren'
        self.animation_draufsicht.pointG2.set_visible(True)
        self.animation_draufsicht.pointG4.set_visible(True)
        self.animation_draufsicht.pointG5.set_visible(True)
        self.animation_draufsicht.lineG1.set_visible(True)
        self.animation_draufsicht.lineG2.set_visible(True)
        self.animation_draufsicht.lineG3.set_visible(True)
        
        'Draufsicht aktualisieren'
        self.animation_draufsicht.ansicht_aktualisieren( \
        self.xP2in0, self.yP2in0, self.xP4in0, \
        self.yP4in0, self.xP5in0, self.yP5in0)
        
        'Lagekoordinaten des Werkzeugkoordinatensystems'
        x5in0 = int(self.xP5in0)
        y5in0 = int(self.yP5in0)
        z5in0 = int(self.zP5in0)
        
        'Signal zum Aktualisieren der Lagekoordinaten senden'
        self.signal_koordinaten.emit(x5in0, y5in0, z5in0)
        
        'Signal, das die Bewegung des digitalen Roboters signalisiert, senden'
        self.signal_animation_aktiv.emit(True)

    '''Methode koordinaten_abfragen - Die Methode gibt die aktuellen 
    Lagekoordinaten des Werkzeugkoordinatensystems zurück.'''
    def koordinaten_abfragen(self):
        
        xP5in0 = self.xP5in0
        yP5in0 = self.yP5in0
        zP5in0 = self.zP5in0
        
        return xP5in0, yP5in0, zP5in0
        
    '''Methode lage_berechnen - Die Methode gibt die Lage (Zeilenvektor 
    vom Format 1x3) und Orientierung (Zeilenvektor vom Format 1x9) des
    Werkzeugkoordinatensystems in 0-Koordinaten, die Winkel (Denavit-
    Hartenberg-Parameter) (Zeilenvektor vom Format 1x5) und den 
    Öffnungsradius des Greifers (Zeilenvektor vom Format 1x1) zurück.'''
    def lage_berechnen(self):
        
        'Geist ausblenden'
        self.geisterstunde(False)
        
        '''Kinematische Vorwärtstransformation zur Berechnung von Lage
        und Orientierung des Werkzeugkoordinatensystems in 0-Koordinaten.
        Die Vektoren werden im Format 3x1 zurückgegeben.'''
        x5in0, y5in0, z5in0, P05in0 = kinematik_vor(self.theta1, \
        self.theta2, self.theta3, self.theta4, self.theta5)
        
        'Orientierung des Werkzeugkoordinatensystems'
        
        'Format der Einheitsvektoren anpassen'
        x5in0 = x5in0.transpose() #Format 1x3
        y5in0 = y5in0.transpose() #Format 1x3
        z5in0 = z5in0.transpose() #Format 1x3
        
        'Orientierungsvektor erstellen'
        orientierung = hstack((x5in0, y5in0, z5in0)) #Format 1x9
        orientierung = around(orientierung, 3)
        
        'Lage des Werkzeugkoordinatensystems'
        
        'Format des Lagevektors anpassen und Vektor zuweisen'
        lage = P05in0.transpose() #Format 1x3
        lage = around(lage, 3)
        
        'Winkelvektor erstellen'
        winkel = array([[self.theta1, self.theta2, \
        self.theta3, self.theta4, self.theta5]]) #Format 1x5
        winkel = around(winkel, 3)
        
        'Öffnungsradius des Greifers'
        greifer = array([[self.r6]]) #Format 1x1
        
        return orientierung, lage, winkel, greifer
        
    '''Methode modellrechnung - Die Methode berechnet aus der Lage und 
    Orientierung des Werkzeugkoordinatensystems in 0-Koordinaten sowie 
    dem Öffnungsradius des Greifers die Mittelpunktkoordinaten der Circle-
    Objekte. Insgesamt gibt es sieben Circle-Objekte und drei Ansichten. Die 
    Draufsicht ist die Projektion des digitalen Roboters auf die x0,y0-Ebene. 
    Dargestellt werden Punkt1, Punkt2, Punkt4 und Punkt5. Die Seitenansicht 
    ist die Projektion des digitalen Roboters auf die x1,y1-Ebene. Dargestellt 
    werden Punkt1, Punkt2, Punkt3, Punkt4 und Punkt5. Die Ansicht des Greifers
    ist die Projektion auf eine Zeichenebene parallel zur x4,y4-Ebene.
    Dargestellt werden Punkt6 und Punkt7. Während die Mittelpunktkoordinaten
    von Punkt6 und Punkt 7 nur in Zeichenkoordinaten berechnet werden, werden
    die Koordinaten der Punkte 1 bis 5 auch in 0-Koordinaten berechnet.'''
    def modellrechnung(self):
        
        '''Kinematische Rückwärtstransformation zur Berechnung der 
        Winkel (Denavit-Hartenberg-Parameter) bei gegebener Lage und
        Orientierung des Werkzeugkoordinatensystems'''
        theta = kinematik_inv(self.x5in0, self.y5in0, self.z5in0, self.P05in0)
        
        'Drehwinkel zuordnen'
        self.theta1 = theta[0]
        self.theta2 = theta[1]
        self.theta3 = theta[2]
        self.theta4 = theta[3]
        self.theta5 = theta[4]
        
        'Transformationsmatrizen Aij zur Überführung von Ki in Kj'
        self.A01 = A01(self.theta1)
        self.A02 = A02(self.theta1, self.theta2)
        self.A03 = A03(self.theta1, self.theta2, self.theta3)
        self.A04 = A04(self.theta1, self.theta2, self.theta3, self.theta4)
        self.A05 = A05(self.theta1, self.theta2, self.theta3, self.theta4, \
        self.theta5)
        
        self.A12 = A12(self.theta2)
        self.A13 = A13(self.theta2, self.theta3)
        self.A14 = A14(self.theta2, self.theta3, self.theta4)
        self.A15 = A15(self.theta2, self.theta3, self.theta4, self.theta5)
        
        self.A45 = A45(self.theta5)

        'Ortsvektor von Punkt2'
        #in 2-Koordinaten
        rP2in2 = array([[0], [0], [0], [1]])
        #in 1-Koordinaten
        rP2in1 = around(dot(self.A12, rP2in2), 3)
        #in 0-Koordinaten
        rP2in0 = around(dot(self.A02, rP2in2), 3)
        
        'Ortsvektor von Punkt3'
        l = self.a3*(cos(8*pi/180) - sin(8*pi/180))
        #in 3-Koordinaten
        rP3in3 = array([[-l*cos(8*pi/180)], [l*sin(8*pi/180)], [0], [1]])
        #in 1-Koordinaten
        rP3in1 = around(dot(self.A13, rP3in3), 3)
        #in 0-Koordinaten
        rP3in0 = around(dot(self.A03, rP3in3), 3)
        
        'Ortsvektor von Punk4'
        #in 4-Koordinaten
        rP4in4 = array([[0], [0], [0], [1]])
        #in 1-Koordinaten
        rP4in1 = around(dot(self.A14, rP4in4), 3)
        #in 0-Koordinaten
        rP4in0 = around(dot(self.A04, rP4in4), 3)
        
        'Ortsvektor von Punk5'
        #in 5-Koordinaten
        rP5in5 = array([[0], [0], [0], [1]])
        #in 1-Koordinaten
        rP5in1 = around(dot(self.A15, rP5in5), 3)
        #in 0-Koordinaten
        rP5in0 = self.P05in0
        
        phi6 = pi - self.theta5
        phi7 = phi6 + pi

        'Ortsvektor von Punkt6'
        #in 4z-Koordinaten
        rP6in4z = array([[self.r6*cos(phi6)], [self.r6*sin(phi6)], [0], [1]])
        
        'Ortsvektor von Punkt7'
        #in 4z-Koordinaten
        rP7in4z = array([[self.r7*cos(phi7)], [self.r7*sin(phi7)], [0], [1]])        
    
        'Koordinaten von Punkt1'
        #in 1-Koordinaten
        self.xP1in1, self.yP1in1, self.zP1in1 = (0, 0, 0)
        #in 0-Koordinaten
        self.xP1in0, self.yP1in0, self.zP1in0 = (0, 0, 0)
        
        'Koordinaten von Punkt2'
        #in 1-Koordinaten
        self.xP2in1, self.yP2in1, self.zP2in1 = self.koordinaten(rP2in1)
        #in 0-Koordinaten
        self.xP2in0, self.yP2in0, self.zP2in0 = self.koordinaten(rP2in0)
        
        'Koordinaten von Punkt3'
        #in 1-Koordinaten
        self.xP3in1, self.yP3in1, self.zP3in1 = self.koordinaten(rP3in1)
        #in 0-Koordinaten
        self.xP3in0, self.yP3in0, self.zP3in0 = self.koordinaten(rP3in0)
        
        'Koordinaten von Punkt4'
        #in 1-Koordinaten
        self.xP4in1, self.yP4in1, self.zP4in1 = self.koordinaten(rP4in1)
        #in 0-Koordinaten
        self.xP4in0, self.yP4in0, self.zP4in0 = self.koordinaten(rP4in0)
        
        'Koordinaten von Punkt5'
        #in 1-Koordinaten
        self.xP5in1, self.yP5in1, self.zP5in1 = self.koordinaten(rP5in1)
        #in 0-Koordinaten
        self.xP5in0, self.yP5in0, self.zP5in0 = self.koordinaten(rP5in0)
        
        'Zeichenkoordinaten von Punkt6'
        #in 4z-Koordinaten
        self.xP6in4z, self.yP6in4z, self.zP6in4z = self.koordinaten(rP6in4z)
        
        'Zeichenkoordinaten von Punkt7'
        #in 4z-Koordinaten
        self.xP7in4z, self.yP7in4z, self.zP7in4z = self.koordinaten(rP7in4z)
        
    '''Methode orientierung_laden - Die Methode lädt die Orientierung des
    Werkzeugkoordinatensystems in 0-Koordinaten (Zeilenvektor vom Format 
    1x9) und gibt die Einheitsvektoren des Werkzeugkoordinatensystems als 
    Spaltenvektoren vom Format 4x1 zurück.'''
    def orientierung_laden(self, name):
        
        'Arbeitsverzeichnis'
        workdir = getcwd()
        
        'Dateiname und Pfad'
        dateiname = name + '_orientierung.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', dateiname)
        
        'Orientierung laden'
        orientierung = load(dir)
        
        'Einheitsvektoren zuordnen'
        x5in0, y5in0, z5in0 = hsplit(orientierung, 3) #Format 1x3
        
        'Format anpassen'
        x5in0 = x5in0.transpose() #Format 3x1
        x5in0 = vstack((x5in0, array([[0]]))) #Format 4x1
        y5in0 = y5in0.transpose() #Format 3x1
        y5in0 = vstack((y5in0, array([[0]]))) #Format 4x1
        z5in0 = z5in0.transpose() #Format 3x1
        z5in0 = vstack((z5in0, array([[0]]))) #Format 4x1
        
        return x5in0, y5in0, z5in0
        
    '''Methode lage_laden - Die Methode lädt den Lagevektor des
    Werkzeugkoordinatensystems in 0-Koordinaten (Zeilenvektor vom Format 
    1x3) und gibt diese als Spaltenvektor vom Format 4x1 zurück.'''
    def lage_laden(self, name):
        
        'Arbeitsverzeichnis'
        workdir = getcwd()
        
        'Dateiname und Pfad'
        dateiname = name + '_lage.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', dateiname)
        
        'Lagevektor laden'        
        lage = load(dir)
        
        'Format anpassen'
        P05in0 = lage #Format 1x3
        P05in0 = P05in0.transpose() #Format 3x1
        P05in0 = vstack((P05in0, array([[1]]))) #Format 4x1
        
        return P05in0