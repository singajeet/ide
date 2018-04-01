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


DESCRIPTION = 'DESCRIPTION'
TOKEN_CALLBACK = 'TOKEN_CALLBACK'
PROCESSOR_CALLBACK = 'PROCESSOR_CALLBACK'
SUB_COMMANDS = 'SUB_COMMANDS'
MAIN_CMD = 'MAIN_CMD'
SUB_CMD = 'SUB_CMD'
OPTIONS = 'OPTIONS'
OPTION = 'OPTION'
KW_OPTIONS = 'KW_OPTIONS'
KW_OPTION = 'KW_OPTION'


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
        """Init the AIML generator
        """
        self._current_cmd = None
        self._current_sub_cmd = None
        self._is_command_completed = None
        self._commands_registry = {}
        self._db_user = config.AIML_DB_USER
        self._db_password = config.AIML_DB_PASSWORD
        self._db_host = config.AIML_DB_HOST
        self._db_port = config.AIML_DB_PORT
        self._database = config.AIML_DB
        self._connection = mysql.connector.connect(host=self._db_host,\
                port=self._db_port, user=self._db_user,\
                password=self._db_password, database=self._database)
        self._cmd_history = FileHistory('.ide_aiml_gen.history')
        self._cmd_completer = self.get_cmd_completer()

    def register_command(self, cmd, description=None, get_prompt_tokens_callback=None, cmd_processor_callback=None):
        """docstring for register_command"""
        if self._command_registry is None:
            self._command_registry = {}
        if cmd is not None:
            cmd = cmd.upper()
            if self._command_registry.__contains__(cmd):
                self._command_registry.pop(cmd)
            cmd_record = {}
            cmd_record[DESCRIPTION] = description
            cmd_record[TOKEN_CALLBACK] = get_prompt_tokens_callback
            cmd_record[PROCESSOR_CALLBACK] = cmd_processor_callback
            cmd_record[SUB_COMMANDS] = {}
            self._command_registry[cmd] = cmd_record

    def register_sub_command(self, cmd, sub_cmd, description=None, get_prompt_tokens_callback=None):
        """docstring for register_sub_command"""
        if self._command_registry is None:
            raise Exception('Command registry is not yet initialized. Atleast one command needs to registered to init the command registry')
        cmd = cmd.upper()
        if self._command_registry.__contains__(cmd):
            cmd_record = self._command_registry[cmd]
            sub_cmds = cmd_record[SUB_COMMANDS]
            if sub_cmds.__contains__(sub_cmd):
                sub_cmds.pop(sub_cmd)
            sub_cmd_record = {}
            sub_cmd_record[DESCRIPTION] = description
            sub_cmd_record[TOKEN_CALLBACK] = get_prompt_tokens_callback
            sub_cmds[sub_cmd] = sub_cmd_record
        else:
            raise Exception('Main command [%s] is not registered yet' % cmd)

    def get_cmd_completer(self):
        """Returns the list of words to use with completer
        """
        cmds_list = []
        cmds_meta_dict = {}
        for cmd_name, cmd in self._commands_registry.items():
            if cmds_list.__contains__(cmd_name):
                cmds_list.pop(cmd_name)
                cmds_meta_dict.pop(cmd_name)
            cmds_list.append(cmd_name)
            cmds_meta_dict[cmd_name] = cmd[DESCRIPTION]
            sub_cmds = cmd[SUB_COMMANDS]
            for sub_cmd_name, sub_cmd in sub_cmds.items():
                if not cmds_list.__contains__(sub_cmd_name):
                    cmds_list.append(sub_cmd_name)
                    cmds_meta_dict[sub_cmd_name] = sub_cmd[DESCRIPTION]
        return WordCompletor(cmds_list, meta_dict=cmds_meta_dict, ignore_case=True)

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

    def get_sub_cmds(self, cmd_name):
        """docstring for get_sub_cmds"""
        cmd_name = cmd_name.upper()
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(SUB_COMMANDS):
                sub_cmds = cmd[SUB_COMMANDS]
                return sub_cmds
        return None

    def get_cmds(self):
        """docstring for get_cmds"""
        if self._commands_registry is None:
            return None
        return self._commands_registry

    def get_cmd(self, cmd_name):
        """docstring for get_cmd"""
        cmd_name = cmd_name.upper()
        if self.cmd_exists(cmd_name):
            return self.get_cmds()[cmd_name]
        return None

    def get_cmd_description(self, cmd_name):
        """docstring for get_cmd_details"""
        cmd_name = cmd_name.upper()
        cmd = self.get_cmd(cmd_name)
        if cmd is not None:
            return cmd[DESCRIPTION]
        else:
            return None

    def get_cmd_prompt_token_callback(self, cmd_name):
        """docstring for get_cmd_prompt_token_callback"""
        cmd_name = cmd_name.upper()
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            return cmd[TOKEN_CALLBACK]
        else:
            return None

    def get_cmd_processor_callback(self, cmd_name):
        """docstring for get_cmd_processor_callback"""
        cmd_name = cmd_name.upper()
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            return cmd[PROCESSOR_CALLBACK]
        else:
            return None

    def cmd_exists(self, cmd_name):
        """docstring for cmd_exists"""
        if self._commands_registry is None:
            return False
        cmd_name = cmd_name.upper()
        if self._commands_registry.__contains__(cmd_name):
            return True
        else:
            return False

    def sub_cmd_exists(self, cmd_name, sub_cmd_name):
        """docstring for sub_cmd_exists"""
        cmd_name = cmd_name.upper()
        sub_cmd_name = sub_cmd_name.upper()
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(SUB_COMMANDS):
                sub_cmds = cmd[SUB_COMMANDS]
                if sub_cmds.__contains__(sub_cmd_name):
                    return True
        return False

    def get_sub_cmd(self, cmd_name, sub_cmd_name):
        """docstring for get_sub_cmd"""
        cmd_name = cmd_name.upper()
        sub_cmd_name = sub_cmd_name.upper()
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmds = self.get_sub_cmds(cmd_name)
            return sub_cmds[sub_cmd_name]
        return None

    def get_sub_cmd_description(self, cmd_name, sub_cmd_name):
        """docstring for get_sub_cmd_description"""
        cmd_name = cmd_name.upper()
        sub_cmd_name = sub_cmd_name.upper()
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            if sub_cmd is not None:
                return sub_cmd[DESCRIPTION]
        return None

    def get_sub_cmd_prompt_token_callback(self, cmd_name, sub_cmd_name):
        """docstring for get_sub_cmd_prompt_token_callback"""
        cmd_name = cmd_name.upper()
        sub_cmd_name = sub_cmd_name.upper()
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            if sub_cmd is not None:
                return cmd[TOKEN_CALLBACK]
        return None

    def cmd_has_sub_cmds(self, cmd_name):
        """docstring for cmd_has_sub_cmds"""
        cmd_name = cmd_name.upper()
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(SUB_COMMANDS):
                sub_cmds = cmd[SUB_COMMANDS]
                if len(sub_cmds) > 0:
                    return True
        return False

    def cmd_has_options(self, cmd_name):
        """docstring for cmd_has_options"""
        cmd_name = cmd_name.upper()
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(OPTIONS):
                opts = cmd[OPTIONS]
                if len(opts) > 0:
                    return True
        return False

    def cmd_has_kw_options(self, cmd_name):
        """docstring for cmd_has_kw_options"""
        cmd_name = cmd_name.upper()
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(KW_OPTIONS):
                kw_opts = cmd[KW_OPTIONS]
                if len(kw_opts) > 0:
                    return True
        return False


    def parse_cmd_text(self, cmd_text):
        """docstring for parse_cmd_text"""
        if cmd_text is None:
            return None
        cmd_tokens = cmd_text.split()
        cmd = {}
        if len(cmd_tokens) > 0:
            #the first token is main command
            main_cmd = cmd_tokens[0]
            #check if the provided cmd is registered or not
            if self.cmd_exists(main_cmd):
                #process the command further to get subcmds and opts
                cmd[MAIN_CMD] = main_cmd
                if len(cmd_tokens) > 0:
                    #we still have more tokens to be processed
                    #The tokens could be param to main cmd or
                    #it could be an subcmd.
                    sub_cmds = self._comm
            else:
                #Command is not registered, will return None
                return None

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

