"""
.. module:: gui_config
   :platform: Any
   :synopsis: Configuration for editor
.. moduleauthor:: ajeet singh
"""
from configparser import ConfigParser
from configparser import ExtendedInterpolation
import pathlib


# Constants
CONFIG_FILE = 'editor_global_config.ini'

# Setup config
_base_path = pathlib.Path(__file__).parent
_config_path = _base_path.joinpath(CONFIG_FILE)
_config_file = pathlib.Path(_config_path).absolute()
_config = ConfigParser(interpolation=ExtendedInterpolation())
_config.read(_config_file)

# Configuration start
APP_BASE_PATH = str(_base_path)
EDITOR_SECTION = 'editor'
#--------------
EDITOR_TITLE_KEY = 'editor_title'
EDITOR_TITLE = _config.get(EDITOR_SECTION, EDITOR_TITLE_KEY)
EDITOR_MOUSE_SUPPORT_KEY = 'enable_mouse_support'
EDITOR_MOUSE_SUPPORT = _config.get(EDITOR_SECTION, EDITOR_MOUSE_SUPPORT_KEY)
EDITOR_EDITING_MODE_KEY = 'edit_mode'
EDITOR_EDITING_MODE = _config.get(EDITOR_SECTION, EDITOR_EDITING_MODE_KEY)
EDITOR_HISTORY_FILE_KEY = 'history_file'
EDITOR_HISTORY_FILE = _config.get(EDITOR_SECTION, EDITOR_HISTORY_FILE_KEY)
EDITOR_EXTENDED_CONFIGS_FOLDER_KEY = 'extended_config_folder'
EDITOR_EXTENDED_CONFIGS_FOLDER = _config.get(EDITOR_SECTION, EDITOR_EXTENDED_CONFIGS_FOLDER_KEY)
EDITOR_ACTIVE_CONF_KEY = 'active_conf'
EDITOR_ACTIVE_CONF = _config.get(EDITOR_SECTION, EDITOR_ACTIVE_CONF_KEY)
#--------------
KEY_BINDINGS_SECTION = 'key_bindings'
KB_ABORT_EXIT_BIND_KEY = 'enable_abort_exit_binding'
KB_ABORT_EXIT_BIND = _config.get(KEY_BINDINGS_SECTION, KB_ABORT_EXIT_BIND_KEY)
KB_SYSTEM_BIND_KEY = 'enable_system_binding'
KB_SYSTEM_BIND = _config.get(KEY_BINDINGS_SECTION, KB_SYSTEM_BIND_KEY)
KB_SEARCH_KEY = 'enable_search'
KB_SEARCH = _config.get(KEY_BINDINGS_SECTION, KB_SEARCH_KEY)
KB_OPEN_IN_EDITOR_KEY = 'enable_open_in_editor'
KB_OPEN_IN_EDITOR = _config.get(KEY_BINDINGS_SECTION, KB_OPEN_IN_EDITOR_KEY)
KB_PAGE_SCROLL_KEY = 'enable_page_scroll_binding'
KB_PAGE_SCROLL = _config.get(KEY_BINDINGS_SECTION, KB_PAGE_SCROLL_KEY)
KB_AUTO_SUGGEST_KEY = 'enable_auto_suggest'
KB_AUTO_SUGGEST = _config.get(KEY_BINDINGS_SECTION, KB_AUTO_SUGGEST_KEY)
#--------------
BUFFER_SECTION = 'buffers'
BUFFER_COMPLETER_KEY = 'enable_completer'
BUFFER_COMPLETER = _config.get(BUFFER_SECTION, BUFFER_COMPLETER_KEY)
BUFFER_AUTO_SUGGEST_KEY = 'enable_auto_suggest'
BUFFER_AUTO_SUGGEST = _config.get(BUFFER_SECTION, BUFFER_AUTO_SUGGEST_KEY)
BUFFER_HISTORY_KEY = 'enable_history'
BUFFER_HISTORY = _config.get(BUFFER_SECTION, BUFFER_HISTORY_KEY)
BUFFER_TEMP_FILE_SUFFIX_KEY = 'temp_file_suffix'
BUFFER_TEMP_FILE_SUFFIX = _config.get(BUFFER_SECTION, BUFFER_TEMP_FILE_SUFFIX_KEY)
BUFFER_MULTILINE_KEY = 'enable_multiline'
BUFFER_MULTILINE = _config.get(BUFFER_SECTION, BUFFER_MULTILINE_KEY)
BUFFER_COMPLETE_WHILE_TYPING_KEY = 'enable_complete_while_typing'
BUFFER_COMPLETE_WHILE_TYPING = _config.get(BUFFER_SECTION, BUFFER_COMPLETE_WHILE_TYPING_KEY)
BUFFER_ENABLE_HIST_SEARCH_KEY = 'enable_history_search'
BUFFER_ENABLE_HIST_SEARCH = _config.get(BUFFER_SECTION, BUFFER_ENABLE_HIST_SEARCH_KEY)
#---------------
TEXT_EDITOR_SECTION = 'text_editor'
TEXT_EDITOR_ENABLE_LEFT_MARGIN_KEY = 'enable_left_margin'
TEXT_EDITOR_ENABLE_RIGHT_MARGIN_KEY = 'enable_right_margin'
TEXT_EDITOR_ENABLE_LEFT_MARGIN = _config.get(TEXT_EDITOR_SECTION, TEXT_EDITOR_ENABLE_LEFT_MARGIN_KEY)
TEXT_EDITOR_ENABLE_RIGHT_MARGIN = _config.get(TEXT_EDITOR_SECTION, TEXT_EDITOR_ENABLE_LEFT_MARGIN_KEY)

# Configuration end
