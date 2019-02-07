# -*- coding: utf-8 -*-
"""
Created on Wed May 24 19:05:17 2017

@author: Thomas
"""

from PyQt4.QtCore import QSize, QThread, pyqtSignal
from PyQt4.QtGui import QApplication, QColor, QPalette, QWidget
from sys import argv, exit


from Sender import Server_sender
from Empfaenger import Server_empfaenger



class widget(QWidget):
    
    'Methode __init__'
    def __init__(self, parent = None):
        
        'Vererbung aller Attribute und Methoden von QWidget'
        super(widget, self).__init__(parent)
        self.fn()

    def fn(self):
        
        'QThread-Objekt instanziieren'
        thread_empfaenger = QThread()
        thread_sender = QThread()
        'Motor-Objekt instanziieren'
        self.empfaenger = Server_empfaenger()
        self.sender = Server_sender()
        'Motor-Objekt an den Thread übergeben'
        self.empfaenger.moveToThread(thread_empfaenger)
        self.sender.moveToThread(thread_sender)    
        
        'Signale und Slots verbinden'
        thread_empfaenger.started.connect(self.empfaenger.starten)
#        self.empfaenger.finished.connect(thread_empfaenger.quit)   
#        self.empfaenger.finished.connect(self.empfaenger.deleteLater)
        thread_empfaenger.finished.connect(thread_empfaenger.deleteLater)
    
        thread_sender.started.connect(self.sender.starten)
#        self.sender.finished.connect(thread_sender.quit)   
#        self.sender.finished.connect(self.sender.deleteLater)
        thread_sender.finished.connect(thread_sender.deleteLater)     
        
        

        'Methode start des Thread-Objektes aufrufen'
        thread_empfaenger.start()
        thread_sender.start()
        'Methode exec des Thread-Objektes aufrufen'
        thread_empfaenger.exec()
        thread_sender.exec()
        
        
 
'Funktion hauptprogramm_benutzungsoberflaeche'
def prim_main():   
    
    'Application-Objekt instanziieren'
    app = QApplication(argv)
    
    'Widget instanziieren'
    win = widget()
    
#    'Attribute von Window setzen'
#    #Größe von Window - Raspberry Pi Touchscreen Display 800 x 480 Pixel
#    win.setFixedSize(QSize(200, 10))
#    #Hintergrundfarbe von Window setzen - Farbe: weiß
#    pal = QPalette()
#    pal.setColor(QPalette.Window, QColor(255, 255, 255))
#    win.setPalette(pal)
#    #Schriftart und Schriftgröße von Window setzen
#    win.setStyleSheet('font-size: 14px')
#    #Titel von Window setzen
#    win.setWindowTitle('SMfive Robotics')
 

    win.show()    
    exit(app.exec_())
    
'Hauptprogramm ausführen'
if __name__ == '__main__':
    prim_main()