# coding: utf8

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
