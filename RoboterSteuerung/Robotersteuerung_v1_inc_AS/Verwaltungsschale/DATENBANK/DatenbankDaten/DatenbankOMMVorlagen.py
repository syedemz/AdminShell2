#==============================================================================
# OMM Vorlagen erstellen, füllen und einfügen
#
#==============================================================================
'Importe'
from xml.dom import minidom
from os import path, getcwd, chdir
import time
import random

#==============================================================================
'Klasse OMMVorlagen'
class OMMVorlagen():
    #==========================================================================
    # Die Klasse erstellt neue XML-Dokumente oder
    # fügt bestehenden XML-Dokumenten neue Blöcke mit ToC-Eintrag ein
    #==========================================================================
    'Konstruktor'
    # angegebene XML-Datei wird geparst
    def __init__(self, newDict):

        'Speicherpfad und Filename auf Vorhandensein prüfen'
        basispfad = getcwd() # Dateipfad bis VerwaltungsschaleDatenbank
        Datenordner = path.join(basispfad, 'DatenbankDaten')
        self.Filename = newDict['Filename']
        self.Dateipfad = path.join(Datenordner, self.Filename)
        chdir(Datenordner) # setzt das aktuelle Arbeitsverzeichnis auf übergebenen Pfad
        self.Existenz = path.isfile(self.Filename)


        'Daten voreingestellt'
        self.PrimaryID_URL = 'URL'
        self.IDBlock = 99999
        self.Title = 'No Title'
        self.Titel = 'Kein Titel'
        self.Namespace = 'http://www.w3.org/2005/Incubator/omm/ns/sample'
        self.Description = 'No Description'
        self.Beschreibung = 'Keine Beschreibung'
        self.Creator = 00000000000
        self.Date = time.strftime("%Y-%m-%dT%H:%M:%S") # String mit Datum und Uhrzeit
        self.Subject = 'Keine weiteren Daten gespeichert'
        self.ID_URL_Subject = 'Hier sollte die ID (URL) des Subjekts stehen, dessen Dokument dies ist!'
        self.Payload = 'Leerer Payload'

        'neue ID für Block ermitteln'
        if self.Existenz == True:
            # Prüfung nach Vorhandensein einer ID als IDBlock der Blöcke in Dokument

            # Zufällige fünfstellige Blocknummer:
            self.IDBlock = random.randint(10000,99999)

            # XML des Dokuments wird geparst:
            self.tree = minidom.parse(self.Filename)
            self.Wurzel = self.tree.childNodes[0]
            self.ToC = self.Wurzel.getElementsByTagName('omm:toc')[0]
            ToCEintraege = self.ToC.getElementsByTagName('omm:element')

            for ToCEintrag in ToCEintraege:
                Block_ID = ToCEintrag.attributes['omm:id'].value
                if self.IDBlock == Block_ID:
                    while self.IDBlock == Block_ID:
                        self.IDBlock = random.randint(10000,99999)

        'EingabeDaten auswerten'
        try:
            self.New = newDict['New']
            self.PrimaryID_URL = (newDict['PrimaryID_URL'] if newDict['PrimaryID_URL'] != '' else self.PrimaryID_URL)
            self.Title = (newDict['Title english'] if newDict['Title english'] != '' else self.Title)
            self.Titel = (newDict['Titel deutsch'] if newDict['Titel deutsch'] != '' else self.Titel)
            self.Namespace = (newDict['Namespace'] if newDict['Namespace'] != '' else self.Namespace)
            self.Description = (newDict['Description english'] if newDict['Description english'] != '' else self.Description)
            self.Beschreibung = (newDict['Beschreibung deutsch'] if newDict['Beschreibung deutsch'] != '' else self.Beschreibung)
            self.Creator = (newDict['Creator'] if newDict['Creator'] != '' else self.Creator)
            self.Subject = (newDict['Subject'] if newDict['Subject'] != '' else self.Subject)
            self.ID_URL_Subject = (newDict['ID_URL_Subject'] if newDict['ID_URL_Subject'] != '' else self.ID_URL_Subject)
            self.Payload = (newDict['Payload'] if newDict['Payload'] != '' else self.Payload)
        except (NameError):
            None

        'Zusammenführen aller Daten'
        self.new = {'PrimaryID_URL': self.PrimaryID_URL,
                   'IDBlock': self.IDBlock,
                   'Title english': self.Title,
                   'Titel deutsch': self.Titel,
                   'Namespace': self.Namespace,
                   'Description english': self.Description,
                   'Beschreibung deutsch': self.Beschreibung,
                   'Creator': self.Creator,
                   'Date': self.Date,
                   'Subject': self.Subject,
                   'ID_URL_Subject': self.ID_URL_Subject,
                   'Payload': self.Payload,}

    #==========================================================================
    'OMM:XML erstellen oder durch Block mit ToC-Eintrag erweitern'
    def XMLOMMErstellung(self):
        # durchsucht den Hauptspeicher der Schale nach den angegebenen Schlagwörtern
        # Vorlagen als Strings

        if self.New == 'Eintrag' or self.New == 'Block' or self.New == 'block':
            # Neuer Block mit ToC-Eintrag

            VorlageToC = '''<?xml version="1.0" encoding="UTF-8"?>
<Platzhalter xmlns="https://www.w3.org/2005/Incubator/omm/elements/1.0/"
xmlns:omm="https://www.w3.org/2005/Incubator/omm/elements/1.0/">
  <omm:element omm:id="{IDBlock}">

    <omm:title xml:lang="en">{Title english}</omm:title>
    <omm:title xml:lang="de">{Titel deutsch}</omm:title>

    <omm:namespace>{Namespace}</omm:namespace>

    <omm:creation>
      <omm:creator omm:type="duns">{Creator}</omm:creator>
      <omm:date omm:encoding="ISO8601">{Date}</omm:date>
    </omm:creation>

    <omm:description xml:lang="en">{Description english}</omm:description>
    <omm:description xml:lang="de">{Beschreibung deutsch}</omm:description>

    <omm:subject>
      <omm:tag omm:type="text" omm:value="{Subject}"/>
    </omm:subject>

  </omm:element>
</Platzhalter>'''.format(**self.new)

            VorlageBlock = '''<?xml version="1.0" encoding="UTF-8"?>
<Platzhalter xmlns="https://www.w3.org/2005/Incubator/omm/elements/1.0/" xmlns:omm="https://www.w3.org/2005/Incubator/omm/elements/1.0/">
<omm:block omm:id="{IDBlock}">

    <omm:title xml:lang="en">{Title english}</omm:title>
    <omm:title xml:lang="de">{Titel deutsch}</omm:title>

    <omm:namespace>{Namespace}</omm:namespace>

    <omm:creation>
      <omm:creator omm:type="duns">{Creator}</omm:creator>
      <omm:date omm:encoding="ISO8601">{Date}</omm:date>
    </omm:creation>

    <omm:description xml:lang="en">{Description english}</omm:description>
    <omm:description xml:lang="de">{Beschreibung deutsch}</omm:description>

    <omm:subject>
      <omm:tag omm:type="text" omm:value="{Subject}"/>
    </omm:subject>

	<omm:payload omm:encoding="base64">{Payload}</omm:payload>

</omm:block>

</Platzhalter>'''.format(**self.new)

            if self.Existenz == True:
                # bestehendes XML-Dokument parsen, bearbeiten und schließen

                # XML der Vorlagen wird geparst:
                treeVorlageToC = minidom.parseString(VorlageToC)
                VorlToC = treeVorlageToC.getElementsByTagName('omm:element')[0]

                treeVorlageBlock = minidom.parseString(VorlageBlock)   ####geht noch nicht
                VorlBlock = treeVorlageBlock.getElementsByTagName('omm:block')[0]

                # Vorlagen werden in Dokument eingefügt:
                self.ToC.appendChild(VorlToC)
                self.Wurzel.appendChild(VorlBlock)

                # finales Dokument wird präsentiert
                Endversion = self.tree.toxml()
                print('\n====================')
                print(Endversion)
                print('====================\n')
                OK = input('Soll das bestehende Dokument %s so gespeichert werden (ja/nein): ' % self.Filename)
                if OK == 'ja':
                    # Dokument wird überschrieben
                    OMMDokumentBearb = open(self.Filename,'w')
                    OMMDokumentBearb.write(Endversion)
                    OMMDokumentBearb.close()
                    answer = ('XML-Dokument überschrieben und gespeichert. '
                             'Datei %s ist jetzt verändert.' % self.Filename)
                    return answer
                else:
                    return 'Vorgang abgebrochen. Versuchen Sie es nochmal.'

            else:
                return 'Es gibt noch kein Dokument dieses Filenames'


        elif self.New == 'Dokument' or self.New == 'document' or self.New == 'XML-Dokument' or self.New == 'dokument':
            # neues Dokument erstellen

            VorlageDok = '''<?xml version="1.0" encoding="UTF-8"?>
<mdm xmlns="https://www.w3.org/2005/Incubator/omm/elements/1.0/" xmlns:omm="https://www.w3.org/2005/Incubator/omm/elements/1.0/">

<omm:header>
    <omm:version>1.0</omm:version>
    <omm:primaryID omm:type="url">{PrimaryID_URL}</omm:primaryID>
</omm:header>


<omm:toc>

  <omm:element omm:id="00000">

    <omm:title xml:lang="en">Basic Data</omm:title>
    <omm:title xml:lang="de">Basisdaten</omm:title>

    <omm:namespace>{Namespace}</omm:namespace>

    <omm:creation>
      <omm:creator omm:type="duns">{Creator}</omm:creator>
      <omm:date omm:encoding="ISO8601">{Date}</omm:date>
    </omm:creation>

    <omm:description xml:lang="en">{Description english}</omm:description>
    <omm:description xml:lang="de">{Beschreibung deutsch}</omm:description>

    <omm:subject>
      <omm:tag omm:type="text" omm:value="ID: {ID_URL_Subject}"/>
      <omm:tag omm:type="text" omm:value="{Subject}"/>
    </omm:subject>

  </omm:element>

</omm:toc>


<omm:block omm:id="00000">

    <omm:title xml:lang="en">Basic Data</omm:title>
    <omm:title xml:lang="de">Basisdaten</omm:title>

    <omm:namespace>{Namespace}</omm:namespace>

    <omm:creation>
      <omm:creator omm:type="duns">{Creator}</omm:creator>
      <omm:date omm:encoding="ISO8601">{Date}</omm:date>
    </omm:creation>

    <omm:description xml:lang="en">{Description english}</omm:description>
    <omm:description xml:lang="de">{Beschreibung deutsch}</omm:description>

    <omm:subject>
      <omm:tag omm:type="text" omm:value="ID: {ID_URL_Subject}"/>
      <omm:tag omm:type="text" omm:value="{Subject}"/>
    </omm:subject>

    <omm:payload omm:encoding="base64">{Payload}</omm:payload>

</omm:block>

</mdm>'''.format(**self.new)


            if self.Existenz == False:
                # neues Dokument mit XML füllen

                # XML der Vorlage wird geparst
                tree = minidom.parseString(VorlageDok)

                print('\n====================')
                print(VorlageDok)
                print('====================\n')
                OK = input('Soll das neue Dokument so als %s gespeichert werden (ja/nein): ' % self.Filename)
                if OK == 'ja':
                    # Dokument wird erstellt
                    neuesDokument = open(self.Dateipfad,'w')
                    tree.writexml(neuesDokument, '', '\t', '\n')
                    neuesDokument.close()

                    answer = ('Ein neues XML-Dokument wurde erstellt. '
                              'Datei %s ist jetzt vorhanden.' % self.Filename)
                    return answer
                else:
                    return 'Vorgang abgebrochen. Versuchen Sie es nochmal.'

            else:
                return ('Es gibt bereits ein Dokument dieses Filenames. '
                        'Ein neues Dokument kann nicht angelegt werden!')

        else:
            return 'Nicht im Angebot!'

#==============================================================================

#==============================================================================
# newDict = {'New':'',
#            'Filename':'',
#            'PrimaryID_URL':'',
#            'Title english':'',
#            'Titel deutsch': '',
#            'Namespace':'',
#            'Description english':'',
#            'Beschreibung deutsch':'',
#            'Creator':'',
#            'Subject':'',
#            'ID_URL_Subject':'',
#            'Payload':'',}
#==============================================================================


