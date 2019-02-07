'''
Autor: Martin Schinnerl
Datum: 25.09.2016

Modulbeschreibung:
Das Modul enthält das Hauptprogramm der Robotersteuerung. Im Rahmen
dieser Arbeit wird das Framework Qt zur Erstellung einer grafischen
Benutzungsoberfläche verwendet. Die Funktion hauptprogramm_benutzungs-
oberflaeche beinhaltet alle wesentlichen Anweisungen zum Ausführen
einer mit Qt erstellten grafischen Benutzungsoberfläche. Das Layout
und die Methoden der Oberfläche werden in einer eigenen Klasse (abge-
leitet von QWidget) definiert, importiert und in die Funktion haupt-
programm_benutzungsoberflaeche integriert (Zeile 30). Am Ende wird
die Funktion als Programm ausgeführt (Zeile 48-50). 
'''

'Module importieren'
from grafische_benutzungsoberflaeche.oberflaeche import Oberflaeche
from PyQt4.QtCore import QSize
from PyQt4.QtGui import QApplication, QColor, QPalette
from sys import argv, exit

'Funktion hauptprogramm_benutzungsoberflaeche'
def hauptprogramm_benutzungsoberflaeche():
    
    'Application-Objekt instanziieren'
    app = QApplication(argv)

    'Oberflächen-Objekt instanziieren'
    win = Oberflaeche()
        
    'Attribute von Window setzen'
    #Größe von Window - Raspberry Pi Touchscreen Display 800 x 480 Pixel
    win.setFixedSize(QSize(800, 480))
    #Hintergrundfarbe von Window setzen - Farbe: weiß
    pal = QPalette()
    pal.setColor(QPalette.Window, QColor(255, 255, 255))
    win.setPalette(pal)
    #Schriftart und Schriftgröße von Window setzen
    win.setStyleSheet('font-size: 14px')
    #Titel von Window setzen
    win.setWindowTitle('SMfive Robotics')
    
    'Oberfläche öffnen'
    win.show()
    exit(app.exec_())
        
'Hauptprogramm ausführen'
if __name__ == '__main__':
    hauptprogramm_benutzungsoberflaeche()