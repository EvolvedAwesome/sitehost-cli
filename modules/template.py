"""Sitehost Module Template.
Copy this file to create an additional sitehost module.
"""

from sitehost_cli import CLI_Module, Generic_CLI_Argument, Smart_CLI_Argument, Client_ID_Arugment, CLI_Command
from sitehost_cli.exceptions import *

class Template_Module(CLI_Module):
    def __init__(self, api_version: str, console):
        super().__init__(api_version, console)

        # Set a title and style for your module
        self.title = "[white bold]SiteHost Template Module"

        # Add additional CLI_Command objects here with additional_commands = []
        self.command_array = self._populate_command_array(additional_commands=[])