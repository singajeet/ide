"""
.. module:: cli
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
from aiml_gen.parser import CommandParser
import mysql.connector


class AimlGeneratorCLI(object):
    """Command Line Interface(CLI) to generate AIML files based on the input provided by user
    """

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
        """docstring for __init__"""
        self._parser = CommandParser()
        self._db_user = config.AIML_DB_USER
        self._db_password = config.AIML_DB_PASSWORD
        self._db_host = config.AIML_DB_HOST
        self._db_port = config.AIML_DB_PORT
        self._database = config.AIML_DB
        self._connection = mysql.connector.connect(host=self._db_host,\
                port=self._db_port, user=self._db_user,\
                password=self._db_password, database=self._database)
        self._cmd_history = FileHistory('.ide_aiml_gen.history')
        self._cmd_completer = self._parser.get_cmd_completer()

    def get_default_prompt_tokens(self, cli):
        """Prompt when in default/no cmd modes
        """
        return [
            (Token.Default, 'CMD '),
            (Token.LeftBracket, '['),
            (Token.Command, '$_'),
            (Token.RightBracket, ']'),
            (Token.Colon, ': '),
        ]

    def get_sub_cmd_prompt_tokens(self, cli):
        """Prompt when in sub command mode
        """
        return [
            (Token.Command, '%s ' % self._current_cmd),
            (Token.LeftBracket, '['),
            (Token.Pattern, self._current_sub_cmd),
            (Token.RightBracket, ']'),
            (Token.Colon, ': '),
        ]

    def get_main_cmd_prompt_tokens(self, cli):
        """Prompt when in main command
        """
        return [
            (Token.Default, 'CMD '),
            (Token.LeftBracket, '['),
            (Token.Command, self._current_cmd),
            (Token.RightBracket, ']'),
            (Token.Colon, ': '),
        ]

    def start(self):
        """Start the while loop for prompt
        """
        cmd_text = ''
        current_cmd = 'DEFAULT'
        current_prompt_tokens_callback = self.get_default_prompt_tokens
        while cmd_text not in ['QUIT', 'EXIT']:
            cmd_text = prompt(
                    get_prompt_tokens=current_prompt_tokens_callback,
                    style=AimlGenerator.cmd_style,
                    history=self._cmd_history,
                    enable_history_search=True,
                    on_abort=AbortAction.RETRY,
                    auto_suggest=AutoSuggestFromHistory(),
                    completer=self._cmd_completer,
                    display_completions_in_columns=True
                    )
            cmd_text = cmd_text.upper()

            """if current_cmd == 'DEFAULT': #not in any command mode, check which command is entered by user
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
            """

    def save_category(self):
        """Save the current category pattern and template in database
        """
        category = Category(self._connection, pattern=self._current_pattern, template=self._current_template)
        category.save()

if __name__ == '__main__':
    gen = AimlGenerator()
    gen.start()
