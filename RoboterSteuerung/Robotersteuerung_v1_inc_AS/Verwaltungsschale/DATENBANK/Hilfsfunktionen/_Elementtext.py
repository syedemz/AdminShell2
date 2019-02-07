#==============================================================================
# Hilfsfunktion
# Elementtext
#==============================================================================

'Hilfsfunktion DOM'
# gibt den Text eines Elements aus
def getElementText(node):
    nodelist = node.childNodes
    result = []
    
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            result.append(node.data)
            
    return ''.join(result)