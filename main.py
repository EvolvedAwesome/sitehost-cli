from sys import argv

# Imports from sitehost_cli
from sitehost_cli.rich_console import console
from sitehost_cli import CLI_Module, Generic_CLI_Argument, CLI_Command, CLI_Completer, CLI_Suggester
from sitehost_cli.exceptions import *

# Prompt toolkit imports
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory

# Typing
from typing import List

# Local module imports
from modules import *
from modules import __all__ as module_classes

class SiteHost_CLI(CLI_Module):
    def __init__(self, api_version: str = "1.2", console_tool: bool = True, input_command_array: List[str] = None):

        super(SiteHost_CLI, self).__init__(api_version, console)
        
        self.command_array = self._populate_command_array(additional_commands = [
            CLI_Command(self, "get_api_info", "/api/get_info", "Get information about the API access of this key", []),
            CLI_Command(self, "get_job_info", "/job/get", "Get information about a job_id returned by the API", ['job_id', Generic_CLI_Argument(self, 'job-type', 'type', ['daemon', 'scheduler'])]),
        ])

        # Load the appropriate CLI_Modules.
        # These can be added to /{base}/modules and loaded int
        # /{base}/modules/init.py 
        self.modules = [self] + [globals()[mod](api_version, console) for mod in module_classes]

        # Set the CLIModule class attributes for this instance
        self.title = "[sitehost]Main Module"
        self.module_method_list = {}

        # Collate all methods we have avaliable to us
        for module in self.modules:
            self.module_method_list.update(module.command_array)

        # If we are running as a console tool
        if console_tool:
            self.console.rule("[sitehost]SiteHost CLI", style="sitehost_grey")
            self.console.print("[sitehost]SiteHost API [sitehost_grey]Command Line Interface")

            with self.console.status("Authenticating and connecting"):
                # Make an API test to test our key
                r = self._get_request('/api/get_info')
                
                # Show that to the user
                if r.status_code != 200:
                    raise API_Exception(f"The API url ({self.api_url}) returned a status code of {r.status_code}")
                if "Unauthorised" in r.json()['msg']:
                    raise API_Exception(f"The supplied API key is not valid.")

                self.console.print("")
                self.console.print("[sitehost_white]API Key Access:")
                self.console.print_json(data=(r.json()['return']))
                self.console.print("")

            self.prompt_session = PromptSession('shcli> : ', 
                history=FileHistory('/tmp/history.txt'), 
                auto_suggest=CLI_Suggester(self.module_method_list),
                completer=CLI_Completer(self.module_method_list))

            self.prompt_loop()

        # Else we directly pass the arguments (after shcli) 
        # and don't start a console session
        else:
            self._handle_input(input_command_array)

    def _handle_input(self, input_command: List[str]):
        """Handle the input provided via either the console tool or directly.
        """
        if len(input_command) == 0:
            return 

        # Our general format is `command arg1 arg2 arg3 arg4`
        # This could change if we switch to `command subcommand arg1 arg2 arg3`
        # But our functions shouldn't need to deal with this.
        command_name = input_command[0]
        args = input_command[1:]

        if command_name in self.module_method_list:
            data = self.module_method_list[command_name] 
            method_py = data['command_py']

            try:
                method_py(args)
            except NotEnoughArgumentsException:
                return
        else:
            console.print(f"No command named {command_name}")

    def prompt_loop(self):
        """Runs the prompter and terminal sessions in a continious loop and
        hands the results to SiteHost_CLI._handle_input.
        """
        while True:
            try:
                input_command = self.prompt_session.prompt() 
                self._handle_input(input_command.split())
            except KeyboardInterrupt as e:
                continue
            
    def _command_help(self, args):
        """Provides an overview of all configured commands 

        Usage: help [function_name]
        """
        if len(args) > 0:
            if args[0] in self.module_method_list:
                try:
                    method = self.module_method_list[args[0]]['command_py'] 
                    console.print('\n'.join([line.strip() for line in method.__doc__.split("\n")]))
                    return
                except AttributeError as e:
                    console.print(f"No command named {args[0]}")

        console.print("[sitehost]SiteHost CLI [sitehost_grey]Help Menu")
        console.print("[sitehost_grey]shcli command \[args]")
        console.print("")

        def process_method(method_py):
            docs_first_line = method_py.__doc__.split("\n")[0].strip()
            docs_usage = ''.join([line for line in method_py.__doc__.split("\n") if "Usage:" in line]).replace("[","\[").strip()
            if docs_usage != "":
                console.print(f"{method_py.__name__.replace('_command_', '')} - \t{docs_first_line}\n\t[italic]{docs_usage}\n")
            else:
                console.print(f"{method_py.__name__.replace('_command_', '')} - \t{docs_first_line}\n")

        for module in self.modules:
            console.rule(module.title, style="sitehost_grey")
            console.print("")

            for _, data in module.command_array.items():
                process_method(data['command_py'])

    def _command_exit(self, args):
        """Exit the CLI tool.
        
        Usage: exit
        """
        console.print("[sitehost_grey]Goodbye!")
        exit()

    def _command_cid(self, args):
        """Set the acting client_id for your commands as a shortcut.
        
        Usage: cid client_id
        """
        if len(args) > 0:
            self.client_id = args[0]
            console.print(f"Updated client_id to {self.client_id}")
        else:
            self.client_id = None
            console.print("Reset client_id to None")

if __name__ == "__main__":

    arguments = argv[1:]

    if len(arguments) == 0:
        sh_cli = SiteHost_CLI()
    else:
        sh_cli = SiteHost_CLI(console_tool=False, input_command_array=arguments)
