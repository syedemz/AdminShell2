# -*- coding: utf-8 -*-
"""
Spyder Editor

Author: Chrisitan Plesker
"""


"""

Funktion zur Kommunikation mittels eines Socket severs
Verwendet wird ZMQ

"""
import os
import sys
"""

Den aktuellen Dateipfad dem Systempfad hinzufügen um eventuelle Problem, beim Finden der Datein, vorzubeugen

"""
aktueller_pfad = os.path.abspath(os.path.dirname(__file__))
uebergeordneter_pfad = os.path.abspath(os.path.join(aktueller_pfad, os.pardir))#os.pardor Funktion zum kombinieren der pfad --> einz drüber

if uebergeordneter_pfad not in sys.path:

    sys.path.insert(0, uebergeordneter_pfad)


from configuration import config
from module import module
import time
"""

Hauptprogramm start

"""
def main():



        #Instanzierung eines zmq socket
    vlacs_empfaenger = module('VLACS_EMPFAENGER', config)     #

    while True:
        """
        Funktion zum erhalten einer Nachricht
        """

        #Nachricht von der Schale empfangen
        nachricht_2 = vlacs_empfaenger.receive()                                       #Warten auf ein Antwort / Kann eventuell darauf verzichtet werden
        kern_2 = vlacs_empfaenger.extract_core(nachricht_2)                            #auspacken der message
        nachricht_2 = kern_2['resource_id']
        
        daten = {"response":"empfangen"}
        ip_adresse = 'http://192.168.0.100:5000'
        pfad = "/vlacs/antwort"
        inhalt = {"request": "POST", "json_data": daten, "ip_address": ip_adresse, "path": pfad }
        anfrage_2 = vlacs_empfaenger.create_message(TO = nachricht_2 ,CORE = inhalt)                             #Funktion ist in module.py        
        vlacs_empfaenger.send(anfrage_2)
        
        


        if nachricht_2 == "weiterleiten":

            print("habe eine nachricht erhalten" + str(nachricht_2))


            """
            Funktion zum verschicken einer Nachricht mit ZMQ
            """
            #Weiterleitung an den Roboter
            adresse = 'API_ROBOTARM'
            inhalt = kern_2['json_data']
            inhalt = inhalt['befehl']
            anfrage_2 = vlacs_empfaenger.create_message(TO = adresse,CORE = inhalt)#Funktion ist in module.py
            vlacs_empfaenger.send(anfrage_2)

            time.sleep(10)

            #Antwort, dass der Roboter sich bewegt hat
            daten = {"response":"weitergeleitet"}
            ip_adresse = 'http://192.168.0.100:5000'
            pfad = "/vlacs/antwort"
            inhalt = {"request": "POST", "json_data": daten, "ip_address": ip_adresse, "path": pfad }
            anfrage_2 = vlacs_empfaenger.create_message(TO = "HTTPOUT" ,CORE = inhalt)                             #Funktion ist in module.py
            vlacs_empfaenger.send(anfrage_2)



        if nachricht_2 == "speichern":

            #Nachricht 2
            inhalt = kern_2['json_data']
            inhalt = inhalt['befehl']

            #Die hinterlegten Werte aus dem String extrahieren
            werte = inhalt.split()
            wert_1 = werte[0]
            wert_2 = werte[1]
            wert_3 = werte[2]

            from vlacs_empfaenger.Kalibrierungsparameter import Parameter
            #Dictionary ersetteln

            add_parameter = {'abweichung_x': wert_1, 'abweichung_y': wert_2, 'gesamtabweichung': wert_3 }
            #An die gewünschte Stelle setzten
            Parameter["Maschine"] = add_parameter

            #Die Syntaxerstellen zum Abspeichern / array wird benötigt, da mtx und dist in numpy.arrays gespecihert werden. Beim Laden ohne numpy importiert gibt dies Probleme
            Parameter = 'Parameter = '+str(Parameter)


            # Den richtige Pfad finden und abspeichern

            workdir = os.getcwd()
            pathToConfFile = os.path.join(workdir, 'FUNCTIONALITY','vlacs_empfaenger','Kalibrierungsparameter.py')
            file = open(pathToConfFile, "w")
            file.write(Parameter)
            file.close()

            #Nachricht an Vlacs, dass erfolgreich gespeichert wurde.

            daten = {'response':'gespeichert'}
            ip_adresse = 'http://192.168.0.100:5000'
            pfad = "/vlacs/antwort"
            inhalt = {"request": "POST", "json_data": daten, "ip_address": ip_adresse, "path": pfad }
            anfrage_2 = vlacs_empfaenger.create_message(TO = "HTTPOUT" ,CORE = inhalt)                             #Funktion ist in module.py
            vlacs_empfaenger.send(anfrage_2)







            except KeyError as e:
                print('KeyError: '+str(e)+' in the vlacs_empfaenger.')
