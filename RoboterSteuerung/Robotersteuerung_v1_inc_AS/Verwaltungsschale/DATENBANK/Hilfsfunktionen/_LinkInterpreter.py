#==============================================================================
# Hilfsfunktion LinkInterpreter
#==============================================================================

def LinkInterpreter(Link):
    # unterscheidet einen internen von einem externen Link
    
    
    Link = Link[0:8] # nur der Anfang des Strings wird betrachtet
    
    'Zeichenkettenvergleich'
    if Link.find('http') == -1:
        LinkArt = 'intern' # Zeichenkette ist intern
    else:
        LinkArt = 'extern' # http... https...
    
    if Link.find('www') == -1:
        x = 0 # Platzhalter
    else:
        LinkArt = 'www' # www... InternetLink
    
    return LinkArt
    

