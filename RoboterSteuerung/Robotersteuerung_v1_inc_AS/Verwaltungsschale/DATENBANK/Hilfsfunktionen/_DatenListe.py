#==============================================================================
# Hilfsfunktion DatenListe
# Gibt eine Liste der xml-Dateien im Ordner DatenbankDaten
#==============================================================================
from os import getcwd, walk, chdir

def DatenListe():
    string = getcwd()
    string = string.replace('\Hilfsfunktionen', '')
    chdir(string)
    Liste = []

    for ordn in walk('DatenbankDaten'):
        for data in ordn[2]:
            if '.py' in data:
                data = data.replace(data, '')
            elif '.txt' in data:
                data = data.replace(data, '')
            else:
                if '.xml' in data:
                    Liste.append(data)
        break
    return Liste