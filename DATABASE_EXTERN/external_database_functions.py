from os import path, getcwd, chdir, pardir, walk, mkdir, sep, listdir
from functools import reduce
import xml.dom.minidom as minidom
import json
import fnmatch

def findBlockId(xml_file, searchId):
    """Parsen der Database nach bestimmten Informationen"""

    # Definition WorkingDirectory = Current Directory
    workdir = getcwd()

    ## Path to  data.xml
    pathToData = path.join(workdir, 'DATABASE', xml_file)

    ## Parsing of data.xml -> DOM
    dataXml = minidom.parse(pathToData)

    ## extraction of all Blocks out of the DOM
    allBlocksInXml = dataXml.getElementsByTagName("omm:block")

    ## searching in all Blocks
    for block in allBlocksInXml:

        ## searching for the id of an block
        blockId = block.getAttribute("omm:id")

        ## Comparison of the BlockId with the searched Id
        if blockId == searchId:

            ## getting the Infos into variables
            blockLink = block.getElementsByTagName("omm:link"
            )[0].firstChild.data
            blockTitle = block.getElementsByTagName("omm:title"
            )[0].firstChild.data

            ## even if the tag is further down the DOM - just call it by name
            blockCreator = block.getElementsByTagName("omm:creator"
            )[0].firstChild.data
            blockCreationDate = block.getElementsByTagName("omm:date"
            )[0].firstChild.data
            ## Payload couild be everthing - give the type of payload
            blockPayloadType = str(type(block.getElementsByTagName("omm:payload"
            )[0].firstChild.data))
            blockPayload = block.getElementsByTagName("omm:payload"
            )[0].firstChild.data

        ## Putting the blockinfo into a dict.
        response = {"blockLink": blockLink,
                    "blockTitle": blockTitle,
                    "blockCreator": blockCreator,
                    "blockCreationDate": blockCreationDate,
                    "blockPayloadType": blockPayloadType,
                    "blockPayload": blockPayload,
                    }

        return response

    raise ValueError("No Block Found")

def tagIterator_extern(xml_file, asset_name):
    """
    Slightly modified tagIterator for parsing external DATABASEs meanwhile
    an external DATABASE is not implemented.
    """

    curDir = getcwd()
    workdir = path.abspath(path.join(curDir, pardir))

    ## intitialisting
    data_dict = {}

    if xml_file == 'add_directory.xml':

        pathToXmlFile = path.join(workdir, 'DATABASE_EXTERN', 'DATABASE',
                                    'Adds', xml_file)

        root = minidom.parse(pathToXmlFile)

        ## getting of all "over"-Blocks
        addList = root.getElementsByTagName("add")

        for add in addList:
            addIdentity = add.getAttribute("id")
            addTitle = add.getElementsByTagName("title"
            )[0].firstChild.data
            addInfo = add.getElementsByTagName("info"
            )[0].firstChild.data
            addPort = add.getElementsByTagName("port"
            )[0].firstChild.data
            addTemplate = add.getElementsByTagName("template"
            )[0].firstChild.data
            addSocket = add.getElementsByTagName("socket"
            )[0].firstChild.data


            addData = {"identity": addIdentity,
                        "title": addTitle,
                        "info": addInfo,
                        "port": addPort,
                        "template": addTemplate,
                        "socket": addSocket
                        }

            ## zuordnen der gewonnenen daten zum speziellen add
            data_dict[addIdentity] = addData

    elif xml_file == 'data.xml':
        """
        Iterates through the data.xml of the external database.
        """
        try:
            pathToXmlFile = path.join(workdir, 'DATABASE_EXTERN', 'DATABASE',
                                        'Assets', asset_name, xml_file)
            root = minidom.parse(pathToXmlFile)
            ## getting of all "over"-Blocks
            blockList = root.getElementsByTagName("omm:block")

            for block in blockList:
                ## extract single tag-info from the "over"-block
                blockTitle = block.getElementsByTagName("omm:title"
                )[0].firstChild.data
                blockCreator = block.getElementsByTagName("omm:creator"
                )[0].firstChild.data
                blockCreationDate = block.getElementsByTagName("omm:date"
                )[0].firstChild.data
                blockLink = block.getElementsByTagName("omm:link"
                )[0].firstChild.data
                blockPayload = block.getElementsByTagName("omm:payload"
                )[0].firstChild.data

                blockData = {
                            "blockTitle": blockTitle,
                            "blockCreator": blockCreator,
                            "blockCreationDate": blockCreationDate,
                            "blockLink": blockLink,
                            "blockPayload": blockPayload,}

                ## Anhaegen des assetData an die asset_list - Dictionary
                data_dict[blockTitle] = blockData
        except:
            """In case the external data.xml is  not reachable
            """
            data_dict = None
    else:
        pass

    ## Because the Dict has be delivered to JavaScript, it should be
    ## konverted in JSON because Python and JS has different
    ## Dict-Definitions - in JSON it is safe
    response = json.dumps(data_dict)

    # print(response) # DEBUGGING
    return response

def get_asset_data(asset_name):
    """Collecting of all asset-data (data.xml, html_code, images)
    and insertign it into one dict which can be transmitted"""
    ## intitialisting of an empty dict for the data
    data_dict = {}

    ## getting the add - path
    curDir = getcwd()
    exAssetDir = path.join(curDir, 'DATABASE',
                                'Assets', asset_name)

    ## assign the data.xml
    data_dict["data_xml"] = get_asset_data_xml(asset_name)

    ## assign all html files from the templates forlder to the data_dict
    data_dict["templates_data"] = get_asset_templates(asset_name = asset_name,
                                                        asset_path = exAssetDir)
    return data_dict

def get_asset_templates(asset_name, asset_path):
    templates_data = {}
    try:
        assetTemplatesDir = path.join(asset_path, 'templates', '')
        ## getting all templates from the root and from the subfolders
        for root, dirs, files in walk(assetTemplatesDir):
            for name in files:
                ## open the file and write the content to the templates data dict
                with open(path.join(root, name), "r") as file:
                    ## the key for every filevalue is the filename
                    templates_data[name] = file.read()
    except:
        templates_data = None
    return templates_data

def get_asset_data_xml(asset_name):
    """A function for getting the content of the data.xml of an specific asset
    (<asset_name>) from the actually 'inactive' DATABASE_EXTERN
    """
    curDir = getcwd()
    workdir = path.abspath(path.join(curDir, pardir))
    ## intitialisting
    data_dict = {}
    exAssetDataPath = path.join(workdir, 'DATABASE_EXTERN', 'DATABASE',
                                'Assets', asset_name, 'data.xml')
    root = minidom.parse(exAssetDataPath)
    data = root.toprettyxml(indent = "", newl = "")
    return data

def get_add_data(add_name):
    """Collecting of all add-data (configuration-data, python_code, html_code)
    """
    ## intitialisting of an empty dict for the data
    data_dict = {}

    ## getting the add - path
    curDir = getcwd()
    workdir = path.abspath(path.join(curDir, pardir))
    exAddDir = path.join(workdir, 'DATABASE_EXTERN', 'DATABASE',
                                'Adds', add_name)
    ## assign the configuration-data from the add_directory
    ## to an configuration_data - key in the dict.
    data_dict["configuration_data"] = get_add_conf(add_name)
    # ## assign all files from the add forlder to the data_dict
    data_dict["add_data"] = get_add_dir(exAddDir)
    return data_dict

def get_add_conf(add_name):
    """A function for getting the configuration data of an specific add
    (<add_name>) from the actually 'inactive' DATABASE_EXTERN
    """
    curDir = getcwd()
    workdir = path.abspath(path.join(curDir, pardir))
    ## intitialisting
    data_dict = {}
    exAddDataPath = path.join(workdir, 'DATABASE_EXTERN', 'DATABASE',
                                'Adds', 'add_directory.xml')
    root = minidom.parse(exAddDataPath)
    ## a list of all adds
    addList = root.getElementsByTagName("add")
    ## going through all the adds
    for add in addList:
        ## if the required add is found, grab the data
        if add.getAttribute("id") == add_name:
            config_data = add.toprettyxml(indent = "", newl = "")
    return config_data

def get_add_dir(add_path):
    """Function for recursive inetating through the dir-tree, reading
    all files and putting the content into a nested dictionary.

    ATTENTION!!! Images cant be tranferred this way at the moment.
    """
    ## the add_data - dict shuld be intantiated just in the first iteration
    try:
        add_data
    except:
        add_data = {}
    for content in listdir(add_path):
        if not (content == '__pycache__' or \
                content == '.DS_Store' or \
                content == 'images'):
            ChildPath = path.join(add_path, content)
            if path.isdir(ChildPath):
                add_data[content] = get_add_dir(ChildPath)
            else:
                with open(ChildPath, "r") as file:
                    add_data[content] = file.read()
    return add_data
