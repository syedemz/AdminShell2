#==============================================================================
# Hilfsfunktion
# Teilstringsuche
#==============================================================================

def TeilStringSuche(String, TeilString):
    ZWErg = {}
    ZWErg['Entd'] = []
    
    # diese Sonderzeichen werden für die Suche aus den Strings entfernt:
    sonderzeichen = [33,34,35,36,37,38,40,41,42,43,44,46,47,58,59,60,61,62,63,64,91,92,93,94,96,123,124,125,126,127,238,239,241,242,243,244,245,246,247,248,249,250,251,252,253,254]  

    
    for sz in sonderzeichen:
        sz = chr(sz) # ASCII-Code Übersetzung
        String = String.replace(sz,'') # löschen der Sonderzeichen
        TeilString = TeilString.replace(sz,'') # löschen der Sonderzeichen
        Anfrage = TeilString 
        
    splitString = String.split(' ') # Splitten in Worte
    splitTeilString = TeilString.split(' ') # Splitten in Worte

    
    'Zeichenkettenvergleich'
    # ebenfalls Suche ohne Sonderzeichen
    ZKvgl = 0
    if String.find(TeilString) == -1:
        ZKvgl = 0 # Zeichenkette nicht enthalten
    else:
        ZKvgl = 1 # Zeichenkette enthalten
        
    
    for x in splitTeilString:
            if String.find(x) == -1:
                None
            else:
                #print(x, 'entdeckt.')
                ZWErg['Entd'].append(x)
                ZKvgl += 1
                
        
    'Wörtervergleich'
    Wvgl = 0
    String = String.replace('_',' ')
    TeilString = TeilString.replace('_',' ')
    
    for i in splitString:
        for j in splitTeilString:
            if i == j:
                #print(i, 'gefunden.')
                ZWErg['Entd'].append(i)
                Wvgl += 1

    'Ergebnis der Suche'
    if ZKvgl > 0:
        #print('Zeichenkette \"%s\" enthalten' % Anfrage)
        #ZWErg['Entd'].append(Anfrage)
        None
    elif Wvgl > 0:
        #print('Wort enthalten')
        None
    else:
        ZWErg['Fazit'] = 'NEIN' # Keine Übereinstimmung gefunden
        return ZWErg 
    
    ZWErg['Fazit'] = 'JA' # Übereinstimmung gefunden
    return ZWErg

#==============================================================================