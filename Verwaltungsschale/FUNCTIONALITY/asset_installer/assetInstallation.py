# DATABASE - Module.
# Author: Vladimir Kutscher


from os import path, getcwd

def save_gui_data(asset_name, templates_data):
    """This function saves the templates of an asset coming from an external
    datebase in the gui folder.
    """

    ## path to the templates in the gui
    workdir = getcwd()
    templates_path = path.join(workdir, 'FUNCTIONALITY', 'gui', 'templates', '')
    ## pasting of the templates - this will overwrite the the existing ones!!!
    for key, value in templates_data.items():
        file = open(templates_path + key, 'w')
        file.write(value)
        file.close()
