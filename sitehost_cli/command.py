from dataclasses import dataclass
from typing import Callable 

from sitehost_cli.module import CLI_Module
from sitehost_cli.arguments import CLI_Argument
from sitehost_cli.exceptions import *

@dataclass
class CLI_Command:
    module: CLI_Module
    name: str
    endpoint: str
    description: str
    args_required: list
    args_optional: list = None
    render_callback: Callable = None 
    additional_parameters: dict = None # {'parameter': [value]}
    args_callback: Callable = None
    pre_callback: Callable = None
    post_callback: Callable = None

    # This will be run after initalisation
    def __post_init__(self):
        for index, arg in enumerate(self.args_required):
            if isinstance(arg, str):
                self.args_required[index] = CLI_Argument(self.module, arg, arg)
        
        self.args_required = [arg[0] if isinstance(arg, tuple) else arg for arg in self.args_required]

    @property
    def __doc__(self):
        """Autogenerate documentation strings for our command line
        argument classes using the argument classes and 'description' instance variable.
        """
        args_r = [arg[0] if isinstance(arg, tuple) else arg for arg in self.args_required]
        return f"""{self.description}

Usage: {' '.join([self.name] + [str(arg) for arg in args_r] if args_r is not None else [])}
    """

    @property
    def __name__(self):
        """Override the default name with our specified cli command
        name.
        """
        return self.name

    # The call method for this cli command
    def __call__(self, args):
        """This class is callable to plug into our pre-existing pluggable
        function infrastructure.
        """
        # Check whether there are the minimum number of arguments
        if len(args) < len(self.args_required):
            self.module.console.print(self.__doc__.replace("[","\[").strip())
            raise NotEnoughArgumentsException("Not enough arguments provided.")

        completed_args = {arg.api_name: args[index] for index, arg in enumerate(self.args_required)}

        # Args callback lets us make changes to the arguments in
        # unique ways based on the inputs.
        if self.args_callback is not None:
            completed_args = self.args_callback(completed_args)
        
        # Substitute additional parameters
        if self.additional_parameters is not None:
            for param in self.additional_parameters.items():
                completed_args[param[0]] = param[1]

        # Pre callback lets us do operations before running
        # the API query (e.g. edit database, change local vars,
        # run another query etc).
        # Theres no defined way to interact with the calling command
        # class.
        if self.pre_callback is not None:
            self.pre_callback()

        response = self.module._post_request(self.endpoint, completed_args) 

        # 500 error code means something went wrong
        if response.status_code == 500:
           raise Exception("Unknown error")

        r_json = response.json()

        # If there isn't a render callback defined, then we render
        # it in the default way as defined by our parent module.
        if self.render_callback is None:
            self.render_callback = self.module._default_render_callback

        # Provide some feedback on the API request.
        if response.status_code != 200 or r_json['status'] is False:
            self.module.console.print(f"[red italic]{r_json['msg']}")
        else:
            self.module.console.print(f"[green]API request successful!") 
            if "return" in r_json:
                self.render_callback(r_json['return'])
            elif "msg" in r_json:
                self.render_callback(r_json['msg'])
            else:
                self.render_callback(r_json) # Fallback
        
        # Do any post or cleanup tasks.
        if self.post_callback is not None:
            self.post_callback()

        # Add a newline
        self.module.console.print("")