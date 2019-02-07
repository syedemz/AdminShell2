#==============================================================================
# Hilfsfunktion
# Ausgabe
#==============================================================================
'Importe'
import json

'Hilfsfunktion Ausgabe'
# sorgt für eine ordentliche Ausgabe der Dictonarys
def OutputDict(Dict):
    DictFormat = json.dumps(Dict, indent=2)
    return DictFormat