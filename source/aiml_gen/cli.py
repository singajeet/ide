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
        Token:          config.Token.Color,
        # Prompt.
        Token.Colon:    config.Token.Colon.Color,
        Token.Pound:    config.Token.Pound.Color,
        Token.Pattern:  config.Token.Pattern.Color,
        Token.Template: config.Token.Template.Color,
        Token.Default:  config.Token.Default.Color,
        Token.LeftBracket: config.Token.LBracket.Color,
        Token.RightBracket: config.Token.RBracket.Color,
        Token.Command: config.Token.Command.Color,
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
        self._register_commands()

    def _register_commands(self):
        """docstring for register_commands"""
        #-------------------- COMMAND => [NEW] SUB-COMMAND => [CATEGORY] --------------------
        cmd = 'NEW'
        cmd_description = 'Help in creating new object passed as sub-command'
        sub_cmd = 'CATEGORY'
        sub_cmd_description = 'The Category object available in AIML namespace'
        sub_cmd_kw_opts = {'PATTERN':'', 'TEMPLATE':'', 'SYSTEM':'',\
                'REF_THAT':'', 'REF_TOPIC':'', 'FORWARD_TO':''}
        sub_cmd_opts = {'--USE_DEFAULTS': False}
        #-------------------- Register Commands --------------------
        self._parser.register_command(cmd, description=cmd_description)
        self._parser.register_sub_command(cmd, sub_cmd, description=sub_cmd_description,\
                p_options=sub_cmd_opts, p_kw_options=sub_cmd_kw_opts)
        #-------------------- End Register Commands --------------------
        #-------------------- Populate command completer dicts --------------------
        cmd_completer = self._parser.get_cmd_completer()
        self._cmd_completer = WordCompleter(cmd_completer[0], meta_dict=cmd_completer[1], ignore_case=True)

    def get_default_prompt_tokens(self, cli):
        """Prompt when in default/no cmd modes
        """
        return [
            (Token.Default, config.Token.Default.Symbol),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.Command, config.Token.Command.Symbol),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Colon, config.Token.Colon.Symbol),
        ]

    def get_sub_cmd_prompt_tokens(self, cli):
        """Prompt when in sub command mode
        """
        return [
            (Token.Command, '%s ' % self._current_cmd),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.Pattern, self._current_sub_cmd),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Colon, config.Token.Colon.Symbol),
        ]

    def get_main_cmd_prompt_tokens(self, cli):
        """Prompt when in main command
        """
        return [
            (Token.Default, config.Token.Default.Symbol),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.Command, self._current_cmd),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Colon, config.Token.Colon.Symbol),
        ]

    def start(self):
        """Start the while loop for prompt
        """
        cmd_text = ''
        #current_cmd = 'DEFAULT'
        current_prompt_tokens_callback = self.get_default_prompt_tokens
        #prompt will use the input provided by user for the same main command
        #until is_cmd_session_in_progress is True. As soon as the cmd_session
        #is marked as False, all the collected information will be forwarded to
        #command processor callable and prompt will be rested to accept next new
        #main command
        #is_cmd_session_in_progress = False
        while cmd_text not in ['QUIT', 'EXIT']:
            cmd_text = prompt(
                    get_prompt_tokens=current_prompt_tokens_callback,
                    style=AimlGeneratorCLI.cmd_style,
                    history=self._cmd_history,
                    enable_history_search=True,
                    on_abort=AbortAction.RETRY,
                    auto_suggest=AutoSuggestFromHistory(),
                    completer=self._cmd_completer,
                    display_completions_in_columns=True
                    )
            cmd_text = cmd_text.upper()
            if len(cmd_text.split()) > 1:
                parsed_cmd = self._parser.parse_cmd_text(cmd_text)
                if parsed_cmd is None:
                    print('Command format is not valid! Kindly check and try again')
                    continue
                valid = self.validate_for_required_args(parsed_cmd)
                if valid:
                    #is_cmd_session_in_progress = True
                    #SCENARIO: Command don't have any sub command
                    if parsed_cmd['SUB_CMD'] is None or len(parsed_cmd['SUB_CMD']) <= 0:
                        processor_callback = parsed_cmd['PROCESSOR_CALLBACK']
                        if processor_callback is None or not callable(processor_callback):
                            print('No such command exists: %s' % parsed_cmd['MAIN_CMD'])
                        else:
                            processor_callback(parsed_cmd['MAIN_CMD'], parsed_cmd['OPTIONS'], parsed_cmd['KW_OPTIONS'])
                    elif parsed_cmd['SUB_CMD'] is not None and len(parsed_cmd['SUB_CMD']) > 0:
                        cmd_name = parsed_cmd['MAIN_CMD']
                        sub_cmd_name = tuple(parsed_cmd['SUB_CMD'])[0]
                        options = parsed_cmd['SUB_CMD'][sub_cmd_name]['OPTIONS']
                        kw_options = parsed_cmd['SUB_CMD'][sub_cmd_name]['KW_OPTIONS']
                        processor_callback = parsed_cmd['SUB_CMD'][sub_cmd_name]['PROCESSOR_CALLBACK']
                        if processor_callback is None or not callable(processor_callback):
                            print('No such sub-command exists: %s' % sub_cmd_name)
                        else:
                            processor_callback(cmd_name, sub_cmd_name, options, kw_options)
                    #is_cmd_session_in_progress = False
            else:
                pass

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
    gen = AimlGeneratorCLI()
    gen.start()
