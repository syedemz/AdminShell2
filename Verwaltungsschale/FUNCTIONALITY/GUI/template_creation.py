# Template creation functions which are used by the GUI.
# Author: Syed Emad

################################################################################
## Imports
################################################################################
from os import path, getcwd
from jinja2 import Template, Environment, FileSystemLoader
from flask import Flask, render_template

################################################################################
## Jinja2 Environment
################################################################################
## WorkingDirectory = CurrentDirectory
workdir = getcwd()
## PATH TO THE GUI
TEMPLATES_DIR =  path.join(workdir, 'FUNCTIONALITY')
## JINJA2 - SETTING AN ENVIRONMENT - JINJA2 SUPPORT MULTIPLE PATHS
env = Environment(loader = FileSystemLoader(TEMPLATES_DIR))

################################################################################
## Methods
################################################################################
def create_template(html_to_render, variables):
    """ A function for rendering the template which has to be
    sended from GUI to HTTPIN via the ZeroMQ-Socket
    """

    ## loading of a template
    template = env.get_template(html_to_render)
    ## rendering of the template
    rendered_template = template.render(variables=variables)

    return rendered_template

def get_resource_as_string(name, charset='utf-8'):
    """Function for getting resources like css and include them into the
        JINJA2-template which then is sended from GUI to the HTTPIN"""

    app = Flask(__name__)
    ## Open the resource - css, js or something
    with app.open_resource(name) as f:
        ## read and decode the resource
        resource=f.read().decode(charset)
        ## return the resource as a utf-8 string
        return resource

## setting the function global so the template (jinja2) can use it
env.globals['get_resource_as_string'] = get_resource_as_string
