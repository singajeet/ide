"""
.. module: config
"""
from configparser import ConfigParser, ExtendedInterpolation
import pathlib


################ Config variables #########################
CONFIG_FILE = 'uml_to_code.ini'
DEFAULT_SECTION = 'default'
APP_BASE_PATH_KEY = 'app_base_path'
CODE_GEN_SECTION = 'code_generator'
OUTPUT_FOLDER_PATH_KEY = 'output_folder_path'
INPUT_FOLDER_PATH_KEY = 'input_folder_path'
RESOURCES_FOLDER_PATH_KEY = 'resources_folder_path'
TEMPLATES_FOLDER_PATH_KEY = 'templates_folder_path'
OVERWRITE_FILE_KEY = 'overwrite_file'

CODE_GEN_PKG = 'code_gen'
RESOURCES_PKG = '%s.resources' % CODE_GEN_PKG

_base_path = pathlib.Path(__file__).parent
_conf_path = _base_path
_conf_file = _conf_path.joinpath(CONFIG_FILE)
CONFIG_FILE = pathlib.Path(_conf_file).absolute()
_config_parser = ConfigParser(interpolation=ExtendedInterpolation())
_config_parser.read(CONFIG_FILE)

APP_BASE_PATH = str(_base_path) #_config_parser.get(DEFAULT_SECTION, APP_BASE_PATH_KEY)
OUTPUT_FOLDER_PATH = str(pathlib.Path(_base_path,
                                  _config_parser.get(CODE_GEN_SECTION,
                                                     OUTPUT_FOLDER_PATH_KEY)))
OVERWRITE_FILE = str(pathlib.Path(_base_path,
                                  _config_parser.get(CODE_GEN_SECTION,
                                                     OVERWRITE_FILE_KEY)))
INPUT_FOLDER_PATH = str(pathlib.Path(_base_path,
                                     _config_parser.get(CODE_GEN_SECTION,
                                                        INPUT_FOLDER_PATH_KEY)))
RESOURCES_FOLDER_PATH = str(pathlib.Path(_base_path,
                                         _config_parser.get(CODE_GEN_SECTION,
                                                            RESOURCES_FOLDER_PATH_KEY)))
TEMPLATES_FOLDER_PATH = str(pathlib.Path(_base_path,
                                         _config_parser.get(CODE_GEN_SECTION,
                                                            TEMPLATES_FOLDER_PATH_KEY)))

############## Templates ###############################
MODULE_TEMPLATE = 'module.j2'
CLASS_TEMPLATE = 'class.j2'
METHOD_TEMPLATE='method.j2'
FUNCTION_TEMPLATE = 'function.j2'

###############CMD Manager##########################
KNOWLEDGE_BASE_PATH_KEY = 'knowledge_base_path'
CMD_MANAGER_PATH_KEY = 'cmd_manager_path'
CMD_MANAGER_SECTION = 'cmd_manager'
CMD_MANAGER_PATH = str(pathlib.Path(_base_path,
                                    _config_parser.get(CMD_MANAGER_SECTION,
                                                       CMD_MANAGER_PATH_KEY)))
KNOWLEDGE_BASE_PATH = str(pathlib.Path(_base_path,
                                       _config_parser.get(CMD_MANAGER_SECTION,
                                                          KNOWLEDGE_BASE_PATH_KEY)))
