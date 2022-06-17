# Typing Imports
from typing import OrderedDict

# We use Requests as a backend for accessing the SiteHost API.
# TODO: Use httpx or an async requests framework 
import requests

# Used for parsing config
import yaml
from pathlib import Path

# Dicts are ordered from Python 3.6, 
# but we include this to maintain compatability. 
# See: https://mail.python.org/pipermail/python-dev/2016-September/146327.html
from collections import OrderedDict

class CLI_Module:
    """Parent class for a sitehost CLI module. This should be inherited and
    customised to suit the parent class.
    
    Supports definition of CLI functions and class definition.
    """
    _sitehost_console_yaml = None
    api_url = None

    def __init__(self, api_version: str, console):
        self.console = console
        self.title = "Generic SiteHost API Module"
        self._commands = {}
        self._client_id = None
        if not self._sitehost_console_yaml:
            self.load_shconsole_yaml()
        self.api_url = self._sitehost_console_yaml['environments']['production']['url']  + f"/{api_version}"

    @property
    def client_id(self) -> int:
        if not self._client_id:
            self._client_id = str(self._sitehost_console_yaml['environments']['production']['client'])
        return self._client_id
    
    @client_id.setter
    def client_id(self, cid: str):
        self._client_id = str(cid)
        for module in self.modules:
            module._client_id = str(cid)
    
    @property 
    def _api_key(self) -> str:
        return str(self._sitehost_console_yaml['environments']['production']['api-key'])

    def _populate_command_array(self, additional_commands: list = None):
        command_array = {}

        # Additional implicit commands
        if additional_commands is not None:
            for command in additional_commands:
                command_array[command.__name__] = {'call_name': command.__name__, 'command_py': command, 'module': self}

        # Explicit python function commands
        for command_name in [f for f in dir(self) if f.startswith("_command_")]:
            command_py = getattr(self, command_name)
            command_array[command_name.replace("_command_","")] = {'call_name': command_name, 'command_py': command_py, 'module': self}
        
        return command_array

    def load_shconsole_yaml(self) -> None:
        """Get the console configuration in yaml format from Albies console tool.
        This means you can drop shcli into your currently configuration.
        """
        with open(str(Path.home()) + "/.sth-console/config.yml") as fp:
            self._sitehost_console_yaml = yaml.load(fp, Loader=yaml.FullLoader)

    def _build_endpoint_url(self, endpoint: str):
        if endpoint.startswith('/'):
            return f"{self.api_url}{endpoint}.json?apikey={self._api_key}"
        else:
            return f"{self.api_url}/{endpoint}.json?apikey={self._api_key}"
    
    def _get_request(self, endpoint: str = "/api/get_info"):
        return requests.get(self._build_endpoint_url(endpoint))

    def _post_request(self, endpoint: str = "/api/get_info", post_data = None, post_dict=True):
        body = OrderedDict()

        if post_data is not None:
            for content in post_data.items():
                body[content[0]] = content[1]

        return requests.post(self._build_endpoint_url(endpoint), data=body)

    # The default method for printing returned information from an API request. 
    def _default_render_callback(self, r):
        self.console.print_json(data=r)
