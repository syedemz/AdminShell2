import json
import pandas

from structure.configuration import config
from structure.module import module

from os import path, getcwd



def main():

    VerwaltungsschaleDatenbank = module('VerwaltungsschaleDatenbank', config)

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


    while True:
        try:


            erg = 'Fehler!'

            'Input Paket'
            #HIER SOLL ER IMMER BEI LAUFENDEM PROGRAMM AUF EIN PAKET WARTEN
            MESSAGE = VerwaltungsschaleDatenbank.receive()
            CORE = VerwaltungsschaleDatenbank.extract_core(MESSAGE)
            Paket = CORE["request"]
            print(Paket)

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


            RESPONSE = VerwaltungsschaleDatenbank.create_message(TO = MESSAGE, CORE = {'ERG' : erg})
            VerwaltungsschaleDatenbank.send(RESPONSE)

        except KeyboardInterrupt:
            break





if __name__ == "__main__":
    main()
