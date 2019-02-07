'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul rueckansicht_greifer enthält die Klasse RückansichtGreifer. Eine 
Animation ermöglicht die Rotation von Punkt6 um den Ursprung. Dabei kann 
der Radius verändert werden. Die Klasse wird von QObject abgeleitet. Das 
Signal xy_neu dient dem Übermitteln der veränderten Mittelpunktkoordinaten. 
Weiter wird das Klassenattribut lock definiert. In der Methode __init__ 
werden die Attribute und Methoden der Klasse QObject vererbt, die Zeichen-
fläche als Parent-Objekt zugewiesen, die Mittelpunktkoordinaten der Circle-
Objekte von kartesischen in Polarkoordinaten umgerechnet, die Grenzen der 
Bewegung festgelegt und die Circle-Objekte sowie Line2D-Objekte instanziiert.
Weitere Methoden der Klasse sind connect, on_press, on_motion, on_release, 
ansicht_aktualisieren, geisterstunde, modellrechnung und punkte_faerben.
'''

'Module importieren'
from berechnung.winkelnormierung import winkel_normieren
from berechnung.winkelberechnung import winkel_berechnen
from math import cos, pi, sin
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from PyQt4.QtCore import QObject, Signal

'Klasse RueckansichtGreifer'
class RueckansichtGreifer(QObject):
    
    'Signal definieren'
    xy_neu = Signal(float, float, float, float)
    
    'Klassenattribut lock definieren'
    lock = None
    
    'Methode __init__'
    def __init__(self, parent, xP6, yP6, xP7, yP7):
        
        'Vererbung aller Attribute und Methoden von QObject'
        super(RueckansichtGreifer, self).__init__(parent)
        
        'Parentobjekt - QPlotWidget'
        self.parent = parent

        'Umrechnung in Polarkoordinaten'
        self.modellrechnung(xP6, yP6, xP7, yP7)
        
        'Grenzradien festlegen'
        self.r_min = 100
        self.r_max = 200
        
        'Grenzwinkel festlegen'
        self.phi6_min = 0
        self.phi6_max = pi
        
        'Farben der Punkte und Linien festlegen'
        self.farbe_allgemein = 'black'
        self.farbe_punkt = '#5c061c'
        self.alpha_allgemein = 0.5
        self.alpha_geist = 0.25
        
        'Punktradius, Linienstärke und Linienende festlegen'
        self.radius_punkt = 55
        self.staerke_linie = 20
        self.ende_linie = 'round'
        
        'Circle-Objekte instanziieren'
        
        'Punkt6 instanziieren'
        self.point6 = Circle((self.xP6, self.yP6))
        self.point6.set_radius(self.radius_punkt)
        self.point6.set_facecolor(self.farbe_allgemein)
        self.point6.set_alpha(self.alpha_allgemein)
        self.parent.axes.add_patch(self.point6)
        
        'Punkt7 instanziieren'
        self.point7 = Circle((self.xP7, self.yP7))
        self.point7.set_radius(self.radius_punkt)
        self.point7.set_facecolor(self.farbe_allgemein)
        self.point7.set_alpha(self.alpha_allgemein)
        self.parent.axes.add_patch(self.point7)
        
        self.point = self.point6
        
        'Line2D-Objekte instanziieren'
        
        'Endpunktkoordinaten von Linie1'
        #Linie1 - verbindet den Ursprung mit Punkt6
        self.xL1 = (0, self.xP6)
        self.yL1 = (0, self.yP6)
        
        'Linie1 instanziieren'
        self.line1 = Line2D(self.xL1, self.yL1)
        self.line1.set_linewidth(self.staerke_linie)
        self.line1.set_color(self.farbe_allgemein)
        self.line1.set_alpha(self.alpha_allgemein)
        self.line1.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line1)
        
        'Endpunktkoordinaten von Linie2'
        #Linie1 - verbindet den Ursprung mit Punkt7
        self.xL2 = (0, self.xP7)
        self.yL2 = (0, self.yP7)
        
        'Linie2 instanziieren'
        self.line2 = Line2D(self.xL2, self.yL2)
        self.line2.set_linewidth(self.staerke_linie)
        self.line2.set_color(self.farbe_allgemein)
        self.line2.set_alpha(self.alpha_allgemein)
        self.line2.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line2)

        'Geisterpunktobjekte instanziieren'
        
        'Geisterpunkt6 instanziieren'
        self.pointG6 = Circle((self.xP6, self.yP6))
        self.pointG6.set_radius(self.radius_punkt)
        self.pointG6.set_facecolor(self.farbe_punkt)
        self.pointG6.set_alpha(self.alpha_geist)
        self.parent.axes.add_patch(self.pointG6)
        self.pointG6.set_visible(False)
        
        'Geisterpunkt7 instanziieren'
        self.pointG7 = Circle((self.xP7, self.yP7))
        self.pointG7.set_radius(self.radius_punkt)
        self.pointG7.set_facecolor(self.farbe_allgemein)
        self.pointG7.set_alpha(self.alpha_geist)
        self.parent.axes.add_patch(self.pointG7)
        self.pointG7.set_visible(False)
        
        'Geisterlinienobjekte instanziieren'
        
        'Geisterlinie1 instanziieren'
        self.lineG1 = Line2D(self.xL1, self.yL1)
        self.lineG1.set_linewidth(self.staerke_linie)
        self.lineG1.set_color(self.farbe_allgemein)
        self.lineG1.set_alpha(self.alpha_geist)
        self.lineG1.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.lineG1)
        self.lineG1.set_visible(False)
        
        'Geisterlinie2 instanziieren'
        self.lineG2 = Line2D(self.xL2, self.yL2)
        self.lineG2.set_linewidth(self.staerke_linie)
        self.lineG2.set_color(self.farbe_allgemein)
        self.lineG2.set_alpha(self.alpha_geist)
        self.lineG2.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.lineG2)
        self.lineG2.set_visible(False)
        
        'Attribut self.press'
        self.press = None
        
        'Attribut self.background'
        self.background = None
        
        'Aufruf der Methode connect'
        self.connect()
    
    '''Methode connect - Die Methode dient dem Verbinden der Events mit den
    entsprechenden Methoden. Beim Drücken der linken Maustaste, dem button_
    press_event, wird die Methode on_press ausgeführt. Weiter führt das 
    Loslassen der linken Maustaste, dem button_release_event, zum Ausführen 
    der Methode on_release. Zuletzt wird bei der Bewegung der Maus, dem 
    motion_notify_event, die Methode on_motion aufgerufen. Vorraussetzung 
    für ein Event ist das Drücken oder Loslassen der linken Maustaste auf 
    oder das Bewegen der Maus über die Zeichenfläche.'''
    def connect(self):
        
        'Verbindet das button_press_event mit der Methode on_press'
        self.cidpress = self.point.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
            
        'Verbindet das button_release_event mit der Methode on_release'
        self.cidrelease = self.point.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
            
        'Verbindet das motion_notify_event mit der Methode on_motion'
        self.cidmotion = self.point.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)
    
    '''Methode on_press - Die Methode on_press wird beim Drücken der linken
    Maustaste auf der Zeichenfläche ausgeführt.'''
    def on_press(self, event):
        
        '''Die Methode wird weiter ausgeführt wenn der Mauszeiger 
        zum Zeitpunkt des Drückens der linken Maustaste innerhalb des 
        Koordinatensystems liegt.'''
        if event.inaxes != self.point.axes: return
        
        '''Die Methode wird weiter ausgeführt wenn vor dem Drücken der 
        linken Maustaste kein Circle-Objekt ausgewählt ist.'''
        if RueckansichtGreifer.lock is not None: return
        contains, attrd = self.point.contains(event)
        
        '''Die Methode wird weiter ausgeführt wenn der Mauszeiger zum
        Zeitpunkt des Drückens der linken Maustaste auf dem bewegbaren
        Circle-Objekt liegt.'''
        if not contains: return
        
        '''Den Mittelpunkt des Circle-Objektes und die x- und y-Koordinaten
        des Mauszeigers zum Zeitpunkt des Drückens der linken Maustaste
        speichern.'''
        self.press = self.point.center, event.xdata, event.ydata
             
        'Das Klassenattribut mit dem Wert self belegen.'
        RueckansichtGreifer.lock = self
        
        'Sichtbarkeit des Geistes ändern'
        self.pointG6.set_visible(True)
        self.pointG7.set_visible(True)
        self.lineG1.set_visible(True)
        self.lineG2.set_visible(True)
        
        'Methoden der Animation-Blit-Technik ausführen'
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point6.set_animated(True)
        self.point7.set_animated(True)
        self.line1.set_animated(True)
        self.line2.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)
        axes.draw_artist(self.point6)
        axes.draw_artist(self.point7)
        axes.draw_artist(self.line1)
        axes.draw_artist(self.line2)
        canvas.blit(axes.bbox)
    
    '''Methode on_motion - Die Methode on_motion wird beim Bewegen des
    Mauszeigers über die Zeichenfläche ausgeführt.'''
    def on_motion(self, event): 
        
        '''Die Methode wird weiter ausgeführt wenn das Klassenattribut 
        mit dem Wert self belegt ist. Das Circle-Objekt darf ohne angeklickt 
        zu sein nicht bewegt werden.'''
        if RueckansichtGreifer.lock is not self: return
            
        '''Die Methode wird weiter ausgeführt wenn der Mauszeiger 
        innerhalb des Koordinatensystems bewegt wird.'''
        if event.inaxes != self.point.axes: return
        
        '''Den Mittelpunkt des Circle-Objektes und die x- und y-Koordinaten
        des Mauszeigers zum Zeitpunkt des Drückens der linken Maustaste
        zuweisen.'''
        self.point.center, xpress, ypress = self.press
        
        'Radien aller Circle-Objekte neu berechnen'
        
        'Verschiebung von Punkt6 in x- und y-Richtung'
        dx = event.xdata - xpress
        dy = event.ydata - ypress
          
        'neue Koordinaten berechnen'
        x_neu = self.point.center[0] + dx
        y_neu = self.point.center[1] + dy
        
        'neuen Radius berechnen'
        r_neu = (x_neu**2 + y_neu**2)**(1/2)
        
        'Radiusbegrenzung [r_min, r_max]'
        if r_neu <= self.r_min:
            r_neu = self.r_min
        elif r_neu >= self.r_max:
            r_neu = self.r_max
        
        'Radien aktualisieren'
        self.r6 = r_neu
        self.r7 = self.r6
        
        'Winkel aller Circle-Objekte neu berechnen'
        
        'Winkel berechnen - Kreismittelpunkt'
        phi = winkel_berechnen(self.point.center[0], self.point.center[1])
                
        'Winkel berechnen - Mauszeiger beim Anklicken des Punktes'
        phi_p = winkel_berechnen(xpress, ypress)
        
        'Winkel berechnen - Mauszeiger bei der Bewegung'
        phi_e = winkel_berechnen(event.xdata, event.ydata)
        
        'Winkeländerung berechnen'
        dphi = phi_e - phi_p
        
        'neuen Positionswinkel berechnen'
        phi_neu = phi + dphi
        
        'Winkel auf [0, 2*pi] normieren um Rundungsfehler auszugleichen'
        phi_neu = winkel_normieren(phi_neu)
        
        'Winkel von Punkt6 aktualisieren'
        self.phi6 = phi_neu
            
        'Winkelbegrenzung [phi_min, phi_max]'
        if self.phi6 < self.phi6_min or self.phi6 > 3*pi/2 and \
        self.phi6 < 2*pi:
            self.phi6 = self.phi6_min
        elif self.phi6 > self.phi6_max and self.phi6 < 3*pi/2:
            self.phi6 = self.phi6_max
                
        'Winkel von Punkt7 aktualisieren'
        self.phi7 = self.phi6 + pi

        'Winkel auf [0, 2*pi] normieren um Rundungsfehler auszugleichen'                    
        self.phi7 = winkel_normieren(self.phi7)
        
        'Theta5 (Denavit-Hartenberg-Parameter) aktualisieren'
        self.theta5 = pi - self.phi6
    
        'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
        'Koordinaten von Punkt6'
        self.xP6 = self.r6*cos(self.phi6)
        self.yP6 = self.r6*sin(self.phi6)
        'Koordinaten akualisieren'
        self.point6.center = ((self.xP6, self.yP6))
        
        'Koordinaten von Punkt7'
        self.xP7 = self.r7*cos(self.phi7)
        self.yP7 = self.r7*sin(self.phi7)
        'Koordinaten akualisieren'
        self.point7.center = ((self.xP7, self.yP7))
                 
        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Linie1'
        self.xL1 = (0, self.xP6)
        self.yL1 = (0, self.yP6)
        'Koordinaten akualisieren'
        self.line1.set_data(self.xL1, self.yL1)
        
        'Koordinaten von Linie2'
        self.xL2 = (0, self.xP7)
        self.yL2 = (0, self.yP7)
        'Koordinaten akualisieren'
        self.line2.set_data(self.xL2, self.yL2)
        
        'Methoden der Animation-Blit-Technik ausführen'
        canvas = self.point.figure.canvas
        axes = self.point.axes
        canvas.restore_region(self.background)
        axes.draw_artist(self.point6)
        axes.draw_artist(self.point7)
        axes.draw_artist(self.line1)
        axes.draw_artist(self.line2)
        canvas.blit(axes.bbox)
        
        'Signal mit den neuen Koordinaten senden'
        self.xy_neu.emit(self.xP6, self.yP6, self.xP7, self.yP7)
        
    '''Methode on_release - Die Methode on_release wird beim Loslassen
    der linken Maustaste auf der Zeichenfläche ausgeführt.'''
    def on_release(self, event):
        
        '''Die Methode wird weiter ausgeführt wenn das Klassenattribut 
        mit dem Wert self belegt ist.'''
        if RueckansichtGreifer.lock is not self: return

        'Werte der Attribute zurücksetzen'
        self.press = None
        RueckansichtGreifer.lock = None
            
        'Attribute auf False setzen'
        self.point6.set_animated(False)
        self.point7.set_animated(False)
        self.line1.set_animated(False)
        self.line2.set_animated(False)
        
        'Hintergrund zurücksetzen'
        self.background = None
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
        
    '''Methode ansicht_aktualisieren - Die Methode ermöglicht das
    Aktualisieren der Ansicht.'''
    def ansicht_aktualisieren(self, xP6, yP6, xP7, yP7):
        
        'Umrechnung in Polarkoordinaten'
        self.modellrechnung(xP6, yP6, xP7, yP7)
                
        'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
        'Koordinaten von Punkt6 aktualisieren'
        self.point6.center = ((self.xP6, self.yP6))
        
        'Koordinaten von Punkt7 aktualisieren'
        self.point7.center = ((self.xP7, self.yP7))
                
        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Linie1'
        self.xL1 = (0, self.xP6)
        self.yL1 = (0, self.yP6)
        'Koordinaten aktualisieren'
        self.line1.set_data(self.xL1, self.yL1)
        
        'Koordinaten von Linie2'
        self.xL2 = (0, self.xP7)
        self.yL2 = (0, self.yP7)
        'Koordinaten aktualisieren'
        self.line2.set_data(self.xL2, self.yL2)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
        
    '''Methode geisterstunde - Die Methode dient dem Ein- oder Ausblenden
    des Geistes. Weiter werden die Koordinaten aktualisiert.'''
    def geisterstunde(self, b):
        
        'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
        'Koordinaten von Geisterpunkt6'
        xGp6 = self.point6.center[0]
        yGp6 = self.point6.center[1]
        'Koordinaten aktualisieren'
        self.pointG6.center = (xGp6, yGp6)
        
        'Koordinaten von Geisterpunkt7'
        xGp7 = self.point7.center[0]
        yGp7 = self.point7.center[1]
        'Koordinaten aktualisieren'
        self.pointG7.center = (xGp7, yGp7)
        
        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Geisterlinie1'
        xGl1 = (0, self.xP6)
        yGl1 = (0, self.yP6)
        'Koordinaten aktualisieren'
        self.lineG1.set_data(xGl1, yGl1)
        
        'Koordinaten von Geisterlinie2'
        xGl2 = (0, self.xP7)
        yGl2 = (0, self.yP7)
        'Koordinaten aktualisieren'
        self.lineG2.set_data(xGl2, yGl2)
        
        'Sichtbarkeit des Geistes ändern'
        #Sichtbarkeit ändern - True oder False
        self.pointG6.set_visible(b)
        self.pointG7.set_visible(b)
        self.lineG1.set_visible(b)
        self.lineG2.set_visible(b)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
    
    '''Methode modellrechnung - Die Methode rechnet die kartesischen
    Mittelpunktkoordinaten in Polarkoordinaten um.'''
    def modellrechnung(self, xP6, yP6, xP7, yP7):
    
        'Kartesische Koordinaten'
        
        'Punkt6 und Punkt7'
        self.xP6 = xP6
        self.yP6 = yP6
        self.xP7 = xP7
        self.yP7 = yP7
        
        'Polarkoordinaten'
        
        'Radien von Punkt6 und Punkt7'
        self.r6 = ((self.xP6)**2 + (self.yP6)**2)**(1/2)
        self.r7 = self.r6
        
        'Winkel im Intervall [0, 2*pi]'
        
        'Winkel von Punkt6 berechnen'
        self.phi6 = winkel_berechnen(self.xP6, self.yP6)
        
        'Winkel von Punkt7 berechnen'
        self.phi7 = self.phi6 + pi
        
        'Winkel theta5 (Denavit-Hartenberg-Parameter) berechnen'
        self.theta5 = pi - self.phi6
        
    '''Methode punkte_faerben - Die Methode färbt oder entfärbt den 
    bewegbaren Punkt6.'''
    def punkte_faerben(self, b):
        
        'Fallunterscheidung'
        if b == True: #Farbe
            farbe = self.farbe_punkt
        elif b == False: #Schwarz
            farbe = self.farbe_allgemein
            
        'Farbe von Punkt6 festlegen'            
        self.point6.set_facecolor(farbe)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()