"""
.. module:: interactive
   :platform: Any
   :synopsis: a module to present cmd line manager and issue commands to system
.. moduleauthor:: Ajeet Singh
"""
import aiml
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from UMLToCodeApp import config
from prompt_toolkit.token import Token
from prompt_toolkit.enums import EditingMode
import os
import pathlib



class CmdManager(object):
    """Command manager to init the aiml kernel, accept commands, parse and execute same
    """

    # Create a set of key bindings.
    manager = KeyBindingManager.for_prompt()

    cmd_style = style_from_dict({
        # User input.
        Token:          '#ff0066',

        # Prompt.
        Token.Username: '#884444',
        Token.At:       '#00aa00',
        Token.Colon:    '#00aa00',
        Token.Pound:    '#00aa00',
        Token.Host:     '#000088 bg:#aaaaff',
        Token.Path:     '#884444 underline',
    })


    def __init__(self, user='ajeet', host='localhost', home_dir='/'):
        """default constructor
        """
        self._username = user
        self._host = host
        self._home_dir = home_dir
        self._kernel = aiml.Kernel()
        self._kernel.verbose(True)
        self._kernel.bootstrap(learnFiles=os.path.join(config.KNOWLEDGE_BASE_PATH, 'startup.xml'), chdir=config.KNOWLEDGE_BASE_PATH)
        self._kernel.respond('load aiml b')

    def start(self):
        """Starts the loop to take inputs from cmd line
        """
        self._kernel.learn('%s*.aiml' % config.KNOWLEDGE_BASE_PATH)
        text = ''
        while text.lower() not in ['exit', 'quit']:
            text = prompt(get_prompt_tokens=self.get_prompt_tokens, style=CmdManager.cmd_style, key_bindings_registry=CmdManager.manager.registry, get_bottom_toolbar_tokens=self.get_bottom_toolbar_tokens)
            print(self._kernel.respond(text))

    # Add an additional key binding for toggling this flag.
    @manager.registry.add_binding(Keys.F4)
    def _(event):
        " Toggle between Emacs and Vi mode. "
        cli = event.cli

        if cli.editing_mode == EditingMode.VI:
            cli.editing_mode = EditingMode.EMACS
        else:
            cli.editing_mode = EditingMode.VI

    # Add a toolbar at the bottom to display the current input mode.
    def get_bottom_toolbar_tokens(self, cli):
        " Display the current input mode. "
        text = 'Vi' if cli.editing_mode == EditingMode.VI else 'Emacs'
        return [
            (Token.Toolbar, ' [F4] %s ' % text)
        ]

    def get_prompt_tokens(self, cli):
        return [
            (Token.Username, self._username),
            (Token.At,       '@'),
            (Token.Host,     self._host),
            (Token.Colon,    ':'),
            (Token.Path,     self._home_dir),
            (Token.Pound,    '# '),
        ]
