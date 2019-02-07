#==============================================================================
# Hilfsfunktion
# Pfad
#==============================================================================


'Hilfsfunktionen Pfad in XMLBaum'
# sucht eine Zeichenkette in einem String    
def StringSucher(string, zeichen):
    # Bem.: erstes Zeichen des Strings ist an Position 0, nicht 1
    index = 0
    Treffer = []
    if zeichen in string:
        c = zeichen[0]
        for ch in string:
            if ch == c:
                if string[index:index+len(zeichen)] == zeichen:
                    Treffer.append(index)
            index += 1
        return Treffer
    return -1


# Auswertung des Strings
def PfadInterpreter(Path):
    PathString = Path
    
    # Positionen der Auszeichnungen
    ListStart = StringSucher(PathString, '<')
    ListEnde = StringSucher(PathString, '>')
    ListElemente = []
    i = 0
    while i < PathString.count('<'):
        x = PathString[ListStart[i]+1:ListEnde[i]]
        ListElemente.append(x)
        i += 1
    #print(json.dumps(ListElemente, indent=2))
    
    # [zahl] auswerten
    j = 0
    ListKlammerAuf = []
    ListKlammerZu = []
    ListNummer = []
    for E in ListElemente:
        ListKlammerAuf.append(StringSucher(E, '['))        
        ListKlammerZu.append(StringSucher(E, ']'))

        if ListKlammerAuf[j] != -1:
            wert1 = ListKlammerAuf[j][0]
            wert2 = ListKlammerZu[j][0]
            y = E[wert1+1:wert2]
            ListNummer.append(y)
            
            diff = wert2 - (wert1-1)
            ListElemente[j] = E[:-diff]
            
        elif ListKlammerAuf[j] == -1:
            ListNummer.append(-1)
            
        j += 1  
    #print(json.dumps(ListNummer, indent=2))
    #print(json.dumps(ListElemente, indent=2))
    return [ListElemente, ListNummer]


def getXMLpath(W, Pfad):
    # ermittelt den XMLpath zur weiteren Verarbeitung
    ListData = PfadInterpreter(Pfad)
    # ListData enthält Liste mit Elementen & Liste ElementNummern
    XMLpath = None
    #print(ListData[0], ListData[1], len(ListData[0]), ListData[0][2])
    print('Pfadangabe:', Pfad)            
    
    if W.nodeName == ListData[0][0]:
        print('\nPrüfung...\nKeine Fehler gefunden\n')
        XMLpath = W # Wurzel
    else:
        print('\nPrüfung...\nFehler: Wurzel existiert nicht. Fehler.\n')
    
    # Pfad generieren    
    t = 1 # Tiefenzähler für XML-Baum
    
    # wertet die Zwischenebenen aus
    while t < (len(ListData[0])-1):
        Ebene = XMLpath.childNodes
        Namensvetter = []
        k = 0 # Knotenzähler (inkl. der NichtElemente)
        e = 0 # Elementzähler ()

        for E in Ebene:
            if E.nodeType == Node.ELEMENT_NODE:
                if E.nodeName == ListData[0][t] and ListData[1][t] == -1:
                    XMLpath = Ebene[k]
                        
                elif E.nodeName == ListData[0][t] and ListData[1][t] != -1:
                    e += 1
                    Namensvetter.append(k)      
            k += 1
            pos = int(ListData[1][t])
            
        if e > 0: # bedeutet, dass eine ElementNummer angegeben ist
            p = Namensvetter[pos-1]
            XMLpath = Ebene[p]

        e = 0
        t += 1
    
    # wertet letzte Ebene aus
    # unterscheidet zwischen einem oder mehreren ausgewählten Elementen  
    if t > (len(ListData[0])-2): 
        
        Ebene = XMLpath.childNodes
        Namensvetter = []
        k = 0 # Knotenzähler (inkl. der NichtElemente)
        e = 0 # Elementzähler ()
        EbeneList = []
        for E in Ebene:
            if E.nodeType == Node.ELEMENT_NODE:
                if E.nodeName == ListData[0][t] and ListData[1][t] == -1:
                    EbeneList.append(E)
                    
                elif E.nodeName == ListData[0][t] and ListData[1][t] != -1:
                    e += 1
                    Namensvetter.append(k)      
            k += 1
            pos = int(ListData[1][t])
            
        if e > 0: # bedeutet, dass eine ElementNummer angegeben ist
            p = Namensvetter[pos-1]
            XMLpath = Ebene[p]
        else:
            # nicht optimal, da theoretisch Elemente tieferer Ebene 
            # ... gleichen Namens mit gelistet werden könnten
            XMLpath = XMLpath.getElementsByTagName(ListData[0][t])
        
        e = 0

    return XMLpath