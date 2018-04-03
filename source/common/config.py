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

#base path pointing to ide/source/common
_base_path = pathlib.Path(__file__).parent
_conf_path = _base_path
_conf_file = _conf_path.joinpath(CONFIG_FILE)
CONFIG_FILE = pathlib.Path(_conf_file).absolute()
_config_parser = ConfigParser(interpolation=ExtendedInterpolation())
_config_parser.read(CONFIG_FILE)

#change base path to point to ide/source
_base_path = _base_path.parent
APP_BASE_PATH = str(_base_path) #_config_parser.get(DEFAULT_SECTION, APP_BASE_PATH_KEY)
OUTPUT_FOLDER_PATH = str(pathlib.Path(_base_path, CODE_GEN_PKG,
                                  _config_parser.get(CODE_GEN_SECTION,
                                                     OUTPUT_FOLDER_PATH_KEY)))
OVERWRITE_FILE = str(pathlib.Path(_base_path, CODE_GEN_PKG,
                                  _config_parser.get(CODE_GEN_SECTION,
                                                     OVERWRITE_FILE_KEY)))
INPUT_FOLDER_PATH = str(pathlib.Path(_base_path, CODE_GEN_PKG,
                                     _config_parser.get(CODE_GEN_SECTION,
                                                        INPUT_FOLDER_PATH_KEY)))
RESOURCES_FOLDER_PATH = str(pathlib.Path(_base_path, CODE_GEN_PKG,
                                         _config_parser.get(CODE_GEN_SECTION,
                                                            RESOURCES_FOLDER_PATH_KEY)))
TEMPLATES_FOLDER_PATH = str(pathlib.Path(_base_path, CODE_GEN_PKG,
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
CMD_MANAGER_PATH = str(pathlib.Path(_base_path, CODE_GEN_PKG,
                                    _config_parser.get(CMD_MANAGER_SECTION,
                                                       CMD_MANAGER_PATH_KEY)))
KNOWLEDGE_BASE_PATH = str(pathlib.Path(_base_path, CODE_GEN_PKG,
                                       _config_parser.get(CMD_MANAGER_SECTION,
                                                          KNOWLEDGE_BASE_PATH_KEY)))

############## AIML gen ################################
AIML_SECTION = 'aiml_gen'
AIML_DB_USER_KEY = 'aiml_db_user'
AIML_DB_USER = _config_parser.get(AIML_SECTION, AIML_DB_USER_KEY)
AIML_DB_PASSWORD_KEY = 'aiml_db_password'
AIML_DB_PASSWORD = _config_parser.get(AIML_SECTION, AIML_DB_PASSWORD_KEY)
AIML_DB_HOST_KEY = 'aiml_db_host'
AIML_DB_HOST = _config_parser.get(AIML_SECTION, AIML_DB_HOST_KEY)
AIML_DB_PORT_KEY = 'aiml_db_port'
AIML_DB_PORT = _config_parser.get(AIML_SECTION, AIML_DB_PORT_KEY)
AIML_FILES_OUTPUT_PATH_KEY = 'aiml_files_output_path'
AIML_FILES_OUTPUT_PATH = _config_parser.get(AIML_SECTION,
                                            AIML_FILES_OUTPUT_PATH_KEY)
AIML_DB_KEY = 'aiml_db'
AIML_DB = _config_parser.get(AIML_SECTION, AIML_DB_KEY)

################ CLI configuration #############################
TOKENS_SECTION = 'tokens'
class Token(object):
    _symbol_key = 'token_symbol'
    _color_key = 'token_color'
    Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
    Color =  _config_parser.get(TOKENS_SECTION, _color_key)

    class Colon(object):
        _symbol_key = 'colon_symbol'
        _color_key = 'colon_color'
        Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
        Color =  _config_parser.get(TOKENS_SECTION, _color_key)

    class Pound(object):
        _symbol_key = 'pound_symbol'
        _color_key = 'pound_color'
        Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
        Color =  _config_parser.get(TOKENS_SECTION, _color_key)

    class Pattern(object):
        _symbol_key = 'pattern_symbol'
        _color_key = 'pattern_color'
        Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
        Color =  _config_parser.get(TOKENS_SECTION, _color_key)

    class Template(object):
        _symbol_key = 'template_symbol'
        _color_key = 'template_color'
        Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
        Color =  _config_parser.get(TOKENS_SECTION, _color_key)

    class Default(object):
        _symbol_key = 'default_symbol'
        _color_key = 'default_color'
        Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
        Color =  _config_parser.get(TOKENS_SECTION, _color_key)

    class LBracket(object):
        _symbol_key = 'lbracket_symbol'
        _color_key = 'lbracket_color'
        Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
        Color =  _config_parser.get(TOKENS_SECTION, _color_key)

    class RBracket(object):
        _symbol_key = 'rbracket_symbol'
        _color_key = 'rbracket_color'
        Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
        Color =  _config_parser.get(TOKENS_SECTION, _color_key)

    class Command(object):
        _symbol_key = 'command_symbol'
        _color_key = 'command_color'
        Symbol = _config_parser.get(TOKENS_SECTION, _symbol_key)
        Color =  _config_parser.get(TOKENS_SECTION, _color_key)
