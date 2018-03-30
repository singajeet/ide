"""
.. module:: main
   :platform: Any
   :synopsis: Utility to generate AIML files
.. moduleauthor:: ajeet singh
"""
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.filters import Condition
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.keys import Keys
from common import config
from prompt_toolkit.token import Token
from prompt_toolkit.enums import EditingMode
from aiml_gen.aiml_category import BaseCategory
import os
import pathlib


class AimlGenerator(object):
    """Class to generate AIML files based on the input provided by user
    """

    ADD_CATEGORY_CMD = 'add_category_cmd'
    ASK_TEMPLATE_SUB_CMD = 'ask_template_sub_cmd'
    REMOVE_CATEGORY_CMD = 'remove_category_cmd'
    UPDATE_CATEGORY_CMD = 'update_category_cmd'

    manager = KeyBindingManager.for_prompt()

    cmd_style = style_from_dict({
        # User input.
        Token:          '#ff0066',

        # Prompt.
        Token.Colon:    '#ff0066',
        Token.Pound:    '#ff0066',
        Token.Pattern:  '#884444',
        Token.Template: '#00aa00',
        Token.Default:  '#ff0066',
        Token.LeftBracket: '#224422',
        Token.RightBracket: '#224422',
        Token.Command: '#242424',
    })

    def __init__(self):
        """Init the AIML generator
        """
        self._db_username = config.AIML_DB_USER
        self._db_password = config.AIML_DB_PASSWORD
        self._current_pattern = None
        self._current_template = None

    def get_default_prompt_tokens(self, cli):
        """Return text for prompt tokens
        """
        return [
            (Token.Default, 'CMD '),
            (Token.LeftBracket, '['),
            (Token.Command, '_'),
            (Token.RightBracket, ']'),
            (Token.Colon, ': '),
        ]

    def get_template_prompt_tokens(self, cli):
        """Prompt when asking for template for a category
        """
        return [
            (Token.Command, 'CAT+ '),
            (Token.LeftBracket, '['),
            (Token.Pattern, self._current_pattern),
            (Token.RightBracket, ']'),
            (Token.Colon, ': '),
        ]

    def get_pattern_prompt_tokens(self, cli):
        """Prompt when asking for template for a category
        """
        return [
            (Token.Default, 'CAT '),
            (Token.LeftBracket, '['),
            (Token.Command, '+'),
            (Token.RightBracket, ']'),
            (Token.Colon, ': '),
        ]

    def start(self):
        """Start the while loop for prompt
        """
        cmd = ''
        current_cmd = 'DEFAULT'
        current_prompt_tokens_callback = self.get_default_prompt_tokens
        while cmd.lower() not in ['quit', 'exit']:
            cmd = prompt(get_prompt_tokens=self.current_prompt_tokens_callback, style=AimlGenerator.cmd_style)
            if current_cmd == 'DEFAULT': #not in any command mode, check which command is entered by user
                if cmd.lower() == 'new cat' or cmd.lower() == 'new category':
                    current_prompt_tokens_callback = self.get_pattern_prompt_tokens
                    current_cmd = 'CAT+'
                elif cmd.lower() in ['quit', 'exit']:
                    continue
                else:
                    print('Unsupported Command! Use help to find supported commands')
            elif current_cmd == 'CAT+': #In category-add cmd mode, next input is a pattern
                self._current_pattern = cmd.upper()
                current_cmd = 'CAT+PAT'
                current_prompt_tokens_callback = self.get_template_prompt_tokens
            elif current_cmd == 'CAT+PAT': #In category-add cmd mode with pattern already provided, next input is a template
                self._current_template = cmd.upper()
                current_cmd = 'DEFAULT'
                current_prompt_tokens_callback = self.get_default_prompt_tokens
                #we got both category and template, so saving it now
                self.save_category()
                cmd=''
                self._current_pattern = None
                self._current_template = None
            else: #unknown cmd-mode, will print error
                print('Unknown command mode, please try again!')

    def save_category(self):
        """Save the current category pattern and template in database
        """
        pass

if __name__ == '__main__':
    gen = AimlGenerator()
    gen.start()

