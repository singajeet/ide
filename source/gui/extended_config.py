"""
.. module:: extended_config
   :platform: Any
   :synopsis: Extended confirguration for editor
.. moduleauthor: ajeet singh
"""
from configparser import ConfigParser
from configparser import ExtendedInterpolation
import pathlib
from gui import editor_global_config as egc



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

    def list_configs(self):
        """docstring for list_configs()"""
        if self._config_repo is not None and len(self._config_repo) > 0:
            print('List of configs available:')
            for name, conf in self._config_repo.items():
                print('%s => %s' % (name, conf['PATH']))
        else:
            print('No configs found!')

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


BUFFERS_SECTION = 'buffers_section'
BUFFERS_KEY = 'buffers'
BUFFERS = None
BUFFER_KEY = 'buffer'
BUFFER = None


class ExtendedConfig(object):
    """Extended configuration for editor
    """

    def __init__(self, parsed_conf):
        """docstring for __init__"""
        self._parsed_conf = parsed_conf
        self._buffers_collection = None
        self.load_config()

    def load_config(self):
        """docstring for load_config"""
        self.load_buffers()

    def load_buffers(self):
        """docstring for load_buffers"""
        if self._parsed_conf.get(BUFFERS_SECTION) is not None:
            for buf_name, buf_conf in self._parsed_conf.get(BUFFERS_SECTION):
                buf = BufferConfig(buf_name, buf_conf)
                self._buffers_collection[buf_name] = buf
        else:
            #no buffers defined, so load a default one
            buf = BufferConfig('DefaultBuffer', None)
            self._buffers_collection['DefaultBuffer'] = buf


class BufferConfig(object):
    """Class representing buffer config
    """

    def __init__(self, name, conf):
        """docstring for __init__"""
        self.name = name
        self.enable_completer = conf.get('enable_completer')
        self.completer_type = conf.get('completer_type')
        self.enable_auto_suggest = conf.get('enable_auto_suggest')
        self.auto_suggest_type = conf.get('auto_suggest_type')
        self.enable_history = conf.get('enable_history')
        self.history_type = conf.get('history_type')
        self.history_file = conf.get('history_file_path')
        self.allow_multiline = conf.get('allow_multiline')
        self.enable_complete_while_typing = conf.get('enable_complete_while_typing')
        self.enable_history_search = conf.get('enable_history_search')
        self.enable_rich_text_support = conf.get('enable_rich_text_support')
        self.enable_default_editing_commands = conf.get('enable_default_editing_commands')
        self.enable_fs_save_command = conf.get('enable_fs_save_command')
        self.enable_fs_open_command = conf.get('enable_fs_save_command')
        self.enable_fs_browse_command = conf.get('enable_fs_browse_command')
        self.enable_indent_support = conf.get('enable_indent_support')
        self.indent_width = conf.get('indent_width')
        self.indent_char = conf.get('indent_char')
        self.enable_tab_support = conf.get('enable_tab_support')
        self.tab_width = conf.get('tab_width')
        self.enable_tab_to_space_conversion = conf.get('enable_tab_to_space_conversion')
        self.enable_space_to_tab_conversion = conf.get('enable_space_to_tab_conversion')


if __name__ == '__main__':
    conf_mgr = ConfigManager()
    conf_mgr.collect_configs()
    conf_mgr.list_configs()
