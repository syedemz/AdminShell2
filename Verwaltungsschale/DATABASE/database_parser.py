# Author: Vladimir Kutscher
# Author: Syed Emad

from os import path, getcwd
import xml.dom.minidom as minidom
import json
import base64

def getImage(Image):
    if path.exists(Image):
        f = open(Image,'rb')
        bytes = bytearray(f.read())
        Image2 = base64.b64encode(bytes)
        f.close()
        return Image2
    else:
        print("file does not exist")

def findBlockId(xml_file, searchId):

    ROOT_DIR = path.abspath(path.dirname(__file__))
    #print (ROOT_DIR)
    head, tail = path.split(ROOT_DIR)
    workdir = head

    """Parsing of the DATABASE"""

    ## Path to  data.xml
    pathToData = path.join(path.abspath(path.dirname(__file__)), xml_file)

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
            payLoadList = blockPayload.split("/")
            BlockPayload = payLoadList[0]
            ImageFile1 = path.join(workdir, 'FUNCTIONALITY/GUI/static/images', payLoadList[1])
            Image1 = getImage(ImageFile1)
            ImageFile2 = path.join(workdir, 'FUNCTIONALITY/GUI/static/images', payLoadList[2])
            Image2 = getImage(ImageFile2)
            ImageFile3 = path.join(workdir, 'FUNCTIONALITY/GUI/static/images', payLoadList[3])
            Image3 = getImage(ImageFile3)
            ImageFile4 = path.join(workdir, 'FUNCTIONALITY/GUI/static/images', payLoadList[4])
            Image4 = getImage(ImageFile4)
            ImageFile5 = path.join(workdir, 'FUNCTIONALITY/GUI/static/images', blockLink)
            Image5 = getImage(ImageFile5)


        ## Putting the blockinfo into a dict.
        response = {"blockLink": blockLink,
                    "blockTitle": blockTitle,
                    "blockCreator": blockCreator,
                    "blockCreationDate": blockCreationDate,
                    "blockPayloadType": blockPayloadType,
                    "blockPayload": BlockPayload,
                    "blockImage1": Image1.decode(),
                    "blockImage2": Image2.decode(),
                    "blockImage3": Image3.decode(),
                    "blockImage4": Image4.decode(),
                    "blockImage5": Image5.decode(),
                    }

        return response

    raise ValueError("No Block Found")

def tagIterator(xml_file):
    """
    A function for parsing an XML file for tags and sending back
    the information in an dictionary. At the moment specialised
    for the asset_list.xml
    """
    workdir = getcwd()
    pathToXmlFile = path.join(path.abspath(path.dirname(__file__)), xml_file)
    root = minidom.parse(pathToXmlFile)
    ## intitialisting
    data_dict = {}

    try:
        """To be safe, that the xml exists
        """

        if xml_file == 'asset_list.xml':

            ## getting of all "over"-Blocks
            blockList = root.getElementsByTagName("asset")

            for block in blockList:
                ## extract single tag-info from the "over"-block
                assetIdentity = block.getAttribute("id")
                assetName = block.getElementsByTagName("name"
                )[0].firstChild.data
                assetShortInfo = block.getElementsByTagName("shortInfo"
                )[0].firstChild.data
                assetThumbnail = block.getElementsByTagName("thumbnail"
                )[0].firstChild.data
                ImageFile = path.join(workdir, 'FUNCTIONALITY/GUI/static/images', assetThumbnail)
                Image = getImage(ImageFile)


                blockData = {"name": assetName,
                            "shortInfo": assetShortInfo,
                            "thumbnail": assetThumbnail,
                            "identity": assetIdentity,
                            "ImageData": Image.decode()}

                ## Anhaegen des assetData an die asset_list - Dictionary
                data_dict[assetName] = blockData

        elif xml_file == 'data.xml':
            """
            URL: stackoverflow.com/questions/15554605/python-list-index-out-of-range-minidom

            Idee, um eine Ebene weiter rein zu gehen!: Zuerst den Tag, der
            andere Tags enghält mit creationTag = block.getElementsByTagName("omm:creation")
            komplett holen und dann reingehen:
            blockCreator = creationTag.getElementsByTagName("omm:creator")[0].firstChild.data
            blockCreationDate = creationTag.getElementsByTagName("omm:date")[0].firstChild.data

            Idee, Absichern dass Tag existent und dadruch Fehlervermeidung
            am Beispiel von "wenn creationTag existiert":

            creationTag = block.getElementsByTagName("omm:creation")
            if creationTag:
                blockCreator = creationTag.getElementsByTagName("omm:creator")[0].firstChild.data

            """


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

        elif xml_file == 'installed_adds.xml':

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


                addData = {"title": addTitle,
                            "identity": addIdentity,
                            "info": addInfo,
                            "port": addPort,
                            "template": addTemplate,
                            }

                ## Anhaegen des assetData an die asset_list - Dictionary
                data_dict[addIdentity] = addData

        else:
            pass

        ## Because the Dict has be delivered to JavaScript, it should be
        ## konverted in JSON because Python and JS has different
        ## Dict-Definitions - in JSON it is safe
        response = json.dumps(data_dict)
    except:
        """Catch all kinds of Exceptions
        """
        response = 'XML not Found. Check if the required File is in DATABASE.'

    return response

def saveDataXml(data_xml):
    ## path to the data.xml
    data_path = path.join(path.abspath(path.dirname(__file__)),
                            'data.xml')
    ## write to data.xml - file
    file = open(data_path, 'w')
    file.write(data_xml)
    file.close()
    response = "dataXml saved"
    return response
