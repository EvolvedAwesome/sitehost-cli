from sitehost_cli import CLI_Module, CLI_Argument, Generic_CLI_Argument, Smart_CLI_Argument, Client_ID_Arugment, CLI_Command
from sitehost_cli.exceptions import *

class Server_Module(CLI_Module):
    def __init__(self, api_version, console):
        super(Server_Module, self).__init__(api_version, console)
        self.title = "[purple bold]SiteHost Server Module"

        self.client_id_argument = Client_ID_Arugment(self, 'client_id', 'client_id'), 
        self.server_location = Smart_CLI_Argument(self, 'location', 'location', '/server/list_locations', '[*].code'),#, label_path='[*].label', dynamic_completion=True),
        self.server_resources = Generic_CLI_Argument(self, 'resource_type', 'product_code', ['XENLIT', 'XENPRO', 'XENEXT', 'XENULT', 'XEN24G', 'WIN1GB', 'WIN2GB', 'WIN4G', 'WIN8GB', 'WIN16G', 'WINHA'], 'XENLIT'),
        self.server_type = Smart_CLI_Argument(self, 'server_type', 'image', '/server/list_images', '[*].code'),
        self.ssh_key = Smart_CLI_Argument(self, 'ssh_key', 'params[ssh_keys][0]', '/ssh/key/list_all', 'data[*].id', label_path='data[*].label', dynamic_completion=True)
        self.server_name = Smart_CLI_Argument(self, 'server_name', 'name', '/server/list_servers', 'data[*].name', label_path='data[*].label', dynamic_completion=True)

        self.command_array = self._populate_command_array(additional_commands = [
            CLI_Command(self, "provision_server", 
                                "/server/provision", 
                                "Provision a server with the provided characteristics", 
                                [
                                    self.client_id_argument, 
                                    'label', 
                                    self.server_location,
                                    self.server_resources, 
                                    self.server_type, 
                                    CLI_Argument(self, 'name', 'params[name]'), 
                                    self.ssh_key 
                                ], 
                                additional_parameters={'params[ipv4]':'auto', 'params[ipv6]':'auto', 'params[send_email]':0}),
            CLI_Command(self, "delete_server", 
                                "/server/delete", 
                                "Remove the specified server", 
                                [
                                    self.client_id_argument, 
                                    self.server_name
                                ]),
            CLI_Command(self, "reboot_server", 
                                "/server/change_state", 
                                "Reboot a server by changing the state to reboot", 
                                [
                                    self.client_id_argument, 
                                    self.server_name
                                ], 
                                args_callback=self._server_state_edit_callback_template("reboot")),
            CLI_Command(self, "stop_server", 
                                "/server/change_state", 
                                "Power off a server by changing the state to power_off", 
                                [
                                    self.client_id_argument, 
                                    self.server_name
                                ], 
                                args_callback=self._server_state_edit_callback_template("power_off")),
            CLI_Command(self, "start_server", 
                                "/server/change_state", 
                                "Start a server by changing the state to power_on", 
                                [
                                    self.client_id_argument, 
                                    self.server_name
                                ], 
                                args_callback=self._server_state_edit_callback_template("power_on")),
            CLI_Command(self, "start_rescue_mode", 
                                "/server/change_state", 
                                "Start a server into rescue mode", 
                                [
                                    self.client_id_argument, 
                                    self.server_name
                                ], 
                                args_callback=self._server_state_edit_callback_template("rescue_on")),
            CLI_Command(self, "stop_rescue_mode", 
                                "/server/change_state", 
                                "Stop rescue mode on a server", 
                                [
                                    self.client_id_argument, 
                                    self.server_name
                                ], 
                                args_callback=self._server_state_edit_callback_template("rescue_off")),
            CLI_Command(self, "list_images", 
                                "/server/list_images", 
                                "Show the avaliable server images", 
                                []),
            CLI_Command(self, "list_servers", 
                                "/server/list_servers", 
                                "Show the servers associated with a client account", 
                                [
                                    self.client_id_argument 
                                ])
            ])

    def _server_state_edit_callback_template(self, state: str):
        def _server_state_edit(args_dict: dict):
            args_dict["state"] = [state]
            return args_dict
        
        return _server_state_edit

    def _command_upgrade_disk(self, args: list):
        """Upgrades the disk for a server.
        
        Usage: upgrade_disk client_id name disk added_GB
        """
        return


    def _command_lv_resize(self, args: list):
        """Conducts a live resize on the specified server.
        
        Usage: lv_resize client_id name disk_name added_disk_GB
        """
        return