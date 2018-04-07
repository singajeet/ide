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
        Token.Dollar:   config.Token.Dollar.Color,
        Token.Pattern:  config.Token.Pattern.Color,
        Token.Template: config.Token.Template.Color,
        Token.Default:  config.Token.Default.Color,
        Token.LeftBracket: config.Token.LBracket.Color,
        Token.RightBracket: config.Token.RBracket.Color,
        Token.Command: config.Token.Command.Color,
        Token.SubCommand: config.Token.SubCommand.Color,
        Token.CmdOpt: config.Token.CmdOpt.Color,
        Token.SubCmdOpt: config.Token.SubCmdOpt.Color,
        Token.LessThan: config.Token.LessThan.Color,
        Token.GreaterThan: config.Token.GreaterThan.Color,
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
        self._current_cmd_missing_opt = None
        self._current_sub_cmd_missing_opt = None
        self.__test_register_commands()

    def __test_new_cmd_callback(self, *args, **kwargs):
        """docstring for new_cmd_callback"""
        print('NEW CMD: ')
        print(*args)
        print(**kwargs)

    def __test_new_category_sub_cmd_callback(self, *args, **kwargs):
        """docstring for new_category_sub_cmd_callback"""
        print('NEW CATEGORY SUB-CMD: ')
        print(*args)
        print(**kwargs)

    def __test_register_commands(self):
        """docstring for register_commands"""
        #-------------------- COMMAND => [NEW] SUB-COMMAND => [CATEGORY] --------------------
        cmd = 'NEW'
        cmd_description = 'Help in creating new object passed as sub-command'
        sub_cmd = 'CATEGORY'
        sub_cmd_description = 'The Category object available in AIML namespace'
        sub_cmd_kw_opts = {'PATTERN':'', 'TEMPLATE':'', 'SYSTEM':'',\
                'REF_THAT':'', 'REF_TOPIC':'', 'FORWARD_TO':''}
        sub_cmd_opts = {'--USE_DEFAULTS': False}
        sub_cmd_required = ['PATTERN', 'TEMPLATE']
        #-------------------- Register Commands --------------------
        self._parser.register_command(cmd, description\
                =cmd_description, prompt_tokens_callback\
                =self.get_cmd_prompt_tokens, \
                cmd_processor_callback\
                =self.__test_new_cmd_callback)
        self._parser.register_sub_command(cmd, sub_cmd,\
                description=sub_cmd_description,\
                prompt_tokens_callback\
                =self.get_sub_cmd_prompt_tokens,
                cmd_processor_callback=\
                        self.__test_new_category_sub_cmd_callback,
                options=sub_cmd_opts,\
                kw_options=sub_cmd_kw_opts,\
                required_fields=sub_cmd_required)
        #-------------------- End Register Commands --------------------
        #-------------------- Populate command completer dicts --------------------
        cmd_completer = self._parser.get_cmd_completer()
        self._cmd_completer = WordCompleter(cmd_completer[0], meta_dict=cmd_completer[1], ignore_case=True)

    def get_default_prompt_tokens(self, cli):
        """Prompt when in default/no cmd modes
        """
        return [
            (Token.Dollar, config.Token.Dollar.Symbol),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.Default, config.Token.Default.Symbol),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Colon, config.Token.Colon.Symbol),
        ]

    def get_sub_cmd_prompt_tokens(self, cli):
        """Prompt when in sub command mode
        """
        return [
            (Token.Dollar, config.Token.Dollar.Symbol),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.Command, '%s' % self._current_cmd),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Seperator, '-'),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.SubCommand, '%s' % self._current_sub_cmd),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Dot, '.'),
            (Token.Dot, '.'),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.SubCmdOpt, self._current_sub_cmd_missing_opt \
                if self._current_sub_cmd_missing_opt is not None\
                else 'OPT'),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Colon, config.Token.Colon.Symbol),
        ]

    def get_cmd_prompt_tokens(self, cli):
        """Prompt when in main command and prompting values for
        missing options or kw-options
        """
        return [
            (Token.Dollar, config.Token.Dollar.Symbol),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.Command, '%s' % self._current_cmd),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Dot, '.'),
            (Token.Dot, '.'),
            (Token.LeftBracket, config.Token.LBracket.Symbol),
            (Token.CmdOpt, self._current_cmd_missing_opt\
                    if self._current_cmd_missing_opt is not None\
                    else 'OPT'),
            (Token.RightBracket, config.Token.RBracket.Symbol),
            (Token.Colon, config.Token.Colon.Symbol),
        ]

    def validate_for_required_args(self, parsed_cmd):
        """docstring for validate_for_required_args"""
        #SCENARIO: Return True (i.e., cmd is valid)
        #if no required attributes for main cmd
        #and no sub-cmd for this main cmd found
        if len(parsed_cmd['REQUIRED']) <= 0 and\
                len(parsed_cmd['SUB_CMD']) <= 0:
            return (True, {})
        #SCENARIO: Main cmd has required attr's and\
        #no-sub cmd for this main cmd
        elif len(parsed_cmd['REQUIRED']) > 0 and\
                len(parsed_cmd['SUB_CMD']) <= 0:
            #SUB-SCENARIO: if no opts or kw-opts exists
            #in cmd, return true
            if len(parsed_cmd['OPTIONS']) <= 0 and\
                    len(parsed_cmd['KW_OPTIONS']) <= 0:
                return (True, {})
            #SUB-SCENARIO: if opts or kw-opts exist in cmd
            #check whether all required flds exists in any
            #opt or kw-opt
            else:
                (status, cmd_flds) = self.validate_options(parsed_cmd)
                flds_dict = {}
                flds_dict['CMD'] = cmd_flds
                return (status, flds_dict)
        elif len(parsed_cmd['REQUIRED']) <= 0 and\
                len(parsed_cmd['SUB_CMD']) > 0:
            #sub_cmds = parsed_cmd['SUB_CMD']
            sub_cmd_name = tuple(parsed_cmd['SUB_CMD'])[0]
            sub_cmd_details = parsed_cmd['SUB_CMD'][sub_cmd_name]
            (status, sub_cmd_flds) =  self.validate_options(sub_cmd_details)
            flds_dict = {}
            flds_dict['SUB_CMD'] = sub_cmd_flds
            return (status, flds_dict)
        elif len(parsed_cmd['REQUIRED']) > 0 and\
                len(parsed_cmd['SUB_CMD']) > 0:
            flds_dict={}
            (cmd_status, cmd_flds) = self.validate_options(parsed_cmd)
            flds_dict['CMD'] = cmd_flds
            #sub_cmds = parsed_cmd['SUB_CMD']
            sub_cmd_name = tuple(parsed_cmd['SUB_CMD'])[0]
            sub_cmd_details = parsed_cmd['SUB_CMD'][sub_cmd_name]
            (sub_cmd_status, sub_cmd_flds) = \
                    self.validate_options(sub_cmd_details)
            flds_dict['SUB_CMD'] = sub_cmd_flds
            if cmd_status is False or  sub_cmd_status is False:
                return (False, flds_dict)
        else:
            return (True, {})

    def validate_options(self, parsed_cmd):
        required_fields = parsed_cmd['REQUIRED']
        req_fld_dict = { fld : False for fld in required_fields }
        if req_fld_dict is not None and len(req_fld_dict) > 0:
            if len(parsed_cmd['OPTIONS']) > 0:
                for fld_name, status in req_fld_dict.items():
                    #check if fld available in options
                    if status is False:
                        if parsed_cmd['OPTIONS'].\
                                __contains__(fld_name)\
                                and parsed_cmd['OPTIONS'][fld_name]\
                                is not None:
                                    req_fld_dict[fld_name] = True
            if len(parsed_cmd['KW_OPTIONS']) > 0:
                for fld_name, status in req_fld_dict.items():
                    #check if fld available in kw-options
                    if status is False:
                        if parsed_cmd['KW_OPTIONS'].\
                                __contains__(fld_name) and\
                                parsed_cmd['KW_OPTIONS'][fld_name]\
                                is not None:
                                    req_fld_dict[fld_name] = True
        #return required fields dict containing items in following form:
        # { field_name : status } where status it true or false based on
        # whether the field has a value or not.
        #
        #We start with first item in dict and return as soon as we get the
        #first field with no value. No need to check the remaining fields
        #since dict already contains the status of each field.
        #
        #A list of fields with empty value will be returned only
        #
        #Calling method will iterate all list items and will prompt input
        #from user
        for fld, status in req_fld_dict.items():
            if status is False:
                return (False, [fld for fld, status in req_fld_dict\
                        .items() if status is False])
        return (True, [])

    def start(self):
        """Start the while loop for prompt
        """
        cmd_text = ''
        #prompt will use the input provided by user for the same main command
        #until is_cmd_session_in_progress is True. As soon as the cmd_session
        #is marked as False, all the collected information will be forwarded to
        #command processor callable and prompt will be rested to accept next new
        #main command
        while cmd_text not in ['QUIT', 'EXIT']:
            cmd_text = prompt(
                    get_prompt_tokens=self.get_default_prompt_tokens,
                    style=AimlGeneratorCLI.cmd_style,
                    history=self._cmd_history,
                    enable_history_search=True,
                    on_abort=AbortAction.RETRY,
                    auto_suggest=AutoSuggestFromHistory(),
                    completer=self._cmd_completer,
                    display_completions_in_columns=True,
                    complete_while_typing=True
                    )
            cmd_text = cmd_text.upper()
            #Process command text if atleast 2 tokens are provided
            #It can be a combo of "CMD SUB-CMD" or "CMD OPTIONS"
            if len(cmd_text.split()) > 1:
                parsed_cmd = self._parser.parse_cmd_text(cmd_text)
                if parsed_cmd is None:
                    print('Invalid command syntax!')
                    self.list_all_cmds()
                    continue
                (valid, missing_flds) = self.validate_for_required_args(parsed_cmd)
                if valid:
                    self._current_cmd = parsed_cmd['MAIN_CMD']
                    if len(parsed_cmd['SUB_CMD']) > 0:
                        self._current_sub_cmd = tuple(parsed_cmd['SUB_CMD'])[0]
                    else:
                        self._current_sub_cmd = None
                    self.execute_command(parsed_cmd)
                else:
                    #required fields are missing, prompt for same
                    self._current_cmd = parsed_cmd['MAIN_CMD']
                    if len(parsed_cmd['SUB_CMD']) > 0:
                        self._current_sub_cmd = tuple(parsed_cmd['SUB_CMD'])[0]
                    else:
                        self._current_sub_cmd = None
                    for flds_type, flds_list in missing_flds.items():
                        for fld in flds_list:
                            parsed_cmd = self.get_missing_fld_input(fld,\
                                    flds_type, parsed_cmd)
                    self.execute_command(parsed_cmd)
            #Only one token is provided in the command text
            else:
                #if the only token provided is a valid command
                #process it
                if self._parser.cmd_exists(cmd_text):
                    if not self._parser.cmd_has_sub_cmds(cmd_text):
                        processor_callback = \
                                self._parser.get_cmd_processor_callback(cmd_text)
                        if processor_callback is not None\
                                and callable(processor_callback):
                            processor_callback(cmd_text)
                        else:
                            print("No callable found for command: %s" % cmd_text)
                    else:
                        print('No sub-command provided for command: %s' % cmd_text)
                        self.list_sub_cmds_of_cmd(cmd_text)
                else:
                    print('No such command found: %s' % cmd_text)
                    self.list_all_cmds()

    def list_all_cmds(self):
        """docstring for list_all_cmds"""
        self._parser.list_all_cmds();

    def list_sub_cmds_of_cmd(self, cmd_name):
        """docstring for list_sub_cmds_of_cmd"""
        self._parser.list_sub_cmds_of_cmd(cmd_name)

    def execute_command(self, parsed_cmd):
        """docstring for execute_command"""
        #SCENARIO: Command don't have any sub command
        if parsed_cmd['SUB_CMD'] is None or len(parsed_cmd['SUB_CMD']) <= 0:
            processor_callback = parsed_cmd['PROCESSOR_CALLBACK']
            if processor_callback is None or not callable(processor_callback):
                print('No callable found for command: %s' % parsed_cmd['MAIN_CMD'])
            else:
                processor_callback(parsed_cmd['MAIN_CMD'], parsed_cmd['OPTIONS'], parsed_cmd['KW_OPTIONS'])
        #SCENARIO: Command have an sub command
        elif parsed_cmd['SUB_CMD'] is not None and len(parsed_cmd['SUB_CMD']) > 0:
            cmd_name = parsed_cmd['MAIN_CMD']
            sub_cmd_name = tuple(parsed_cmd['SUB_CMD'])[0]
            options = parsed_cmd['SUB_CMD'][sub_cmd_name]['OPTIONS']
            kw_options = parsed_cmd['SUB_CMD'][sub_cmd_name]['KW_OPTIONS']
            processor_callback = parsed_cmd['SUB_CMD'][sub_cmd_name]['PROCESSOR_CALLBACK']
            if processor_callback is None or not callable(processor_callback):
                print('No callable found for sub-command: %s' % sub_cmd_name)
            else:
                processor_callback(cmd_name, sub_cmd_name, options, kw_options)

    def get_missing_fld_input(self, fld_name, flds_type, parsed_cmd):
        """docstring for get_missing_fld_input"""
        missing_cmd_value = ''
        missing_cmd_dict = parsed_cmd if flds_type == 'CMD' else parsed_cmd['SUB_CMD'][self._current_sub_cmd]
        prompt_tokens_callback = None
        self._current_cmd_missing_opt = None
        self._current_sub_cmd_missing_opt = None
        if flds_type == 'CMD':
            prompt_tokens_callback = self._parser.get_cmd_prompt_token_callback(self._current_cmd)\
            if self._parser.get_cmd_prompt_token_callback(self._current_cmd) is not None\
            else self.get_cmd_prompt_tokens #the default prompt tokens callback
            self._current_sub_cmd_missing_opt = None
            self._current_cmd_missing_opt = fld_name
        else:
            prompt_tokens_callback = self._parser.get_sub_cmd_prompt_token_callback(self._current_cmd, self._current_sub_cmd)\
            if self._parser.get_sub_cmd_prompt_token_callback(self._current_cmd, self._current_sub_cmd) is not None\
            else self.get_sub_cmd_prompt_tokens #the default prompt tokens callback
            self._current_cmd_missing_opt = None
            self._current_sub_cmd_missing_opt = fld_name

        missing_cmd_value = prompt(
                get_prompt_tokens=prompt_tokens_callback,
                style=AimlGeneratorCLI.cmd_style
                )
        if fld_name.startswith('-'):
            if missing_cmd_value is not None and missing_cmd_value in ['YES', 'Y', 'TRUE', 'T']:
                missing_cmd_dict['OPTIONS'][fld_name] = True
            else:
                missing_cmd_dict['OPTIONS'][fld_name] = False
        else:
            missing_cmd_dict['KW_OPTIONS'][fld_name] = missing_cmd_value
        if flds_type == 'CMD':
            return missing_cmd_dict #i.e., parsed_cmd
        else:
            parsed_cmd['SUB_CMD'][self._current_sub_cmd] = missing_cmd_dict
            return parsed_cmd

    def print_cmd_help(self, cmd_name, sub_cmd_name=None):
        """docstring for print"""
        print('Will print help here!')


if __name__ == '__main__':
    gen = AimlGeneratorCLI()
    gen.start()
