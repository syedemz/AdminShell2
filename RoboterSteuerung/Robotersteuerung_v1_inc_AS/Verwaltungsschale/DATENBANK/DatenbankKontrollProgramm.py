#==============================================================================
# DatenbankKontrollProgramm
#
# Auswahl eines Modus
# 1. Beispielmodus
# 2. Administratormodus
#==============================================================================
'Importe'
from DatenbankSchnittstelle import XMLClass
from Hilfsfunktionen._Ausgabe import OutputDict
from Hilfsfunktionen._DatenListe import DatenListe
from DatenbankDaten.DatenbankOMMVorlagen import OMMVorlagen
from os import path, getcwd
#==============================================================================
'Input Paket als Dictonary'
# für den Beispielmodus

AufrufDict = {'Suchoption':'SucheDurchName',
              'ArtAusgabe':'ElementName',
              'MengeAusgabe':'alle',
              'Element_Name':'omm:element',
              'Attribut_Name':'',
              'Pfad':'<PlayerCharacter>/<EquippedItems>/<Slot[1]>/<ItemPropertyList>/<ItemProperty>',
              'SucheDurchNameMenge':'alle'}

OMMAufrufDict = {'SuchText':'Memory_App',
                 'SuchArt':'direkt'}

IDDict = {'BlockID':'00000'}

newDict = {'New':'block',
           'Filename':'Testlauf_Erstellen_main.xml',
           'PrimaryID_URL':'http://ichbineinbeispiel/1/',
           'Title english':'#######T#######',
           'Titel deutsch': '#######T#######',
           'Namespace':'',
           'Description english':'#######D#######',
           'Beschreibung deutsch':'#######D#######',
           'Creator':'123456789',
           'Subject':'',
           'ID_URL_Subject':'',
           'Payload':''}

BlockBearbDict = {'BlockID':'00000',
                  'Metadaten':'namespace',
                  'String':'---NEW---'}

#==============================================================================
'DatenbankDaten'

# Dateipfad bis VerwaltungsschaleDatenbank
basispfad = getcwd()
# Dateipfad der DatenbankDaten
Datenordner = path.join(basispfad, "DatenbankDaten")

# Header-Dokument in der XML-Dokumenten-Hierarchie
HauptSpeicher = (Datenordner + '\OMM_Memory_VS_main.xml')

# für den Beispielmodus
Speicher = (Datenordner + '\Testlauf_Erstellen_main.xml') # zum Testen
Speicher2 = (Datenordner + '\Testlauf_Erstellen_123456789.xml') # zum Testen

#==============================================================================
'Eingabe der Anweisungen (Dictonary)'
# für den Administratormodus
def EditDict(Form):
    # Form gibt an, welches Dictonary benötigt wird

    if Form == 1:
        # AufrufDict

        # Eingaben
        print('\nAuswahl:\n',
              '1: SucheDurchPosition\n',
              '2: SucheDurchName\n')
        while True:
            x1 = input('Suchoption: ')
            y1 = None
            if x1 == '1':
                y1 = 'SucheDurchPosition'
                break
            elif x1 == '2':
                y1 = 'SucheDurchName'
                break
            else:
                print('Ungültige Eingabe! Bitte Zahl eingeben.')

        print('\nAuswahl:\n',
              '1: ElementName\n',
              '2: ElementText\n',
              '3: ElementKinder\n',
              '4: Attribut\n',
              '5: AttributName\n')
        while True:
            x2 = input('ArtAusgabe: ')
            y2 = None
            if x2 == '1':
                y2 = 'ElementName'
                break
            elif x2 == '2':
                y2 = 'ElementText'
                break
            elif x2 == '3':
                y2 = 'ElementKinder'
                break
            elif x2 == '4':
                y2 = 'Attribut'
                break
            elif x2 == '5':
                y2 = 'AttributName'
                break
            else:
                print('Ungültige Eingabe! Bitte Zahl eingeben.')

        print('\nAuswahl:\n',
              '1: alle\n',
              '2: erste\n')
        while True:
            x3 = input('MengeAusgabe: ')
            y3 = None
            if x3 == '1':
                y3 = 'alle'
                break
            elif x3 == '2':
                y3 = 'erste'
                break
            else:
                print('Ungültige Eingabe! Bitte Zahl eingeben.')
        x4 = input('Element_Name: ')
        x5 = input('Attribut_Name: ')
        x6 = input('Pfad: ')

        print('\nAuswahl:\n',
              '1: alle\n',
              '2: erste\n')
        while True:
            x7 = input('SucheDurchNameMenge: ')
            y7 = None
            if x7 == '1':
                y7 = 'alle'
                break
            elif x7 == '2':
                y7 = 'erste'
                break
            else:
                print('Ungültige Eingabe! Bitte Zahl eingeben.')

        # Einfügen der Eingaben
        Dict = {'Suchoption':y1,
                'ArtAusgabe':y2,
                'MengeAusgabe':y3,
                'Element_Name':x4,
                'Attribut_Name':x5,
                'Pfad':x6,
                'SucheDurchNameMenge':y7}

    elif Form == 2:
        # OMMAufrufDict

        # Eingaben
        x1 = input('SuchText: ')
        print('\nAuswahl:\n',
              '1: normal\n',
              '2: direkt\n')
        while True:
            x2 = input('SuchArt: ')
            y2 = None
            if x2 == '1':
                y2 = 'normal'
                break
            elif x2 == '2':
                y2 = 'direkt'
                break
            else:
                print('Ungültige Eingabe! Bitte Zahl eingeben.')

        # Einfügen der Eingaben
        Dict = {'SuchText':x1,
                'SuchArt':y2}

    elif Form == 3:
        # IDDict

        # Eingaben
        x1 = input('BlockID: ')

        # Einfügen der Eingaben
        Dict = {'BlockID':x1}

    elif Form == 4:
        #newDict

        # Eingaben
        print('\nAuswahl:\n',
              '1: Dokument\n',
              '2: Block\n')
        while True:
            x1 = input('New: ')
            y1 = None
            if x1 == '1':
                y1 = 'Dokument'
                break
            elif x1 == '2':
                y1 = 'Block'
                break
            else:
                print('Ungültige Eingabe! Bitte Zahl eingeben.')
        x2 = input('Filename: ')
        x3 = input('PrimaryID_URL: ')
        x4 = input('Title english: ')
        x5 = input('Titel deutsch: ')
        x6 = input('Namespace: ')
        x7 = input('Description english: ')
        x8 = input('Beschreibung deutsch: ')
        x9 = input('Creator: ')
        x10 = input('Subject: ')
        x11 = input('ID_URL_Subject: ')
        x12 = input('Payload: ')

        # Einfügen der Eingaben
        Dict = {'New':y1,
                'Filename':x2,
                'PrimaryID_URL':x3,
                'Title english':x4,
                'Titel deutsch':x5,
                'Namespace':x6,
                'Description english':x7,
                'Beschreibung deutsch':x8,
                'Creator':x9,
                'Subject':x10,
                'ID_URL_Subject':x11,
                'Payload':x12}

    elif Form == 5:
        # BlockBearbDict

        # Eingaben
        x1 = input('BlockID: ')
        print('\nAuswahl:\n',
              '1: title english\n',
              '2: Titel deutsch\n',
              '3: description english\n',
              '4: Beschreibung deutsch\n',
              '5: namespace\n',
              '6: subject\n',
              '7: contributor\n',
              '8: format\n',
              '9: type\n')
        while True:
            x2 = input('Metadaten: ')
            y2 = None
            if x2 == '1':
                y2 = 'title english'
                break
            elif x2 == '2':
                y2 = 'Titel deutsch'
                break
            elif x2 == '3':
                y2 = 'description english'
                break
            elif x2 == '4':
                y2 = 'Beschreibung deutsch'
                break
            elif x2 == '5':
                y2 = 'namespace'
                break
            elif x2 == '6':
                y2 = 'subject'
                break
            elif x2 == '7':
                y2 = 'contributor'
                break
            elif x2 == '8':
                y2 = 'format'
                break
            elif x2 == '9':
                y2 = 'type'
                break
            else:
                print('Ungültige Eingabe! Bitte Zahl eingeben.')
        x3 = input('String: ')

        # Einfügen der Eingaben
        Dict = {'BlockID':x1,
                'Metadaten':y2,
                'String':x3}

    else:
        print('Fehler! Form nicht bekannt.')

    return Dict


def Einwilligung():
    while True:
        Antwort = input('Soll die Aktion ausgeführt werden (ja/nein): ')

        if Antwort == 'ja':
            A = 1
            break

        elif Antwort == 'nein':
            A = 0
            break

        else:
            print('Ungültige Eingabe! Bitte antworten Sie mit "ja" oder "nein".')
    return A

#==============================================================================
'Einleitung'

print('\n'
      '==========================================\n'
      ' Willkommen zum DatenbankKontrollProgramm\n'
      '==========================================\n\n'
      ' * Beenden des Programms mit Strg + C\n')

#==============================================================================
'Formatierungshilfen'
DOPPELLINIE =  '==============================================================================='
EINFACHLINIE = '-------------------------------------------------------------------------------'

#==============================================================================
'Auswahl eines Modus'

def Modus():
    try:
        while True:
            print(DOPPELLINIE)
            print('\n'
                  '   Auswahl eines Modus:\n\n'
                  '        1: Beispielmodus\n'
                  '        2: Administratormodus\n'
                  '        3: Automatischer Modus\n')
            print(DOPPELLINIE)

            Konsole = input('Gewünschter Modus: ')
            erg = {'Fehler!':'Eingabe ist dem KontrollProgramm nicht bekannt'}
            if Konsole == '1':
                print('\nBeispielmodus wird gestartet...\n')
                Modus = 1
                break
            if Konsole == '2':
                print('\nAdministratormodus wird gestartet...\n')
                Modus = 2
                break
            if Konsole == '3':
                print('\nAutomatischer Modus wird gestartet...\n')
                Modus = 3
                break

            x = 0 # Prüfer, ob ein Ergebnis ausgegeben werden soll
            print(EINFACHLINIE)
            if x == 0:
                print(OutputDict(erg))

    except KeyboardInterrupt: # mit Strg+C kann jederzeit beendet werden
        print('Beendet')
    return Modus

Modus = Modus()

#==============================================================================
'Beispielmodus'
#dient zur Vorführung des Projekts

if Modus == 1:
    print(DOPPELLINIE)
    print(DOPPELLINIE)
    print()
    print('===========================\n'
          ' DatenbankKontrollProgramm \n'
          ' Beispielmodus\n'
          '===========================\n\n'
          ' * Befehlsübersicht mit help\n')

    helpText = '''\nBefehlsübersicht:\n
        help: Befehlsübersicht (Sie haben sie gerade aufgerufen.)
        data: Liste aller XML-Dateien im Ordner Datenbankdaten

        OMM01: Bsp OMM durchsuchen
        OMM02: Bsp OMM Payload ausgeben
        OMM03: Bsp OMM Titel ausgeben
        OMM04: Bsp OMM Beschreibung ausgeben
        OMM05: Bsp OMM Dokument erstellen oder erweitern
        OMM06: Bsp OMM Dokument in Hierarchie einbetten
        OMM07: Bsp OMM Block bearbeiten
        ...

        Baum: gibt den gesamten XML-Baum aus
        Struktur: gibt Ausgangselement und die Ebene darunter aus
        Wurzel: gibt das Ausgangselement aus
        Auslesen: geeignet für das Auslesen von Daten jeder Art
                  aus XML-Dokumenten beliebiger Form
        \n'''

    try:
        #print(helpText)
        while True:
            print(DOPPELLINIE)
            print(DOPPELLINIE)
            Konsole = input('> ')
            erg = {'Fehler!':'Eingabe ist dem KontrollProgramm nicht bekannt'}
            x = 0 # Prüfer, ob ein Ergebnis ausgegeben werden soll

            if Konsole == 'help' or Konsole == 'Hilfe':
                print(helpText)
                x = 1
            if Konsole == 'data' or Konsole == 'Daten' or Konsole == 'Dateien':
                erg = DatenListe()
                Ergebnis = {'Ergebnis': erg}
                print(EINFACHLINIE)
                print(OutputDict(Ergebnis))
                x = 1

            if Konsole == 'Baum' or Konsole == 'baum' or Konsole =='tree':
                print('\nDieses XML-Dokument wird aufgerufen:\n', Speicher)
                print(EINFACHLINIE)
                erg = XMLClass(Speicher).XMLBaum()
            if Konsole == 'Struktur' or Konsole == 'structure' or Konsole == 'struktur':
                print('\nDieses XML-Dokument wird aufgerufen:\n', HauptSpeicher)
                print(EINFACHLINIE)
                erg = XMLClass(HauptSpeicher).XMLStruktur()
            if Konsole == 'Wurzel' or Konsole == 'root' or Konsole == 'wurzel':
                print('\nDieses XML-Dokument wird aufgerufen:\n', HauptSpeicher)
                print(EINFACHLINIE)
                erg = XMLClass(HauptSpeicher).XMLWurzel()
            if Konsole == 'Auslesen' or Konsole == 'auslesen':
                print('\nDieses XML-Dokument wird aufgerufen:\n', HauptSpeicher)
                print(EINFACHLINIE)
                print('\nDieses Paket wird zum Aufruf eingeschickt:\n', OutputDict(AufrufDict))
                print(EINFACHLINIE)
                erg = XMLClass(HauptSpeicher).XMLAuslesen(AufrufDict)

            if Konsole == 'OMM01' or Konsole == '1':
                print('\nDieses XML-Dokument wird aufgerufen:\n', HauptSpeicher)
                print(EINFACHLINIE)
                print('\nDieses Paket wird zum Aufruf eingeschickt:\n', OutputDict(OMMAufrufDict))
                print(EINFACHLINIE)
                erg = XMLClass(HauptSpeicher).XMLOMMDurchsuchen(OMMAufrufDict)
            if Konsole == 'OMM02' or Konsole == '2':
                print('\nDieses XML-Dokument wird aufgerufen:\n', HauptSpeicher)
                print(EINFACHLINIE)
                print('\nDieses Paket wird zum Aufruf eingeschickt:\n', OutputDict(IDDict))
                print(EINFACHLINIE)
                erg = XMLClass(HauptSpeicher).XMLOMMPayload(IDDict)
            if Konsole == 'OMM03' or Konsole == '3':
                print('\nDieses XML-Dokument wird aufgerufen:\n', Speicher2)
                print(EINFACHLINIE)
                print('\nDieses Paket wird zum Aufruf eingeschickt:\n', OutputDict(IDDict))
                print(EINFACHLINIE)
                erg = XMLClass(Speicher2).XMLOMMTitel(IDDict)
            if Konsole == 'OMM04' or Konsole == '4':
                print('\nDieses XML-Dokument wird aufgerufen:\n', Speicher)
                print(EINFACHLINIE)
                print('\nDieses Paket wird zum Aufruf eingeschickt:\n', OutputDict(IDDict))
                print(EINFACHLINIE)
                erg = XMLClass(Speicher).XMLOMMBeschreibung(IDDict)
            if Konsole == 'OMM05' or Konsole == '5':
                print('\nDieses Paket wird zum Aufruf eingeschickt:\n', OutputDict(newDict))
                print(EINFACHLINIE)
                erg = OMMVorlagen(newDict).XMLOMMErstellung()
            if Konsole == 'OMM06' or Konsole == '6':
                print('\nIn dieses XML-Dokument wird eingebettet:\n', Speicher)
                print(EINFACHLINIE)
                print('\nDieses Paket wird zum Aufruf eingeschickt:\n', OutputDict(newDict))
                print(EINFACHLINIE)
                erg = XMLClass(Speicher).XMLOMMHierarchie(newDict)
            if Konsole == 'OMM07' or Konsole == '7':
                print('\nIn diesem XML-Dokument wird bearbeitet:\n', Speicher)
                print(EINFACHLINIE)
                print('\nDieses Paket wird zum Aufruf eingeschickt:\n', OutputDict(BlockBearbDict))
                print(EINFACHLINIE)
                erg = XMLClass(Speicher).XMLOMMBearbeiten(BlockBearbDict)

            print(EINFACHLINIE)
            if x == 0:
                print(OutputDict(erg))

    except KeyboardInterrupt: # mit Strg+C kann jederzeit beendet werden
        print('Beendet')

#==============================================================================
'Administratormodus'
# alle Befehle/Methoden/... sind manuell aufrufbar

if Modus == 2:
    print(DOPPELLINIE)
    print(DOPPELLINIE)
    print()
    print('===========================\n'
          ' DatenbankKontrollProgramm \n'
          ' Administratormodus\n'
          '===========================\n\n'
          ' * Befehlsübersicht mit help\n')

    helpText = '''\nBefehlsübersicht:\n
      help:   Befehlsübersicht (Sie haben sie gerade aufgerufen.)
      data:   Liste aller XML-Dateien im Ordner Datenbankdaten auflisten

      aktion: eine beliebige Aktion ausführen
        \n'''

    try:
        #print(helpText)
        while True:
            print(DOPPELLINIE)
            print(DOPPELLINIE)
            Konsole = input('> ')
            erg = {'Fehler!':'Eingabe ist dem KontrollProgramm nicht bekannt'}
            x = 0 # Prüfer, ob ein Ergebnis ausgegeben werden soll

            if Konsole == 'help' or Konsole == 'Hilfe' or Konsole == '0' or Konsole == '00':
                print(helpText)
                x = 1
            if Konsole == 'data' or Konsole == 'Daten' or Konsole == 'Dateien':
                erg = DatenListe()
                Ergebnis = {'Ergebnis': erg}
                print(EINFACHLINIE)
                print(OutputDict(Ergebnis))
                x = 1

            if Konsole == 'Aktion' or Konsole == 'aktion' or Konsole == 'action' or Konsole == 'a':
                d = 1
                DatListe = DatenListe()
                print()

                # Ausgabe der Liste aller XML-Dateien
                print('Auswahl der Datei:\n')
                for data in DatListe:
                    print('        ', d, ':', data)
                    d += 1
                print()
                print(EINFACHLINIE)

                # Auswahl einer XML-Datei für die Aktion
                Datei = 'leer'
                AnzahlEintrag = len(DatListe)
                while True:
                    Akt = input('Auswahl einer XML-Datei: ')

                    try:
                        Akt = int(Akt)

                        if Akt > AnzahlEintrag or Akt < 1:
                            print('Keine Datei unter dieser Nummer vorhanden!')
                        else:
                            a = 0
                            for data in DatListe:
                                if Akt == a + 1:
                                    print('\nAuswahl: ', data, '\n')
                                    print(EINFACHLINIE)
                                    Datei = DatListe[a]
                                    DateiPfad = path.join(Datenordner, Datei)
                                    break
                                a += 1

                    except ValueError:
                        print('Bitte eine Zahl angeben!')

                    if Datei != 'leer':
                        break

                # Auswahl der Aktion
                AktionAuswahl = '''\nAuswahl der Aktion:\n
         1: OMM durchsuchen
         2: OMM Payload ausgeben
         3: OMM Titel ausgeben
         4: OMM Beschreibung ausgeben
         5: OMM Dokument erstellen oder erweitern
         6: OMM Dokument in Hierarchie einbetten
         7: OMM Block bearbeiten
         8:     Baum: gibt den gesamten XML-Baum aus
         9:     Struktur: gibt Ausgangselement und die Ebene darunter aus
        10:     Wurzel: gibt das Ausgangselement aus
        11:     Auslesen: geeignet für das Auslesen von Daten jeder Art
                          aus XML-Dokumenten beliebiger Form
        \n'''
                print(AktionAuswahl)
                Aktion = 'leer'
                while True:
                    Akt = input('Auswahl einer Aktion: ')

                    try:
                        Akt = int(Akt)

                        if Akt > 11 or Akt < 1:
                            print('Keine Datei unter dieser Nummer vorhanden!')
                        else:
                            Aktion = str(Akt)
                            if Akt == 1:
                                AktText = 'OMM durchsuchen'
                            if Akt == 2:
                                AktText = 'OMM Payload ausgeben'
                            if Akt == 3:
                                AktText = 'OMM Titel ausgeben'
                            if Akt == 4:
                                AktText = 'OMM Beschreibung ausgeben'
                            if Akt == 5:
                                AktText = 'OMM Dokument erstellen oder erweitern'
                            if Akt == 6:
                                AktText = 'OMM Dokument in Hierarchie einbetten'
                            if Akt == 7:
                                AktText = 'OMM Block bearbeiten'
                            if Akt == 8:
                                AktText = 'Baum'
                            if Akt == 9:
                                AktText = 'Struktur'
                            if Akt == 10:
                                AktText = 'Wurzel'
                            if Akt == 11:
                                AktText = 'Auslesen'

                    except ValueError:
                        print('Bitte eine Zahl angeben!')

                    if Aktion != 'leer':
                        break
                print(EINFACHLINIE)

                # Ausführen der Aktion
                def Zusammenfassung(Datei, AktText, Dict, DateiPfad):
                    print('\nAusgewählte Datei:    ', Datei,
                          '\nAusgewählte Aktion:   ', AktText,
                          '\nErstelltes Dictonary: \n', OutputDict(Dict),
                          '\nDateipfad:', DateiPfad, '\n')

                if Aktion == '1':
                    Dict = EditDict(2)
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLOMMDurchsuchen(Dict)

                if Aktion == '2':
                    Dict = EditDict(3)
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLOMMPayload(Dict)

                if Aktion == '3':
                    Dict = EditDict(3)
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLOMMTitel(Dict)

                if Aktion == '4':
                    Dict = EditDict(3)
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLOMMBeschreibung(Dict)

                if Aktion == '5':
                    Dict = EditDict(4)
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLOMMErstellung(Dict)

                if Aktion == '6':
                    Dict = EditDict(4)
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLOMMHierarchie(Dict)

                if Aktion == '7':
                    Dict = EditDict(5)
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLOMMBearbeiten(Dict)

                if Aktion == '8':
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLBaum()

                if Aktion == '9':
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLStruktur()

                if Aktion == '10':
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLWurzel()

                if Aktion == '11':
                    Dict = EditDict(1)
                    print('Zusammenfassung der Daten:')
                    Zusammenfassung(Datei,AktText,Dict,DateiPfad)

                    Wille = Einwilligung()
                    if Wille == 0:
                        print('\nAbbruch!\n')
                        continue
                    elif Wille == 1:
                        print('\nAktion wird ausgeführt...\n')
                        erg = XMLClass(DateiPfad).XMLAuslesen(Dict)



            print(EINFACHLINIE)
            if x == 0:
                print(OutputDict(erg))

    except KeyboardInterrupt: # mit Strg+C kann jederzeit beendet werden
        print('Beendet')
#==============================================================================
'Automatischer Modus'

# Form des Inputs
#Paket = {'Link':'',
#         'Aktion': '',
#         'Dict':{...}}

if Modus == 3:
    print(DOPPELLINIE)
    print(DOPPELLINIE)    
    print()
    print('===========================\n'
          ' DatenbankKontrollProgramm \n'
          ' Automatischer Modus\n'
          '===========================\n\n'
          
    try: #######################Wieso ist hier ein Fehler ???????????????
        
        while True:
            erg = 'Fehler!'
            
            'Input Paket'
            #...                                    #HIER SOLL ER IMMER BEI LAUFENDEM PROGRAMM AUF EIN PAKET WARTEN
            # Paket = ...
            #
            
            'Verarbeitung Paket'
            Link = HauptSpeicher
            Aktion = None
            Dict = {}
            
            Link = Paket['Link']
            Aktion = Paket['Aktion']
            Dict = Paket['Dict']

            'Aktion durchführen'                    # DAS IST IM MOMENT EGAL; DA KÜMMER ICH MICH SELBST DRUM
            if Aktion == '8':
                erg = {'Ergebnis': DatenListe()}
            if Aktion == '9':
                erg = XMLClass(Link).XMLBaum()
            if Aktion == '10':
                erg = XMLClass(Link).XMLStruktur()
            if Aktion == '11':
                erg = XMLClass(Link).XMLWurzel()
            if Aktion == '12':
                erg = XMLClass(Link).XMLAuslesen(Dict)

            if Aktion == '1':
                erg = XMLClass(Link).XMLOMMDurchsuchen(Dict)
            if Aktion == '2':
                erg = XMLClass(Link).XMLOMMPayload(Dict)
            if Aktion == '3':
                erg = XMLClass(Link).XMLOMMTitel(Dict)
            if Aktion == '4':
                erg = XMLClass(Link).XMLOMMBeschreibung(Dict)
            if Aktion == '5':
                erg = OMMVorlagen(Link).XMLOMMErstellung()
            if Aktion == '6':
                erg = XMLClass(Link).XMLOMMHierarchie(Dict)
            if Aktion == '7':
                erg = XMLClass(Link).XMLOMMBearbeiten(Dict)

            #print(OutputDict(erg))
            'Output Paket'
            #...                                    #HIER SOLL ER EIN PAKET MIT DEM ERGEBNIS ZUSAMMENSTELLEN UND ZURÜCKSENDEN
            #
            #

    except KeyboardInterrupt: # mit Strg+C kann jederzeit beendet werden
        print('Beendet')
    