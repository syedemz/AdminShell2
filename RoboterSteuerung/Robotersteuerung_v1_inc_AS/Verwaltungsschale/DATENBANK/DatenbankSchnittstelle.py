#==============================================================================
# XML Schnittstelle mit DOM
# Klasse zum Auslesen und Bearbeiten von XML-Dateien
#==============================================================================
'Importe'
from xml.dom import minidom
from xml.dom import Node
from os import path, getcwd
import time

from Hilfsfunktionen._Teilstringsuche import TeilStringSuche
from Hilfsfunktionen._Elementtext import getElementText
from Hilfsfunktionen._Ausgabe import OutputDict
from Hilfsfunktionen._Pfad import getXMLpath #,StringSucher, PfadInterpreter
from DatenbankDaten.DatenbankOMMVorlagen import OMMVorlagen

#==============================================================================
'Klasse XML'
class XMLClass():
    #==========================================================================
    # Die Klasse besitzt einerseits allgeimeine Methoden zur Manipulation von XML-Dateien,
    # zum anderen spezielle Methoden zur Manipulation von XML-Dateien im OMM-Format,
    # die mit der Hierarchie dieser Dateien umgehen können
    #==========================================================================
    'Konstruktor'
    # angegebene XML-Datei wird geparst
    def __init__(self, XMLDateiname):
        # minidom-Baumstruktur wird aufgebaut
        self.tree = minidom.parse(XMLDateiname)
        self.XMLDateiname = XMLDateiname

    #==========================================================================
    'OMM:XML durchsuchen '
    def XMLOMMDurchsuchen(self, OMMAufrufDict):
        # durchsucht den Hauptspeicher der Schale nach den angegebenen Schlagwörtern
        # SuchText ist beliebig, SuchArt kann normal oder direkt sein
        print('\nMethode XMLOMMDurchsuchen wird ausgeführt...')

        'Input Paket Dictonary auswerten'
        # Variablen deklarieren:
        SuchText = None
        SuchArt = None

        # Variablen mit Werten versehen:
        SuchText = OMMAufrufDict['SuchText']
        SuchArt = OMMAufrufDict['SuchArt']

        'Titel in Table of Contents mit SuchText vergleichen'
        ToC = self.tree.getElementsByTagName('omm:toc')[0]
        ToCEintraege = ToC.getElementsByTagName('omm:element')

        alletreffer = []
        bestertreffer = []
        maxlen = 1

        for ToCEintrag in ToCEintraege:
            Titel = ToCEintrag.getElementsByTagName('omm:title')
            BlockID = ToCEintrag.attributes['omm:id'].value

            if len(Titel) > 1:
                for T in Titel:
                    Einzeltitel = getElementText(T)

                    if SuchArt == 'normal':
                        ZWErg = TeilStringSuche(Einzeltitel,SuchText)
                        Fazit = ZWErg['Fazit']

                        if Fazit == 'NEIN':
                            None

                        elif Fazit == 'JA':
                            # Trefferdokumentation
                            treffer = {'BlockID': None,
                                       'Titel': None,
                                       'Entdeckung': None}
                            treffer['BlockID'] = BlockID
                            treffer['Titel'] = Einzeltitel
                            treffer['Entdeckung'] = ZWErg['Entd']
                            alletreffer.append(treffer)

                            if len(ZWErg['Entd']) == maxlen:
                                # beste Treffer Liste wird erweitert
                                bestertreffer.append(treffer)

                            elif len(ZWErg['Entd']) > maxlen:
                                # bester Treffer erreicht höheres Level
                                bestertreffer = [treffer]
                                maxlen = len(ZWErg['Entd'])


                    elif SuchArt == 'direkt':

                        if Einzeltitel.find(SuchText) == -1:
                            None

                        else:
                            # Trefferdokumentation
                            treffer = {'BlockID': None,
                                       'Titel': None,
                                       'Entdeckung': None}
                            treffer['BlockID'] = BlockID
                            treffer['Titel'] = Einzeltitel
                            treffer['Entdeckung'] = [SuchText]
                            alletreffer.append(treffer)
                            bestertreffer.append(treffer)

                    else:
                        print('ungültige Eingabe: SuchArt')

            elif len(Titel) == 1:
                Einzeltitel = getElementText(T)

                if SuchArt == 'normal':
                    ZWErg = TeilStringSuche(Einzeltitel,SuchText)
                    Fazit = ZWErg['Fazit']

                    if Fazit == 'NEIN':
                        None

                    elif Fazit == 'JA':
                        treffer = {'BlockID': None,
                                   'Titel': None,
                                   'Entdeckung': None}
                        treffer['BlockID'] = BlockID
                        treffer['Titel'] = Einzeltitel
                        treffer['Entdeckung'] = ZWErg['Entd']
                        alletreffer.append(treffer)

                        if len(ZWErg['Entd']) == maxlen:
                            # beste Treffer Liste wird erweitert
                            bestertreffer.append(treffer)

                        elif len(ZWErg['Entd']) > maxlen:
                            # bester Treffer erreicht höheres Level
                            bestertreffer = [treffer]

                elif SuchArt == 'direkt':

                    if Einzeltitel.find(SuchText) == -1:
                        None

                    else:
                        # Trefferdokumentation
                        treffer = {'BlockID': None,
                                   'Titel': None,
                                   'Entdeckung': None}
                        treffer['BlockID'] = BlockID
                        treffer['Titel'] = Einzeltitel
                        treffer['Entdeckung'] = [SuchText]
                        alletreffer.append(treffer)
                        bestertreffer.append(treffer)

                else:
                        print('ungültige Eingabe: SuchArt')



        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        erg = {'alle Treffer': alletreffer,
               'bester Treffer': bestertreffer}
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis

    #==========================================================================
    'OMM:XML bestimmten Payload ausgeben '
    def XMLOMMPayload(self, IDDict):
        # gibt den Payload eines Blocks aus, dessen BlockID angegeben wird
        print('\nMethode XMLOMMPayload wird ausgeführt...')

        'Input Paket Dictonary auswerten'
        ID = None
        ID = IDDict['BlockID']

        Blocks = self.tree.getElementsByTagName('omm:block')
        Anzahl = len(Blocks)

        if Anzahl == 1:
            IDBl = Blocks[0].attributes['omm:id'].value
            if ID == IDBl:
                Payload = Blocks[0].getElementsByTagName('omm:payload')[0]

        elif Anzahl > 1:
            for Block in Blocks:
                IDBl = Block.attributes['omm:id'].value
                if ID == IDBl:
                    Payload = Block.getElementsByTagName('omm:payload')[0]
        else:
            print('Fehler')

        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        erg = getElementText(Payload)
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis

    #==========================================================================
    'OMM:XML alle Titel aus ToC ausgeben'
    def XMLOMMTitel(self, IDDict):
        # gibt den Titel eines Blocks aus, dessen BlockID angegeben wird
        print('\nMethode XMLOMMTitel wird ausgeführt...')

        'Input Paket Dictonary auswerten'
        ID = None
        ID = IDDict['BlockID']

        Blocks = self.tree.getElementsByTagName('omm:block')

        if len(Blocks) == 1:
            IDBl = Blocks[0].attributes['omm:id'].value
            if ID == IDBl:
                TitleList = Blocks[0].getElementsByTagName('omm:title')
                if len(TitleList) == 1:
                    TitleList = Blocks[0].getElementsByTagName('omm:title')[0]
                    erg = getElementText(TitleList)

                elif len(TitleList) > 1:
                    erg = []
                    for Title in TitleList:
                        Erg = getElementText(Title)
                        erg.append(Erg)

        elif len(Blocks) > 1:
            for Block in Blocks:
                IDBl = Block.attributes['omm:id'].value
                if ID == IDBl:
                    TitleList = Block.getElementsByTagName('omm:title')
                    if len(TitleList) == 1:
                        TitleList = Blocks.getElementsByTagName('omm:title')[0]
                        erg = getElementText(TitleList)

                    elif len(TitleList) > 1:
                        erg = []
                        for Title in TitleList:
                            Erg = getElementText(Title)
                            erg.append(Erg)

        else:
            print('Fehler')



        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis

    #==========================================================================
    'OMM:XML alle Beschreibungen aus ToC ausgeben '
    def XMLOMMBeschreibung(self, IDDict):
        # gibt die Beschreibung eines Blocks aus, dessen BlockID angegeben wird
        print('\nMethode XMLOMMBeschreibung wird ausgeführt...')

        'Input Paket Dictonary auswerten'
        ID = None
        ID = IDDict['BlockID']

        Blocks = self.tree.getElementsByTagName('omm:block')

        if len(Blocks) == 1:
            IDBl = Blocks[0].attributes['omm:id'].value
            if ID == IDBl:
                DescrList = Blocks[0].getElementsByTagName('omm:description')
                if len(DescrList) == 1:
                    DescrList = Blocks[0].getElementsByTagName('omm:description')[0]
                    erg = getElementText(DescrList)

                elif len(DescrList) > 1:
                    erg = []
                    for Descr in DescrList:
                        Erg = getElementText(Descr)
                        erg.append(Erg)

        elif len(Blocks) > 1:
            for Block in Blocks:
                IDBl = Block.attributes['omm:id'].value
                if ID == IDBl:
                    DescrList = Block.getElementsByTagName('omm:description')
                    if len(DescrList) == 1:
                        DescrList = Blocks.getElementsByTagName('omm:description')[0]
                        erg = getElementText(DescrList)

                    elif len(DescrList) > 1:
                        erg = []
                        for Descr in DescrList:
                            Erg = getElementText(Descr)
                            erg.append(Erg)

        else:
            print('Fehler')

        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis

    #==========================================================================
    'OMM:XML XML-Dokument in Dokumentenhierarchie einfügen'
    def XMLOMMHierarchie(self, newDict):
        # trägt ein neu erstelltes XML-Dokument in die Hierarchie der Dokumente ein
        # dafür wird XMLClass mit Eltern-Dokument gestartet und das Kind-Dokument
        #   im Dictonary angegeben
        print('\nMethode XMLOMMHierarchie wird ausgeführt...')

        'Dateipfad von einzufügendem Dokument für Payload aufstellen'
        KindDokument = newDict['Filename']
        Link = None
        basispfad = getcwd() # Dateipfad bis VerwaltungsschaleDatenbank
        Link = path.join(basispfad, 'DatenbankDaten\\', KindDokument)

        'Anpassungen Dictonary'
        newDict['Filename'] = self.XMLDateiname
        newDict['New'] = 'Block'
        newDict['Payload'] = Link # hier muss Dateipfad rein

        'Block mit ToC-Eintrag wird erstelllt'
        Erg = OMMVorlagen(newDict).XMLOMMErstellung()

        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        erg = Erg
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis

    #==========================================================================
    def XMLOMMBearbeiten(self, BlockBearbDict):
        # angegeben wird ein Block der von XMLClass geparstem Dokument
        # nun kann mit den Angaben Metadaten und String die Metadaten ergänzt/ ersetzt werden
        # Auswahl Metadaten:
        # String sind die Daten, die hinzugefügt werden sollen
        print('\nMethode XMLOMMBearbeiten wird ausgeführt...')
        print()

        'Input Paket Dictonary auswerten'
        # Variablen deklarieren:
        ID = None
        Metadaten = None
        String = None

        # Variablen mit Werten versehen:
        ID = BlockBearbDict['BlockID']
        Metadaten = BlockBearbDict['Metadaten']
        String = BlockBearbDict['String']

        'Funktion Metadaten bearbeiten'
        def BearbMetadaten(MD, String):
            # für die Bearbeitung der xml-Datei wird diese geöffnet
            # wählt die Metadaten aus und erstellt oder ersetzt diese
            newChild = self.tree.createTextNode(String)

            #'Bearbeitung Metadaten: Titel'
            if MD == 'title english' or MD == 'title' or MD == 'Titel' or MD == 'Titel deutsch':

                #Bearbeitung
                List = Blocks.getElementsByTagName('omm:title')
                for T in List:
                    if MD == 'title english' or MD == 'title':
                        if T.getAttribute('xml:lang') == 'en':
                            oldChild = T.firstChild # Text-Node
                            T.replaceChild(newChild, oldChild)
                            xx = T

                    if MD == 'Titel' or MD == 'Titel deutsch':
                        if T.getAttribute('xml:lang') == 'de':
                            oldChild = T.firstChild # Text-Node
                            T.replaceChild(newChild, oldChild)
                            xx = T

            #'Bearbeitung Metadaten: Beschreibung'
            elif MD == 'description english' or MD == 'description' or MD == 'Beschreibung' or MD == 'Beschreibung deutsch':

                'Bearbeitung'
                List = Blocks.getElementsByTagName('omm:description')
                for D in List:
                    if MD == 'description english' or MD == 'description':
                        if D.getAttribute('xml:lang') == 'en':
                            oldChild = D.firstChild # Text-Node
                            D.replaceChild(newChild, oldChild)
                            xx = D

                    if MD == 'Beschreibung' or MD == 'Beschreibung deutsch':
                        if D.getAttribute('xml:lang') == 'de':
                            oldChild = D.firstChild # Text-Node
                            D.replaceChild(newChild, oldChild)
                            xx = D

            #'Bearbeitung Metadaten: Namespace'
            elif MD == 'Namespace' or MD == 'namespace':
                E = Blocks.getElementsByTagName('omm:namespace')[0]
                oldChild = E.firstChild
                E.replaceChild(newChild, oldChild)
                xx = E

            #'Bearbeitung Metadaten: Subject'
            elif MD == 'Subject' or MD == 'subject':
                E = Blocks.getElementsByTagName('omm:subject')[0]
                newTag = self.tree.createElement('omm:tag')
                T = E.appendChild(newTag)
                T.setAttribute('omm:type', 'text')
                T.appendChild(newChild)
                xx = E

            #'Bearbeitung Metadaten: Creation'
            # keine Bearbeitung möglich, da dies eine feste Angabe ist

            #'Bearbeitung Metadaten: Payload'
            # keine Bearbeitung möglich, da dies eine feste Angabe ist

            #'Bearbeitung Metadaten: Contributor'
            elif MD == 'contribution' or MD == 'contributor' or MD == 'Beitrag':
                Date = time.strftime("%Y-%m-%dT%H:%M:%S") # String mit Datum und Uhrzeit
                newTime = self.tree.createTextNode(Date)

                try: # Versuche zu ändern
                    C = Blocks.getElementsByTagName('omm:contribution')[0]
                    P = C.getElementsByTagName('omm:contributor')[0]
                    D = C.getElementsByTagName('omm:date')[0]
                    oldChild = P.firstChild # Text-Node
                    oldChild2 = D.firstChild # Text-Node
                    P.replaceChild(newChild, oldChild)
                    D.replaceChild(newTime, oldChild2)
                    xx = C

                except IndexError: # sonst neu erstellen
                    newContribution = self.tree.createElement('omm:contribution')
                    newContributor = self.tree.createElement('omm:contributor')
                    newPerson = self.tree.createTextNode(String)
                    newDate = self.tree.createElement('omm:date')
                    C = Blocks.appendChild(newContribution)
                    P = C.appendChild(newContributor)
                    D = C.appendChild(newDate)
                    P.setAttribute('omm:type', 'duns')
                    D.setAttribute('omm:encoding', 'ISO8601')
                    P.appendChild(newPerson)
                    D.appendChild(newTime)
                    xx = C

            #'Bearbeitung Metadaten: Format'
            elif MD == 'format' or MD == 'Format':

                try: # Versuche zu ändern
                    F = Blocks.getElementsByTagName('omm:format')[0]
                    oldChild = F.firstChild
                    F.replaceChild(newChild, oldChild)
                    xx = F

                except IndexError: # sonst neu erstellen
                    newFormat = self.tree.createElement('omm:format')
                    newText = self.tree.createTextNode(String)
                    F = Blocks.appendChild(newFormat)
                    F.setAttribute('omm:encryption', 'none')
                    F.setAttribute('omm:schema', 'http://dummy.org/sample.xsd')
                    F.appendChild(newText)
                    xx = F


            #'Bearbeitung Metadaten: Type'
            elif MD == 'Type' or MD == 'type' or MD == 'typ' or MD == 'Typ':

                try: # Versuche zu ändern
                    T = Blocks.getElementsByTagName('omm:type')[0]
                    oldChild = T.firstChild
                    T.replaceChild(newChild, oldChild)
                    xx = T

                except IndexError: # sonst neu erstellen
                    newFormat = self.tree.createElement('omm:type')
                    newText = self.tree.createTextNode(String)
                    T = Blocks.appendChild(newFormat)
                    T.appendChild(newText)
                    xx = T

            else:
                print('Fehler')


            'Änderungen in Datei speichern'
            Endversion = self.tree.toxml()
            Dokument = open(self.XMLDateiname, 'w')
            Dokument.write(Endversion)
            Dokument.close()

            print(xx.toprettyxml())
            xxx = xx.toxml()
            Erg = str(xxx)
            return Erg


        'Block auswählen und bearbeiten'
        Blocks = self.tree.getElementsByTagName('omm:block')
        Anzahl = len(Blocks)

        if Anzahl == 1:
            IDBl = Blocks[0].attributes['omm:id'].value
            if ID == IDBl:
                Blocks = Blocks[0]
                erg = BearbMetadaten(Metadaten, String)
            else:
                erg = 'Kein Block dieser BlockID auffindbar'

        elif Anzahl > 1:
            for Block in Blocks:
                IDBl = Block.attributes['omm:id'].value
                if ID == IDBl:
                    Blocks = Block
                    erg = BearbMetadaten(Metadaten, String)
                    break
        else:
            print('Fehler')

        'ToC-Eintrag auswählen und bearbeiten'
        ToCBlocks = self.tree.getElementsByTagName('omm:element')
        Anzahl = len(ToCBlocks)

        if Anzahl == 1:
            IDBl = ToCBlocks[0].attributes['omm:id'].value
            if ID == IDBl:
                Blocks = ToCBlocks[0]
                erg = BearbMetadaten(Metadaten, String)
            else:
                erg = 'Kein Eintrag im ToC des Blocks dieser BlockID auffindbar'

        elif Anzahl > 1:
            for Block in ToCBlocks:
                IDBl = Block.attributes['omm:id'].value
                if ID == IDBl:
                    Blocks = Block
                    erg = BearbMetadaten(Metadaten, String)
                    break
        else:
            print('Fehler')


        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis


    #==========================================================================
    #==========================================================================
    #==========================================================================
    'Ausgabe der gesamten XML'
    def XMLBaum(self):
        # gibt den XMLBaum aus
        print('\nMethode XMLAusgabeBaum wird ausgeführt...')

        Baum = self.tree.childNodes[0].toxml()
        print(Baum)
        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        erg = str(Baum)
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis


    #==========================================================================
    'Ausgabe WurzelElement'
    def XMLWurzel(self):
        # gibt das WurzelElement des XML-Baums aus
        print('\nMethode XMLWurzel wird ausgeführt...')

        WurzelElement = self.tree.childNodes[0].nodeName

        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        erg = {'Wurzelelement': WurzelElement}
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis

    #==========================================================================
    'Schrittweises manuelles Durchsuchen des XML-Dokuments'
    def XMLStruktur(self):
        # gibt die grobe Struktur der XML aus
        print('\nMethode XMLStruktur wird ausgeführt...')

        # WurzelElement
        WurzelElement = self.tree.childNodes[0]

        # erste Ebene
        ElementEbene01 = WurzelElement.childNodes
        kinderlist = []
        for E in ElementEbene01:
            if E.nodeType == Node.ELEMENT_NODE:
                kinderlist.append(E.nodeName)

        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        erg = {'Wurzelelement':WurzelElement.nodeName,
               'Kindelemenete des Wurzelelements': kinderlist}
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis

    #==========================================================================
    'gewünschte Teile der XMLDatei auslesen'
    def XMLAuslesen(self, AufrufDict):
        # Suchoptinon (SucheDurchPosition, SucheDurchName)
        # ArtAusgabe (ElementName, ElementText, ElementKinder, Attribut, AttributName)
        # MengeAusgabe (alle, erste)
        # Element_Name
        # Attribut_Name
        # Pfad (<Wurzel>/<ElementName>/<ElementName[Z]>) (Syntax einhalten)
        # SucheDurchNameMenge (alle, erstes)
        print('\nMethode XMLAuslesen wird ausgeführt...')


        'Prüfung Paket auf Korrektheit'
        # Prüfung der Länge als erstes Indiz für die korrekte Angabe des Pakets:
        if len(AufrufDict) == 8:
            print('Prüfung...\nPaket wahrscheinlich korrekt.\n')
        else:
            print('Mit Paket stimmt was nicht.')


        'Input Paket Dictonary auswerten'
        # Variablen deklarieren:
        Suchoption = None
        ArtAusgabe = None
        MengeAusgabe = None
        Element_Name = None
        #Attribut_Name = None
        Pfad = None
        SucheDurchNameMenge = None

        # Variablen mit Werten versehen:
        Suchoption = AufrufDict['Suchoption']
        ArtAusgabe = AufrufDict['ArtAusgabe']
        MengeAusgabe = AufrufDict['MengeAusgabe']
        Element_Name = AufrufDict['Element_Name']
        #Attribut_Name = AufrufDict['Attribut_Name']
        Pfad = AufrufDict['Pfad']
        SucheDurchNameMenge = AufrufDict['SucheDurchNameMenge']


        'XMLpath aus Pfad ermitteln'
        # Syntax: <Wurzel>/<ElementName>/<ElementName[Z]>
        # [Z] gibt an, das wievielte KindElement mit dem Namen <...>
        # des davor angegebenen Elements gemeint ist;
        # keine Angabe von [Z] meint automatisch das einzige (erste) Kindelement


        'Auswertung Suchoption'
        if Suchoption == 'SucheDurchPosition':
            Wurzel = self.tree.childNodes[0]
            XMLpath = getXMLpath(Wurzel, Pfad) # als Liste speichern
            #auswerten/durch Baum manövrieren
            auswahl = []
            print('Durch XMLpath ausgewählte(s) Element(e):')
            try:
                for E in XMLpath:
                        if E.nodeType == Node.ELEMENT_NODE:
                            auswahl.append(E)
                for a in auswahl:
                    print(a)

            except (AttributeError, TypeError):
                print(XMLpath)

        elif Suchoption == 'SucheDurchName':
            # ElementName wird verarbeitet
            ListElement_Name = self.tree.getElementsByTagName(Element_Name)

            'Auswertung SucheDurchNameMenge'
            if SucheDurchNameMenge == 'erstes':
                XMLpath = ListElement_Name[0]
                ElementMenge = 1
                print(XMLpath, '\n')

            elif SucheDurchNameMenge == 'alle':
                XMLpath = ListElement_Name
                ElementMenge = len(XMLpath)

                if ElementMenge == 1:
                    XMLpath = ListElement_Name[0]
                    print(XMLpath)
                elif ElementMenge > 1:
                    g = 0
                    while g < ElementMenge:
                        print(XMLpath[g])
                        g += 1


            else:
                print('Ungültige Angabe der SucheDurchNameMenge!')
                print('Auswahl: alle, erstes')


        else:
            print('Ungültige Angabe der Suchoption!')
            print('Auswahl: SucheDurchPosition, SucheDurchName')


        'XMLpath: Anzahl der Elemente herausfinden'
        # es muss differenziert werden, welchen Typs der Pfad ist
        # es gibt:
        #       <class 'xml.dom.minidom.Element'>
        #       <class 'xml.dom.minicompat.NodeList'>

        try:
            RohMenge = XMLpath.length
            if RohMenge > 1:
                ElementMenge = 0
                for E in XMLpath:
                    if E.nodeType == Node.ELEMENT_NODE:
                        ElementMenge += 1

        except (AttributeError):
            if XMLpath.nodeType == Node.ELEMENT_NODE:
                ElementMenge = 1
            else:
                print('Fehler bei Pfad! Keine Elemente gefunden.')
        print('\nAnzahl ausgewählter Elemente: %s\n' % ElementMenge)


        'Auswertung ArtAusgabe'
        # Auswahl: ElementName, ElementText, ElementKinder, Attribut, AttributName
        # XMLpass gibt jetzt konkrete Elemente mit Pfad vor, ...
        # ... deren Infos nun ausgegeben werden soll

        if ArtAusgabe == 'ElementName':
            # ist nicht immer sinnvoll aufzurufen, da man evtl. über den Namen gesucht hat

            # für XMLpath mit einem ausgewählten Element:
            if ElementMenge == 1:
                if XMLpath.nodeType == Node.ELEMENT_NODE:
                    print(XMLpath.nodeName)
                else:
                    print('Fehler')

            # für XMLpath mit mehreren ausgewählten Elementen:
            elif ElementMenge > 1:
                # für MengeAusgabe 'alle' oder 'erste':
                for E in XMLpath:
                    if E.nodeType == Node.ELEMENT_NODE:
                        print(E.nodeName)
                        if MengeAusgabe == 'erste':
                            break

            #Ergebnis =

        elif ArtAusgabe == 'ElementText':

            # für XMLpath mit einem ausgewählten Element:
            if ElementMenge == 1:
                print(getElementText(XMLpath))

            # für XMLpath mit mehreren ausgewählten Elementen:
            elif ElementMenge > 1:
                for E in XMLpath:
                    if E.nodeType == Node.ELEMENT_NODE:
                        if getElementText(E).strip() == '':
                            print('[leer]')
                        else:
                            print(getElementText(E).strip())
                            if MengeAusgabe == 'erste':
                                break

            #Ergebnis =

        elif ArtAusgabe == 'ElementKinder':

            def getKinderMenge(node):
                try:
                    RohMenge = node.childNodes.length
                    if RohMenge > 1:
                        KinderMenge = 0
                        for E in node.childNodes:
                            if E.nodeType == Node.ELEMENT_NODE:
                                KinderMenge += 1
                    else:
                        KinderMenge = 0

                #    print('NodeType:', XMLpath.nodeType)
                except (AttributeError):
                    if node.childNodes.nodeType == Node.ELEMENT_NODE:
                        KinderMenge = 1
                    else:
                        KinderMenge = 0
                return(KinderMenge, RohMenge)


            # für XMLpath mit einem ausgewählten Element:
            if ElementMenge == 1:
                KinderMenge = getKinderMenge(XMLpath)[0]
                RohMenge = getKinderMenge(XMLpath)[1]
                print('Kindermenge von <%s>: %s' % (XMLpath.nodeName, KinderMenge))

                if KinderMenge == 0:
                    print('Keine ElementKinder vorhanden.')

                elif KinderMenge == 1:
                    if RohMenge == 1:
                        print(XMLpath.childNodes.nodeName)
                    elif RohMenge > 1:
                        for K in XMLpath.childNodes:
                            if K.nodeType == Node.ELEMENT_NODE:
                                print(K.nodeName)

                elif KinderMenge > 1:
                    for K in XMLpath.childNodes:
                        if K.nodeType == Node.ELEMENT_NODE:
                            print(K.nodeName)

            # für XMLpath mit mehreren ausgewählten Elementen:
            elif ElementMenge > 1:
                for E in XMLpath:
                    x = 0
                    if E.nodeType == Node.ELEMENT_NODE:
                        x += 1
                        KinderMenge = getKinderMenge(E)[0]
                        RohMenge = getKinderMenge(E)[1]
                        print('Kindermenge von <%s>: %s' % (E.nodeName, KinderMenge))

                        if KinderMenge == 0:
                            print('Keine ElementKinder vorhanden.\n')

                        elif KinderMenge == 1:
                            if RohMenge == 1:
                                print(E.childNodes.nodeName)
                            elif RohMenge > 1:
                                for K in E.childNodes:
                                    if K.nodeType == Node.ELEMENT_NODE:
                                        print(K.nodeName)
                            print()

                        elif KinderMenge > 1:
                            for K in E.childNodes:
                                if K.nodeType == Node.ELEMENT_NODE:
                                    print(K.nodeName)
                            print()

                    if MengeAusgabe == 'erste' and x > 0:
                            break

            #Ergebnis =

        elif ArtAusgabe == 'Attribut' or ArtAusgabe == 'AttributName':
            # als DictAttribut ausgeben
            # MengeAusgabe = 'erste' bezieht sich in diesem Fall auf die Ausgabe aller...
            # ... Attribute des ersten ausgewählten Elements

            # für XMLpath mit einem ausgewählten Element:
            if ElementMenge == 1:
                DictAttribut = {}
                ListAttribut = []
                if XMLpath.nodeType == Node.ELEMENT_NODE:

                    if ArtAusgabe == 'Attribut':
                        print('Attribut(e) von <%s>:' % XMLpath.nodeName)
                        for AttrName, AttrWert in XMLpath.attributes.items():
                            DictAttribut.update({AttrName: AttrWert})
                    print(OutputDict(DictAttribut), '\n')

                    if ArtAusgabe == 'AttributName':
                        print('AttributName(n) von <%s>:' % XMLpath.nodeName)
                        for AttrName in XMLpath.attributes.keys():
                            ListAttribut.append(AttrName)
                    print(OutputDict(ListAttribut), '\n')

                Ergebnis = ListAttribut

            # für XMLpath mit mehreren ausgewählten Elementen:
            elif ElementMenge > 1:
                x = 0
                ListAttributPaket = []
                for E in XMLpath:
                    DictAttribut = {}
                    ListAttribut = []
                    if E.nodeType == Node.ELEMENT_NODE:

                        if ArtAusgabe == 'Attribut':
                            x += 1
                            if MengeAusgabe == 'erste' and x > 1:
                                break
                            print('Attribut(e) von <%s>:' % E.nodeName)
                            for AttrName, AttrWert in E.attributes.items():
                                DictAttribut.update({AttrName: AttrWert})
                            ListAttributPaket.append(DictAttribut)
                            print(OutputDict(DictAttribut), '\n')

                        if ArtAusgabe == 'AttributName':
                            x += 1
                            if MengeAusgabe == 'erste' and x > 1:
                                break
                            print('AttributName(n) von <%s>:' % E.nodeName)
                            for AttrName in E.attributes.keys():
                                ListAttribut.append(AttrName)
                            ListAttributPaket.append(ListAttribut)
                            print(OutputDict(ListAttribut), '\n')

                        Ergebnis = ListAttributPaket #fehlt noch: ElementNamen in umfangreicheres Dict einfügen;
                                                     #sonst Attribute schwer zuzuordnen

            print('Ergebnis:\n\n', Ergebnis)


        elif ArtAusgabe == 'ElementBaum':

            if ElementMenge == 1:
                Baum = XMLpath.toxml()
                print('Baum von', XMLpath, ':\n', Baum)
            elif MengeAusgabe == 'erste':
                Baum = XMLpath[0].toxml()
                print('Baum von', XMLpath[0], ':\n', Baum)
            elif MengeAusgabe == 'alle':
                for E in XMLpath:
                    Baum = E.toxml()
                    print('\n\nBaum von', E, ':\n', Baum)

            #Ergebnis =

        else:
            print('Ungültige Angabe der ArtAusgabe!')
            print('Auswahl: ElementName, ElementText, ElementKinder, Attribut, AttributName, Position, ElementBaum')


        'Erstellen des Dictonary und Rückgabe der gewünschten Daten'
        erg = None
        print()
        Ergebnis = {'Ergebnis': erg}
        return Ergebnis

#==============================================================================