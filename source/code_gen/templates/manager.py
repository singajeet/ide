"""
.. module:: manager
   :platform: Any
   :synopsis: template manager

.. moduleauthor:: Ajeet Singh
"""
from jinja2 import Environment, PackageLoader, select_autoescape
import pathlib
from UMLToCodeApp import config

TEMPLATE_PATH_REL = pathlib.Path(config.TEMPLATES_FOLDER_PATH).name
RESOURCES_PATH_REL = pathlib.Path(config.RESOURCES_FOLDER_PATH).name

template_env = Environment(loader=PackageLoader(config.UMLTOCODEAPP_PKG,
                                                str(pathlib.Path(RESOURCES_PATH_REL, 
                                                             TEMPLATE_PATH_REL))), 
                           autoescape=select_autoescape(['json','xml']))

def apply_to_module(module_name: str, platform: str='Any', synopsis:
                    str=None, author: str=None):
    """Apply the arguments to the module template and returns the rendered
    string

    Args:
        module_name (str): Module name. A module file with ext .py will be
        created in output folder
        platform (str): platforms on which module can run
        synopsis (str): details about the module
        author (str): Module authors name or email

    Returns:
        module_str (str): rendered string after applying template

    """
    template = template_env.get_template(config.MODULE_TEMPLATE)
    module_str = template.render(module_name=module_name, platform=platform,
                                 synopsis=synopsis, author=author)
    return module_str
