'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul seitenansicht_roboter enthält die Klasse SeitenansichtRoboter. 
Eine Animation ermöglicht die Verschiebung von Punkt4 in zwei Richtungen
sowie die Rotation von Punkt5 um Punkt4. Die Klasse wird von QObject 
abgeleitet. Das Signal xy_neu dient dem Übermitteln der veränderten 
Mittelpunktkoordinaten. Weiter wird das Klassenattribut lock definiert. 
In der Methode __init__ werden die Attribute und Methoden der Klasse QObject 
vererbt, die Zeichenfläche als Parent-Objekt zugewiesen, die Zeichenwinkel 
der Circle-Objekte berechnet, die Grenzen der Bewegung festgelegt und die 
Circle-Objekte sowie Line2D-Objekte instanziiert. Weitere Methoden der 
Klasse sind connect, on_press, on_motion, on_release, ansicht_aktualisieren, 
geisterstunde, modellrechnung und punkte_faerben.
'''

'Module importieren'
from berechnung.winkelnormierung import winkel_normieren
from berechnung.winkelberechnung import winkel_berechnen
from math import acos, cos, pi, sin
from matplotlib.lines import Line2D
from matplotlib.patches import Circle
from PyQt4.QtCore import QObject, Signal

'Klasse SeitenansichtRoboter'
class SeitenansichtRoboter(QObject):
    
    'Signal definieren'
    xy_neu = Signal(float, float, float, float, float, float, float, float)
    
    'Klassenattribut lock definieren'
    lock = None
    
    'Methode __init__'
    def __init__(self, parent, xP1, yP1, xP2, yP2, xP3, yP3, \
    xP4, yP4, xP5, yP5):
        
        'Vererbung aller Attribute und Methoden von QObject'
        super(SeitenansichtRoboter, self).__init__(parent)
        
        'Parentobjekt - QPlotWidget'
        self.parent = parent
      
        'Kartesische Koordinaten'
        self.xP1 = xP1
        self.yP1 = yP1
        
        'Längen berechnen'
        self.a2 = ((xP2 - xP1)**2 + (yP2 - yP1)**2)**(1/2)
        self.a3 = ((xP4 - xP2)**2 + (yP4 - yP2)**2)**(1/2)
        
        'Zeichenwinkel berechnen'
        self.modellrechnung(xP2, yP2, xP3, yP3, xP4, yP4, xP5, yP5)
        
        'Kleinsten x-Wert und y-Wert festlegen'
        self.x_min = 0.001
        self.y_min = 45
        
        'Grenzwinkel festlegen'
        self.theta2_min = 0
        self.theta2_max = pi
        
        self.theta3_min = -(pi - 8*pi/180)
        self.theta3_max = 0
        
        self.theta4_min = -8*pi/180
        self.theta4_max = pi - 8*pi/180
        
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
        
        'Punkt3 instanziieren'
        self.point3 = Circle((self.xP3, self.yP3))
        self.point3.set_radius(self.staerke_linie)
        self.point3.set_facecolor(self.farbe_allgemein)
        self.point3.set_alpha(self.alpha_allgemein)
        self.parent.axes.add_patch(self.point3)
        self.point3.set_visible(False)
        
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
        self.xL1 = (self.point1.center[0], self.point2.center[0])
        self.yL1 = (self.point1.center[1], self.point2.center[1])
        #Länge der Linie berechnen
        self.l1 = ((self.xL1[1] - self.xL1[0])**2 + (self.yL1[1] - \
        self.yL1[0])**2)**(1/2)
        
        'Linie1 instanziieren'
        self.line1 = Line2D(self.xL1, self.yL1)
        self.line1.set_linewidth(self.staerke_linie)
        self.line1.set_color(self.farbe_allgemein)
        self.line1.set_alpha(self.alpha_allgemein)
        self.line1.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line1)
        
        'Endpunktkoordinaten von Linie2'
        #Linie2 - verbindet Punkt2 mit Punkt3
        self.xL2 = (self.point2.center[0], self.point3.center[0])
        self.yL2 = (self.point2.center[1], self.point3.center[1])
        #Länge der Linie berechnen
        self.l2 = ((self.xL2[1] - self.xL2[0])**2 + (self.yL2[1] - \
        self.yL2[0])**2)**(1/2)
        
        'Linie2 instanziieren'
        self.line2 = Line2D(self.xL2, self.yL2)
        self.line2.set_linewidth(self.staerke_linie)
        self.line2.set_color(self.farbe_allgemein)
        self.line2.set_alpha(self.alpha_allgemein)
        self.line2.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line2)
        
        'Endpunktkoordinaten von Linie3'
        #Linie3 - verbindet Punkt3 mit Punkt4
        self.xL3 = (self.point3.center[0], self.point4.center[0])
        self.yL3 = (self.point3.center[1], self.point4.center[1])
        #Länge der Linie berechnen
        self.l3 = ((self.xL3[1] - self.xL3[0])**2 + (self.yL3[1] - \
        self.yL3[0])**2)**(1/2)
        
        'Linie3 instanziieren'
        self.line3 = Line2D(self.xL3, self.yL3)
        self.line3.set_linewidth(self.staerke_linie)
        self.line3.set_color(self.farbe_allgemein)
        self.line3.set_alpha(self.alpha_allgemein)
        self.line3.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line3)
        
        'Endpunktkoordinaten von Linie4'
        #Linie3 - verbindet Punkt4 mit Punkt5
        self.xL4 = (self.point4.center[0], self.point5.center[0])
        self.yL4 = (self.point4.center[1], self.point5.center[1])
        #Länge der Linie berechnen
        self.l4 = ((self.xL4[1] - self.xL4[0])**2 + (self.yL4[1] - \
        self.yL4[0])**2)**(1/2)
        
        'Linie4 instanziieren'
        self.line4 = Line2D(self.xL4, self.yL4)
        self.line4.set_linewidth(self.staerke_linie)
        self.line4.set_color(self.farbe_allgemein)
        self.line4.set_alpha(self.alpha_allgemein)
        self.line4.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.line4)
        
        'Geisterpunktobjekte instanziieren'
        
        'Geisterpunkt2 instanziieren'
        self.pointG2 = Circle((self.xP2, self.yP2))
        self.pointG2.set_radius(self.radius_punkt)
        self.pointG2.set_facecolor(self.farbe_allgemein)
        self.pointG2.set_alpha(self.alpha_geist)
        self.parent.axes.add_patch(self.pointG2)
        self.pointG2.set_visible(False)
        
        'Geisterpunkt3 instanziieren'
        self.pointG3 = Circle((self.xP3, self.yP3))
        self.pointG3.set_radius(self.staerke_linie)
        self.pointG3.set_facecolor(self.farbe_allgemein)
        self.pointG3.set_alpha(self.alpha_geist)
        self.parent.axes.add_patch(self.pointG3)
        self.pointG3.set_visible(False)
        
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
        self.pointG5.set_facecolor(self.farbe_punkt)
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
                
        'Geisterlinie4 instanziieren'
        self.lineG4 = Line2D(self.xL4, self.yL4)
        self.lineG4.set_linewidth(self.staerke_linie)
        self.lineG4.set_color(self.farbe_allgemein)
        self.lineG4.set_alpha(self.alpha_geist)
        self.lineG4.set_solid_capstyle(self.ende_linie)
        self.parent.axes.add_line(self.lineG4)
        self.lineG4.set_visible(False)
        
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
        if SeitenansichtRoboter.lock is not None: return 
        
        'Fallunterscheidung - Punkt4 oder Punkt5'
        if self.point4.contains(event)[0] == True:
            self.point = self.point4
            
        elif self.point5.contains(event)[0] == True:
            self.point = self.point5
        
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
        SeitenansichtRoboter.lock = self
        
        'Sichtbarkeit des Geistes ändern'
        self.pointG2.set_visible(True)
        self.pointG4.set_visible(True)
        self.pointG5.set_visible(True)
        self.lineG1.set_visible(True)
        self.lineG2.set_visible(True)
        self.lineG3.set_visible(True)
        self.lineG4.set_visible(True)
        
        'Methoden der Animation-Blit-Technik ausführen'
        canvas = self.point.figure.canvas
        axes = self.point.axes
        self.point2.set_animated(True)
        self.point3.set_animated(True)
        self.point4.set_animated(True)
        self.point5.set_animated(True)
        self.line1.set_animated(True)
        self.line2.set_animated(True)
        self.line3.set_animated(True)
        self.line4.set_animated(True)
        canvas.draw()
        self.background = canvas.copy_from_bbox(self.point.axes.bbox)
        axes.draw_artist(self.point2)
        axes.draw_artist(self.point3)
        axes.draw_artist(self.point4)
        axes.draw_artist(self.point5)
        axes.draw_artist(self.line1)
        axes.draw_artist(self.line2)
        axes.draw_artist(self.line3)
        axes.draw_artist(self.line4)
        canvas.blit(axes.bbox)
    
    '''Methode on_motion - Die Methode on_motion wird beim Bewegen des
    Mauszeigers über die Zeichenfläche ausgeführt.'''
    def on_motion(self, event):
        
        '''Die Methode wird weiter ausgeführt wenn das Klassenattribut 
        mit dem Wert self belegt ist. Das Circle-Objekt darf ohne angeklickt 
        zu sein nicht bewegt werden.'''
        if SeitenansichtRoboter.lock is not self: return
            
        '''Die Methode wird weiter ausgeführt wenn der Mauszeiger 
        innerhalb des Koordinatensystems bewegt wird.'''
        if event.inaxes != self.point.axes: return
        
        '''Den Mittelpunkt des Circle-Objektes und die x- und y-Koordinaten
        des Mauszeigers zum Zeitpunkt des Drückens der linken Maustaste
        zuweisen.'''
        self.point.center, xpress, ypress = self.press     
        
        'Fallunterscheidung - Punkt4 oder Punkt5'
        if self.point == self.point4:
            
            'Verschiebung von Punkt4 in x-, und y-Richtung'
            dx = event.xdata - xpress
            dy = event.ydata - ypress
                
            'neue Koordinaten berechnen'
            x_neu = self.point.center[0] + dx
            y_neu = self.point.center[1] + dy
            
            'Begrenzung auf [x_min,...[ und [y_min...['
            if x_neu < self.x_min and dx < 0:
                x_neu = self.x_min
            if y_neu < self.y_min and dy < 0:
                y_neu = self.y_min
            
            'Länge des Ortsvektors zu Punkt4 berechnen'
            self.r4 = (x_neu**2 + y_neu**2)**(1/2)
                        
            'Hilfswinkel berechnen - Cosinussatz'
            b = (self.a3**2 - self.l1**2 - self.r4**2)/(-2*self.l1*self.r4)
            if b >= 1: b = 1
            elif b <= -1: b = -1
            beta1 = acos(b)
            beta2 = acos(x_neu/self.r4)
            
            'Winkel von Punkt2 berechnen'
            self.phi2 = beta1 + beta2
           
            'Winkel auf [0, 2*pi] normieren um Rundungsfehler auszugleichen'
            self.phi2 = winkel_normieren(self.phi2)
            
            'Winkelgrenzen zuweisen'
            phi2_min = self.theta2_min
            phi2_max = self.theta2_max
        
            'Winkelbegrenzung [phi_min, phi_max]'
            if self.phi2 < phi2_min:
                self.phi2 = phi2_min
            elif self.phi2 > phi2_max:
                self.phi2 = phi2_max
            
            'Theta2 (Denavit-Hartenberg-Parameter) aktualisieren'
            self.theta2 = self.phi2
            
            'Hilfswinkel berechnen - Cosinussatz'
            b = (self.r4**2 - self.l1**2 - self.a3**2)/(-2*self.l1*self.a3)
            if b >= 1: b = 1
            elif b <= -1: b = -1
            beta3 = acos(b)
            
            'Winkelgrenzen zuweisen'
            beta3_min = self.theta3_min + pi
            beta3_max = self.theta3_max + pi
            
            'Winkelbegrenzung [phi_min, phi_max]'
            if beta3 < beta3_min:
                beta3 = beta3_min
            elif beta3 > beta3_max:
                beta3 = beta3_max
                
            'Winkel von Punkt4 berechnen'
            self.phi4 = beta3 - (pi - self.phi2)
            
            'Theta3 (Denavit-Hartenberg-Parameter) berechnen'
            self.theta3 = -(pi - beta3)
            
            'Winkel von Punkt3 berechnen'
            self.phi3 = self.phi4 + pi/4 - 8*pi/180
            
            'Winkel auf [0, 2*pi] normieren um Rundungsfehler auszugleichen'
            self.phi3 = winkel_normieren(self.phi3)
            
            'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
            'Koordinaten von Punkt2'
            self.xP2 = self.l1*cos(self.phi2)
            self.yP2 = self.l1*sin(self.phi2)
            'Koordinaten akualisieren'
            self.point2.center = ((self.xP2, self.yP2))
            
            'Koordinaten von Punkt3'
            self.xP3 = self.point2.center[0] + self.l2*cos(self.phi3)
            self.yP3 = self.point2.center[1] + self.l2*sin(self.phi3)
            'Koordinaten akualisieren'
            self.point3.center = ((self.xP3, self.yP3))
            
            'Koordinaten von Punkt4'
            self.xP4 = self.point2.center[0] + self.a3*cos(self.phi4)
            self.yP4 = self.point2.center[1] + self.a3*sin(self.phi4)
            'Koordinaten akualisieren'
            self.point4.center = ((self.xP4, self.yP4))
            
        elif self.point == self.point5:
            
            'relative Verschiebung'
            dx = self.point5.center[0] - self.point4.center[0]
            dy = self.point5.center[1] - self.point4.center[1]
                    
            'Winkel berechnen - Kreismittelpunkt'
            phi = winkel_berechnen(dx, dy)
            
            'relative Verschiebung'
            dx_p = xpress - self.point4.center[0]
            dy_p = ypress - self.point4.center[1]
            
            'Winkel berechnen - Mauszeiger beim Anklicken des Punktes'
            phi_p = winkel_berechnen(dx_p, dy_p)
            
            'relative Verschiebung'
            dx_e = event.xdata - self.point4.center[0]
            dy_e = event.ydata - self.point4.center[1] 
            
            'Winkel berechnen - Mauszeiger bei der Bewegung'
            phi_e = winkel_berechnen(dx_e, dy_e)
            
            'Winkeländerung berechnen'
            dphi = phi_e - phi_p
            
            'neuen Positionswinkel berechnen'
            phi_neu = phi + dphi        
            
            'Winkel auf [0, 2*pi] normieren um Rundungsfehler auszugleichen'
            phi_neu = winkel_normieren(phi_neu)
            
            'Winkel von Punkt5 berechnen'
            self.phi5 = phi_neu
        
        'Winkelgrenzen - senkrechter Anschlag'
        if self.phi5 > pi/2 and self.phi5 < pi:
            self.phi5 = pi/2
        elif self.phi5 >= pi and self.phi5 < 3*pi/2:
            self.phi5 = 3*pi/2
            
        'Winkelgrenzen - rechtwinkeliger Anschlag'
        phi5_min = self.phi4 - 8*pi/180 + 3*pi/2
        phi5_max = self.phi4 - 8*pi/180 + pi/2
        
        'Winkelbegrenzung [phi_min, phi_max]'
        if self.phi5 >= pi and self.phi5 < phi5_min:
            self.phi5 = phi5_min
        elif self.phi5 > phi5_max and self.phi5 < pi:
            self.phi5 = phi5_max
        
        'Theta4 (Denavit-Hartenberg-Parameter) aktualisieren'
        if self.phi5 >= 0 and self.phi5 <= pi/2:
            self.theta4 = pi/2 - self.phi4 + self.phi5
        elif self.phi5 >= 3*pi/2 and self.phi5 < 2*pi:
            self.theta4 = pi/2 - self.phi4 + self.phi5 - 2*pi
        
        'Koordinaten von Punkt5'
        self.xP5 = self.point4.center[0] + self.l4*cos(self.phi5)
        self.yP5 = self.point4.center[1] + self.l4*sin(self.phi5)
        'Koordinaten akualisieren'
        self.point5.center = ((self.xP5, self.yP5))
        
        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Linie1'
        self.xL1 = (self.point1.center[0], self.point2.center[0])
        self.yL1 = (self.point1.center[1], self.point2.center[1])
        'Koordinaten akualisieren'
        self.line1.set_data(self.xL1, self.yL1)
        
        'Koordinaten von Linie2'
        self.xL2 = (self.point2.center[0], self.point3.center[0])
        self.yL2 = (self.point2.center[1], self.point3.center[1])
        'Koordinaten akualisieren'
        self.line2.set_data(self.xL2, self.yL2)
        
        'Koordinaten von Linie3'
        self.xL3 = (self.point3.center[0], self.point4.center[0])
        self.yL3 = (self.point3.center[1], self.point4.center[1])
        'Koordinaten akualisieren'
        self.line3.set_data(self.xL3, self.yL3)
        
        'Koordinaten von Linie4'
        self.xL4 = (self.point4.center[0], self.point5.center[0])
        self.yL4 = (self.point4.center[1], self.point5.center[1])
        'Koordinaten akualisieren'
        self.line4.set_data(self.xL4, self.yL4)
        
        'Methoden der Animation-Blit-Technik ausführen'
        canvas = self.point.figure.canvas
        axes = self.point.axes
        canvas.restore_region(self.background)
        axes.draw_artist(self.point2)
        axes.draw_artist(self.point3)
        axes.draw_artist(self.point4)
        axes.draw_artist(self.point5)
        axes.draw_artist(self.line1)
        axes.draw_artist(self.line2)
        axes.draw_artist(self.line3)
        axes.draw_artist(self.line4)
        canvas.blit(axes.bbox)
        
        'Signal mit den neuen Koordinaten senden'
        self.xy_neu.emit(self.xP2, self.yP2, self.xP3, self.yP3, \
        self.xP4, self.yP4, self.xP5, self.yP5)
        
    '''Methode on_release - Die Methode on_release wird beim Loslassen
    der linken Maustaste auf der Zeichenfläche ausgeführt.'''
    def on_release(self, event):
        
        '''Die Methode wird weiter ausgeführt wenn das Klassenattribut 
        mit dem Wert self belegt ist.'''
        if SeitenansichtRoboter.lock is not self: return
        
        'Werte der Attribute zurücksetzen'
        self.press = None
        SeitenansichtRoboter.lock = None
            
        'Attribute auf False setzen'
        self.point2.set_animated(False)
        self.point3.set_animated(False)
        self.point4.set_animated(False)
        self.point5.set_animated(False)
        self.line1.set_animated(False)
        self.line2.set_animated(False)
        self.line3.set_animated(False)
        self.line4.set_animated(False)
        
        'Hintergrund zurücksetzen'
        self.background = None

        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
        
    '''Methode ansicht_aktualisieren - Die Methode ermöglicht das
    Aktualisieren der Ansicht.'''
    def ansicht_aktualisieren(self, xP2, yP2, xP3, yP3, xP4, yP4, xP5, yP5):
        
        'Zeichenwinkel berechnen'
        self.modellrechnung(xP2, yP2, xP3, yP3, xP4, yP4, xP5, yP5)
            
        'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
        'Koordinaten von Punkt2 aktualisieren'
        self.point2.center = (self.xP2, self.yP2)
        
        'Koordinaten von Punkt3 aktualisieren'
        self.point3.center = (self.xP3, self.yP3)
        
        'Koordinaten von Punkt4 aktualisieren'
        self.point4.center = (self.xP4, self.yP4)
        
        'Koordinaten von Punkt5 aktualisieren'
        self.point5.center = (self.xP5, self.yP5)
        
        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Linie1'
        self.xL1 = (self.point1.center[0], self.point2.center[0])
        self.yL1 = (self.point1.center[1], self.point2.center[1])
        'Koordinaten aktualisieren'
        self.line1.set_data(self.xL1, self.yL1)
        
        'Koordinaten von Linie2'
        self.xL2 = (self.point2.center[0], self.point3.center[0])
        self.yL2 = (self.point2.center[1], self.point3.center[1])
        'Koordinaten aktualisieren'
        self.line2.set_data(self.xL2, self.yL2)
        
        'Koordinaten von Linie3'
        self.xL3 = (self.point3.center[0], self.point4.center[0])
        self.yL3 = (self.point3.center[1], self.point4.center[1])
        'Koordinaten aktualisieren'
        self.line3.set_data(self.xL3, self.yL3)
        
        'Koordinaten von Linie4'
        self.xL4 = (self.point4.center[0], self.point5.center[0])
        self.yL4 = (self.point4.center[1], self.point5.center[1])
        'Koordinaten aktualisieren'
        self.line4.set_data(self.xL4, self.yL4)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
    
    '''Methode geisterstunde - Die Methode dient dem Ein- oder Ausblenden
    des Geistes. Weiter werden die Koordinaten aktualisiert.'''
    def geisterstunde(self, b):
        
        'Mittelpunktkoordinaten der Circle-Objekte aktualisieren'
        
        'Koordinaten von Geisterpunkt2'
        xGp2 = self.point2.center[0]
        yGp2 = self.point2.center[1]
        'Koordinaten aktualisieren'
        self.pointG2.center = (xGp2, yGp2)
        
        'Koordinaten von Geisterpunkt3'
        xGp3 = self.point3.center[0]
        yGp3 = self.point3.center[1]
        'Koordinaten aktualisieren'
        self.pointG3.center = (xGp3, yGp3)
        
        'Koordinaten von Geisterpunkt4'
        xGp4 = self.point4.center[0]
        yGp4 = self.point4.center[1]
        'Koordinaten aktualisieren'
        self.pointG4.center = (xGp4, yGp4)
        
        'Koordinaten von Geisterpunkt5'
        xGp5 = self.point5.center[0]
        yGp5 = self.point5.center[1]
        self.pointG5.center = (xGp5, yGp5)
        
        'Endpunktkoordinaten der Line2D-Objekte aktualisieren'
        
        'Koordinaten von Geisterlinie1'
        xGl1 = (self.point1.center[0], self.point2.center[0])
        yGl1 = (self.point1.center[1], self.point2.center[1])
        'Koordinaten akualisieren'
        self.lineG1.set_data(xGl1, yGl1)
        
        'Koordinaten von Geisterlinie2'
        xGl2 = (self.point2.center[0], self.point3.center[0])
        yGl2 = (self.point2.center[1], self.point3.center[1])
        'Koordinaten akualisieren'
        self.lineG2.set_data(xGl2, yGl2)
        
        'Koordinaten von Geisterlinie3'
        xGl3 = (self.point3.center[0], self.point4.center[0])
        yGl3 = (self.point3.center[1], self.point4.center[1])
        'Koordinaten akualisieren'
        self.lineG3.set_data(xGl3, yGl3)
        
        'Koordinaten von Geisterlinie4'
        xGl4 = (self.point4.center[0], self.point5.center[0])
        yGl4 = (self.point4.center[1], self.point5.center[1])
        'Koordinaten akualisieren'
        self.lineG4.set_data(xGl4, yGl4)
        
        'Sichtbarkeit des Geistes ändern'
        #Sichtbarkeit ändern - True oder False
        self.pointG2.set_visible(b)
        self.pointG4.set_visible(b)
        self.pointG5.set_visible(b)
        self.lineG1.set_visible(b)
        self.lineG2.set_visible(b)
        self.lineG3.set_visible(b)
        self.lineG4.set_visible(b)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()
     
    '''Methode modellrechnung -  Die Punkte werden als Vektorzug 
    gezeichnet. Die Methode berechnet die zum Zeichnen notwendigen 
    Winkel der vier Punkte.'''
    def modellrechnung(self, xP2, yP2, xP3, yP3, xP4, yP4, xP5, yP5):
        
        'Kartesische Koordinaten'
        
        'Punkt2, Punkt3, Punkt4 und Punkt5'
        self.xP2 = xP2
        self.yP2 = yP2
        self.xP3 = xP3
        self.yP3 = yP3
        self.xP4 = xP4
        self.yP4 = yP4
        self.xP5 = xP5
        self.yP5 = yP5

        'Länge des Ortsvektors zu Punkt4 berechnen'
        self.r4 = (self.xP4**2 + self.yP4**2)**(1/2)
                    
        'Hilfswinkel berechnen - Cosinussatz'
        b = (self.a3**2 - self.a2**2 - self.r4**2)/(-2*self.a2*self.r4) 
        if b >= 1: b = 1
        elif b <= -1: b = -1
        beta1 = acos(b)
        beta2 = acos(self.xP4/self.r4)
        
        'Winkel von Punkt2 berechnen'
        self.phi2 = beta1 + beta2
       
        'Winkel auf [0, 2*pi] normieren um Rundungsfehler auszugleichen'
        self.phi2 = winkel_normieren(self.phi2)

        'Theta2 (Denavit-Hartenberg-Parameter) berechnen'
        self.theta2 = self.phi2
        
        'Hilfswinkel berechnen - Cosinussatz'
        b = (self.r4**2 - self.a2**2 - self.a3**2)/(-2*self.a2*self.a3)
        if b >= 1: b = 1
        elif b <= -1: b = -1
        beta3 = acos(b)
        
        'Winkel von Punkt4 berechnen'
        self.phi4 = beta3 - (pi - self.phi2)
        
        'Theta3 (Denavit-Hartenberg-Parameter) berechnen'
        self.theta3 = -(pi - beta3)
        
        'Winkel von Punkt3 berechnen'
        self.phi3 = self.phi4 + pi/4 - 8*pi/180
        
        'Winkel auf [0, 2*pi] normieren um Rundungsfehler auszugleichen'
        self.phi3 = winkel_normieren(self.phi3)
        
        'Verschiebung von Punkt5 relativ zu Punkt4'
        dx = self.xP5 - self.xP4
        dy = self.yP5 - self.yP4
                
        'Winkel von Punkt5 berechnen'
        self.phi5 = winkel_berechnen(dx, dy)
        
        'Winkel normieren'
        self.phi5 = winkel_normieren(self.phi5)
        
        'Theta4 (Denavit-Hartenberg-Parameter) berechnen'
        if self.phi5 >= 0 and self.phi5 <= pi/2:
            self.theta4 = self.phi5 + pi/2 - 8*pi/180
        elif self.phi5 >= 3*pi/2 and self.phi5 < 2*pi:
            self.theta4 = pi/2 - 8*pi/180 - 2*pi + self.phi5
            
    '''Methode punkte_faerben - Die Methode färbt oder entfärbt die
    bewegbaren Circle-Objekte.'''
    def punkte_faerben(self, b):
        
        'Fallunterscheidung'
        if b == True: #Farbe
            farbe = self.farbe_punkt
        elif b == False: #Schwarz
            farbe = self.farbe_allgemein
            
        'Farbe von Punkt4 und Punkt 5 festlegen'
        self.point4.set_facecolor(farbe)
        self.point5.set_facecolor(farbe)
        
        'Das gesamte Bild neu zeichnen'
        self.point.figure.canvas.draw()