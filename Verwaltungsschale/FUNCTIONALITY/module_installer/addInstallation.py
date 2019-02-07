.# Author: Vladimir Kutscher
# Author: Syed Emad

import xml.dom.minidom as dom
import shutil
import os

def save_config(configData):
    """A function to get the required configuration-data (like portnumber,
    path to the thumbnail-picture and so on) in the installed_adds.xml
    where the GUI can take this information if it wants to show all installed
    adds"""

    ## generating a DOM ouf of the XML - String
    configDataDom = dom.parseString(configData)

    ## Because an DOM - Document cant be appended to another Document,
    ## we extract the main DOM - Element of the DOM - Document
    configDataElement = configDataDom.documentElement

    ## Definition WorkingDirectory = Dir where the script is initially called
    ## from. In this case is it the module_start.py on the top level.
    workdir = os.getcwd()

    ## Problem here again - GUI cant access Database directly.
    ## Has to be replaced later!!!
    pathToInstalledAddsXml = os.path.join(workdir, 'DATABASE', 'installed_adds.xml')

    ## Parsing of the DOM to an Document
    addDomDocument = dom.parse(pathToInstalledAddsXml)

    ## Getting the right place to enter the stuff
    func = addDomDocument.getElementsByTagName("Functionality")
    ## appending the <add> to <Functionality>
    func[0].appendChild(configDataElement)

    ## write the DOM back to the xml-file
    file = open(pathToInstalledAddsXml, "w")
    addDomDocument.writexml(file, encoding="UTF-8")
    file.close

def del_config(add_id):
    """Function for deleting the add information from the installed_adds.xml
    """

    ## Definition WorkingDirectory = Current Directory
    workdir = os.getcwd()
    ## Problem here again - GUI cant access Database directly.
    ## Has to be replaced later!!!
    pathToInstalledAddsXml = os.path.join(workdir, 'DATABASE',
                                            'installed_adds.xml')
    ## Parsing of the DOM to an Document
    addDomDocument = dom.parse(pathToInstalledAddsXml)
    ## Getting an add list
    addList = addDomDocument.getElementsByTagName("add")
    ## going through all elements in addList
    for add in addList:
        ## if the required add_id is found
        if add.getAttribute("id") == add_id:
            ## Getting the Functionality DOM Element
            root = addDomDocument.getElementsByTagName("Functionality")
            ## remove the child node
            root[0].removeChild(add)
            add.unlink()

    ## writing the changed DOM back in the installed_adds.xml
    file = open(pathToInstalledAddsXml, "w")
    addDomDocument.writexml(file, encoding="UTF-8")
    file.close

def save_add_dir(addData, add_path):
    """An recursive function for iterating the dict (add_data), deciding
    if the dict-key is an folder (=nested dict) or a file (usual key-value-pair)
    If its a folder, the function repeat recursively and when its a file,
    the value (=file-content) is passed to the write_data function"""
    ## iterate through the addData
    for key, value in addData.items():
        ## if the value of the key is an nested dict
        if isinstance(value, dict):
            ## create a dir_path with the new dir
            new_path = os.path.join(add_path, key)
            ## pass the path recursively back to the function
            save_add_dir(value, new_path)
        else:
            ## if the value of the key is not a dict itself, it has to be
            ## file - content. So write it to an file by passing to write_data()
            write_data(add_path, key, value)

def write_data(add_path, key, value):
    """This function takes the path, the name(key) and the content(value) of
    a file and write it to a newly created file"""
    ## create the path to the file
    file_path = os.path.join(add_path, '', key)
    ## create the file
    os.makedirs(os.path.dirname(file_path), exist_ok = True)
    ## write to the file
    with open(file_path, "w") as f:
        f.write(value)

def save_socket(add_name, socket_name, port):
    """A function for appending the add configuration - info into the
    FUNCTIONALITY/configuration.py"""
    ## importing the config. Has to be in the function, because it
    ## changes a lot...
    from FUNCTIONALITY.configuration import config
    ## bulding the add socket entry
    add_socket = {'identity': add_name.encode('ascii'), 'url': 'tcp://127.0.0.1:' + port}
    config[socket_name] = add_socket

    ## workaround to obtain the config - dict in the expected form
    config = 'config = '+str(config)

    ## writing the config back to file
    workdir = os.getcwd()
    pathToConfFile = os.path.join(workdir, 'FUNCTIONALITY', 'configuration.py')
    file = open(pathToConfFile, "w")
    file.write(config)
    file.close()
    return(add_socket)

def del_socket(socket_name):
    """Remove the socket from the configuration.py"""
    from FUNCTIONALITY.configuration import config

    ## deleting of the socket
    del config[socket_name]

    ## workaround to obtain the config - dict in the expected form
    config = 'config = '+str(config)

    ## writing the config back to file
    workdir = os.getcwd()
    pathToConfFile = os.path.join(workdir, 'FUNCTIONALITY', 'configuration.py')
    file = open(pathToConfFile, "w")
    file.write(config)
    file.close()

def add_install(add_name, addData):
    """The function for add installation. It takes the add_name and the addData
    which are delivered from the gui.py and installs the new add.
    """
    ## path to the add
    workdir = os.getcwd()
    add_path = os.path.join(workdir, 'FUNCTIONALITY', add_name, '')

    ## checking, if the path already exists == add is already installed
    if not os.path.exists(add_path):
        ## creating a new folder for the add
        os.mkdir(add_path)

        """ADD DATA"""
        ## extracting the add data from dict
        add_data = addData.get('add_data')

        ## put the files in the new add - folder
        save_add_dir(addData = add_data, add_path = add_path)

        # """HTML CODE"""
        # ## extracting the html code data
        # templatesData = addData.get('templates_data')
        #
        # ## the add - templates are inserted in an own templates - folder
        # addTemplatesDir = os.path.join(workdir, 'FUNCTIONALITY', add_name,
        #                                 'templates', '')
        #
        # ## create the templates folder
        # os.mkdir(addTemplatesDir)
        # ## put the html files into the templates folder
        # save_code_data(codeData = templatesData, add_path = addTemplatesDir)


        """CONFIG DATA"""
        ## extracting the configuration-data out of the addData.
        ## The get - Method provides an None, if the key is not found
        configData = addData.get('configuration_data')

        ## Adding the config - data into installed_adds.xml
        save_config(configData = configData)

        ## getting info for the socket configuration
        pathToInstalledAddsXml = os.path.join(workdir, 'DATABASE',
                                             'installed_adds.xml')
        addDomDocument = dom.parse(pathToInstalledAddsXml)
        adds = addDomDocument.getElementsByTagName("add")
        for add in adds:
            ## searching for the id
            addId = add.getAttribute("id")
            if addId == add_name:
                socket_name = add.getElementsByTagName("socket"
                )[0].firstChild.data
                port = add.getElementsByTagName("port"
                )[0].firstChild.data

        ## Add Socket to configuration.py
        add_socket = save_socket(add_name = add_name, socket_name = socket_name,
                            port = port)

        add_socket = {add_name: add_socket}
        return add_socket

def add_deinstall(add_name):
    """The function for add removing. It takes the add_name and removes
    the add from installed_adds.xml, from FUNCTIONALITY, configuration.py, ...
    """
    ## path to the add
    workdir = os.getcwd()
    add_path = os.path.join(workdir, 'FUNCTIONALITY', add_name, '')

    ## checking if the path exists
    if os.path.exists(add_path):

        ## removing the add directory
        shutil.rmtree(add_path)

        ## getting the socket_name
        pathToInstalledAddsXml = os.path.join(workdir, 'DATABASE', 'installed_adds.xml')
        addDomDocument = dom.parse(pathToInstalledAddsXml)
        adds = addDomDocument.getElementsByTagName("add")
        for add in adds:
            ## searching for the id
            addId = add.getAttribute("id")
            if addId == add_name:
                socket_name = add.getElementsByTagName("socket"
                )[0].firstChild.data

        del_socket(socket_name = socket_name)

        ## removing the configuration data from installed_adds.xml
        del_config(add_id = add_name)
