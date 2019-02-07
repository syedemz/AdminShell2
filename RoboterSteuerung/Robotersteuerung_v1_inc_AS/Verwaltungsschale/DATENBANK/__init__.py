from xml.dom import minidom
from xml.dom import Node
from os import path, getcwd
import time

from VerwaltungsschaleDatenbank.Hilfsfunktionen._Teilstringsuche import TeilStringSuche
from VerwaltungsschaleDatenbank.Hilfsfunktionen._Elementtext import getElementText
from VerwaltungsschaleDatenbank.Hilfsfunktionen._Ausgabe import OutputDict
from VerwaltungsschaleDatenbank.Hilfsfunktionen._Pfad import getXMLpath #,StringSucher, PfadInterpreter
from VerwaltungsschaleDatenbank.DatenbankDaten.DatenbankOMMVorlagen import OMMVorlagen
