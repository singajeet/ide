"""
.. module:: main
   :platform: Any
   :synopsis: Utility to generate AIML files
.. moduleauthor:: ajeet singh
"""
from prompt_toolkit.shortcuts import prompt
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.interface import AbortAction
from prompt_toolkit.contrib.completers import WordCompleter
from common import config
from prompt_toolkit.token import Token
from aiml_gen.aiml import Category
import mysql.connector

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
        self._db_user = config.AIML_DB_USER
        self._db_password = config.AIML_DB_PASSWORD
        self._db_host = config.AIML_DB_HOST
        self._db_port = config.AIML_DB_PORT
        self._database = config.AIML_DB
        self._connection = mysql.connector.connect(host=self._db_host,\
                port=self._db_port, user=self._db_user,\
                password=self._db_password, database=self._database)
        self._current_pattern = None
        self._current_template = None
        self._cmd_history = FileHistory('.ide_aiml_gen.history')
        self._cmd_completer = self.get_cmd_completer()

    def get_cmd_completer(self):
        """Returns the list of words to use with completer
        """
        return WordCompleter(['New',
                'Category',
                'Edit',
                'Delete',
                'Exit',
                'Quit'],
                meta_dict = {
                    'New': 'Creates a new category and asks for pattern & template',
                    'Edit': 'Edit an exisiting category',
                    'Delete': 'Delete category from the system',
                    'Exit': 'Exit from this application',
                    'Quit': 'Quit from this application'
                    },
                ignore_case=True)

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
            cmd = prompt(
                    get_prompt_tokens=current_prompt_tokens_callback,
                    style=AimlGenerator.cmd_style,
                    history=self._cmd_history,
                    enable_history_search=True,
                    on_abort=AbortAction.RETRY,
                    auto_suggest=AutoSuggestFromHistory(),
                    completer=self._cmd_completer,
                    display_completions_in_columns=True
                    )
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
                self._current_template = cmd
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
        category = Category(self._connection, pattern=self._current_pattern, template=self._current_template)
        category.save()

if __name__ == '__main__':
    gen = AimlGenerator()
    gen.start()

