'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul draufsicht_roboter enthält die Klasse DraufsichtRoboter. Eine
Animation ermöglicht die Rotation von Punkt4 um den Ursprung. Die Klasse 
wird von QObject abgeleitet. Das Signal xy_neu dient dem Übermitteln 
der veränderten Mittelpunktkoordinaten. Weiter wird das Klassenattribut
lock definiert. In der Methode __init__ werden die Attribute und Methoden
der Klasse QObject vererbt, die Zeichenfläche als Parent-Objekt zugewiesen,
die Mittelpunktkoordinaten der Circle-Objekte von kartesischen in Polar-
koordinaten umgerechnet, die Grenzen der Bewegung festgelegt und die 
Circle-Objekte sowie Line2D-Objekte instanziiert. Weitere Methoden der
Klasse sind connect, on_press, on_motion, on_release, ansicht_aktualisieren,
geisterstunde, modellrechnung und punkte_faerben.
'''

'Module importieren'
from berechnung.winkelnormierung import winkel_normieren
from berechnung.winkelberechnung import winkel_berechnen
from math import cos, pi, sin
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from PyQt4.QtCore import QObject, Signal
    
'Klasse DraufsichtRoboter'
class DraufsichtRoboter(QObject):
    
    'Signal definieren'
    xy_neu = Signal(float, float, float, float, float, float)
    
    'Klassenattribut lock definieren'
    lock = None
    
    'Methode __init__'
    def __init__(self, parent, xP1, yP1, xP2, yP2, xP4, yP4, xP5, yP5):
        
        'Vererbung aller Attribute und Methoden von QObject'
        super(DraufsichtRoboter, self).__init__(parent)
        
        'Parentobjekt - QPlotWidget'
        self.parent = parent
        
        'Kartesische Koordinaten'
        self.xP1 = xP1
        self.yP1 = yP1
        
        'Umrechnung in Polarkoordinaten'
        self.modellrechnung(xP2, yP2, xP4, yP4, xP5, yP5)
        
        'Grenzwinkel festlegen'
        self.theta1_min = 0
        self.theta1_max = pi
        
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
        
        'Punkt1 instanziieren'
        #Fixpunkt im Ursprung des Koordinatensystems
        self.point1 = Circle((self.xP1, self.yP1))
        self.point1.set_radius(self.radius_punkt)
        self.point1.set_facecolor(self.farbe_allgemein)
        self.point1.set_alpha(self.alpha_allgemein)
        self.parent.axes.add_patch(self.point1)
        
        'Punkt2 instanziieren'
        self.point2 = Circle((self.xP2, self.yP2))
        self.point2.set_radius(self.radius_punkt)
        self.point2.set_facecolor(self.farbe_allgemein)
        self.point2.set_alpha(self.alpha_allgemein)
        self.parent.axes.add_patch(self.point2)
        
        'Punkt4 instanziieren'
        self.point4 = Circle((self.xP4, self.yP4))
        self.point4.set_radius(self.radius_punkt)
        self.point4.set_facecolor(self.farbe_allgemein)
        self.point4.set_alpha(self.alpha_allgemein)
        self.parent.axes.add_patch(self.point4)
        
        'Punkt5 instanziieren'
        self.point5 = Circle((self.xP5, self.yP5))
        self.point5.set_radius(self.radius_punkt)
        self.point5.set_facecolor(self.farbe_allgemein)
        self.point5.set_alpha(self.alpha_allgemein)
        self.parent.axes.add_patch(self.point5)
        
        self.point = self.point4
        
        'Line2D-Objekte instanziieren'
        
        'Endpunktkoordinaten von Linie1'
        #Linie1 - verbindet Punkt1 mit Punkt2
        self.xL1 = (self.xP1, self.xP2)
        self.yL1 = (self.yP1, self.yP2)
                
        'Linie1 instanziieren'
        self.line1 = Line2D(self.xL1, self.yL1)
        self.line1.set_linewidth(self.staerke_linie)
        self.line1.set_color(self.farbe_allgemein)
        self.line1.set_alpha(self.alpha_allgemein)
        self.line1.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line1)
        
        'Endpunktkoordinaten von Linie2'
        #Linie2 - verbindet Punkt2 mit Punkt4
        self.xL2 = (self.xP2, self.xP4)
        self.yL2 = (self.yP2, self.yP4)
                
        'Linie2 instanziieren'
        self.line2 = Line2D(self.xL2, self.yL2)
        self.line2.set_linewidth(self.staerke_linie)
        self.line2.set_color(self.farbe_allgemein)
        self.line2.set_alpha(self.alpha_allgemein)
        self.line2.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line2)
        
        'Endpunktkoordinaten von Linie3'
        #Linie3 - verbindet Punkt4 mit Punkt5
        self.xL3 = (self.xP4, self.xP5)
        self.yL3 = (self.yP4, self.yP5)
                
        'Linie3 instanziieren'
        self.line3 = Line2D(self.xL3, self.yL3)
        self.line3.set_linewidth(self.staerke_linie)
        self.line3.set_color(self.farbe_allgemein)
        self.line3.set_alpha(self.alpha_allgemein)
        self.line3.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line3)
        
        'Geisterpunktobjekte instanziieren'
        
        'Geisterpunkt2 instanziieren'
        self.pointG2 = Circle((self.xP2, self.yP2))
        self.pointG2.set_radius(self.radius_punkt)
        self.pointG2.set_facecolor(self.farbe_allgemein)
        self.pointG2.set_alpha(self.alpha_geist)
        self.parent.axes.add_patch(self.pointG2)
        self.pointG2.set_visible(False)
        
        'Geisterpunkt4 instanziieren'
        self.pointG4 = Circle((self.xP4, self.yP4))
        self.pointG4.set_radius(self.radius_punkt)
        self.pointG4.set_facecolor(self.farbe_punkt)
        self.pointG4.set_alpha(self.alpha_geist)
        self.parent.axes.add_patch(self.pointG4)
        self.pointG4.set_visible(False)
        
        'Geisterpunkt5 instanziieren'
        self.pointG5 = Circle((self.xP5, self.yP5))
        self.pointG5.set_radius(self.radius_punkt)
        self.pointG5.set_facecolor(self.farbe_allgemein)
        self.pointG5.set_alpha(self.alpha_geist)
        self.parent.axes.add_patch(self.pointG5)
        self.pointG5.set_visible(False)
        
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
        
        'Geisterlinie3 instanziieren'
        self.lineG3 = Line2D(self.xL3, self.yL3)
        self.lineG3.set_linewidth(self.staerke_linie)
        self.lineG3.set_color(self.farbe_allgemein)
        self.lineG3.set_alpha(self.alpha_geist)
        self.lineG3.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.lineG3)
        self.lineG3.set_visible(False)
        
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
        if DraufsichtRoboter.lock is not None: return
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
        DraufsichtRoboter.lock = self
        
        'Sichtbarkeit des Geistes ändern'
        self.pointG2.set_visible(True)
        self.pointG4.set_visible(True)
        self.pointG5.set_visible(True)
        self.lineG1.set_visible(True)
        self.lineG2.set_visible(True)
        self.lineG3.set_visible(True)
        
        'Methoden der Animation-Blit-Technik ausführen'
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point2.set_animated(True)
        self.point4.set_animated(True)
        self.point5.set_animated(True)
        self.line1.set_animated(True)
        self.line2.set_animated(True)
        self.line3.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)
        axes.draw_artist(self.point2)
        axes.draw_artist(self.point4)
        axes.draw_artist(self.point5)
        axes.draw_artist(self.line1)
        axes.draw_artist(self.line2)
        axes.draw_artist(self.line3)
        canvas.blit(axes.bbox)
    
    '''Methode on_motion - Die Methode on_motion wird beim Bewegen des
    Mauszeigers über die Zeichenfläche ausgeführt.'''
    def on_motion(self, event):
        
        '''Die Methode wird weiter ausgeführt wenn das Klassenattribut 
        mit dem Wert self belegt ist. Das Circle-Objekt darf ohne angeklickt 
        zu sein nicht bewegt werden.'''
        if DraufsichtRoboter.lock is not self: return
            
        '''Die Methode wird weiter ausgeführt wenn der Mauszeiger 
        innerhalb des Koordinatensystems bewegt wird.'''
        if event.inaxes != self.point.axes: return
        
        '''Den Mittelpunkt des Circle-Objektes und die x- und y-Koordinaten
        des Mauszeigers zum Zeitpunkt des Drückens der linken Maustaste
        zuweisen.'''
        self.point.center, xpress, ypress = self.press
        
        'Winkel aller Circle-Objekte neu berechnen'
        
        'Winkel berechnen - Kreismittelpunkt'
        phi = winkel_berechnen(self.point4.center[0], self.point4.center[1])
        
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
                
        'Winkelgrenzen zuweisen'
        phi_min = self.theta1_min
        phi_max = self.theta1_max
        
        'Winkelbegrenzung [phi_min, phi_max]'
        if phi_neu <= phi_min or phi_neu > 3*pi/2 and phi_neu < 2*pi:
            phi_neu = phi_min
        elif phi_neu >= phi_max:
            phi_neu = phi_max
        
        'Winkel von Punkt2 aktualisieren'
        #Rundungsfehler berücksichtigen
        if round(self.phi2, 3) == round(self.phi4, 3):
            self.phi2 = phi_neu
        elif round(self.phi2, 3) != round(self.phi4, 3):
            self.phi2 = phi_neu + pi
        
        'Winkel von Punkt4 aktualisieren'
        self.phi4 = phi_neu
        
        'Winkel von Punkt5 aktualisieren'
        self.phi5 = self.phi4
        
        'Theta1 (Denavit-Hartenberg-Parameter) aktualisieren'
        self.theta1 = self.phi4
        
        'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
        'Koordinaten von Punkt2'
        self.xP2 = self.r2*cos(self.phi2) 
        self.yP2 = self.r2*sin(self.phi2)
        'Koordinaten akualisieren'
        self.point2.center = ((self.xP2, self.yP2))
        
        'Koordinaten von Punkt4'
        self.xP4 = self.r4*cos(self.phi4)
        self.yP4 = self.r4*sin(self.phi4)
        'Koordinaten akualisieren'
        self.point4.center = ((self.xP4, self.yP4))
        
        'Koordinaten von Punkt5'
        self.xP5 = self.r5*cos(self.phi5)
        self.yP5 = self.r5*sin(self.phi5)
        'Koordinaten akualisieren'
        self.point5.center = ((self.xP5, self.yP5))

        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Linie1'
        self.xL1 = (self.point1.center[0], self.point2.center[0])
        self.yL1 = (self.point1.center[1], self.point2.center[1])
        'Koordinaten akualisieren'
        self.line1.set_data(self.xL1, self.yL1)
        
        'Koordinaten von Linie2'
        self.xL2 = (self.point2.center[0], self.point4.center[0])
        self.yL2 = (self.point2.center[1], self.point4.center[1])
        'Koordinaten akualisieren'
        self.line2.set_data(self.xL2, self.yL2)
        
        'Koordinaten von Linie3'
        self.xL3 = (self.point4.center[0], self.point5.center[0])
        self.yL3 = (self.point4.center[1], self.point5.center[1])
        'Koordinaten akualisieren'
        self.line3.set_data(self.xL3, self.yL3)
        
        'Methoden der Animation-Blit-Technik ausführen'
        canvas = self.point.figure.canvas
        axes = self.point.axes        
        canvas.restore_region(self.background)      
        axes.draw_artist(self.point2)
        axes.draw_artist(self.point4)
        axes.draw_artist(self.point5)
        axes.draw_artist(self.line1)
        axes.draw_artist(self.line2)
        axes.draw_artist(self.line3)
        canvas.blit(axes.bbox)
        
        'Signal mit den neuen Koordinaten senden'
        self.xy_neu.emit(self.xP2, self.yP2, self.xP4, self.yP4, \
        self.xP5, self.yP5)
    
    '''Methode on_release - Die Methode on_release wird beim Loslassen
    der linken Maustaste auf der Zeichenfläche ausgeführt.'''
    def on_release(self, event):
        
        '''Die Methode wird weiter ausgeführt wenn das Klassenattribut 
        mit dem Wert self belegt ist.'''
        if DraufsichtRoboter.lock is not self: return
        
        'Werte der Attribute zurücksetzen'
        self.press = None
        DraufsichtRoboter.lock = None
            
        'Attribute auf False setzen'
        self.point2.set_animated(False)
        self.point4.set_animated(False)
        self.point5.set_animated(False)
        self.line1.set_animated(False)
        self.line2.set_animated(False)
        self.line3.set_animated(False)
        
        'Hintergrund zurücksetzen'
        self.background = None
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
    
    '''Methode ansicht_aktualisieren - Die Methode ermöglicht das
    Aktualisieren der Ansicht.'''
    def ansicht_aktualisieren(self, xP2, yP2, xP4, yP4, xP5, yP5):
        
        'Umrechnung in Polarkoordinaten'
        self.modellrechnung(xP2, yP2, xP4, yP4, xP5, yP5)
        
        'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
        'Koordinaten von Punkt2 aktualisieren'
        self.point2.center = (self.xP2, self.yP2)
        
        'Koordinaten von Punkt4 aktualisieren'
        self.point4.center = (self.xP4, self.yP4)
        
        'Koordinaten von Punkt5 aktualisieren'
        self.point5.center = (self.xP5, self.yP5)
        
        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Linie1'
        self.xL1 = (self.xP1, xP2)
        self.yL1 = (self.yP1, yP2)
        'Koordinaten aktualisieren'
        self.line1.set_data(self.xL1, self.yL1)
        
        'Koordinaten von Linie2'
        self.xL2 = (xP2, xP4)
        self.yL2 = (yP2, yP4)
        'Koordinaten aktualisieren'
        self.line2.set_data(self.xL2, self.yL2)
        
        'Koordinaten von Linie3'
        self.xL3 = (xP4, xP5)
        self.yL3 = (yP4, yP5)
        'Koordinaten aktualisieren'
        self.line3.set_data(self.xL3, self.yL3)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
        
    '''Methode geisterstunde - Die Methode dient dem Ein- oder Ausblenden
    des Geistes. Weiter werden die Koordinaten des Geistes aktualisiert.'''
    def geisterstunde(self, b):
        
        'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
        'Koordinaten von Geisterpunkt2'
        xGp2 = self.point2.center[0]
        yGp2 = self.point2.center[1]
        'Koordinaten aktualisieren'
        self.pointG2.center = (xGp2, yGp2)
        
        'Koordinaten von Geisterpunkt4'
        xGp4 = self.point4.center[0]
        yGp4 = self.point4.center[1]
        'Koordinaten aktualisieren'
        self.pointG4.center = (xGp4, yGp4)
        
        'Koordinaten von Geisterpunkt5'
        xGp5 = self.point5.center[0]
        yGp5 = self.point5.center[1]
        'Koordinaten aktualisieren'
        self.pointG5.center = (xGp5, yGp5)
        
        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Geisterlinie1'
        xGl1 = (self.point1.center[0], self.point2.center[0])
        yGl1 = (self.point1.center[1], self.point2.center[1])
        'Koordinaten akualisieren'
        self.lineG1.set_data(xGl1, yGl1)
        
        'Koordinaten von Geisterlinie2'
        xGl2 = (self.point2.center[0], self.point4.center[0])
        yGl2 = (self.point2.center[1], self.point4.center[1])
        'Koordinaten akualisieren'
        self.lineG2.set_data(xGl2, yGl2)
        
        'Koordinaten von Geisterlinie3'
        xGl3 = (self.point4.center[0], self.point5.center[0])
        yGl3 = (self.point4.center[1], self.point5.center[1])
        'Koordinaten akualisieren'
        self.lineG3.set_data(xGl3, yGl3)
        
        'Sichtbarkeit des Geistes ändern'
        #Sichtbarkeit ändern - True oder False
        self.pointG2.set_visible(b)
        self.pointG4.set_visible(b)
        self.pointG5.set_visible(b)
        self.lineG1.set_visible(b)
        self.lineG2.set_visible(b)
        self.lineG3.set_visible(b)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
    
    '''Methode modellrechnung - Die Methode rechnet die kartesischen
    Mittelpunktkoordinaten in Polarkoordinaten um.'''
    def modellrechnung(self, xP2, yP2, xP4, yP4, xP5, yP5):
        
        'Kartesische Koordinaten'
        
        'Punkt2, Punkt4 und Punkt5'
        self.xP2 = xP2
        self.yP2 = yP2
        self.xP4 = xP4
        self.yP4 = yP4      
        self.xP5 = xP5
        self.yP5 = yP5
        
        'Polarkoordinaten'
        
        'Radien von Punkt2, Punkt4 und Punkt5'
        self.r2 = ((self.xP2 - self.xP1)**2 + (self.yP2 - self.yP1)**2)**(1/2)
        self.r4 = ((self.xP4 - self.xP1)**2 + (self.yP4 - self.yP1)**2)**(1/2)
        self.r5 = ((self.xP5 - self.xP1)**2 + (self.yP5 - self.yP1)**2)**(1/2)
        
        'Winkel im Intervall [0, 2*pi]'
        
        'Winkel von Punkt2 berechnen'
        self.phi2 = winkel_berechnen(self.xP2, self.yP2)
        
        'Winkel von Punkt4 berechnen'
        self.phi4 = winkel_berechnen(self.xP4, self.yP4)
        
        'Winkel von Punkt5 berechnen'
        self.phi5 = self.phi4
        
        'Theta1 (Denavit-Hartenberg-Parameter) berechnen'
        self.theta1 = self.phi4
        
    '''Methode punkte_faerben - Die Methode färbt oder entfärbt das
    bewegbare Circle-Objekt.'''
    def punkte_faerben(self, b):
        
        'Fallunterscheidung'
        if b == True: #Farbe
            farbe = self.farbe_punkt
        elif b == False: #Schwarz
            farbe = self.farbe_allgemein
        
        'Farbe von Punkt4 festlegen'            
        self.point4.set_facecolor(farbe)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()