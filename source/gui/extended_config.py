"""
.. module:: extended_config
   :platform: Any
   :synopsis: Extended confirguration for editor
.. moduleauthor: ajeet singh
"""
from configparser import ConfigParser
from configparser import ExtendedInterpolation
import pathlib
import editor_global_config as egc



class ConfigManager(object):
    """A manager class to load and manage all configurations except global config
    """

    def __init__(self):
        """docstring for __init__"""
        self._base_path = pathlib.Path(__file__).parent
        self._config_folder =\
                self._base_path.joinpath(egc.EDITOR_EXTENDED_CONFIGS_FOLDER)
        self._config_repo = {}

    def collect_configs(self):
        """docstring for load_configs"""
        if self._config_folder is not None:
            for file in pathlib.Path(self._config_folder).glob('*.ini'):
                conf_file = pathlib.Path(file).absolute()
                conf_name = file.name.upper()
                self._config_repo[conf_name] = {}
                self._config_repo[conf_name]['PATH'] = conf_file
                self._config_repo[conf_name]['PARSED_CONFIG'] =\
                        ConfigParser(interpolation=ExtendedInterpolation())
                self._config_repo[conf_name]['PARSED_CONFIG'].read(conf_file)

    def load_config(self, conf_name):
        """docstring for load_config"""
        conf_name = conf_name.upper()
        if self._config_repo is not None and len(self._config_repo) > 0:
            if self._config_repo.__contains__(conf_name):
                parsed_conf = self._config_repo[conf_name]['PARSED_CONFIG']
                self._loaded_conf = ExtendedConfig(parsed_conf)
                return self._loaded_conf
            else:
                return None
        else:
            raise Exception('No config files collected yet!')


class ExtendedConfig(object):
    """Extended configuration for editor
    """

    def __init__(self, parsed_conf):
        """docstring for __init__"""
        pass
