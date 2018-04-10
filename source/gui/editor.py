"""
.. module: gui
   :platform: Any
   :synopsis: Gui for the AIML generator
.. moduleauthor: ajeet singh
"""
from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.application import Application
from prompt_toolkit.shortcuts import create_eventloop
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.enums import EditingMode
from prompt_toolkit.layout.containers import VSplit, Window
from prompt_toolkit.layout.controls import BufferControl, FillControl, TokenListControl
from prompt_toolkit.layout.dimension import LayoutDimension as D
from prompt_toolkit.clipboard.in_memory import InMemoryClipboard
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.contrib.completers import WordCompleter
from prompt_toolkit.layout.margins import NumberredMargin, ScrollbarMargin
from pygments.token import Token
from gui import editor_global_config as egc


class Editor(object):
    """Gui Editor for AIML gen
    buffer -> layout -> application -> cli
    """

    def __init__(self):
        """docstring for __init__"""
        self._key_handlers = KeyHandlers()
        self._loop = create_eventloop()
        self._key_binding_mgr = self._key_handlers.get_key_binding_manager()
        self._key_binding_registry = self._key_handlers.get_key_binding_registry()
        self._application = None
        self._cli = None
        self._editor_title = egc.EDITOR_TITLE
        self._on_editor_started = None
        self._on_editor_rendered = None
        self._on_editor_content_changed = None
        self._editor_buffer = None
        self._editor_buffer_name = 'MainBuffer'
        self._completer_list = ['abc', 'def']
        self._left_margin = None
        self._right_margin = None

    def setup_buffer(self):
        """docstring for setup_buffer"""
        completer = None
        auto_suggest = None
        history = None
        if bool(egc.BUFFER_COMPLETER) is True:
            completer = WordCompleter(self._completer_list)
        if bool(egc.BUFFER_AUTO_SUGGEST) is True:
            auto_suggest = AutoSuggestFromHistory()
        if bool(egc.BUFFER_HISTORY) is True:
            history = FileHistory('history.temp')
        self._editor_buffer = Buffer(
                completer=completer,
                auto_suggest=auto_suggest,
                history=history,
                tempfile_suffix=bool(egc.BUFFER_TEMP_FILE_SUFFIX),
                is_multiline=bool(egc.BUFFER_MULTILINE),
                complete_while_typing=bool(egc.BUFFER_COMPLETE_WHILE_TYPING),
                enable_history_search=bool(egc.BUFFER_ENABLE_HIST_SEARCH)
                )

    def setup_cli(self):
        """docstring for run"""
        self._cli = CommandLineInterface(application=self._application, eventloop=self._loop)
        self._cli.add_buffer(self._editor_buffer_name, self._editor_buffer) #, focus=True)

    def setup_layout(self):
        """docstring for setup_layout"""
        if bool(egc.TEXT_EDITOR_ENABLE_LEFT_MARGIN) is True:
            self._left_margin = NumberredMargin(display_tildes=True)
        if bool(egc.TEXT_EDITOR_ENABLE_RIGHT_MARGIN) is True:
            self._right_margin = ScrollbarMargin(display_arrows=True)
        self._buffer_control = BufferControl(buffer_name=self._editor_buffer_name)
        self._editor_aiml_code_window = Window(content=self._buffer_control, left_margins=[self._left_margin,])
        self._vertical_line = FillControl('|', token=Token.Line)
        self._window_separater = Window(width=D.exact(1), content=self._vertical_line)
        self._aiml_list = TokenListControl(get_tokens=self.get_aiml_list)
        self._editor_aiml_list_window = Window(content=self._aiml_list, right_margins=[self._right_margin,])
        self._layout = VSplit([
            self._editor_aiml_code_window,
            self._window_separater,
            self._editor_aiml_list_window,
            ])

    def get_editor_title(self):
        """docstring for get_editor_title"""
        return self._editor_title

    def get_aiml_list(self, cli):
        """docstring for get_aiml_list"""
        return [
                (Token.ABC, 'abc'),
                (Token.DEF, 'def')
                ]

    def editor_started_callback(self, cli):
        """docstring for editor_started_callback"""
        if self._on_editor_started is not None and\
                callable(self._on_editor_started):
            self._on_editor_started(cli)

    def editor_rendered_callback(self, cli):
        """docstring for editor_rendered_callback"""
        if self._on_editor_rendered is not None and\
                callable(self._on_editor_rendered):
                    self._on_editor_rendered(cli)

    def editor_content_changed(self, cli):
        """docstring for editor_content_changed"""
        if self._on_editor_content_changed is not None and\
                callable(self._on_editor_content_changed):
                    self._on_editor_content_changed(cli)


    def setup_application(self):
        """docstring for setup_application"""
        self._clipboard = InMemoryClipboard()
        self._application = Application(key_bindings_registry=self._key_binding_registry,
                layout=self._layout,
                mouse_support=bool(egc.EDITOR_MOUSE_SUPPORT),
                use_alternate_screen=True,
                initial_focussed_buffer=self._editor_buffer_name,
                clipboard=self._clipboard,
                get_title=self.get_editor_title,
                editing_mode=EditingMode.VI if egc.EDITOR_EDITING_MODE == 'VI' else EditingMode.EMACS,
                on_initialize=self.editor_started_callback,
                on_render=self.editor_rendered_callback,
                on_buffer_changed=self.editor_content_changed
                )



class KeyHandlers(object):
    """Contains all handlers registered with key bindings
    """

    __single_instance = None
    __key_binding_manager = KeyBindingManager(
            enable_abort_and_exit_bindings=bool(egc.KB_ABORT_EXIT_BIND),
            enable_system_bindings=bool(egc.KB_SYSTEM_BIND),
            enable_search=bool(egc.KB_SEARCH),
            enable_open_in_editor=bool(egc.KB_OPEN_IN_EDITOR),
            enable_extra_page_navigation=bool(egc.KB_PAGE_SCROLL),
            enable_auto_suggest_bindings=bool(egc.KB_AUTO_SUGGEST)
            )
    registry = __key_binding_manager.registry

    def __new__(cls):
        """docstring for __new__"""
        if cls != type(cls.__single_instance):
            cls.__single_instance = object.__new__(cls)
        return cls.__single_instance

    def get_key_binding_manager(self):
        """docstring for get_key_binding_manager"""
        return KeyHandlers.__key_binding_manager

    def get_key_binding_registry(self):
        """docstring for get_key_binding_registry"""
        return KeyHandlers.registry


if __name__=='__main__':
    ed = Editor()
    ed.setup_buffer()
    ed.setup_layout()
    ed.setup_application()
    ed.setup_cli()
    ed._cli.run()
