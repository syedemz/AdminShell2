'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul oberflaeche enthält die vier Klassen Oberflaeche, Oberflaeche_
Einschalten, Oberflaeche_Betrieb und Oberflaeche_Ausschalten. Die Klasse
Oberflaeche dient der Verwaltung der drei Benutzungsoberflaechen Oberfl-
aeche_Einschalten, Oberflaeche_Betrieb und Oberflaeche_Ausschalten. Alle
anderen enthalten das Layout und die Methoden, die bei der Bedienung der
grafischen Benutzungsoberfläche aufgerufen werden.
'''

'Module importieren'
from grafische_benutzungsoberflaeche.grafikelemente import QKoordinaten
from motorsteuerung.steuerung import Motor
from numpy import array, load, save, hsplit, vsplit, vstack
from os import getcwd, path
from PyQt4.QtCore import QObject, Signal, QSize, Qt, QThread
from PyQt4.QtGui import QAbstractItemView, QHBoxLayout, QVBoxLayout, QBrush, \
QColor, QComboBox, QDialog, QFormLayout, QFrame, QGroupBox, QHeaderView, \
QLabel, QLinearGradient, QListWidget, QPalette, QPixmap, QPushButton, \
QStackedLayout, QStackedWidget, QTabWidget, QTableWidget, QTableWidgetItem, \
QTextEdit, QWidget, QGridLayout
from schnittstelle.server import Server
from digitaler_roboter.roboter import DigitalerRoboter

'''TEST'''

from pprint import pprint

'''Klasse Oberflaeche - Die Klasse Oberflaeche wird von QWidget 
abgeleitet, in das Hauptprogramm importiert und in die Funktion 
hauptprogramm_benutzungsoberflaeche integriert. In der Klasse werden 
Objekte der Klassen Oberflaeche_Einschalten, Oberflaeche_Betrieb und
Oberflaeche ausschalten instanziiert und gestapelt, wobei beim Einschalt-
vorgang die erste Oberfläche (Index 0) angezeigt wird. Die angezeigte 
Oberfläche kann mit der Methode oberflaeche_wechseln geändert werden.'''
class Oberflaeche(QWidget):
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QWidget'
        super(Oberflaeche, self).__init__(parent)
        
        
        'Methode oberflaechen_laden aufrufen'
        self.oberflaechen_laden()
        
        'Signale und Slots verbinden'
        self.startbildschirm.wechseln.connect(self.oberflaeche_wechseln)
        self.hauptbildschirm.wechseln.connect(self.oberflaeche_wechseln)
        self.beendenbildschirm.wechseln.connect(self.oberflaeche_wechseln)
        
        
        
        
    'Methode oberflaechen_laden'
    def oberflaechen_laden(self):
        
        'Oberflächenobjekte instanziieren'
        self.startbildschirm = Oberflaeche_Einschalten()
        self.hauptbildschirm = Oberflaeche_Betrieb()
        self.beendenbildschirm = Oberflaeche_Ausschalten()
        
        'Stacked Layout - Oberflächen stapeln'
        self.oberflaechen = QStackedLayout()
        #entspricht CurrenIndex(0)
        self.oberflaechen.addWidget(self.startbildschirm)
        #entspricht CurrentIndex(1)
        self.oberflaechen.addWidget(self.hauptbildschirm)
        #entspricht CurrentIndex(2)
        self.oberflaechen.addWidget(self.beendenbildschirm)

        'Layout der Oberfläche festlegen'
        layout = QVBoxLayout()
        layout.addLayout(self.oberflaechen)
        self.setLayout(layout)
        
    'Methode oberflaeche_wechseln'
    def oberflaeche_wechseln(self, int):
        
        self.oberflaechen.setCurrentIndex(int)

'Klasse Oberflaeche_Einschalten'
class Oberflaeche_Einschalten(QWidget):
    
    'Signal zum Wechseln der Oberfläche definieren'
    wechseln = Signal(int)
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QWidget'
        super(Oberflaeche_Einschalten, self).__init__(parent)
        
        'Hintergrundfarbe der Oberfläche festlegen'
        self.setAutoFillBackground(True)
        pal = QPalette()
        gradient = QLinearGradient(0, 0, 0, 500)
        gradient.setColorAt(0.0, QColor(255, 255, 255))
        gradient.setColorAt(1.0, QColor(92, 6, 28))
        pal.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(pal)
        
        'Schriftgröße festlegen'
        self.setStyleSheet('QGroupBox {font-size: 14px; \
        font-weight: bold} \
        QLabel {font-size: 14px} \
        QPushButton {font-size: 14px}')
        
        'Höhe der Widgets festlegen'
        self.widget_hoehe = 45
        
        'Methode grafik_laden aufrufen'
        self.grafik_laden()
        
        'Signale und Slots verbinden'
        self.button_einschalten.clicked.connect(self.steuerung_einschalten)

    '''Methode grafik_laden - Die Methode enthält die Grafikelemente der 
    Oberfläche.'''
    def grafik_laden(self):
        
        'GroupBox instanziieren'   
        info = QGroupBox()
        info.setTitle('Wichtige Informationen')
        
        'Textfeld instanziieren'
        self.textinfo = QLabel()
        self.textinfo.setFixedHeight(self.widget_hoehe)
        self.textinfo.setText('Den Roboter von Hand in ' 
        'die abgebildete Parkposition bringen, ' 
        'Position halten und Steuerung einschalten drücken!')

        'Button instanziieren'
        self.button_einschalten = QPushButton('Steuerung einschalten')
        self.button_einschalten.setFixedHeight(self.widget_hoehe)

        'Textfeld und Button untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.textinfo)
        layout.addWidget(self.button_einschalten)
        
        'Layout der GroupBox festlegen'
        info.setLayout(layout)
        
        'GroupBox instanziieren'
        bilder = QGroupBox()
        bilder.setTitle('Parkposition')
        
        'Bilder der Ausgangsposition laden'
        workdir = getcwd()
        
        #Bild Draufsicht
        dateiname = 'bild_draufsicht.svg'
        dir = path.join(workdir, 'speicher', 'bildspeicher', dateiname)
        pix = QPixmap(dir)
                
        bild_draufsicht = QLabel()
        bild_draufsicht.setPixmap(pix)
        bild_draufsicht.setAlignment(Qt.AlignCenter)
                
        #Bild Seitenansicht
        dateiname = 'bild_seitenansicht.svg'
        dir = path.join(workdir, 'speicher', 'bildspeicher', dateiname)
        pix = QPixmap(dir)
        
        bild_seitenansicht = QLabel()
        bild_seitenansicht.setPixmap(pix)
        bild_seitenansicht.setAlignment(Qt.AlignCenter)
        
        'Bilder nebeneinander anordnen'      
        layout = QHBoxLayout()
        layout.addWidget(bild_draufsicht)
        layout.addWidget(bild_seitenansicht)
        
        'Layout der GroupBox festlegen'
        bilder.setLayout(layout)
                
        'Grafikelemente untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(info)
        layout.addWidget(bilder)
        
        'Layout der Oberfläche festlegen'
        self.setLayout(layout)
    
    '''Methode steueung_einschalten - Die Methode wird nach dem Betätigen von
    button_einschalten ausgeführt. Aktiviert die Servomotoren dauerhaft.'''
    def steuerung_einschalten(self):
        
        'Information ausgeben'
        print('Steuerung ein')

        'Signal zum Wechseln der Oberfläche senden'
        #wechseln zum Hauptbildschirm
        self.wechseln.emit(1)
        
        'Motorsteuerung'
        'Motor-Objekt instanziieren'
        motor = Motor('COM3')
        #Ausgangsposition laden
        motor.programm_laden('programmEin')
        #Zeit festlegen
        

        
        motor.steuerung_synchron(t = 10) #t wird überschrieben
        #Servomotoren einschalten
        motor.servo_start()
        #Servomotoren kalibrieren
        motor.servo_kalibrieren()
        


'Klasse Oberflaeche_betrieb'
class Oberflaeche_Betrieb(QTabWidget):
    
    'Signal zum Wechseln der Oberfläche definieren'
    wechseln = Signal(int)
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QTabWidget'
        super(Oberflaeche_Betrieb, self).__init__(parent)
        
        
        
        'Attribute definieren'
        self.motor = None        
        self.programmaufnahme = False
        self.programmwahl = None
        self.fernsteuerung = False

        self.motor_belegt = False

        self.nachrichten_protokoll = []
        
        'Hintergrundfarbe der Oberfläche festlegen'
        self.pal = QPalette()
        gradient = QLinearGradient(0, 0, 0, 500)
        gradient.setColorAt(0.0, QColor(255, 255, 255))
        gradient.setColorAt(1.0, QColor(92, 6, 28))
        self.pal.setBrush(QPalette.Window, QBrush(gradient))
        
        'Schriftgröße festlegen'
        self.setStyleSheet('QGroupBox {font-size: 14px; \
        font-weight: bold} \
        QLabel {font-size: 14px} \
        QPushButton {font-size: 14px}')
        
        'Höhe der Widgets festlegen'
        self.widget_breite1 = 100
        self.widget_breite2 = 150
        self.widget_hoehe1 = 35
        self.widget_hoehe2 = 45
        
        'Methoden grafik_laden aufrufen'
        self.grafik_tab1_laden()
        self.grafik_tab2_laden()
        self.grafik_tab3_laden()
        self.grafik_tab4_laden()
        self.grafik_tab5_laden() ##
    
        'Dialogfenster Speichern instanziieren'
        self.grafik_dialogfensterSpeichern()
        
        'Signale und Slots verbinden'
        
        'Tab1 - Programme'
        self.button_programm1.clicked.connect(self.programm_oeffnen)
        self.button_programm2.clicked.connect(self.programm_oeffnen)
        self.button_programm3.clicked.connect(self.programm_oeffnen)
        self.button_programm4.clicked.connect(self.programm_oeffnen)
        self.button_programm5.clicked.connect(self.programm_oeffnen)
        self.button_auswahlAendern.clicked.connect( \
        self.programmauswahl_aendern)
        
        self.button_programmErstellen.clicked.connect(self.programm_erstellen)
        self.button_programmBearbeiten.clicked.connect( \
        self.programm_bearbeiten)
        
        self.button_start.clicked.connect(self.start)
        self.button_fortsetzen.clicked.connect(self.fortsetzen)
        self.button_stop.clicked.connect(self.stop)
        self.button_anmelden.clicked.connect(self.schnittstelle_anmelden)
        self.button_ausschalten.clicked.connect(self.ausschalten)
        self.button_wartung.clicked.connect(self.wartung_oeffnen)
        
        'Tab2 - Programm erstellen'
        self.digRob.signal_animation_aktiv.connect( \
        self.button_positionEinlesen_aktivieren)
        self.digRob.signal_koordinaten.connect( \
        self.anzeige.koordinaten_aktualisieren)

        self.button_draufsicht.clicked.connect(self.ansicht_wechseln)
        self.button_seitenansicht.clicked.connect(self.ansicht_wechseln)
        self.button_greifer.clicked.connect(self.ansicht_wechseln)
        
        self.button_aufnahmeBeginnen.clicked.connect(self.aufnahme_beginnen)
        self.button_positionEinlesen.clicked.connect(self.position_einlesen)
        self.button_aufnahmeBeenden.clicked.connect(self.aufnahme_beenden)
        self.button_aufnahmeSpeichern.clicked.connect( \
        self.dialogfensterSpeichern_oeffnen)
        self.button_zuruecksetzen.clicked.connect(self.aufnahme_zuruecksetzen)
        self.button_aufnahmeAbbrechen.clicked.connect(self.aufnahme_abbrechen)
        
        self.button_positionAnfang.clicked.connect(self.position_anfang)
        self.button_positionZurueck.clicked.connect(self.position_zurueck)
        self.button_positionAendern.clicked.connect(self.position_aendern)
        self.button_positionSpeichern.clicked.connect( \
        self.position_speichern)
        self.button_positionVor.clicked.connect(self.position_vor)
        self.button_positionEnde.clicked.connect(self.position_ende)
        
        'Tab3 - Programm bearbeiten'
        self.button_positionAnzeigen.clicked.connect(self.position_anzeigen)
        self.button_bearbeitenSchliessen.clicked.connect( \
        self.bearbeiten_schliessen)
        self.tabelle.cellClicked.connect( \
        self.button_positionAnzeigen_aktivieren)
        
        'Tab4 - Wartung'
        self.button_uebertragung.clicked.connect(self.fernsteuerung_zulassen)
#        self.button_wartungBeginnen.clicked.connect(self.wartung_beginnen)
#        self.button_wartungBeenden.clicked.connect(self.wartung_beenden)
#        self.button_wartungSchliessen.clicked.connect(self.wartung_schliessen)
        
        'Tab5 - Manuelle Steuerung' ##
        self.button_1.clicked.connect(self.button1)
        self.button_2.clicked.connect(self.button2)
        self.button_3.clicked.connect(self.button3)
        self.button_4.clicked.connect(self.button4)
        self.button_5.clicked.connect(self.button5)
        self.button_6.clicked.connect(self.button6)
        self.button_7.clicked.connect(self.button7)
        self.button_8.clicked.connect(self.button8)
        self.button_9.clicked.connect(self.button9)
        self.button_10.clicked.connect(self.button10)
        self.button_11.clicked.connect(self.button11)
        self.button_12.clicked.connect(self.button12)
        self.button_ManStart.clicked.connect(self.buttonManStart)
        self.button_ManStop.clicked.connect(self.buttonManStop)
        
        'Dialogfenster - Speichern'
        self.dialogbutton_ok.clicked.connect(self.aufnahme_speichern)
        self.dialogbutton_abbrechen.clicked.connect( \
        self.dialogfensterSpeichern_schliessen)
        
#        'Signale zum Durchrouten der Fernsteuerung'
#        self.Greifer_position = Signal(int, int, int, int, int, int)
#        self.roboter_manuell = Signal(int, int, int, int, int, int)
#        self.roboter_manuell_aus = Signal()
        
       
    '''Methode ansicht_wechseln - Die Methode wird beim Wechseln 
    der Ansicht des digitalen Roboters ausgeführt, wobei die gewählte 
    Ansicht geöffnet und die Bedienelemente dementsprechend aktiviert 
    oder deaktiviert werden.'''
    def ansicht_wechseln(self):
        
        if self.button_draufsicht.isChecked() == True:
            
            'Information erstellen'
            ansicht = 'Draufsicht'
            info = ansicht + ' anzeigen'
            
            'Ansicht wechseln'
            self.digRob.ansicht_wechseln(0)
            
            'Bedienelemente aktivieren/deaktivieren'
            self.button_draufsicht.setChecked(False)
            self.button_draufsicht.setEnabled(False)           
            self.button_seitenansicht.setEnabled(True)
            self.button_greifer.setEnabled(True)
        
        elif self.button_seitenansicht.isChecked() == True:
            
            'Information erstellen'
            ansicht = 'Seitenansicht'
            info = ansicht + ' anzeigen'
            
            'Ansicht wechseln'
            self.digRob.ansicht_wechseln(1)
            
            'Bedienelemente aktivieren/deaktivieren'
            self.button_draufsicht.setEnabled(True)
            self.button_seitenansicht.setChecked(False)
            self.button_seitenansicht.setEnabled(False)
            self.button_greifer.setEnabled(True)
            
        elif self.button_greifer.isChecked() == True:
            
            'Information erstellen'
            ansicht = 'Ansicht Greifer'
            info = ansicht + ' anzeigen'
            
            'Ansicht wechseln'
            self.digRob.ansicht_wechseln(2)
            
            'Bedienelemente aktivieren/deaktivieren'
            self.button_draufsicht.setEnabled(True)
            self.button_seitenansicht.setEnabled(True)
            self.button_greifer.setChecked(False)
            self.button_greifer.setEnabled(False)
            
        'Information ausgeben'
        print(info)
        
    '''Methode ansicht_zuruecksetzen - Die Methode setzt die Ansicht
    des digitalen Roboters auf die Draufsicht zurück. Wenn diese an-
    gezeigt wird, gibt es keine Änderungen.'''
    def ansicht_zuruecksetzen(self, b):
        
        if self.button_draufsicht.isChecked() == False:
            
            'Ansicht wechseln'
            self.digRob.ansicht_wechseln(0)
            
            'Bedienelemente aktivieren/deaktivieren'
            self.button_draufsicht.setChecked(False)
            self.button_draufsicht.setEnabled(False)
            self.button_seitenansicht.setChecked(False)           
            self.button_seitenansicht.setEnabled(True)
            self.button_greifer.setChecked(False)
            self.button_greifer.setEnabled(True)   
            
    '''Methode aufnahme_abbrechen - Die Methode wird nach dem Betätigen
    von button_aufnahmeAbbrechen ausgeführt. In Folge wird eine begonnene
    Aufnahme abgebrochen (dem Attribut self.programmaufnahme der Wert False
    zugewiesen), die zweite Seite in den Ausgangszustand versetzt und
    die erste Seite geöffnet.'''
    def aufnahme_abbrechen(self):
        
        'Information ausgeben'
        print('Aufnahme abbrechen')
        
        'Attribut zurücksetzen'
        self.programmaufnahme = False
        
        'Tab2 - Programm erstellen - deaktivieren'
        self.setTabEnabled(1, False)
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_aufnahmeBeginnen.setEnabled(True)
        self.button_positionEinlesen.setEnabled(False)
        self.button_aufnahmeBeenden.setEnabled(False)
        self.button_aufnahmeSpeichern.setEnabled(False)
        self.button_zuruecksetzen.setEnabled(False)
        
        'Ansicht des digitalen Roboters zurücksetzen'
        self.ansicht_zuruecksetzen(True)
        
        'Digitalen Roboter in den Ausgangszustand versetzen'
        self.digRob.animation_aktivieren(False)
        self.digRob.animation_zuruecksetzen(True)
        
        'Tab1- Programme - öffnen und aktivieren'
        self.setCurrentIndex(0)
        self.setTabEnabled(0, True)       
        
    '''Methode aufnahme_beenden - Die Methode wird nach dem Betätigen von
    button_aufnahmeBeenden ausgeführt. In Folge wird der digitale Roboter
    deaktiviert und die Ausgangsposition des Roboters als letzte Position 
    des aufgenommenen Programmes gespeichert. Wenn kein Programm existiert 
    wird eine neue Datei mit der Ausgangsposition erstellt. Ansonsten wird 
    das aufgenommene Programm geladen, die Position eingefügt und die Datei 
    gespeichert.'''
    def aufnahme_beenden(self):
        
        'Information ausgeben'
        print('Aufnahme beenden')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_aufnahmeBeenden.setEnabled(False)
        self.button_aufnahmeSpeichern.setEnabled(True)
        
        'Digitalen Roboter deaktivieren'
        self.digRob.animation_aktivieren(False)

        'Ausgangsposition laden'
        orientierung_neu, lage_neu, \
        winkel_neu, greifer_neu = self.laden('programmEin')
        
        'Speichername'
        speichername = 'programm'            
            
        'Fallunterscheidung'
        if self.programmaufnahme == False:
            
            'Ausgangsposition in einer neuen Datei speichern'
            self.speichern(speichername, orientierung_neu, lage_neu, \
            winkel_neu, greifer_neu)
            
        elif self.programmaufnahme == True:
            
            'Programm laden'
            orientierung, lage, winkel, greifer = self.laden(speichername)
            
            'Ausgangsposition als letzte Position einfügen'
            pprint(orientierung)
            pprint(orientierung_neu)
            orientierung = vstack((orientierung, orientierung_neu))
            lage = vstack((lage, lage_neu))
            winkel = vstack((winkel, winkel_neu))
            greifer = vstack((greifer, greifer_neu))
            
            'Programm speichern'
            self.speichern(speichername, orientierung, lage, \
            winkel, greifer)
            
            'Attribut zurücksetzen'
            self.programmaufnahme = False
            
    '''Methode aufnahme_beginnen - Die Methode wird nach dem Betätigen von
    button_aufnahmeBeginnen ausgeführt. In Folge wird der digitale Roboter 
    aktiviert.'''
    def aufnahme_beginnen(self):
        
        'Information ausgeben'
        print('Aufnahme beginnen')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_aufnahmeBeginnen.setEnabled(False)
        self.button_aufnahmeBeenden.setEnabled(True)
        self.button_zuruecksetzen.setEnabled(True)
        
        'Digitalen Roboter aktivieren'
        self.digRob.animation_aktivieren(True)
        
    '''Methode aufnahme_speichern - Die Methode wird nach dem Betätigen 
    von button_dialogbutton_ok ausgeführt. In Folge wird das aufgenommene 
    Programm geladen und dem gewählten Speicherplatz zugewiesen. Weiter 
    werden das Dialogfenster und die zweite Seite geschlossen sowie die 
    erste Seite geöffnet.'''
    def aufnahme_speichern(self):
        
        'Information ausgeben'
        print('Aufnahme speichern')
        
        'Programm laden'
        orientierung, lage, winkel, greifer = self.laden('programm')
        
        'Speichername'
        ind = self.speicherplatz.currentIndex()
        
        if ind == 0:
            speichername = 'programm1'
        elif ind == 1:
            speichername = 'programm2'
        elif ind == 2:
            speichername = 'programm3'
        elif ind == 3:
            speichername = 'programm4'
        elif ind == 4:
            speichername = 'programm5'
        
        'Programm speichern'
        self.speichern(speichername, orientierung, lage, winkel, greifer)
        
        'Wahlmöglichkeiten zurücksetzen und das Dialogfenster schließen'
        self.speicherplatz.setCurrentIndex(0)
        self.dialogfensterSpeichern.close()
        
        'Tab2 - Programm aufnehmen - deaktivieren'
        self.setTabEnabled(1, False)
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_aufnahmeBeginnen.setEnabled(True)
        self.button_positionEinlesen.setEnabled(False)
        self.button_aufnahmeBeenden.setEnabled(False)
        self.button_aufnahmeSpeichern.setEnabled(False)
        self.button_zuruecksetzen.setEnabled(False)
        
        'Ansicht des digitalen Roboters zurücksetzen'
        self.ansicht_zuruecksetzen(True)
        
        'Digitalen Roboter in den Ausgangszustand versetzen'
        self.digRob.animation_aktivieren(False)
        self.digRob.animation_zuruecksetzen(True)
                
        'Tab1- Programme - öffnen und aktivieren'
        self.setCurrentIndex(0)
        self.setTabEnabled(0, True)
        
    '''Methode aufnahme_zuruecksetzen - Die Methode wird nach dem Betätigen
    von button_zuruecksetzen ausgeführt. In Folge wird dem Attribut self.
    programmaufnahme der Wert False zugewiesen und die Ansicht des digitalen
    Roboters sowie der digitale Roboter selbst in den Ausgangszustand 
    versetzt.'''
    def aufnahme_zuruecksetzen(self):
        
        'Information ausgeben'
        print('Aufnahme zurücksetzen')
        
        'Attribut zurücksetzen'
        self.programmaufnahme = False
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_aufnahmeBeginnen.setEnabled(True)
        self.button_positionEinlesen.setEnabled(False)
        self.button_aufnahmeBeenden.setEnabled(False)
        self.button_aufnahmeSpeichern.setEnabled(False)
        self.button_zuruecksetzen.setEnabled(False)
        
        'Ansicht des digitalen Roboters zurücksetzen'
        self.ansicht_zuruecksetzen(True)
        
        'Digitalen Roboter in den Ausgangszustand versetzen'
        self.digRob.animation_aktivieren(False)
        self.digRob.animation_zuruecksetzen(True)
        
    '''Methode ausschalten - Die Methode wird nach dem Betätigen von 
    button_ausschalten ausgeführt. In Folge wird die dritte Oberfläche
    geöffnet und der Roboter in die Ausgangsposition gefahren.'''
    def ausschalten(self):
        
        'Information ausgeben'
        print('Steuerung aus')
        
        'Signal zum Wechseln der Oberfläche senden'
        #wechseln zum Beendenbildschirm
        self.wechseln.emit(2)
        
        
        motor = Motor('COM3') 
        'Motorsteuerung'
#        motor.motorsteuerung('programmAus', t = 3000)
#        
#                
#        motor.steuerung_synchron(t = 3) #t wird überschrieben
#        #Servomotoren einschalten
#        motor.servo_start()
        motor.shield_abschalten()
        
    '''Methode bearbeiten_schliessen - Die Methode wird nach dem Betätigen 
    von button_bearbeitenSchliessen ausgeführt. In Folge werden die zweite
    und dritte Seite in den Ausgangszustand versetzt sowie die erste Seite
    geöffnet.'''
    def bearbeiten_schliessen(self):
        
        'Information ausgeben'
        print('Bearbeiten schließen')
        
        'Tab2 und Tab3 deaktivieren'
        self.setTabEnabled(1, False)
        self.setTabEnabled(2, False)
        
        'Aufnahmeelemente anzeigen'
        self.bedienelemente.setCurrentIndex(0)
        
        'Ansicht des digitalen Roboters zurücksetzen'
        self.ansicht_zuruecksetzen(True)
        
        'Digitalen Roboter in den Ausgangszustand versetzen'
        self.digRob.animation_aktivieren(False)
        self.digRob.animation_zuruecksetzen(True)
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_positionAnzeigen.setEnabled(False)
        
        'Tabelle zurücksetzen'
        self.tabelle_zuruecksetzen()
        
        'Tab1- Programme - öffnen und aktivieren'
        self.setCurrentIndex(0)
        self.setTabEnabled(0, True)
        
    '''Methode button_positionAnzeigen_aktivieren - Die Methode aktiviert
    den Button zur Anzeige einer ausgewählten Position. Der Button wird
    bei der Auswahl der Überschriftenzeile deaktiviert. '''
    def button_positionAnzeigen_aktivieren(self, zeile, spalte):
        
        if zeile == 0:
            self.button_positionAnzeigen.setEnabled(False)
        elif zeile >= 1:
            self.button_positionAnzeigen.setEnabled(True)

    '''Methode button_positionEinlesen_aktivieren - Die Methode wird beim
    Bewegen des digitalen Roboters ausgeführt. In Folge wird der Button
    aktiviert und das Einlesen der Position ermöglicht.'''
    def button_positionEinlesen_aktivieren(self, b):
        
        'der Button darf beim Bearbeiten nicht aktiviert werden'
        if self.tab3.isEnabled() == False:
            
            'Bedienelemente aktivieren/deaktivieren'
            self.button_positionEinlesen.setEnabled(b)
            self.button_aufnahmeBeenden.setEnabled(not b)
            
    '''Methode_buttonStart_aktivieren -  Der Button ist beim Ausführen eines
    Programmes deaktiviert. Erst am Ende des Programmes wird vom Motor-Objekt
    ein Signal gesendet und der Button aktiviert.'''
    def button_start_aktivieren(self):
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_start.setEnabled(True)
        self.button_stop.setEnabled(False)
        self.button_wartung.setEnabled(True)
        self.button_ausschalten.setEnabled(True)
           
    '''Methode dialogfensterSpeichern_oeffnen - Die Methode wird nach dem 
    Betätigen des buttons_aufnahmeSpeichern ausgeführt. In Folge wird das
    Dialogfenster geöffnet.'''
    def dialogfensterSpeichern_oeffnen(self):
        
        self.dialogfensterSpeichern.exec_()
        
    '''Methode dialogfensterSpeichern_schliessen - Die Methode schließt das
    Dialogfenster.'''
    def dialogfensterSpeichern_schliessen(self):
        
        'Information ausgeben'
        print('Speichern abgebrochen')
        
        'Wahlmöglichkeiten zurücksetzen und das Dialogfenster schließen'
        self.speicherplatz.setCurrentIndex(0)
        self.dialogfensterSpeichern.close()
    
    def fernsteuerung_anfrage(self, app_anfrage):
        
        angefragte_apps = []
        for index in range(0, self.textfeld2.count()):
            angefragte_apps.append(self.textfeld2.item(index).text())
            
        if app_anfrage not in angefragte_apps:
            self.textfeld2.addItem(app_anfrage)
           
        self.button_uebertragung.setEnabled
        
    '''   asd'''    
    def fernsteuerung_zulassen(self):
        if self.fernsteuerung == False:
            if self.textfeld2.currentItem():
                self.auswahl_app = self.textfeld2.currentItem().text()
                self.fernsteuerung = True
                self.server.fernsteuerung_mot.emit(self.auswahl_app)
                '''Zulassen von einzelnen Verbindungen'''
    #            self.thread_server.server.verbindung_zulassen(self.auswahl_app)
                
                self.button_uebertragung.setText('Verbindung trennen')
                
                self.textfeld3_text = 'Fernsteuerung AKTIV. Verbunden mit: ' + self.auswahl_app
                self.textfeld3.setText('Fernsteuerung AKTIV. Verbunden mit: ' + self.auswahl_app)
                
                angefragte_apps = []
                for index in range(0, self.textfeld2.count()):
                    angefragte_apps.append(self.textfeld2.item(index).text())
                    
                angefragte_apps.remove(self.auswahl_app)
                
                self.textfeld2.clear()
                for index in range(0, len(angefragte_apps)):
                    self.textfeld2.addItem(angefragte_apps[index])
            
            elif not self.textfeld2.currentItem():
                print('Keine Auswahl getroffen')
            
        elif self.fernsteuerung == True:
            print('Fernsteuerung deaktiviert')
            self.server.fernsteuerung_mot.emit(' ')
            self.fernsteuerung = False
#            self.thread_server.server.verbindung_zulassen(' ')
            self.button_uebertragung.setText('Fernsteuerung zulassen')
            self.textfeld3.setText('Fernsteuerung inaktiv.')
            
#    def fernsteuerung_befehlsausgabe(self, anfrage)
    
    '''Methode fortsetzen - Die Methode wird nach dem Betätigen von 
    button_fortsetzen ausgeführt. In Folge wird der Roboter in die 
    Ausgangsposition gefahren.'''
    def fortsetzen(self):

        'Information ausgeben'
        print('Fortsetzen')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_start.setVisible(True)
        self.button_fortsetzen.setVisible(False)
        self.button_stop.setEnabled(True)
        self.button_wartung.setEnabled(False)
        
        'Motorsteuerung'
        if self.motor is not None:
            self.motor.fortsetzen()
        
    '''Methode grafik_dialogfenster - Die Methode legt das Layout und die
    Bedienelemente des Dialogfensters fest. '''
    def grafik_dialogfensterSpeichern(self):
        
        'Dialogfenster instanziieren'
        self.dialogfensterSpeichern = QDialog()
        self.dialogfensterSpeichern.setWindowTitle('Aufnahme speichern')
        self.dialogfensterSpeichern.setFixedSize(QSize(250, 100))
        
        'Textfeld instanziieren'
        dateiname = QLabel('Dateiname:')
        dateiname.setFixedHeight(self.widget_hoehe2)
        
        'ComboBox mit 5 Wahlmöglichkeiten instanziieren'
        self.speicherplatz = QComboBox()
        self.speicherplatz.setFixedHeight(self.widget_hoehe1)
        self.speicherplatz.addItem(' Programm 1')
        self.speicherplatz.addItem(' Programm 2')
        self.speicherplatz.addItem(' Programm 3')
        self.speicherplatz.addItem(' Programm 4')
        self.speicherplatz.addItem(' Programm 5')
        
        'Textfeld und ComboBox nebeneinander anordnen'
        zeile1 = QFormLayout()
        zeile1.addRow(dateiname, self.speicherplatz)
        
        'Buttons instanziieren'
        self.dialogbutton_ok = QPushButton('Ok')
        self.dialogbutton_ok.setFixedHeight(self.widget_hoehe1)
        
        self.dialogbutton_abbrechen = QPushButton('Abbrechen')
        self.dialogbutton_abbrechen.setFixedHeight(self.widget_hoehe1)
        
        'Buttons nebeneinander anordnen'
        zeile2 = QHBoxLayout()
        zeile2.addWidget(self.dialogbutton_ok)
        zeile2.addWidget(self.dialogbutton_abbrechen)
        
        'Zeilen untereinander anordnen'
        layout = QVBoxLayout()
        layout.addLayout(zeile1)
        layout.addLayout(zeile2)
        
        'Layout des Dialogfensters festlegen'
        self.dialogfensterSpeichern.setLayout(layout)
    
    '''Methode grafik_tab1_laden - Die Methode legt das Layout der ersten
    Seite fest.'''
    def grafik_tab1_laden(self):
        
        'Tab1 instanziieren'
        self.tab1 = QWidget()
        self.tab1.setAutoFillBackground(True)
        self.tab1.setPalette(self.pal)
        self.addTab(self.tab1, 'Programme')
        
        'GroupBox instanziieren'
        auswahl = QGroupBox()
        auswahl.setTitle('Auswahl')
        
        'Buttons instanziieren'
        self.button_programm1 = QPushButton('Programm 1')
        self.button_programm1.setCheckable(True)
        self.button_programm1.setFixedHeight(self.widget_hoehe2)
        self.button_programm1.setEnabled(False)
        
        self.button_programm2 = QPushButton('Programm 2')
        self.button_programm2.setCheckable(True)
        self.button_programm2.setFixedHeight(self.widget_hoehe2)
        self.button_programm2.setEnabled(False)
        
        self.button_programm3 = QPushButton('Programm 3')
        self.button_programm3.setCheckable(True)
        self.button_programm3.setFixedHeight(self.widget_hoehe2)
        self.button_programm3.setEnabled(False)
        
        self.button_programm4 = QPushButton('Programm 4')
        self.button_programm4.setCheckable(True)
        self.button_programm4.setFixedHeight(self.widget_hoehe2)
        self.button_programm4.setEnabled(False)
        
        self.button_programm5 = QPushButton('Programm 5')
        self.button_programm5.setCheckable(True)
        self.button_programm5.setFixedHeight(self.widget_hoehe2)
        self.button_programm5.setEnabled(False)
        
        self.button_auswahlAendern = QPushButton('Ändern')
        self.button_auswahlAendern.setFixedHeight(self.widget_hoehe2)
        self.button_auswahlAendern.setEnabled(False)
        
        'Buttons untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.button_programm1)
        layout.addWidget(self.button_programm2)
        layout.addWidget(self.button_programm3)
        layout.addWidget(self.button_programm4)
        layout.addWidget(self.button_programm5)
        layout.addStretch()
        layout.addWidget(self.button_auswahlAendern)
        
        'Layout der GroupBox festlegen'
        auswahl.setLayout(layout)
        
        'Layout von Spalte1 festlegen'
        spalte1 = QVBoxLayout()
        spalte1.addWidget(auswahl)
        
        'GroupBox instanziieren'
        programm = QGroupBox()
        programm.setTitle('Programm')
        
        'Buttons instanziieren'
        self.button_programmErstellen = QPushButton('Erstellen')
        self.button_programmErstellen.setFixedHeight(self.widget_hoehe2)
        self.button_programmErstellen.setEnabled(False)
        
        self.button_programmBearbeiten = QPushButton('Bearbeiten')
        self.button_programmBearbeiten.setFixedHeight(self.widget_hoehe2)
        self.button_programmBearbeiten.setEnabled(False)
        
        self.button_start = QPushButton('Start')
        self.button_start.setFixedHeight(self.widget_hoehe2)
        self.button_start.setEnabled(False)
        
        self.button_fortsetzen = QPushButton('Auf Start fahren')
        self.button_fortsetzen.setFixedHeight(self.widget_hoehe2)
        self.button_fortsetzen.setVisible(False)
        
        self.button_stop = QPushButton('Stop')
        self.button_stop.setFixedHeight(self.widget_hoehe2)
        self.button_stop.setEnabled(False)
        
        'Buttons untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.button_programmErstellen)
        layout.addWidget(self.button_programmBearbeiten)
        layout.addStretch()
        layout.addWidget(self.button_start)
        layout.addWidget(self.button_fortsetzen)
        layout.addWidget(self.button_stop)
        
        'Layout der GroupBox festlegen'
        programm.setLayout(layout)
        
        'GroupBox instanziieren'
        roboter = QGroupBox()
        roboter.setTitle('Roboter')
        
        'Buttons instanziieren'
        self.button_anmelden = QPushButton('Anmelden')
        self.button_anmelden.setFixedHeight(self.widget_hoehe2)
        
        self.button_wartung = QPushButton('Wartung')
        self.button_wartung.setFixedHeight(self.widget_hoehe2)
        self.button_wartung.setVisible(False)
        
        self.button_ausschalten = QPushButton('Ausschalten')
        self.button_ausschalten.setFixedHeight(self.widget_hoehe2)
        
        'Buttons untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.button_anmelden)
        layout.addWidget(self.button_wartung)
        layout.addWidget(self.button_ausschalten)
        
        'Layout der GroupBox festlegen'
        roboter.setLayout(layout)
        
        'Layout von Spalte2 festlegen'
        spalte2 = QVBoxLayout()
        spalte2.addWidget(programm)
        spalte2.addWidget(roboter)
        
        'Spalten nebeneinander anordnen'
        layout = QHBoxLayout()
        layout.addLayout(spalte1)
        layout.addLayout(spalte2)
        
        'Layout der ersten Seite festlegen'
        self.tab1.setLayout(layout)   

    '''Methode grafik_tab2_laden - Die Methode legt das Layout der zweiten
    Seite fest.'''
    def grafik_tab2_laden(self):
        
        'Tab2 instanziieren'
        self.tab2 = QWidget()
        self.tab2.setAutoFillBackground(True)
        self.tab2.setPalette(self.pal)
        self.addTab(self.tab2, 'Programm erstellen')
        self.setTabEnabled(1, False)
        
        'Koordinatenanzeige instanziieren'
        self.anzeige = QKoordinaten()
        self.anzeige.groesse_festlegen(self.widget_breite1, self.widget_hoehe1)
        
        'GroupBox instanziieren'
        erstellen = QGroupBox()
        erstellen.setTitle('Aufnahme')
        
        'Buttons instanziieren'
        self.button_aufnahmeBeginnen = QPushButton('Beginnen')
        self.button_aufnahmeBeginnen.setFixedHeight(self.widget_hoehe1)

        self.button_positionEinlesen = QPushButton('Einlesen')
        self.button_positionEinlesen.setFixedHeight(self.widget_hoehe1)
        self.button_positionEinlesen.setEnabled(False)

        self.button_aufnahmeBeenden = QPushButton('Beenden')
        self.button_aufnahmeBeenden.setFixedHeight(self.widget_hoehe1)
        self.button_aufnahmeBeenden.setEnabled(False)

        self.button_aufnahmeSpeichern = QPushButton('Speichern')
        self.button_aufnahmeSpeichern.setFixedHeight(self.widget_hoehe1)
        self.button_aufnahmeSpeichern.setEnabled(False)

        self.button_zuruecksetzen = QPushButton('Zurücksetzen')
        self.button_zuruecksetzen.setFixedHeight(self.widget_hoehe1)
        self.button_zuruecksetzen.setEnabled(False)

        self.button_aufnahmeAbbrechen = QPushButton('Abbrechen')
        self.button_aufnahmeAbbrechen.setFixedHeight(self.widget_hoehe1)

        'Buttons untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.button_aufnahmeBeginnen)
        layout.addWidget(self.button_positionEinlesen)
        layout.addWidget(self.button_aufnahmeBeenden)
        layout.addWidget(self.button_aufnahmeSpeichern)
        layout.addWidget(self.button_zuruecksetzen)
        layout.addWidget(self.button_aufnahmeAbbrechen)
        
        'Layout der GroupBox festlegen'
        erstellen.setLayout(layout)
        
        'GroupBox instanziieren'
        bearbeiten = QGroupBox()
        bearbeiten.setTitle('Position')
        
        'Buttons instanziieren'
        self.button_positionAnfang = QPushButton('Erste')
        self.button_positionAnfang.setFixedHeight(self.widget_hoehe1)
        
        self.button_positionZurueck = QPushButton('Zurück')
        self.button_positionZurueck.setFixedHeight(self.widget_hoehe1)
        
        self.button_positionAendern = QPushButton('Ändern')
        self.button_positionAendern.setFixedHeight(self.widget_hoehe1)
        
        self.button_positionSpeichern = QPushButton('Speichern')
        self.button_positionSpeichern.setFixedHeight(self.widget_hoehe1)
        self.button_positionSpeichern.setEnabled(False)
        
        self.button_positionVor = QPushButton('Vor')
        self.button_positionVor.setFixedHeight(self.widget_hoehe1)
        
        self.button_positionEnde = QPushButton('Letzte')
        self.button_positionEnde.setFixedHeight(self.widget_hoehe1)
        
        'Buttons untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.button_positionAnfang)
        layout.addWidget(self.button_positionZurueck)
        layout.addWidget(self.button_positionAendern)
        layout.addWidget(self.button_positionSpeichern)
        layout.addWidget(self.button_positionVor)
        layout.addWidget(self.button_positionEnde)
        
        'Layout der GroupBox festlegen'
        bearbeiten.setLayout(layout)
        
        'Stacked Widget - Grafikelemente stapeln'
        self.bedienelemente = QStackedWidget()
        self.bedienelemente.addWidget(erstellen)
        self.bedienelemente.addWidget(bearbeiten)
        self.bedienelemente.setFixedWidth(self.widget_breite2)
        
        'Layout von Spalte1 festlegen'
        spalte1 = QVBoxLayout()
        spalte1.addWidget(self.anzeige)
        spalte1.setAlignment(self.anzeige, Qt.AlignCenter)
        spalte1.addWidget(self.bedienelemente)
          
        'Digitalen Roboter instanziieren'
        self.digRob = DigitalerRoboter()
        
        'GroupBox instanziieren'
        ansicht = QGroupBox()
        ansicht.setTitle('Ansicht')
        
        'Buttons instanziieren'
        self.button_draufsicht = QPushButton('Draufsicht')
        self.button_draufsicht.setCheckable(True)
        self.button_draufsicht.setFixedHeight(self.widget_hoehe1)
        self.button_draufsicht.setEnabled(False)
        
        self.button_seitenansicht = QPushButton('Seitenansicht')
        self.button_seitenansicht.setCheckable(True)
        self.button_seitenansicht.setFixedHeight(self.widget_hoehe1)
        
        self.button_greifer = QPushButton('Greifer')
        self.button_greifer.setCheckable(True)
        self.button_greifer.setFixedHeight(self.widget_hoehe1)
               
        'Buttons nebeneinander anordnen'
        layout = QHBoxLayout()
        layout.addWidget(self.button_draufsicht)
        layout.addWidget(self.button_seitenansicht)
        layout.addWidget(self.button_greifer)
        
        'Layout der GroupBox festlegen'
        ansicht.setLayout(layout)
        
        'Layout von Spalte2 festlegen'
        spalte2 = QVBoxLayout()
        spalte2.addWidget(ansicht)
        spalte2.addWidget(self.digRob)
        
        'Spalten nebeneinander anordnen'
        layout = QHBoxLayout()
        layout.addLayout(spalte1)
        layout.addLayout(spalte2)
        
        'Layout der zweiten Seite festlegen'
        self.tab2.setLayout(layout)    
        
        'Koordinatenanzeige aktualisieren'
        x, y, z = self.digRob.koordinaten_abfragen()
        self.anzeige.koordinaten_aktualisieren(x, y, z)
    
    '''Methode grafik_tab3_laden - Die Methode legt das Layout der dritten
    Seite fest.'''
    def grafik_tab3_laden(self):
        
        'Tab3 instanziieren'
        self.tab3 = QWidget()
        self.tab3.setAutoFillBackground(True)
        self.tab3.setPalette(self.pal)
        self.addTab(self.tab3, 'Programm bearbeiten')
        self.setTabEnabled(2, False)
        
        'GroupBox instanziieren'
        position = QGroupBox()
        position.setTitle('Position')
        
        'Button instanziieren'
        self.button_positionAnzeigen = QPushButton('Anzeigen')
        self.button_positionAnzeigen.setFixedHeight(self.widget_hoehe1)
        self.button_positionAnzeigen.setEnabled(False)
        
        'Button anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.button_positionAnzeigen)
        
        'Layout der GroupBox festlegen'
        position.setLayout(layout)
        
        'GroupBox instanziieren'
        bearbeiten = QGroupBox()
        bearbeiten.setTitle('Bearbeiten')
        
        'Button instanziieren'
        self.button_bearbeitenSchliessen = QPushButton('Schließen')
        self.button_bearbeitenSchliessen.setFixedHeight(self.widget_hoehe1)
        
        'Button anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.button_bearbeitenSchliessen)
        
        'Layout der GroupBox festlegen'
        bearbeiten.setLayout(layout)
        
        'Layout von Zeile1 festlegen'
        zeile1 = QHBoxLayout()
        zeile1.addWidget(position)
        zeile1.addWidget(bearbeiten)
        
        'Tabelle instanziieren'
        self.tabelle = QTableWidget()
        #Tabelle mit 1 Zeile und 4 Spalten
        self.tabelle.setRowCount(1)        
        self.tabelle.setColumnCount(4)
        #Tabelle ohne Rahmen
        self.tabelle.setFrameShape(QFrame.NoFrame)
        #Horizontal Header und Line Counter ausblenden
        self.tabelle.horizontalHeader().setVisible(False)
        self.tabelle.verticalHeader().setVisible(False)
        #Spalten gleich breit machen und an die Tabellenbreite anpassen
        self.tabelle.horizontalHeader().setResizeMode(QHeaderView.Stretch)
        #Manuelle Eingaben sind nicht möglich
        self.tabelle.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #nur die Auswahl ganzer Zeilen ist möglich
        self.tabelle.setSelectionBehavior(QAbstractItemView.SelectRows)
        #die gleichzeitige Auswahl mehrerer Zeilen ist nicht möglich
        self.tabelle.setSelectionMode(QAbstractItemView.SingleSelection)      
        #Hintergrundfarbe der ausgewählten Zeile festlegen
        pal = QPalette()
        pal.setColor(QPalette.Highlight, QColor(181, 175, 181))
        self.tabelle.setPalette(pal)
        #Überschriftenzeile beschriften
        self.tabelle.setItem(0, 0, QTableWidgetItem('Position'))
        self.tabelle.item(0, 0).setTextAlignment(Qt.AlignCenter)
        self.tabelle.item(0, 0).setFlags(Qt.ItemIsEnabled)
        self.tabelle.setItem(0, 1, QTableWidgetItem('X'))
        self.tabelle.item(0, 1).setTextAlignment(Qt.AlignCenter)
        self.tabelle.item(0, 1).setFlags(Qt.ItemIsEnabled)
        self.tabelle.setItem(0, 2, QTableWidgetItem('Y'))
        self.tabelle.item(0, 2).setTextAlignment(Qt.AlignCenter)
        self.tabelle.item(0, 2).setFlags(Qt.ItemIsEnabled)
        self.tabelle.setItem(0, 3, QTableWidgetItem('Z'))
        self.tabelle.item(0, 3).setTextAlignment(Qt.AlignCenter)
        self.tabelle.item(0, 3).setFlags(Qt.ItemIsEnabled)
        
        'Layout von Zeile2 festlegen'
        zeile2 = QVBoxLayout()
        zeile2.addWidget(self.tabelle)

        'Zeilen untereinander anordnen'
        layout = QVBoxLayout()
        layout.addLayout(zeile1)
        layout.addLayout(zeile2)
        
        'Layout der dritten Seite festlegen'
        self.tab3.setLayout(layout)
        
    '''Methode grafik_tab4_laden - Die Methode legt das Layout der vierten
    Seite fest.'''
    def grafik_tab4_laden(self):
        
        'Tab4 instanziieren'
        self.tab4 = QWidget()
        self.tab4.setAutoFillBackground(True)
        self.tab4.setPalette(self.pal)
        self.addTab(self.tab4, 'Fernsteuerung')
        self.setTabEnabled(3, False)
        
#        'GroupBox instanziieren'
#        fernwartung = QGroupBox()
#        fernwartung.setTitle('Fernwartung')
        
        'Textfelder instanziieren'
        self.textfeld1 = QTextEdit()
        self.textfeld1.setFixedHeight(self.widget_hoehe2)
        self.textfeld1.setFixedWidth(self.widget_breite2)
        self.textfeld1.setReadOnly(True)
        self.textfeld1.setText('Verbindungsanfragen:')
                
        self.textfeld2 = QListWidget()
        self.textfeld2.setFixedWidth(self.widget_breite2)
        self.textfeld2.setSelectionMode(QAbstractItemView.SingleSelection)
        
        'Layout von Spalte1 festlegen'
        spalte1 = QVBoxLayout()
        spalte1.addWidget(self.textfeld1)
        spalte1.addWidget(self.textfeld2)
        
        'Textfelder instanziieren'
        self.textfeld3 = QTextEdit()
        self.textfeld3.setFixedHeight(self.widget_hoehe2)
        self.textfeld3.setReadOnly(True)
        self.textfeld3.setFontPointSize(16)
        self.textfeld3.setText('Fernsteuerung inaktiv.')
        
        self.textfeld4 = QListWidget()
        self.textfeld4.setSelectionMode(QAbstractItemView.SingleSelection)
        
        'Button instanziieren'
        self.button_uebertragung = QPushButton('Fernsteuerung zulassen')
        self.button_uebertragung.setFixedHeight(self.widget_hoehe2)
        self.button_uebertragung.setDisabled
        
        'Layout von Spalte2 festlegen'
        spalte2 = QVBoxLayout()
        spalte2.addWidget(self.textfeld3)
        spalte2.addWidget(self.textfeld4)
        spalte2.addWidget(self.button_uebertragung)
        
        'Spalten nebeneinander anordnen'
        layout = QHBoxLayout()
        layout.addLayout(spalte1)
        layout.addLayout(spalte2)
        
#        'Buttons instanziieren'
#        self.button_wartungBeginnen = QPushButton('Beginnen')
#        self.button_wartungBeginnen.setFixedHeight(self.widget_hoehe2)
#        
#        self.button_wartungBeenden = QPushButton('Beenden')
#        self.button_wartungBeenden.setFixedHeight(self.widget_hoehe2)
#        self.button_wartungBeenden.setEnabled(False)
#        
#        self.button_wartungSchliessen = QPushButton('Schließen')
#        self.button_wartungSchliessen.setFixedHeight(self.widget_hoehe2)
#        
#        'Buttons untereinander anordnen'
#        layout = QVBoxLayout()
#        layout.addWidget(self.button_wartungBeginnen)
#        layout.addWidget(self.button_wartungBeenden)
#        layout.addStretch()
#        layout.addWidget(self.button_wartungSchliessen)
#        
#        'Layout der GroupBox festlegen'
#        fernwartung.setLayout(layout)
#        
#        'GroupBox anordnen'
#        layout = QVBoxLayout()
#        layout.addWidget(fernwartung)
        
        
        'Layout der vierten Seite setzen'
        self.tab4.setLayout(layout)
     
    '''Methode grafik_tab5_laden - Die Methode legt das Layout der fünften
    Seite fest.'''
    def grafik_tab5_laden(self): ##
        
        'Tab5 instanziieren'
        self.tab5 = QWidget()
        self.tab5.setAutoFillBackground(True)
        self.tab5.setPalette(self.pal)
        self.addTab(self.tab5, 'Manuelle Steuerung')
#        self.setTabEnabled(3, False)
        
        'Buttons instanziieren'
        self.button_1 = QPushButton('Hoch')
        self.button_1.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_1.setEnabled(False)
        self.button_2 = QPushButton('Runter')
        self.button_2.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_2.setEnabled(False)
        self.button_3 = QPushButton('Links')
        self.button_3.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_3.setEnabled(False)
        self.button_4 = QPushButton('Rechts')
        self.button_4.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_4.setEnabled(False)
        self.button_5 = QPushButton('Vor')
        self.button_5.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_5.setEnabled(False)
        self.button_6 = QPushButton('Rück')
        self.button_6.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_6.setEnabled(False)
        self.button_7 = QPushButton('Auf')
        self.button_7.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_7.setEnabled(False)
        self.button_8 = QPushButton('Zu')
        self.button_8.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_8.setEnabled(False)
        self.button_9 = QPushButton('L.Dreh')
        self.button_9.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_9.setEnabled(False)
        self.button_10 = QPushButton('R.Dreh')
        self.button_10.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_10.setEnabled(False)
        self.button_11 = QPushButton('H.Kipp')
        self.button_11.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_11.setEnabled(False)
        self.button_12 = QPushButton('R.Kipp')
        self.button_12.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_12.setEnabled(False)
        self.button_ManStart = QPushButton('ManStart')
        self.button_ManStart.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_ManStop = QPushButton('ManStop')
        self.button_ManStop.setFixedSize(QSize(self.widget_breite1, \
        self.widget_breite1))
        self.button_ManStop.setEnabled(False)
        
        'Buttons nebeneinander anordnen'
        layout = QGridLayout()
        layout.addWidget(self.button_1, 2, 1)
        layout.addWidget(self.button_2, 2, 2)
        layout.addWidget(self.button_3, 2, 3)
        layout.addWidget(self.button_4, 2, 5)
        layout.addWidget(self.button_5, 1, 4)
        layout.addWidget(self.button_6, 2, 4)
        layout.addWidget(self.button_7, 1, 6)
        layout.addWidget(self.button_8, 1, 7)
        layout.addWidget(self.button_9, 2, 6)
        layout.addWidget(self.button_10, 2, 7)
        layout.addWidget(self.button_11, 3, 6)
        layout.addWidget(self.button_12, 3, 7)
        layout.addWidget(self.button_ManStart, 3, 1)
        layout.addWidget(self.button_ManStop, 3, 2)
        
        'Layout der fünften Seite setzen'
        self.tab5.setLayout(layout)
        
    def button1(self):
        self.motor.steuerung_fern_vektor(0, 0, 4, 0, 0, 0)
        
    def button2(self): 
        self.motor.steuerung_fern_vektor(0, 0, -4, 0, 0, 0)
    
    def button3(self): 
        self.motor.steuerung_fern_vektor(-4, 0, 0, 0, 0, 0)
        
    def button4(self): 
        self.motor.steuerung_fern_vektor(4, 0, 0, 0, 0, 0)

    def button5(self): 
        self.motor.steuerung_fern_vektor(0, 4, 0, 0, 0, 0)
        
    def button6(self): 
        self.motor.steuerung_fern_vektor(0, -4, 0, 0, 0, 0)
        
    def button7(self): 
        self.motor.steuerung_fern_vektor(0, 0, 0, 4, 0, 0)
        
    def button8(self): 
        self.motor.steuerung_fern_vektor(0, 0, 0, -4, 0, 0)
    
    def button9(self): 
        self.motor.steuerung_fern_vektor(0, 0, 0, 0, 0, 0)
        
    def button10(self): 
        self.motor.steuerung_fern_vektor(0, 0, 0, 0, 0, 0)
    
    def button11(self): 
        self.motor.steuerung_fern_vektor(0, 0, 0, 0, 0, 4)
        
    def button12(self): 
        self.motor.steuerung_fern_vektor(0, 0, 0, 0, 0, -4)
        
    def buttonManStart(self):
        self.button_1.setEnabled(True)
        self.button_2.setEnabled(True)
        self.button_3.setEnabled(True)
        self.button_4.setEnabled(True)
        self.button_5.setEnabled(True)
        self.button_6.setEnabled(True)
        self.button_7.setEnabled(True)
        self.button_8.setEnabled(True)
        self.button_9.setEnabled(True)
        self.button_10.setEnabled(True)
        self.button_11.setEnabled(True)
        self.button_12.setEnabled(True)
        self.button_ManStart.setEnabled(False)
        self.button_ManStop.setEnabled(True)
        self.motorsteuerung_manuell()        

        
    def buttonManStop(self):
        self.button_1.setEnabled(False)
        self.button_2.setEnabled(False)
        self.button_3.setEnabled(False)
        self.button_4.setEnabled(False)
        self.button_5.setEnabled(False)
        self.button_6.setEnabled(False)
        self.button_7.setEnabled(False)
        self.button_8.setEnabled(False)
        self.button_9.setEnabled(False)
        self.button_10.setEnabled(False)
        self.button_11.setEnabled(False)
        self.button_12.setEnabled(False)
        self.button_ManStart.setEnabled(True)
        self.button_ManStop.setEnabled(False)
        self.motor.steuerung_fern_aus()

        
        
    '''Methode laden - Die Methode lädt die Lage und Orientierung des 
    Werkzeugkoordinatensystems sowie die Winkel (Denavit-Hartenberg-
    Parameter) und den Öffnungsradius des Greifers und gibt diese zurück.'''
    def laden(self, speichername):
        
        'Arbeitsverzeichnis'
        workdir = getcwd()
        
        'Orientierung des Werkzeugkoordinatensystems'
        dateiname = speichername + '_orientierung.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', \
        dateiname)
        orientierung = load(dir)
        
        'Lage des Werkzeugkoordinatensystems'
        dateiname = speichername + '_lage.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', \
        dateiname)
        lage = load(dir)
        
        'Winkel - Denavit-Hartenberg-Parameter'
        dateiname = speichername + '_winkel.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', \
        dateiname)
        winkel = load(dir)
        
        'Öffnungsradius des Greifers'
        dateiname = speichername + '_greifer.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', \
        dateiname)
        greifer = load(dir)
        
        return orientierung, lage, winkel, greifer


    '''Methode motor_freigeben - gibt die Erlaubnis zur neuen Erstellung eines
    Motorthreads wieder frei. Ohne den Aufruf dieser Funktion kann kein
    weiteres Programm gestartet werden.'''
    
    def motor_freigeben(self):
        self.motor_belegt = False

    '''Methode motorsteuerung - Die Methode erzeugt ein Motor-Objekt,
    übergibt das auszuführende Programm und die Synchronisationszeit
    und lagert das Objekt in einen eigenen Thread aus.'''
    def motorsteuerung(self, speichername, t):
        
        
        if self.motor_belegt == False:
            self.motor_belegt = True
            'QThread-Objekt instanziieren'
            thread_motor = QThread()
            
            'Motor-Objekt instanziieren'
            self.motor = Motor('COM3')
            'Programm übergeben'
            self.motor.programm_laden(speichername)
            'Synchronisationszeit übergeben'
            self.motor.steuerung_synchron(t)
            
            'Motor-Objekt an den Thread übergeben'
            self.motor.moveToThread(thread_motor)
            
            'Signale und Slots verbinden'
            thread_motor.started.connect(self.motor.servo_start)
            self.motor.finished.connect(thread_motor.quit)
            self.motor.finished.connect(self.motor.deleteLater)
            self.motor.finished.connect(self.motor_freigeben)
            thread_motor.finished.connect(thread_motor.deleteLater)
            if speichername != 'programmAus':
                self.motor.start_akt.connect(self.button_start_aktivieren)
                
                
            'Methode start des Thread-Objektes aufrufen'
            thread_motor.start()
            'Methode exec des Thread-Objektes aufrufen'
            thread_motor.exec()
        else:
            print("Motor ist schon in Betrieb")
            
    '''Methode fernsteuerung - Die Methode erzeugt ein Motor-Objekt,
    übergibt den Fernsteuerungsvektor und die Synchronisationszeit
    und lagert das Objekt in einen eigenen Thread aus. Das verwendete Format ist
    eine Veränderung des Ortsvektors und eine Angabe über die Eulerwinkel-
    veränderung.'''
    def motorsteuerung_fern(self):
        
        if self.motor_belegt == False:
            self.motor_belegt = True
            'QThread-Objekt instanziieren'
            thread_motor = QThread()
            
            'Motor-Objekt instanziieren'
            self.motor = Motor('COM3')
            'Fernsteuerungsvektor übergeben'
            self.motor.steuerung_fern()
            'Synchronisationszeit übergeben'
            self.motor.steuerung_synchron(6)
            
            self.server.roboter_fern_vektor.connect\
            (self.motor.steuerung_fern_vektor)
            self.server.roboter_fern_aus.connect(self.motor.steuerung_fern_aus)
            
            'Motor-Objekt an den Thread übergeben'
            self.motor.moveToThread(thread_motor)
            
            'Signale und Slots verbinden'
    #        thread_motor.started.connect(self.motor.steuerung_fern)
            self.motor.finished.connect(thread_motor.quit)
            self.motor.finished.connect(self.motor.deleteLater)
            self.motor.finished.connect(self.motor_freigeben)
            thread_motor.finished.connect(thread_motor.deleteLater)    
            
            
            'Methode start des Thread-Objektes aufrufen'
            thread_motor.start()
            'Methode exec des Thread-Objektes aufrufen'
            thread_motor.exec()
        else:
            print("Motor ist schon in Betrieb")
            
            
    '''Methode motorsteuerung g_code - Die Methode erzeugt ein Motor-Objekt,
    übergibt den Fernsteuerungsvektor und die Synchronisationszeit
    und lagert das Objekt in einen eigenen Thread aus. Das verwendete Format ist
    eine Veränderung des Ortsvektors und eine Angabe über die Eulerwinkel-
    veränderung.'''
    def motorsteuerung_fern_g_code(self):
        
        if self.motor_belegt == False:
            self.motor_belegt = True
            'QThread-Objekt instanziieren'
            thread_motor = QThread()
            
            'Motor-Objekt instanziieren'
            self.motor = Motor('COM3')
            'Fernsteuerungsvektor übergeben'
            self.motor.steuerung_fern_g_code()
            'Synchronisationszeit übergeben'
            self.motor.steuerung_synchron(6)
            
            'Alle G-Code Befehle verknüpfen'
            self.server.roboter_fern_g_code_off.connect(self.motor.steuerung_fern_g_code_off)
            self.server.roboter_fern_g_code_move.connect(self.motor.steuerung_fern_g_code_move)
            self.server.roboter_fern_g_code_pause.connect(self.motor.steuerung_fern_g_code_pause)
            self.server.roboter_fern_g_code_switch_inch.connect(self.motor.steuerung_fern_g_code_switch_inch)
            self.server.roboter_fern_g_code_switch_mm.connect(self.motor.steuerung_fern_g_code_switch_mm)
            self.server.roboter_fern_g_code_notaus.connect(self.motor.steuerung_fern_g_code_notaus)
            self.server.roboter_fern_g_code_aus.connect(self.motor.steuerung_fern_g_code_aus)
            self.server.roboter_fern_g_code_start_programm.connect(self.motor.steuerung_fern_g_code_start_programm)
            self.server.roboter_fern_g_code_stop_programm.connect(self.stop)
            
            'Motor-Objekt an den Thread übergeben'
            self.motor.moveToThread(thread_motor)
            
            'Signale und Slots verbinden'
    #        thread_motor.started.connect(self.motor.steuerung_fern)
            self.motor.finished.connect(thread_motor.quit)
            self.motor.finished.connect(self.motor.deleteLater)
            self.motor.finished.connect(self.motor_freigeben)
            thread_motor.finished.connect(thread_motor.deleteLater)    
            
            
            'Methode start des Thread-Objektes aufrufen'
            thread_motor.start()
            'Methode exec des Thread-Objektes aufrufen'
            thread_motor.exec()
        else:
            print("Motor ist schon in Betrieb")
            
    '''Methode fernsteuerung - Die Methode erzeugt ein Motor-Objekt,
    übergibt den Fernsteuerungsvektor und die Synchronisationszeit
    und lagert das Objekt in einen eigenen Thread aus. Das verwendete Format ist
    eine Veränderung des Ortsvektors und eine Angabe über die Eulerwinkel-
    veränderung.'''
    def motorsteuerung_manuell(self):
        
        if self.motor_belegt == False:
            self.motor_belegt = True
            'QThread-Objekt instanziieren'
            thread_motor = QThread()
            
            'Motor-Objekt instanziieren'
            self.motor = Motor('COM3')
            'Fernsteuerungsvektor übergeben'
            self.motor.steuerung_fern()
            'Synchronisationszeit übergeben'
            self.motor.steuerung_synchron(6)
            

            
            'Motor-Objekt an den Thread übergeben'
            self.motor.moveToThread(thread_motor)
            
            'Signale und Slots verbinden'
    #        thread_motor.started.connect(self.motor.steuerung_fern)
            self.motor.finished.connect(thread_motor.quit)
            self.motor.finished.connect(self.motor.deleteLater)
            self.motor.finished.connect(self.motor_freigeben)
            thread_motor.finished.connect(thread_motor.deleteLater)    
            
            
            'Methode start des Thread-Objektes aufrufen'
            thread_motor.start()
            'Methode exec des Thread-Objektes aufrufen'
            thread_motor.exec()
        else:
            print("Motor ist schon in Betrieb")
            
    '''Methode fernsteuerung - Die Methode erzeugt ein Motor-Objekt,
    übergibt den Fernsteuerungsvektor und die Synchronisationszeit
    und lagert das Objekt in einen eigenen Thread aus. Im Unterschied zur normalen
    Fernsteuerung erlaubt diese Funktion die Übergabe von 6 Motorwinkeln'''
    def motorsteuerung_fern_abs(self):
        
        if self.motor_belegt == False:
            self.motor_belegt = True
            'QThread-Objekt instanziieren'
            thread_motor = QThread()
            
            'Motor-Objekt instanziieren'
            self.motor = Motor('COM3')
            'Fernsteuerungsvektor übergeben'
            self.motor.steuerung_fern()
            'Synchronisationszeit übergeben'
            self.motor.steuerung_synchron(6)
            
            self.server.roboter_fern_abs_vektor.connect\
            (self.motor.steuerung_fern_abs_vektor)
            self.server.roboter_fern_abs_aus.connect(self.motor.steuerung_fern_aus)
            
            'Motor-Objekt an den Thread übergeben'
            self.motor.moveToThread(thread_motor)
            
            'Signale und Slots verbinden'
    #        thread_motor.started.connect(self.motor.steuerung_fern)
            self.motor.finished.connect(thread_motor.quit)
            self.motor.finished.connect(self.motor.deleteLater)
            self.motor.finished.connect(self.motor_freigeben)
            thread_motor.finished.connect(thread_motor.deleteLater)    
            
            
            'Methode start des Thread-Objektes aufrufen'
            thread_motor.start()
            'Methode exec des Thread-Objektes aufrufen'
            thread_motor.exec()        
        else:
            print("Motor ist schon in Betrieb")
            
#    '''Methode fernsteuerung - Die Methode erzeugt ein Motor-Objekt,
#    übergibt den Fernsteuerungsvektor und die Synchronisationszeit
#    und lagert das Objekt in einen eigenen Thread aus.'''
#    def motorsteuerung_fern_vektor(self, p1, p2, p3, p4, p5, p6):
#        
#        print("Motorsteuerung_fern_vektor wird erreicht")
#        self.Greifer_position.emit(p1, p2, p3, p4, p5, p6)
 
     
    '''Methode position_aendern - Die Methode wird nach dem Betätigen von 
    button_positionAendern aufgerufen. In Folge wird der digitale Roboter
    aktiviert. Danach kann dieser zur Korrektur der Position bewegt werden.'''
    def position_aendern(self):
        
        'Information ausgeben'
        print('Position ändern')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_positionAnfang.setEnabled(False)
        self.button_positionZurueck.setEnabled(False)
        self.button_positionAendern.setEnabled(False)
        self.button_positionSpeichern.setEnabled(True)
        self.button_positionVor.setEnabled(False)
        self.button_positionEnde.setEnabled(False)
        
        'Digitalen Roboter aktivieren'
        self.digRob.animation_aktivieren(True)
        self.digRob.geisterstunde(False)
        
    '''Methode programmauswahl_aendern - Die Methode wird nach dem
    wiederholten Betätigen einer Auswahltaste oder von button_auswahlAendern
    ausgeführt. In Folge wird die Auswahl eines Programmes zurückgesetzt 
    (dem Attribut self.programmwahl der Wert None zugewiesen).'''
    def programmauswahl_aendern(self):
        
        'Information ausgeben'
        print('Programmauswahl ändern')
        
        'Attribut zurücksetzen'
        self.programmwahl = None
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_programm1.setChecked(False)
        self.button_programm1.setEnabled(True)
        self.button_programm2.setChecked(False)
        self.button_programm2.setEnabled(True)        
        self.button_programm3.setChecked(False)
        self.button_programm3.setEnabled(True)
        self.button_programm4.setChecked(False)
        self.button_programm4.setEnabled(True)
        self.button_programm5.setChecked(False)
        self.button_programm5.setEnabled(True)
        self.button_auswahlAendern.setEnabled(False)
        self.button_programmBearbeiten.setEnabled(False)
        self.button_start.setEnabled(False)
        
    '''Methode position_anfang - Die Methode wird nach dem Betätigen von
    button_positionAnfang ausgeführt. In Folge wird die erste Zeile der 
    Tabelle ausgewählt und der digitale Roboter aktualisiert.'''
    def position_anfang(self):
    
        'Information ausgeben'
        print('Erste Position aufrufen')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_positionAnfang.setEnabled(False)
        self.button_positionZurueck.setEnabled(False)
        self.button_positionVor.setEnabled(True)
        self.button_positionEnde.setEnabled(True)
        
        'Nummer der ersten Zeile'
        nr = 1
        
        'erste Zeile der Tabelle auswählen'
        self.tabelle.selectRow(nr)
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems und 
        den Öffnungsradius des Greifers auslesen'''
        orientierung, lage, greifer = self.tabelleneintrag_finden(nr)        
        
        'Digitalen Roboter aktualisieren'
        self.digRob.animation_aktualisieren(orientierung, lage, greifer)
        
        'Koordinatenanzeige aktualisieren'
        x, y, z = self.digRob.koordinaten_abfragen()
        self.anzeige.koordinaten_aktualisieren(x, y, z)
    
    '''Methode position_anzeigen - Die Methode wird nach dem Betätigen von
    button_positionAnzeigen ausgeführt. In Folge werden die zweite Seite ge-
    öffnet, die Bedienelemente entsprechend aktiviert oder deaktiviert und
    der digitale Roboter aktualisiert.'''
    def position_anzeigen(self):
                
        'Tab2- Programm erstellen - öffnen und aktivieren'
        self.setCurrentIndex(1)
        self.setTabEnabled(1, True)
        
        'Bedienelemente zum Navigieren durch die Positionen anzeigen'
        self.bedienelemente.setCurrentIndex(1)
        
        'Bedienelement aktivieren/deaktivieren'
        self.button_positionAnzeigen.setEnabled(False)
        
        'Nummer der gewählten Zeile'
        nr = self.tabelle.currentRow()
        
        'Gesamtzeilen'
        zeilen_ges = self.tabelle.rowCount() - 1
        
        'Information ausgeben'
        print('Position ' + str(nr) + ' aufrufen')
        
        'Bedienelemente aktivieren/deaktivieren'
        #es gibt nur eine Zeile
        if zeilen_ges == 1:
            if nr == 1:
                self.button_positionAnfang.setEnabled(False)
                self.button_positionZurueck.setEnabled(False)            
                self.button_positionVor.setEnabled(False)
                self.button_positionEnde.setEnabled(False)
        #es gibt mehr als eine Zeile
        elif zeilen_ges > 1:
            #Auswahl der ersten Zeile
            if nr == 1:
                self.button_positionAnfang.setEnabled(False)
                self.button_positionZurueck.setEnabled(False)
                self.button_positionVor.setEnabled(True)
                self.button_positionEnde.setEnabled(True)
            #Auswahl der zweiten bis vorletzten Zeile
            elif nr > 1 and nr < zeilen_ges:
                self.button_positionAnfang.setEnabled(True)
                self.button_positionZurueck.setEnabled(True)            
                self.button_positionVor.setEnabled(True)
                self.button_positionEnde.setEnabled(True)
            #Auswahl der letzten Zeile
            elif nr == zeilen_ges:
                self.button_positionAnfang.setEnabled(True)
                self.button_positionZurueck.setEnabled(True)            
                self.button_positionVor.setEnabled(False)
                self.button_positionEnde.setEnabled(False)
                
        self.button_positionAendern.setEnabled(True)
        self.button_positionSpeichern.setEnabled(False)
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems und 
        den Öffnungsradius des Greifers auslesen'''
        orientierung, lage, greifer = self.tabelleneintrag_finden(nr)

        'Digitalen Roboter aktualisieren'
        self.digRob.animation_aktualisieren(orientierung, lage, greifer)
        
        'Koordinatenanzeige aktualisieren'
        x, y, z = self.digRob.koordinaten_abfragen()
        self.anzeige.koordinaten_aktualisieren(x, y, z)
        
    '''Methode position_einlesen - Die Methode wird nach dem Betätigen 
    von button_positionEinlesen ausgeführt. In Folge wird die Position
    des Roboters gespeichert. Wenn kein Programm existiert wird eine neue
    Datei mit der Position erstellt. Ansonsten wird das aufgenommene Programm
    geladen, die Position eingefügt und die Datei gespeichert.'''
    def position_einlesen(self):
        
        'Information ausgeben'
        print('Position einlesen')
        
        'Bedienelement aktivieren/deaktivieren'
        self.button_positionEinlesen_aktivieren(False)

        '''Lage und Orientierung des Werkzeugkoordinatensystems sowie
        die Winkel und den Öffnungsradius des Greifers abfragen'''
        orientierung_neu, lage_neu, winkel_neu, greifer_neu = \
        self.digRob.lage_berechnen()
        
        'Speichername'
        speichername = 'programm'
        
        'Fallunterscheidung'
        if self.programmaufnahme == False:
            
            'Position in einer neuen Datei speichern'
            self.speichern(speichername, orientierung_neu, lage_neu, \
            winkel_neu, greifer_neu)
            
            'Attribut self.programmaufnahme auf True setzen'
            self.programmaufnahme = True
            
        elif self.programmaufnahme == True:
            
            'Programm laden'
            orientierung, lage, winkel, greifer = self.laden(speichername)
            
            'Position einfügen'
            orientierung = vstack((orientierung, orientierung_neu))
            lage = vstack((lage, lage_neu))
            winkel = vstack((winkel, winkel_neu))
            greifer = vstack((greifer, greifer_neu))
            
            'Programm speichern'
            self.speichern(speichername, orientierung, lage, \
            winkel, greifer)
            
    '''Methode position_ende - Die Methode wird nach dem Betätigen von
    button_positionEnde ausgeführt. In Folge wird die letzte Zeile der
    Tabelle ausgewählt und der digitale Roboter aktualisiert.'''
    def position_ende(self):
    
        'Information ausgeben'
        print('Letzte Position aufrufen')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_positionAnfang.setEnabled(True)
        self.button_positionZurueck.setEnabled(True)
        self.button_positionVor.setEnabled(False)
        self.button_positionEnde.setEnabled(False)
        
        'Nummer der letzten Zeile'
        nr = self.tabelle.rowCount() - 1
        
        'letzte Zeile der Tabelle auswählen'
        self.tabelle.selectRow(nr)
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems und 
        den Öffnungsradius des Greifers auslesen'''
        orientierung, lage, greifer = self.tabelleneintrag_finden(nr)        
                
        'Digitalen Roboter aktualisieren'
        self.digRob.animation_aktualisieren(orientierung, lage, greifer)
        
        'Koordinatenanzeige aktualisieren'
        x, y, z = self.digRob.koordinaten_abfragen()
        self.anzeige.koordinaten_aktualisieren(x, y, z)
    
    '''Methode position_speichern - Die Methode wird nach dem Betätigen 
    von button_positionSpeichern ausgeführt. In Folge wird der digitale
    Roboter deaktiviert, das Programm geladen, die neuen Einträge erstellt, 
    die Tabelle aktualisiert und das Programm gespeichert.'''
    def position_speichern(self):
        
        'Information ausgeben'
        print('Änderungen speichern')
        
        'Nummer der gewählten Zeile'
        nr = self.tabelle.currentRow()
        
        'Gesamtzeilen'
        zeilen_ges = self.tabelle.rowCount() - 1
        
        'Bedienelemente aktivieren/deaktivieren'
        #es gibt nur eine Zeile
        if zeilen_ges == 1:
            if nr == 1:
                self.button_positionAnfang.setEnabled(False)
                self.button_positionZurueck.setEnabled(False)            
                self.button_positionVor.setEnabled(False)
                self.button_positionEnde.setEnabled(False)
        #es gibt mehr als 1 Zeile        
        elif zeilen_ges > 1:
            #Auswahl der ersten Zeile
            if nr == 1:
                self.button_positionAnfang.setEnabled(False)
                self.button_positionZurueck.setEnabled(False)
                self.button_positionVor.setEnabled(True)
                self.button_positionEnde.setEnabled(True)
            #Auswahl der zweiten bis vorletzten Zeile
            elif nr > 1 and nr < zeilen_ges:
                self.button_positionAnfang.setEnabled(True)
                self.button_positionZurueck.setEnabled(True)            
                self.button_positionVor.setEnabled(True)
                self.button_positionEnde.setEnabled(True)
            #Auswahl der letzten Zeile
            elif nr == zeilen_ges:
                self.button_positionAnfang.setEnabled(True)
                self.button_positionZurueck.setEnabled(True)            
                self.button_positionVor.setEnabled(False)
                self.button_positionEnde.setEnabled(False)
                
        self.button_positionAendern.setEnabled(True)
        self.button_positionSpeichern.setEnabled(False)
        
        'Digitalen Roboter deaktivieren'
        self.digRob.animation_aktivieren(False)
        
        'Progamm laden'
        orientierung, lage, winkel, greifer = \
        self.laden(self.programmwahl)
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems und 
        den Öffnungsradius des Greifers auslesen'''     
        orientierung_neu, lage_neu, winkel_neu, greifer_neu = \
        self.digRob.lage_berechnen()
            
        'Einträge aktualisieren'
        orientierung[nr - 1, :] = orientierung_neu
        lage[nr - 1, :] = lage_neu
        winkel[nr - 1, :] = winkel_neu
        greifer[nr - 1, :] = greifer_neu
        
        'Tabelle zurücksetzen und aktualisieren'
        self.tabelle_zuruecksetzen()
        self.tabelle_aktualisieren(lage)
        
        'Zeile der Tabelle auswählen'
        self.tabelle.selectRow(nr)
        
        'Speichername zuweisen'
        if self.button_programm1.isChecked() == True:
            speichername = 'programm1'            
        elif self.button_programm2.isChecked() == True:            
            speichername = 'programm2'            
        elif self.button_programm3.isChecked() == True:            
            speichername = 'programm3'            
        elif self.button_programm4.isChecked() == True:          
            speichername = 'programm4'      
        elif self.button_programm5.isChecked() == True:
            speichername = 'programm5'
        
        'Programm speichern'
        self.speichern(speichername, orientierung, lage, winkel, greifer)
    
    '''Methode position_vor - Die Methode wird nach dem Betätigen von
    button_positionVor ausgeführt. In Folge wird die nachfolgende Zeile
    der Tabelle gewählt und der digitale Roboter aktualisiert.'''
    def position_vor(self):
        
        'Nummer der aktuelle Zeile'
        nr = self.tabelle.currentRow()
        
        'Nummer der nachfolgenden Zeile'
        nr = nr + 1
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_positionAnfang.setEnabled(True)
        self.button_positionZurueck.setEnabled(True)
        
        'beim Erreichen der letzten Zeile deaktivieren'
        if nr == self.tabelle.rowCount() - 1:
            self.button_positionVor.setEnabled(False)
            self.button_positionEnde.setEnabled(False)
        
        'Information ausgeben'
        print('Position ' + str(nr) + ' aufrufen')
        
        'Zeile der Tabelle auswählen'
        self.tabelle.selectRow(nr)
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems und 
        den Öffnungsradius des Greifers auslesen'''
        orientierung, lage, greifer = self.tabelleneintrag_finden(nr)        
        
        'Digitalen Roboter aktualisieren'
        self.digRob.animation_aktualisieren(orientierung, lage, greifer)
        
        'Koordinatenanzeige aktualisieren'
        x, y, z = self.digRob.koordinaten_abfragen()
        self.anzeige.koordinaten_aktualisieren(x, y, z)
    
    '''Methode position_zurueck - Die Methode wird nach dem Betätigen von
    button_positionZurueck ausgeführt. In Folge wird die vorhergehende Zeile
    der Tabelle gewählt und der digitale Roboter aktualisiert.'''
    def position_zurueck(self):
        
        'Nummer der aktuellen Zeile'
        nr = self.tabelle.currentRow()
        
        'Nummer der vorhergehenden Zeile'
        nr = nr - 1
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_positionVor.setEnabled(True)
        self.button_positionEnde.setEnabled(True)
        
        'beim Erreichen der ersten Zeile deaktivieren'
        if nr == 1:
            self.button_positionAnfang.setEnabled(False)
            self.button_positionZurueck.setEnabled(False)
        
        'Information ausgeben'
        print('Position ' + str(nr) + ' aufrufen')
        
        'Zeile der Tabelle auswählen'
        self.tabelle.selectRow(nr)
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems und 
        den Öffnungsradius des Greifers auslesen'''
        orientierung, lage, greifer = self.tabelleneintrag_finden(nr)        
        
        'Digitalen Roboter aktualisieren'
        self.digRob.animation_aktualisieren(orientierung, lage, greifer)
        
        'Koordinatenanzeige aktualisieren'
        x, y, z = self.digRob.koordinaten_abfragen()
        self.anzeige.koordinaten_aktualisieren(x, y, z)
               
    '''Methode programm_bearbeiten - Die Methode wird nach dem Betätigen 
    von button_programmBearbeiten aufgerufen. In Folge wird die erste Seite
    geschlossen, die dritte Seite geöffnet, das gewählte Programm geladen
    und die Tabelle aktualisiert.'''
    def programm_bearbeiten(self):
        
        'Information ausgeben'
        print('Programm bearbeiten')
        
        'Tab1- Programme - deaktivieren'
        self.setTabEnabled(0, False)
        
        'Tab3- Programm erstellen - öffnen und aktivieren'
        self.setCurrentIndex(2)
        self.setTabEnabled(2, True)
        
        'Programm laden'
        orientierung, lage, winkel, greifer = \
        self.laden(self.programmwahl)
        
        'Tabelle aktualisieren'
        self.tabelle_aktualisieren(lage)
        
    '''Methode programm_erstellen - Die Methode wird nach dem Betätigen
    von button_programmErstellen aufgerufen. In Folge wird die erste Seite
    geschlossen und die zweite Seite geöffnet.'''
    def programm_erstellen(self):
        
        'Information ausgeben'
        print('Programm erstellen')
        
        'Tab1- Programme - deaktivieren'
        self.setTabEnabled(0, False)
        
        'Tab2 - Programm erstellen - öffnen und aktivieren'
        self.setCurrentIndex(1)
        self.setTabEnabled(1, True)
        
    '''Methode programm_oeffnen - Die Methode weist dem Attribut
    self.programmwahl das gewählte Programm zu. Entsprechend der
    Auswahl werden die Bedienelemente aktiviert oder deaktiviert.'''
    def programm_oeffnen(self):
        
        'Bedienelemente aktivieren/deaktivieren'
        #Programm1 gewählt
        if self.button_programm1.isChecked() == True:
            
            nr = 1
            
            self.button_programm2.setEnabled(False)
            self.button_programm3.setEnabled(False)
            self.button_programm4.setEnabled(False)
            self.button_programm5.setEnabled(False)
            
        #Programm2 gewählt
        elif self.button_programm2.isChecked() == True:
            
            nr = 2
            
            self.button_programm1.setEnabled(False)
            self.button_programm3.setEnabled(False)
            self.button_programm4.setEnabled(False)
            self.button_programm5.setEnabled(False)
            
        #Programm3 gewählt
        elif self.button_programm3.isChecked() == True:
            
            nr = 3
            
            self.button_programm1.setEnabled(False)
            self.button_programm2.setEnabled(False)
            self.button_programm4.setEnabled(False)
            self.button_programm5.setEnabled(False)
            
        #Programm4 gewählt
        elif self.button_programm4.isChecked() == True:
            
            nr = 4
            
            self.button_programm1.setEnabled(False)
            self.button_programm2.setEnabled(False)
            self.button_programm3.setEnabled(False)
            self.button_programm5.setEnabled(False)
            
        #Programm5 gewählt
        elif self.button_programm5.isChecked() == True:
            
            nr = 5
            
            self.button_programm1.setEnabled(False)
            self.button_programm2.setEnabled(False)
            self.button_programm3.setEnabled(False)
            self.button_programm4.setEnabled(False)
        
        #wird wiederholt auf einen Button geklickt
        elif self.button_programm1.isChecked() == False or \
        self.button_programm2.isChecked() == False or \
        self.button_programm3.isChecked() == False or \
        self.button_programm4.isChecked() == False or \
        self.button_programm5.isChecked() == False:
            
            nr = 0
            
            'Programmauswahl ändern'
            self.programmauswahl_aendern()
        
        if nr != 0:
            
            'Bedienelemente aktivieren/deaktivieren'
            self.button_auswahlAendern.setEnabled(True)
            self.button_programmBearbeiten.setEnabled(True)
            self.button_start.setEnabled(True)
            
            'Zuweisung'
            self.programmwahl = 'programm' + str(nr)
            
            'Information ausgeben'
            print('Programm ' + str(nr) + ' öffnen')
           
           
    def roboter_zustandsanfrage(self, a_sender):
       
        if self.motor_belegt == False:
            
            self.antwort = "0 0 90 180 0 90 90 56"
            self.server.roboter_zustandsaussage.emit(self.antwort, a_sender)
            
        if self.motor_belegt == True:
            self.antwort = "0"
            self.antwort += self.motor.zustand_anfragen()
            self.server.roboter_zustandsaussage.emit(self.antwort, a_sender)
            
            
    '''Methode schnittstelle_animation_aktualisieren - Die Methode 
    ermöglicht das Aktualisieren des digitalen Roboters über den Server.'''
    def schnittstelle_animation_aktualisieren(self, xe1, ye1, ze1, \
    xe2, ye2, ze2, xe3, ye3, ze3, xP5, yP5, zP5, r6):
        
        'Orientierung des Werkzeugkoordinatensystems'
        orientierung = array([[xe1, ye1, ze1, xe2, ye2, ze2, xe3, ye3, ze3]])
        
        'Lage des Werkzeugkoordinatensystems'
        lage = array([[xP5, yP5, zP5]])
        
        'Öffnungsradius des Greifers'
        greifer = array([[r6]])
        
        'Digitalen Roboter aktualisieren'
        self.digRob.animation_aktualisieren(orientierung, lage, greifer)
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_positionEinlesen_aktivieren(True)
        
    '''Methode schnittstelle_anmelden - Die Methode wird nach dem 
    Betätigen von button_anmelden ausgeführt. In Folge wird die
    Methode zum Starten des Schnittstellenservers aufgerufen.'''
    def schnittstelle_anmelden(self):
        
        'Information ausgeben'
        print('Schnittstellenserver starten')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_programm1.setEnabled(True)
        self.button_programm2.setEnabled(True)
        self.button_programm3.setEnabled(True)
        self.button_programm4.setEnabled(True)
        self.button_programm5.setEnabled(True)
        
        self.button_programmErstellen.setEnabled(True)
        
        self.button_anmelden.setVisible(False)
        self.button_wartung.setVisible(True)
        
        'Methode schnittstelle_oeffnen aufrufen'
        self.schnittstelle_oeffnen()
        
    '''Methode schnittstelle_ansicht_abfragen - Die Methode gibt den 
    Index der angezeigten Ansicht an den Server zurück.'''
    def schnittstelle_ansicht_abfragen(self):
        
        'Index der Ansicht abfragen'
        ind = self.digRob.ansicht.currentIndex()
        
        'Index an den Server zurückgeben'
        self.server.antwort_ansicht(ind)
        
    '''Methode schnittstelle__ansicht_wechseln - Die Methode ermöglicht
    das Wechseln der Ansicht über den Server.'''
    def schnittstelle_ansicht_wechseln(self, ind):
        
        'Ansicht auswählen'
        if ind == 0:
            self.button_draufsicht.setChecked(True)
        elif ind == 1:
            self.button_seitenansicht.setChecked(True)
        elif ind == 2:
            self.button_greifer.setChecked(True)
        
        'Methode ansicht_wechseln aufrufen'
        self.ansicht_wechseln()
        
    '''Methode schnittstelle_aufnahme_speichern - Die Methode 
    ermöglicht das Speichern einer Aufnahme über den Server.'''
    def schnittstelle_aufnahme_speichern(self, speicherplatz):
        
        'Programm laden'
        orientierung, lage, winkel, greifer = self.laden('programm')
        
        'Speichername'
        speichername = 'programm' + str(speicherplatz)
        
        'Programm speichern'
        self.speichern(speichername, orientierung, lage, winkel, greifer)
            
        'Tab1- Programme - öffnen und aktivieren'
        self.setCurrentIndex(0)
        self.setTabEnabled(0, True)
        
        'Tab2 - Programm aufnehmen - deaktivieren'
        self.setTabEnabled(1, False)
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_aufnahmeBeginnen.setEnabled(True)
        self.button_positionEinlesen.setEnabled(False)
        self.button_aufnahmeBeenden.setEnabled(False)
        self.button_aufnahmeSpeichern.setEnabled(False)
        self.button_zuruecksetzen.setEnabled(False)
                
        'Ansicht des digitalen Roboters zurücksetzen'
        self.ansicht_zuruecksetzen(True)
        
        'Digitalen Roboter in den Ausgangszustand versetzen'
        self.digRob.animation_aktivieren(False)
        self.digRob.animation_zuruecksetzen(True)
        
    '''Methode schnittstelle_greifer_abfragen - Die Methode gibt den
    Öffnungsradius des Greifers an den Server zurück.'''
    def schnittstelle_greifer_abfragen(self):
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems sowie
        die Winkel und den Öffnungsradius des Greifers abfragen'''
        orientierung, lage, winkel, greifer = self.digRob.lage_berechnen()
        
        'Öffnungsradius an den Server zurückgeben'
        self.server.antwort_greifer(greifer)
        
    '''Methode schnittstelle_lage_abfragen - Die Methode gibt die Lage des
    Werkzeugkoordinatensystems an den Server zurück.'''
    def schnittstelle_lage_abfragen(self):
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems sowie
        die Winkel und den Öffnungsradius des Greifers abfragen'''
        orientierung, lage, winkel, greifer = self.digRob.lage_berechnen()
        
        'Lage an den Server zurückgeben'
        self.server.antwort_lage(lage)
        
    '''Methode schnittstelle_oeffnen - Die Methode startet den
    Schnittstellenserver parallel zur grafischen Benutzungsoberfläche.'''
    def schnittstelle_oeffnen(self):
        
        'QThread-Objekt instanziieren'
        self.thread_server = QThread()
        
        'Server-Objekt instanziieren'
        self.server = Server()
        
        'Server-Objekt an den Thread übergeben'
        self.server.moveToThread(self.thread_server)
        
        'Signale und Slots verbinden'
        self.thread_server.started.connect(self.server.server_starten)
        
        self.server.animation_akt.connect( \
        self.schnittstelle_animation_aktualisieren)
          
        self.server.ansicht_abf.connect(self.schnittstelle_ansicht_abfragen)
        self.server.ansicht_wec.connect(self.schnittstelle_ansicht_wechseln)
        
        self.server.aufnahme_abb.connect(self.aufnahme_abbrechen)
        self.server.aufnahme_bee.connect(self.aufnahme_beenden)
        self.server.aufnahme_beg.connect(self.aufnahme_beginnen)
        self.server.aufnahme_spe.connect( \
        self.schnittstelle_aufnahme_speichern)
        self.server.aufnahme_zur.connect(self.aufnahme_zuruecksetzen)
        
        self.server.bearbeiten_sch.connect(self.bearbeiten_schliessen)
        
        self.server.lage_abf.connect(self.schnittstelle_lage_abfragen)
        
        self.server.greifer_abf.connect(self.schnittstelle_greifer_abfragen)
        self.server.orientierung_abf.connect( \
        self.schnittstelle_orientierung_abfragen)  
        
        self.server.position_aen.connect(self.position_aendern)
        self.server.position_anf.connect(self.position_anfang)
        self.server.position_anz.connect( \
        self.schnittstelle_position_anzeigen)
        self.server.position_ein.connect(self.position_einlesen)
        self.server.position_end.connect(self.position_ende)
        self.server.position_num.connect( \
        self.schnittstelle_positionsnummer_abfragen)
        self.server.position_spe.connect(self.position_speichern)
        self.server.position_vor.connect(self.position_vor)
        self.server.position_zur.connect(self.position_zurueck)
        
        self.server.programmauswahl_abf.connect( \
        self.schnittstelle_programm_abfragen)
        self.server.programmauswahl_aen.connect(self.programmauswahl_aendern)
        self.server.programm_bea.connect(self.programm_bearbeiten)
        self.server.programm_ers.connect(self.programm_erstellen)
        self.server.programm_ext.connect(self.motorsteuerung)
        self.server.programm_for.connect(self.fortsetzen)
        self.server.programm_sta.connect(self.start)
        self.server.programm_sto.connect(self.stop)
        self.server.programm_wae.connect(self.schnittstelle_programm_oeffnen)
                
        self.server.roboter_fern.connect(self.motorsteuerung_fern)
        self.server.roboter_fern_abs.connect(self.motorsteuerung_fern_abs)
#        self.server.roboter_fern_vektor.connect\
#        (self.motorsteuerung_fern_vektor)
        self.server.roboter_fern_g_code_on.connect(self.motorsteuerung_fern_g_code)
        self.server.roboter_fern_anfrage.connect(self.fernsteuerung_anfrage)
        
        
        self.server.roboter_zustandsanfrage.connect(self.roboter_zustandsanfrage)
        self.server.fernsteuerung_mot.connect(self.server.verbindung_zulassen)
        self.server.roboter_zustandsaussage.connect(self.server.zustandsaussage)
        self.server.server_protokoll.connect(self.server_protokoll_update)
        self.server.tab_abf.connect(self.schnittstelle_tab_abfragen)
        
        self.server.wartung_bee.connect(self.wartung_beenden)
        self.server.wartung_beg.connect(self.wartung_beginnen)
        self.server.wartung_oef.connect(self.wartung_oeffnen)
        self.server.wartung_sch.connect(self.wartung_schliessen)
        
        self.server.winkel_abf.connect(self.schnittstelle_winkel_abfragen)
        
        self.server.finished.connect(self.thread_server.quit)
        self.server.finished.connect(self.server.deleteLater)
        self.thread_server.finished.connect(self.thread_server.deleteLater)
        
        
        'Methode start des Thread-Objektes aufrufen'
        self.thread_server.start()
        'Methode exec des Thread-Objektes aufrufen'
        self.thread_server.exec()
    
    '''Methode schnittstelle_orientierung_abfragen - Die Methode gibt die 
    Orientierung des Werkzeugkoordinatensystems an den Server zurück.'''    
    def schnittstelle_orientierung_abfragen(self):
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems sowie
        die Winkel und den Öffnungsradius des Greifers abfragen'''
        orientierung, lage, winkel, greifer = self.digRob.lage_berechnen()
        
        'Orientierung an den Server zurückgeben'
        self.server.antwort_orientierung(orientierung)
    
    '''Methode schnittstelle_position_abfragen - Die Methode gibt die
    Nummer der angezeigten Position an den Server zurück.'''
    def schnittstelle_positionsnummer_abfragen(self):
        
        'gewählte Nummer abfragen'
        nr = self.tabelle.currentRow()
        
        'Positionsnummer an den Server zurückgeben'
        self.server.antwort_positionsnummer(nr)
        
    '''Methode schnittstelle_position_anzeigen - Die Methode ermöglicht 
    das Anzeigen einer Position über den Server.'''
    def schnittstelle_position_anzeigen(self, nr):
        
        'Zeile in der Tabelle auswählen'
        self.tabelle.selectRow(nr)
        
        'Methode position_anzeigen aufrufen'
        self.position_anzeigen()
        
    '''Methode schnittstelle_programm_abfragen - Die Methode gibt das
    ausgewählte Programm an den Server zurück.'''
    def schnittstelle_programm_abfragen(self):
        
        'Programmauswahl abfragen'
        if self.button_programm1.isChecked() == True:
            nr = 1           
        elif self.button_programm2.isChecked() == True:            
            nr = 2           
        elif self.button_programm3.isChecked() == True:            
            nr = 3         
        elif self.button_programm4.isChecked() == True:          
            nr = 4     
        elif self.button_programm5.isChecked() == True:
            nr = 5
        else:
            nr = 0
            
        'Programmnummer an den Server zurückgeben'
        self.server.antwort_programm(nr)
        
    '''Methode schnittstelle_programm_oeffnen - Die Methode ermöglicht
    das Auswählen eines Programmes über den Server.'''
    def schnittstelle_programm_oeffnen(self, nr):
        
        'Bedienelement auswählen'
        if nr == 1:
            self.button_programm1.setChecked(True)
        elif nr == 2:
            self.button_programm2.setChecked(True)
        elif nr == 3:
            self.button_programm3.setChecked(True)
        elif nr == 4:
            self.button_programm4.setChecked(True)
        elif nr == 5:
            self.button_programm5.setChecked(True)
            
        'Methode programm_oeffnen aufrufen'
        self.programm_oeffnen()
        
    '''Methode schnittstelle_tab_abfragen - Die Methode gibt den Index des
    geöffneten Tabs an den Server zurück.'''
    def schnittstelle_tab_abfragen(self):
        
        'Tabindex abfragen'
        ind = self.currentIndex()
        
        'Tabindex an den Server zurückgeben'
        self.server.antwort_tab(ind)
    
    '''Methode schnittstelle_winkel_abfragen - Die Methode gibt die Winkel
    (Denavit-Hartenberg-Parameter) an den Server zurück.'''
    def schnittstelle_winkel_abfragen(self):
        
        '''Lage und Orientierung des Werkzeugkoordinatensystems sowie
        die Winkel und den Öffnungsradius des Greifers abfragen'''
        orientierung, lage, winkel, greifer = self.digRob.lage_berechnen()
        
        'Winkel an den Server zurückgeben'
        self.server.antwort_winkel(winkel)
        
    def server_protokoll_update(self, sender, nachricht):
        protokoll_eintrag = sender + ': ' + nachricht
        self.nachrichten_protokoll.append(protokoll_eintrag)
        if len(self.nachrichten_protokoll) > 12:
            self.nachrichten_protokoll.pop(0)
            self.textfeld4.clear()
            for index in range(0, len(self.nachrichten_protokoll)):
                self.textfeld4.addItem(self.nachrichten_protokoll[index])
        else:
            self.textfeld4.addItem(protokoll_eintrag)    
        
    '''Methode speichern - Die Methode speichert Lage und Orientierung
    des Werkzeugkoordinatensystems sowie die Winkel (Denavit-Hartenberg-
    Parameter) und den Öffnungsradius des Greifers als Matrizen.'''
    def speichern(self, speichername, orientierung, lage, winkel, greifer):
        
        'Arbeitsverzeichnis'
        workdir = getcwd()
        
        'Orientierung des Werkzeugkoordinatensystems speichern'
        dateiname = speichername + '_orientierung.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', dateiname)
        save(dir, orientierung)
        
        'Lage des Werkzeugkoordinatensystems speichern'
        dateiname = speichername + '_lage.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', dateiname)
        save(dir, lage)
        
        'Winkel (Denavit-Hartenberg-Parameter) speichern'
        dateiname = speichername + '_winkel.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', dateiname)
        save(dir, winkel)
        
        'Öffnungsradius des Greifers speichern'
        dateiname = speichername + '_greifer.npy'
        dir = path.join(workdir, 'speicher', 'programmspeicher', dateiname)
        save(dir, greifer)
        
    '''Methode start - Die Methode wird nach dem Betätigen von 
    button_start ausgeführt. In Folge wird das gewählte Programm
    der Motorsteuerung übergeben.'''
    def start(self):
        
        'Information ausgeben'
        print('Motoren starten')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)
        self.button_wartung.setEnabled(False)
        self.button_ausschalten.setEnabled(False)
        
        'Motorsteuerung'
        speichername = self.programmwahl
        self.motorsteuerung(speichername, t = 3000)   

    '''Methode stop - Die Methode wird nach dem Betätigen von 
    button_stop ausgeführt. In Folge wird der Roboter angehalten.'''
    def stop(self):
        
        'Information ausgeben'
        print('Motoren stoppen')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_programmBearbeiten.setEnabled(True)
        self.button_start.setVisible(False)
        self.button_fortsetzen.setVisible(True)
        self.button_stop.setEnabled(False)
        self.button_wartung.setEnabled(True)
        
        if self.motor is not None:
            self.motor.servo_stop()
        
    '''Methode tabelle_aktualisieren - Die Methode aktualisiert die
    Tabelleneinträge.'''
    def tabelle_aktualisieren(self, lage):
        
        'Format der Lage-Matrix abfragen'
        zeilenzahl, spaltenzahl = lage.shape
                
        'Matrix in Zeilen teilen'
        zeilen = vsplit(lage, zeilenzahl)
        
        'Matrix zeilenweise durchlaufen'
        for i in range(0, zeilenzahl):
            
            'eine leere Zeile am Ende der Tabelle einfügen'
            #an der Stelle i+1 einfügen = in der nächsten Zeile
            self.tabelle.insertRow(i+1)
            
            'fortlaufende Positionsnummer'
            nr = str(i + 1)
            
            'Zeile_i auswählen'
            zeile = zeilen[i]
            
            'Zeile_i in Spalten teilen und Einträge den Koordinaten zuordnen'            
            x, y, z = hsplit(zeile, spaltenzahl)
            
            'Lagekoordinaten'
            x = float(x)
            y = float(y)
            z = float(z)
            
            'fortlaufende Positionsnummer eintragen'
            self.tabelle.setItem(i+1, 0, QTableWidgetItem(nr))
            self.tabelle.item(i+1, 0).setTextAlignment(Qt.AlignCenter)
            
            'Lagekoordinaten des Werkzeugkoordinatensystems eintragen'
            self.tabelle.setItem(i+1, 1, QTableWidgetItem(str(x)))
            self.tabelle.item(i+1, 1).setTextAlignment(Qt.AlignCenter)
            
            self.tabelle.setItem(i+1, 2, QTableWidgetItem(str(y)))
            self.tabelle.item(i+1, 2).setTextAlignment(Qt.AlignCenter)
            
            self.tabelle.setItem(i+1, 3, QTableWidgetItem(str(z)))
            self.tabelle.item(i+1, 3).setTextAlignment(Qt.AlignCenter)

    '''Methode tabelleneintrag_finden - Die Methode sucht in dem 
    geladenen Programm nach einem Eintrag und gibt Lage und Orientierung
    des Werkzeugkoordinatensystems sowie den Öffnungsradius des Greifers
    zurück.'''
    def tabelleneintrag_finden(self, nr):
        
        'Programm laden'
        orientierung, lage, winkel, greifer = \
        self.laden(self.programmwahl)
        
        'Orientierung des Werkzeugkoordinatensystems'
        zeilenzahl, spaltenzahl = orientierung.shape
        zeilen = vsplit(orientierung, zeilenzahl)
        orientierung = zeilen[nr-1]
        
        'Lage des Werkzeugkoordinatensystems'
        zeilenzahl, spaltenzahl = lage.shape
        zeilen = vsplit(lage, zeilenzahl)
        lage = zeilen[nr-1]
        
        'Öffnungsradius des Greifers'
        zeilenzahl, spaltenzahl = greifer.shape
        zeilen = vsplit(greifer, zeilenzahl)
        greifer = zeilen[nr-1]
        
        return orientierung, lage, greifer

    '''Methode tabelle_zuruecksetzen - Die Methode setzt die Tabelle in den
    Ausgangszustand zurück. Dabei werden alle Zeilen, mit Ausnahme der 
    Überschriftenzeile, gelöscht.'''
    def tabelle_zuruecksetzen(self):
        
        'Anzahl der Zeilen'
        zeilenzahl = self.tabelle.rowCount()
        
        #einfach immer Zeile1 löschen, zählt ab 0
        for i in range(1, zeilenzahl):
            
            self.tabelle.removeRow(1)
            
    '''Methode wartung_beginnen - Die Methode wird nach dem Betätigen von
    button_wartungBeginnen ausgeführt.'''
    def wartung_beginnen(self):
        
        'Information ausgeben'
        print('Wartung beginnen')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_wartungBeginnen.setEnabled(False)
        self.button_wartungBeenden.setEnabled(True)
        self.button_wartungSchliessen.setEnabled(False)
        
    '''Methode wartung_beenden - Die Methode wird nach dem Betätigen von
    button_wartungBeenden ausgeführt.'''
    def wartung_beenden(self):
        
        'Information ausgeben'
        print('Wartung beenden')
        
        'Bedienelemente aktivieren/deaktivieren'
        self.button_wartungBeginnen.setEnabled(True)
        self.button_wartungBeenden.setEnabled(False)
        self.button_wartungSchliessen.setEnabled(True)

    '''Methode wartung_oeffnen - Die Methode wird nach dem Betätigen von
    button_wartung ausgeführt. In Folge werden die ersten drei Seiten
    geschlossen und die vierte Seite geöffnet.'''
    def wartung_oeffnen(self):
        
        'Information ausgeben'
        print('Wartung öffnen')
        
        'Tab1, Tab2 und Tab3 deaktivieren'
        self.setTabEnabled(0, True)
        self.setTabEnabled(1, False)
        self.setTabEnabled(2, False)
        
        'Tab4 - Wartung - öffnen und aktivieren'
        self.setCurrentIndex(3)
        self.setTabEnabled(3, True)
    
    '''Methode wartung_schliessen - Die Methode wird nach dem Betätigen von
    button_wartungSchliessen ausgeführt. In Folge wird die vierte Seite 
    geschlossen und die erste Seite geöffnet.'''
    def wartung_schliessen(self):
        
        'Information ausgeben'
        print('Wartung schließen')
        
        'Tab4 - Wartung - deaktivieren'
        self.setTabEnabled(3, False)
        
        'Tab1 - Programme - öffnen und aktivieren'
        self.setCurrentIndex(0)
        self.setTabEnabled(0, True)
       
'Klasse Oberflaeche_Ausschalten'
class Oberflaeche_Ausschalten(QWidget):
    
    'Signal zum Wechseln der Oberfläche definieren'
    wechseln = Signal(int)
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QWidget'
        super(Oberflaeche_Ausschalten, self).__init__(parent)
        
        'Hintergrundfarbe der Oberfläche festlegen'
        self.setAutoFillBackground(True)
        pal = QPalette()
        gradient = QLinearGradient(0, 0, 0, 500)
        gradient.setColorAt(0.0, QColor(255, 255, 255))
        gradient.setColorAt(1.0, QColor(92, 6, 28))
        pal.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(pal)
        
        'Schriftgröße festlegen'
        self.setStyleSheet('QGroupBox {font-size: 14px; \
        font-weight: bold} \
        QLabel {font-size: 14px} \
        QPushButton {font-size: 14px}')
        
        'Höhe der Widgets festlegen'
        self.widget_hoehe = 45
        
        'Methode grafik_laden aufrufen'
        self.grafik_laden()
        
        'Signale und Slots verbinden'
        self.button_neustarten.clicked.connect(self.neustarten)
        
    '''Methode grafik_laden - Die Methode enthält die Grafikelemente der 
    Oberfläche.'''
    def grafik_laden(self):
        
        'GroupBox instanziieren'
        info = QGroupBox()
        info.setTitle('Wichtige Informationen')
        
        'Textfeld instanziieren'
        self.textinfo = QLabel()
        self.textinfo.setFixedHeight(self.widget_hoehe)
        self.textinfo.setText('Roboter festhalten und Hauptschalter umlegen! '
        'Fenster schließen oder Neu starten drücken!')
        
        'Button instanziieren'
        self.button_neustarten = QPushButton('Neu starten')
        self.button_neustarten.setFixedHeight(self.widget_hoehe)
        
        'Textfeld und Button untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(self.textinfo)
        layout.addWidget(self.button_neustarten)
        
        'Layout der GroupBox festlegen'
        info.setLayout(layout)
        
        'GroupBox instanziieren'
        bilder = QGroupBox()
        bilder.setTitle('Parkposition')
        
        'Bilder der Ausgangsposition laden'
        workdir = getcwd()
                
        #Bild Draufsicht
        dateiname = 'bild_draufsicht.svg'
        dir = path.join(workdir, 'speicher', 'bildspeicher', dateiname)
        pix = QPixmap(dir)
        
        bild_draufsicht = QLabel()
        bild_draufsicht.setPixmap(pix)
        bild_draufsicht.setAlignment(Qt.AlignCenter)
        
        #Bild Seitenansicht
        dateiname = 'bild_seitenansicht.svg'
        dir = path.join(workdir, 'speicher', 'bildspeicher', dateiname)
        pix = QPixmap(dir)
                
        bild_seitenansicht = QLabel()
        bild_seitenansicht.setPixmap(pix)
        bild_seitenansicht.setAlignment(Qt.AlignCenter)
        
        'Bilder nebeneinandern anordnen'      
        layout = QHBoxLayout()
        layout.addWidget(bild_draufsicht)
        layout.addWidget(bild_seitenansicht)
        
        'Layout der GroupBox festlegen'
        bilder.setLayout(layout)
                
        'Grafikelemente untereinander anordnen'
        layout = QVBoxLayout()
        layout.addWidget(info)
        layout.addWidget(bilder)
        
        'Layout der Oberfläche festlegen'
        self.setLayout(layout)
        
    '''Methode neustarten - Die Methode wird nach dem Betätigen von
    button_neustarten ausgeführt.'''
    def neustarten(self):
       
        'Information ausgeben'
        print('Neustart')
        
        'Signal zum Wechseln der Oberfläche senden'
        #wechseln zum Startbildschirm
        self.wechseln.emit(0)