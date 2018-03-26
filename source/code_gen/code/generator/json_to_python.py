"""
.. module:: json_to_python
   :platform: Any
   :synopsis: Module to parse JSON file and create code

.. moduleauthor:: Ajeet Singh
"""
import ujson
import pathlib
from typing import Type
from configparser import ConfigParser
from UMLToCodeApp import config
from UMLToCodeApp.templates import manager


############### Constants ################################
MODULE = 'module'
NAME = 'name'
CLASSES = 'classes'
DETAILS = 'details'
TYPE = 'type'
INHERITS = 'inherits'
IS_ABSTRACT = 'is_abstract'
IS_INTERFACE = 'is_interface'
CONSTRUCTORS = 'constructors'
DEFAULT = 'default'
REQUIRED = 'required'
ACCESS = 'access'
FIELDS = 'fields'
FUNCTIONS = 'functions'
METHODS = 'methods'


def validate(raw_data):
    """Validates the raw data passed as arg. It checks whether it is in JSON
    format and contains the required keys

    Args:
        raw_data (str): raw_data contains the whole JSON string

    Returns:
        is_valid (bool): True or false
        json_data (dict): parsed json as dict from raw_data

    """
    is_valid = False
    json_data = ujson.loads(raw_data)
    if json_data.__contains__(MODULE):
        module = json_data[MODULE]
        if module.__contains__(CLASSES):
            classes = module[CLASSES]
            if classes.__len__() > 0:
                is_valid = True
        if module.__contains__(FUNCTIONS):
            functions = module[FUNCTIONS]
            if functions.__len__() > 0:
                is_valid = True
    return (is_valid, json_data)

def generate_module_file(module_name):
    """Generates the module file with the name passed as arg

    Args:
        module_name (str): Name of the module passed as arg

    Returns:
        file (Type[pathlib.Path]): An instance of `Path` class pointing to the
        module file

    """
    output_folder = None
    if config.OUTPUT_FOLDER_PATH.find('~') > 0:
        output_folder = pathlib.Path(config.OUTPUT_FOLDER_PATH).expanduser()
    else:
        output_folder = pathlib.Path(config.OUTPUT_FOLDER_PATH).absolute()
    if output_folder is not None:
        if not output_folder.exists():
            output_folder.mkdir(parents=True)
        module_file = output_folder.joinpath('%s.py' % module_name)
        if module_file.exists() and config.OVERWRITE_FILE is True:
            module_file.unlink()
        module_file.touch()
        #Get rendered module template from templates manager
        module_str = manager.apply_to_module(module_name)
        #save rendered string to newly created module file
        with module_file.open('w') as mf:
            mf.write(module_str)
    return module_file

def generate_class(cls_name, cls_def):
    """Generate class using class template and data def passed to this function

    Args:
        cls_name (str): Name of the class
        cls_def (dict): Fields, constructors and methods of class

    Returns:
        cls_def_str (str): class definition as string after template processing

    """
    cls_def_str = '\nclass %s {\n' % cls_name
    fields = None
    constructors = None
    methods = None
    if cls_def.__contains__(FIELDS):
        fields = cls_def[FIELDS]
    if cls_def.__contains__(CONSTRUCTORS):
        constructors = cls_def[CONSTRUCTORS]
    if cls_def.__contains__(METHODS):
        methods = cls_def[METHODS]
    if fields is not None:
        for field_name, field in fields.items():
            cls_def_str += '\t%s %s\n' % (field[TYPE], field_name)
    cls_def_str += '}\n'
    return cls_def_str

def generate_code(file_name):
    """Generates code by parsing the file passed as arg

    Args:
        file_name (str): name of the JSON file

    """
    if file_name is not None:
        file_path = None
        if config.INPUT_FOLDER_PATH.find('~') > 0:
            file_path = pathlib.Path(config.INPUT_FOLDER_PATH, file_name).expanduser()
        else:
            file_path = pathlib.Path(config.INPUT_FOLDER_PATH, file_name).absolute()
        raw_data = open(file_path).read()
        if raw_data is not None:
            (is_valid, json_data) = validate(raw_data)
            if is_valid:
                module_name = json_data[NAME]
                module_file = generate_module_file(module_name)
                module = json_data[MODULE]
                classes = None
                functions = None
                if module.__contains__(CLASSES):
                    classes = module[CLASSES]
                if module.__contains__(FUNCTIONS):
                    functions = module[FUNCTIONS]
                mod_file = module_file.open('a')
                for cls_name, cls_def in classes.items():
                    cls_def_str = generate_class(cls_name, cls_def)
                    mod_file.write(cls_def_str)
                mod_file.close()
        else:
            raise Exception('No data found in the file: %s', file_name)
    else:
        raise Exception('Invalid file name provided')
