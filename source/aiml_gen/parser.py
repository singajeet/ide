"""
.. module:: main
   :platform: Any
   :synopsis: Utility to generate AIML files
.. moduleauthor:: ajeet singh
"""


NAME = 'NAME'
DETAILS = 'DETAILS'
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
REQUIRED = 'REQUIRED'

class CommandParser(object):
    """Parser for parsing line string provided to this class based on the cmds registered
    """

    def __init__(self):
        """Init the AIML generator
        """
        self._current_cmd = None
        self._current_sub_cmd = None
        self._is_command_completed = None
        self._command_registry = {}

    def register_command(self, cmd, description=None, prompt_tokens_callback=None,\
            cmd_processor_callback=None, options={}, kw_options={}, required_fields=[]):
        """docstring for register_command"""
        if self._command_registry is None:
            self._command_registry = {}
        if cmd is not None:
            cmd = cmd.upper()
            if self._command_registry.__contains__(cmd):
                self._command_registry.pop(cmd)
            cmd_record = {}
            cmd_record[DESCRIPTION] = description
            cmd_record[TOKEN_CALLBACK] = prompt_tokens_callback
            cmd_record[PROCESSOR_CALLBACK] = cmd_processor_callback
            cmd_record[SUB_COMMANDS] = {}
            u_options = {}
            for opt, val in options.items():
                u_options[opt.upper()] = val.upper()
            cmd_record[OPTIONS] = u_options
            u_kw_options = {}
            for opt, val in kw_options.items():
                u_kw_options[opt.upper()] = val.upper()
            cmd_record[KW_OPTIONS] = u_kw_options
            cmd_record[REQUIRED] = required_fields
            self._command_registry[cmd] = cmd_record

    def register_sub_command(self, cmd, sub_cmd, description=None, prompt_tokens_callback=None, cmd_processor_callback=None, options={}, kw_options={}, required_fields=[]):
        """docstring for register_sub_command"""
        if self._command_registry is None:
            raise Exception('Command registry is not yet initialized. Atleast one command needs \
                    to registered to init the command registry')
        cmd = cmd.upper()
        sub_cmd = sub_cmd.upper()
        if self._command_registry.__contains__(cmd):
            cmd_record = self._command_registry[cmd]
            sub_cmds = cmd_record[SUB_COMMANDS]
            if sub_cmds.__contains__(sub_cmd):
                sub_cmds.pop(sub_cmd)
            sub_cmd_record = {}
            sub_cmd_record[DESCRIPTION] = description
            sub_cmd_record[TOKEN_CALLBACK] = prompt_tokens_callback
            sub_cmd_record[PROCESSOR_CALLBACK] = cmd_processor_callback
            u_options = {}
            for opt, val in options.items():
                u_options[opt.upper()] = val
            u_kw_options = {}
            for opt, val in kw_options.items():
                u_kw_options[opt.upper()] = val
            sub_cmd_record[OPTIONS] = u_options
            sub_cmd_record[KW_OPTIONS] = u_kw_options
            sub_cmd_record[REQUIRED] = required_fields
            sub_cmds[sub_cmd] = sub_cmd_record
        else:
            raise Exception('Main command [%s] is not registered yet' % cmd)

    def get_cmd_completer(self):
        """Returns the list of words to use with completer
        """
        cmds_list = []
        cmds_meta_dict = {}
        for cmd_name, cmd in self._command_registry.items():
            if cmds_list.__contains__(cmd_name):
                cmds_list.pop(cmd_name)
                cmds_meta_dict.pop(cmd_name)
            cmds_list.append(cmd_name)
            cmds_meta_dict[cmd_name] = cmd[DESCRIPTION]
            #options
            for opt, val in cmd[OPTIONS].items():
                if cmds_list.__contains__(opt):
                    cmds_list.pop(opt)
                cmds_list.append(opt)
            #kw options
            for opt, val in cmd[KW_OPTIONS].items():
                if cmds_list.__contains__(opt):
                    cmds_list.pop(opt)
                cmds_list.append(opt)

            #-------- Sub CMDs ---------#
            sub_cmds = cmd[SUB_COMMANDS]
            for sub_cmd_name, sub_cmd in sub_cmds.items():
                if not cmds_list.__contains__(sub_cmd_name):
                    cmds_list.append(sub_cmd_name)
                    cmds_meta_dict[sub_cmd_name] = sub_cmd[DESCRIPTION]
                #options
                for opt, val in sub_cmd[OPTIONS].items():
                    if cmds_list.__contains__(opt):
                        cmds_list.pop(opt)
                    cmds_list.append(opt)
                #kw options
                for opt, val in sub_cmd[KW_OPTIONS].items():
                    if cmds_list.__contains__(opt):
                        cmds_list.pop(opt)
                    cmds_list.append(opt)

        return (cmds_list, cmds_meta_dict)

    #=========== Begin Commands ============#

    def get_cmds(self):
        """docstring for get_cmds"""
        if self._command_registry is None:
            return None
        return self._command_registry

    def cmd_exists(self, cmd_name):
        """docstring for cmd_exists"""
        if self._command_registry is None:
            return False
        cmd_name = cmd_name.upper()
        if self._command_registry.__contains__(cmd_name):
            return True
        else:
            return False

    def get_cmd_required_fields(self, cmd_name):
        """docstring for get_cmd_required_fields"""
        cmd = self.get_cmd(cmd_name)
        if cmd is not None:
            return cmd[REQUIRED]
        return None

    def get_cmd(self, cmd_name):
        """docstring for get_cmd"""
        cmd_name = cmd_name.upper()
        if self.cmd_exists(cmd_name):
            return self.get_cmds()[cmd_name]
        return None

    def get_cmd_description(self, cmd_name):
        """docstring for get_cmd_details"""
        cmd = self.get_cmd(cmd_name)
        if cmd is not None:
            return cmd[DESCRIPTION]
        else:
            return None

    def get_cmd_prompt_token_callback(self, cmd_name):
        """docstring for get_cmd_prompt_token_callback"""
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            return cmd[TOKEN_CALLBACK]
        else:
            return None

    def get_cmd_processor_callback(self, cmd_name):
        """docstring for get_cmd_processor_callback"""
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            return cmd[PROCESSOR_CALLBACK]
        else:
            return None

    def cmd_has_options(self, cmd_name):
        """docstring for cmd_has_options"""
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(OPTIONS):
                opts = cmd[OPTIONS]
                if len(opts) > 0:
                    return True
        return False

    def cmd_has_kw_options(self, cmd_name):
        """docstring for cmd_has_kw_options"""
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(KW_OPTIONS):
                opts = cmd[KW_OPTIONS]
                if len(opts) > 0:
                    return True
        return False

    def get_cmd_options(self, cmd_name):
        """docstring for get_cmd_options"""
        if self.cmd_has_options(cmd_name):
            cmd = self.get_cmd(cmd_name)
            return cmd[OPTIONS]
        return None

    def get_cmd_kw_options(self, cmd_name):
        """docstring for get_cmd_options"""
        if self.cmd_has_kw_options(cmd_name):
            cmd = self.get_cmd(cmd_name)
            return cmd[KW_OPTIONS]
        return None

    def cmd_has_option(self, cmd_name, opt_name):
        """docstring for has_cmd_option"""
        opt_name = opt_name.upper()
        if self.cmd_has_options(cmd_name):
            opts = self.get_cmd_options(cmd_name)
            if opts.__contains__(opt_name):
                return True
        return False

    def cmd_has_kw_option(self, cmd_name, opt_name):
        """docstring for cmd_has_kw_option"""
        opt_name = opt_name.upper()
        if self.cmd_has_kw_options(cmd_name):
            opts = self.get_cmd_kw_options(cmd_name)
            if opts.__contains__(opt_name):
                return True
        return False

    def get_cmd_option(self, cmd_name, opt_name):
        """docstring for get_cmd_option"""
        opt_name = opt_name.upper()
        if self.cmd_has_option(cmd_name, opt_name):
            opts = self.get_cmd_options(cmd_name)
            return opts[opt_name]
        return None

    def get_cmd_kw_option(self, cmd_name, opt_name):
        """docstring for get_cmd_kw_option"""
        opt_name = opt_name.upper()
        if self.cmd_has_kw_option(cmd_name, opt_name):
            opts = self.get_cmd_kw_options(cmd_name)
            return opts[opt_name]
        return None


    #============== End Commands ==============#
    #============== Begin Sub Commands ========#

    def cmd_has_sub_cmds(self, cmd_name):
        """docstring for cmd_has_sub_cmds"""
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(SUB_COMMANDS):
                sub_cmds = cmd[SUB_COMMANDS]
                if len(sub_cmds) > 0:
                    return True
        return False

    def get_sub_cmds(self, cmd_name):
        """docstring for get_sub_cmds"""
        if self.cmd_exists(cmd_name):
            cmd = self.get_cmd(cmd_name)
            if cmd.__contains__(SUB_COMMANDS):
                sub_cmds = cmd[SUB_COMMANDS]
                return sub_cmds
        return None

    def sub_cmd_exists(self, cmd_name, sub_cmd_name):
        """docstring for sub_cmd_exists"""
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
        sub_cmd_name = sub_cmd_name.upper()
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmds = self.get_sub_cmds(cmd_name)
            return sub_cmds[sub_cmd_name]
        return None

    def get_sub_cmd_required_fields(self, cmd_name, sub_cmd_name):
        """docstring for get_sub_cmd_required_fields"""
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            if sub_cmd is not None:
                return sub_cmd[REQUIRED]
        return None

    def get_sub_cmd_description(self, cmd_name, sub_cmd_name):
        """docstring for get_sub_cmd_description"""
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            if sub_cmd is not None:
                return sub_cmd[DESCRIPTION]
        return None

    def get_sub_cmd_prompt_token_callback(self, cmd_name, sub_cmd_name):
        """docstring for get_sub_cmd_prompt_token_callback"""
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            if sub_cmd is not None:
                return sub_cmd[TOKEN_CALLBACK]
        return None

    def get_sub_cmd_processor_callback(self, cmd_name, sub_cmd_name):
        """docstring for get_cmd_processor_callback"""
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            return sub_cmd[PROCESSOR_CALLBACK]
        else:
            return None

    def sub_cmd_has_options(self, cmd_name, sub_cmd_name):
        """docstring for sub_cmd_has_options"""
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            if sub_cmd.__contains__(OPTIONS):
                opts = sub_cmd[OPTIONS]
                if len(opts) > 0:
                    return True
        return False

    def sub_cmd_has_kw_options(self, cmd_name, sub_cmd_name):
        """docstring for sub_cmd_has_kw_options"""
        if self.sub_cmd_exists(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            if sub_cmd.__contains__(KW_OPTIONS):
                opts = sub_cmd[KW_OPTIONS]
                if len(opts) > 0:
                    return True
        return False

    def get_sub_cmd_options(self, cmd_name, sub_cmd_name):
        """docstring for get_sub_cmd_options"""
        if self.sub_cmd_has_options(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            return sub_cmd[OPTIONS]
        return None

    def get_sub_cmd_kw_options(self, cmd_name, sub_cmd_name):
        """docstring for get_sub_cmd_options"""
        if self.sub_cmd_has_kw_options(cmd_name, sub_cmd_name):
            sub_cmd = self.get_sub_cmd(cmd_name, sub_cmd_name)
            return sub_cmd[KW_OPTIONS]
        return None

    def sub_cmd_has_option(self, cmd_name, sub_cmd_name, opt_name):
        """docstring for sub_cmd_has_option"""
        opt_name = opt_name.upper()
        if self.sub_cmd_has_options(cmd_name, sub_cmd_name):
            opts = self.get_sub_cmd_options(cmd_name, sub_cmd_name)
            if opts.__contains__(opt_name):
                return True
        return False

    def sub_cmd_has_kw_option(self, cmd_name, sub_cmd_name, opt_name):
        """docstring for sub_cmd_has_kw_option"""
        opt_name = opt_name.upper()
        if self.sub_cmd_has_kw_options(cmd_name, sub_cmd_name):
            opts = self.get_sub_cmd_kw_options(cmd_name, sub_cmd_name)
            if opts.__contains__(opt_name):
                return True
        return False

    def get_sub_cmd_option(self, cmd_name, sub_cmd_name, opt_name):
        """docstring for get_sub_cmd_option"""
        opt_name = opt_name.upper()
        if self.sub_cmd_has_option(cmd_name, sub_cmd_name, opt_name):
            opts = self.get_sub_cmd_options(cmd_name, sub_cmd_name)
            return opts[opt_name]
        return None

    def get_sub_cmd_kw_option(self, cmd_name, sub_cmd_name, opt_name):
        """docstring for get_sub_cmd_kw_option"""
        opt_name = opt_name.upper()
        if self.sub_cmd_has_kw_option(cmd_name, sub_cmd_name, opt_name):
            opts = self.get_sub_cmd_kw_options(cmd_name, sub_cmd_name)
            return opts[opt_name]
        return None

    #========== End Sub Commands =============#

    def parse_cmd_text(self, cmd_text):
        """docstring for parse_cmd_text"""
        if cmd_text is None:
            return None
        cmd_tokens = cmd_text.split()
        parsed_cmd = {}
        if len(cmd_tokens) > 0:
            #the first token is main command
            main_cmd = cmd_tokens[0].upper()
            #check if the provided cmd is registered or not
            if self.cmd_exists(main_cmd):
                #process the command further to get subcmds and opts
                parsed_cmd[MAIN_CMD] = main_cmd
                parsed_cmd[REQUIRED] = self.get_cmd_required_fields(main_cmd)
                if len(cmd_tokens) > 1:
                    #we still have more tokens to be processed
                    #The tokens could be param to main cmd or
                    #it could be an subcmd.
                    next_token = cmd_tokens[1]
                    # Next token is an option if any of following are true-
                    # starts with '--' chars
                    # starts with '-' char
                    # contains '=' operator
                    # or token next to 'Next token' is '='
                    if next_token.startswith('--') or\
                            next_token.startswith('-') or\
                            next_token.find('=') > 0 or\
                            (len(cmd_tokens) >= 3 and\
                            cmd_tokens[2] == '='):
                        parsed_cmd = self.build_options(parsed_cmd, cmd_tokens, 'CMD')
                        return parsed_cmd
                    else:
                        #the token could be an sub-command
                        #check same
                        if self.sub_cmd_exists(main_cmd, next_token):
                            sub_cmds = {}
                            parsed_cmd[SUB_CMD] = sub_cmds
                            parsed_sub_cmd = {}
                            sub_cmds[next_token.upper()]\
                                    = parsed_sub_cmd
                            parsed_sub_cmd[REQUIRED] = self\
                                    .get_sub_cmd_required_fields(\
                                    main_cmd, next_token)
                            parsed_sub_cmd[PROCESSOR_CALLBACK] = \
                                    self.get_sub_cmd_processor_callback(main_cmd,\
                                    next_token)
                            parsed_sub_cmd[TOKEN_CALLBACK] = \
                                    self.get_sub_cmd_prompt_token_callback(main_cmd,\
                                    next_token)
                        parsed_cmd = self.build_options(parsed_cmd,\
                                cmd_tokens, 'SUB_CMD')
                        return parsed_cmd
                else:
                    return parsed_cmd
        #Command is not registered, will return None
        return None

    def build_options(self, parsed_cmd, tokens, cmd_type):
        """docstring for build_options"""
        options = {}
        kw_options = {}
        opt_tokens = []
        cmd_name = None
        sub_cmd_name = None
        if cmd_type == 'CMD':
            cmd_name = tokens[0].upper()
            opt_tokens = tokens[1:]
        else:
            cmd_name = tokens[0].upper()
            sub_cmd_name = tokens[1].upper()
            opt_tokens = tokens[2:]
        if len(opt_tokens) > 0:
            skip = 0
            for i in range(len(opt_tokens)):
                if skip > 0:
                    skip -= 1
                    continue
                next_token = opt_tokens[i].upper()
                if next_token.startswith('-'):
                    if cmd_type == 'CMD':
                        if self.cmd_has_option(cmd_name,\
                                next_token):
                            options[next_token] = True
                    else:
                        if self.sub_cmd_has_option(\
                                cmd_name, sub_cmd_name,\
                                next_token):
                            options[next_token] = True
                elif next_token.startswith('--'):
                    if cmd_type == 'CMD':
                        if self.cmd_has_option(cmd_name,\
                                next_token):
                            options[next_token] = True
                    else:
                        if self.sub_cmd_has_option(\
                                cmd_name, sub_cmd_name,\
                                next_token):
                            options[next_token] = True
                elif next_token.find('=') >= 0:
                    kv_token = next_token.split('=')
                    if cmd_type == 'CMD':
                        if self.cmd_has_kw_option(\
                                cmd_name, kv_token[0]):
                            #SCENARIO: kw= val i.e, space
                            #btwn equal(=) sign and 'val'
                            #kv_token[1] will be empty
                            if kv_token[1] == '':
                                #so next token should be
                                #taken from opt_tokens and
                                #skip one loop
                                kw_options[kv_token[0]] = \
                                        opt_tokens[i+1].upper()\
                                        if (i+1) < len(opt_tokens)\
                                        else None
                                skip = 1
                            else:
                                kw_options[kv_token[0]] = kv_token[1]
                    else:
                        if self.sub_cmd_has_kw_option(\
                                cmd_name, sub_cmd_name, kv_token[0]):
                            if kv_token[1] == '':
                                kw_options[kv_token[0]] = \
                                        opt_tokens[i+1].upper()\
                                        if (i+1) < len(opt_tokens)\
                                        else None
                                skip = 1
                            else:
                                kw_options[kv_token[0]] = kv_token[1]
                elif (i+1) < len(opt_tokens) and opt_tokens[i+1] == '=':
                    opt_key = next_token
                    if cmd_type == 'CMD':
                        if self.cmd_has_kw_option(cmd_name, opt_key):
                            kw_options[opt_key] = None
                            if (i+2) < len(opt_tokens) and opt_tokens[i+2] is not None:
                                opt_val = opt_tokens[i+2].upper() #i+1 is an = sign
                                kw_options[opt_key] = opt_val
                                skip = 2 #skip equal to sign and opt_val
                    else:
                        if self.sub_cmd_has_kw_option(cmd_name, sub_cmd_name, opt_key):
                            kw_options[opt_key] = None
                            if (i+2) < len(opt_tokens) and opt_tokens[i+2] is not None:
                                opt_val = opt_tokens[i+2].upper() #i+1 is an = sign
                                kw_options[opt_key] = opt_val
                                skip = 2 #skip equal to sign and opt_val
                #SCENARIO: kw =val i.e., space btwn kw and '=' sign
                elif (i+1) < len(opt_tokens) and opt_tokens[i+1].find('=') >= 0:
                    opt_key = next_token
                    if cmd_type == 'CMD':
                        if self.cmd_has_kw_option(cmd_name, opt_key):
                            opt_val = opt_tokens[i+1].split('=')
                            kw_options[opt_key] = opt_val[1].upper()
                            skip = 1
                    else:
                        if self.sub_cmd_has_kw_option(cmd_name, sub_cmd_name, opt_key):
                            opt_val = opt_tokens[i+1].split('=')
                            kw_options[opt_key] = opt_val[1].upper()
            if cmd_type == 'CMD':
                parsed_cmd[OPTIONS] = options
                parsed_cmd[KW_OPTIONS] = kw_options
            else:
                parsed_cmd[SUB_CMD][sub_cmd_name][OPTIONS] = options
                parsed_cmd[SUB_CMD][sub_cmd_name][KW_OPTIONS] = kw_options
            return parsed_cmd


