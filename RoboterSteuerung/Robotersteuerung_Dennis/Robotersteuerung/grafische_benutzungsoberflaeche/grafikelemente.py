'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul grafikelemente enthält die Klassen QKoordinaten und QPlotWidget. 
Beide werden von der Klasse QWidget abgeleitet. Dies ermöglicht die 
Integration in eine mit dem Framework Qt erstellte Benutzungsoberfläche. 
'''

'Module importieren'
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt4.QtCore import QSize, Qt
from PyQt4.QtGui import QHBoxLayout, QFont, QFormLayout, QLabel, \
QSpinBox, QWidget

'''Klasse QKoordinaten - Die Klasse dient der Definition einer 
Koordinatenanzeige. Dazu werden drei SpinBoxen untereinander angeordnet 
und deren Eigenschaften angepasst. Weiter können mit der Methode
groesse_festlegen die Abmessungen der Widgets verändert und mit der
Methode koordinaten_aktualisieren die angezeigten Koordinaten auf 
dem aktuellen Stand gehalten werden.'''
class QKoordinaten(QWidget):
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QWidget'
        super(QKoordinaten, self).__init__(parent)
        
        'Schriftart und Schriftgröße festlegen'
        self.setFont(QFont('Arial', 12))
        
        'Methode grafikelemente_hinzufuegen aufrufen'
        self.grafikelemente_hinzufuegen()
        
    'Methode grafikelemente_hinzufuegen'    
    def grafikelemente_hinzufuegen(self):
        
        'Textfelder für die Beschriftung instanziieren'
        self.textX = QLabel('X')
        self.textY = QLabel('Y')
        self.textZ = QLabel('Z')
        
        'QSpinBox-Objekt zur Anzeige der x-Koordinate instanziieren'
        self.x = QSpinBox()
        #Wert rechts ausrichten
        self.x.setAlignment(Qt.AlignRight)
        #Anzeigebereich erweitern
        self.x.setRange(-800, 800)
        #manuelle Eingaben deaktivieren
        self.x.setReadOnly(True)
             
        'QSpinBox-Objekt zur Anzeige der y-Koordinate instanziieren'
        self.y = QSpinBox()
        #Wert rechts ausrichten
        self.y.setAlignment(Qt.AlignRight)
        #Anzeigebereich erweitern
        self.y.setRange(-800, 800)
        #manuelle Eingaben deaktivieren
        self.y.setReadOnly(True)
        
        'QSpinBox-Objekt zur Anzeige der z-Koordinate instanziieren'
        self.z = QSpinBox()
        #Wert rechts ausrichten
        self.z.setAlignment(Qt.AlignRight)
        #Anzeigebereich erweitern
        self.z.setRange(-800, 800)
        #manuelle Eingaben deaktivieren
        self.z.setReadOnly(True)
        
        'Grafikelemente untereinander anordnen'
        layout = QFormLayout(self)
        layout.addRow(self.textX, self.x)
        layout.addRow(self.textY, self.y)
        layout.addRow(self.textZ, self.z)

    'Methode groesse_festlegen'
    def groesse_festlegen(self, breite, hoehe):
        
        'Breite und Höhe festlegen'
        self.breite = breite
        self.hoehe = hoehe
        
        'Abmessungen ändern'
        self.textX.setFixedHeight(self.hoehe)
        self.x.setFixedSize(QSize(self.breite, self.hoehe))
        self.textY.setFixedHeight(self.hoehe)
        self.y.setFixedSize(QSize(self.breite, self.hoehe))
        self.textZ.setFixedHeight(self.hoehe)
        self.z.setFixedSize(QSize(self.breite, self.hoehe))
        
    'Methode koordinaten_aktualisieren'
    def koordinaten_aktualisieren(self, x, y, z):
        
        'Werte eintragen'
        self.x.setValue(x)
        self.y.setValue(y)
        self.z.setValue(z)

'''Klasse QPlotWidget - Die Klasse dient der Definition einer 
Zeichenfläche mit Koordinatensystem.'''
class QPlotWidget(QWidget):
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QWidget'
        super(QPlotWidget, self).__init__(parent)
        
        'Methode koordinatensystem_hinzufuegen aufrufen'
        self.koordinatensystem_hinzufuegen()
    
    'Methode koordinatensystem_hinzufuegen'
    def koordinatensystem_hinzufuegen(self):
        
        'Figure-Objekt instanziieren'
        self.figure = Figure()
        
        'Zeichenfläche instanziieren'
        self.canvas = FigureCanvasQTAgg(self.figure)
        
        'Koordinatensystem hinzufügen'
        #in der 1.Zeile und Spalte 1 Koordinatensystem
        self.axes = self.figure.add_subplot(111)
        
        'Layout Management'
        layout = QHBoxLayout(self)
        layout.addWidget(self.canvas)