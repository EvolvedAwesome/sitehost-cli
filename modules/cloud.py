from multiprocessing import context
from sitehost_cli import CLI_Module, Generic_CLI_Argument, Smart_CLI_Argument, Client_ID_Arugment, CLI_Command
from sitehost_cli.arguments import CLI_Argument
from sitehost_cli.exceptions import *

class Cloud_Module(CLI_Module):
    def __init__(self, api_version: str, console):
        super().__init__(api_version, console)

        # Set a title and style for your module
        self.title = "[blue bold]SiteHost Cloud Module"

        # Define argument types.
        self.client_id_argument = Client_ID_Arugment(self, 'client_id', 'client_id'), 
        self.cc_server_name = Smart_CLI_Argument(self, 'server_name', 'server_name', '/cloud/server/list_all', '[*].name', label_path='[*].label', dynamic_completion=True)
        self.custom_image_code = Smart_CLI_Argument(self, 'image_name', 'code', '/cloud/image/list_all', '$..code', label_path='$..label', dynamic_completion=True)
        self.custom_image_id = Smart_CLI_Argument(self, 'image_id', 'image_id', '/cloud/image/list_all', '$..id', label_path='$..label', dynamic_completion=True)
        self.ssh_key = Smart_CLI_Argument(self, 'ssh_key', 'params[ssh_keys][0]', '/ssh/key/list_all', 'data[*].id', label_path='data[*].label', dynamic_completion=True)
        self.ssh_user = Smart_CLI_Argument(self, 'username', 'username', '/cloud/ssh/user/list_all', 'data[*].username', context_attributes=[('server_name', True)], dynamic_completion=True)
        self.database = Smart_CLI_Argument(self, 'database', 'database', '/cloud/db/list_all', 'data[*].db_name', context_attributes=[('server_name', True)], dynamic_completion=True)
        #self.container = Smart_CLI_Argument(self, 'container', 'container', '/cloud/stack/list_all', 'data[*].name', label_path='data[*].label', context_attributes=[('server_name', True)], dynamic_completion=True),
        self.mysql_host = Generic_CLI_Argument(self, 'mysql_container', 'mysql_host', ['mysql56', 'mysql57', 'mysql8']),
        self.mysql_user = Smart_CLI_Argument(self, 'mysql_user', 'username', '/cloud/db/user/list_all', 'data[*].username', context_attributes=[('server_name', True)], dynamic_completion=True),
        self.stack = Smart_CLI_Argument(self, 'container', 'container', '/cloud/stack/list_all', 'data[*].name', label_path='data[*].label', context_attributes=[('server_name', True)], dynamic_completion=True),
        
        # Add additional CLI_Command objects here with additional_commands = []
        self.command_array = self._populate_command_array(additional_commands=[
            CLI_Command(self, 'list_ccs', '/cloud/server/list_all', 'Lists all the Cloud Containers in a client account.', [self.client_id_argument]),
            CLI_Command(self, 'set_min_tls', '/cloud/server/update_minimum_tls_version', 'Sets a Cloud Container servers minimum TLS version.', [
                self.client_id_argument, 
                self.cc_server_name, 
                Generic_CLI_Argument(self, 'min_version', 'minimum_tls_version', ['TLSv1.1', 'TLSv1.2', 'TLSv1.3'])]),
            
            CLI_Command(self, 'list_images', '/cloud/stack/image/list_all', 'Lists all the SiteHost images.', []),
            CLI_Command(self, 'list_custom_images', '/cloud/image/list_all', 'Lists all the custom images in a client account.', [self.client_id_argument]),
            CLI_Command(self, 'get_custom_image', '/cloud/image/get', 'Gets a specified custom image.', [self.client_id_argument, self.custom_image_code]),
            CLI_Command(self, 'delete_custom_image', '/cloud/image/delete', 'Deletes a specified custom image.', [self.client_id_argument, self.custom_image_code]),
            CLI_Command(self, 'create_custom_image', '/cloud/image/create', 'Creates a specified custom image.', [
                self.client_id_argument,
                CLI_Argument(self, 'name', 'label')], 
                args_optional=[
                    CLI_Argument(self, 'code-name', 'params[code]'), 
                    self.ssh_key, 
                    CLI_Argument(self, 'fork-from', 'params[fork-id]')
                ]),
            CLI_Command(self, 'get_custom_image_builds', '/cloud/image/version/list_all', 'Gets the build history for a specified custom image.', [self.client_id_argument, self.custom_image_id]), 
            
            CLI_Command(self, 'list_ssh_users', '/cloud/ssh/user/list_all', 'Returns a list of SSH users.', [self.client_id_argument]),
            CLI_Command(self, 'list_server_ssh_users', '/cloud/ssh/user/list_all', 'Returns a list of SSH users.', [self.client_id_argument, self.cc_server_name.get_filter_copy()]),
            CLI_Command(self, 'get_ssh_user', '/cloud/ssh/user/get', 'Get the details of a specified SSH user.', [self.client_id_argument, self.cc_server_name, self.ssh_user]),
            CLI_Command(self, 'delete_ssh_user', '/cloud/ssh/user/delete', 'Delete the specified SSH user.', [self.client_id_argument, self.cc_server_name, self.ssh_user]),
            CLI_Command(self, 'create_ssh_user', '/cloud/ssh/user/add', 'Create an SSH user.', [
                self.client_id_argument, 
                self.cc_server_name, 
                CLI_Argument(self, 'username', 'username'), 
                CLI_Argument(self, 'password', 'password'), 
                self.stack[0].get_single_list_copy(), 
                Smart_CLI_Argument(self, 'ssh_key', 'ssh_keys[0]', '/ssh/key/list_all', 'data[*].id', label_path='data[*].label', dynamic_completion=True)]),
            CLI_Command(self, 'update_ssh_user_password', '/cloud/ssh/user/update', 'Update the password of the specified SSH user.', [
                self.client_id_argument, 
                self.cc_server_name, 
                self.ssh_user, 
                CLI_Argument(self, 'password', 'params[password]')]),

            CLI_Command(self, 'list_databases', '/cloud/db/list_all', 'Lists all databases under a specified client account.', [self.client_id_argument]),
            CLI_Command(self, 'list_server_databases', '/cloud/db/list_all', 'Lists all databases on a specified server.', [self.client_id_argument, self.cc_server_name.get_filter_copy()]),
            CLI_Command(self, 'create_database', '/cloud/db/add', 'Create a database on the specified server linked to the specified container.', [
                self.client_id_argument, 
                self.cc_server_name, 
                self.mysql_host,
                CLI_Argument(self, 'database_name', 'database'), 
                self.stack]),
            CLI_Command(self, 'delete_database', '/cloud/db/delete', 'Delete the specified database.', [
                self.client_id_argument, 
                self.cc_server_name, 
                self.mysql_host,
                self.database]),
            CLI_Command(self, 'update_database_container', '/cloud/db/update', 'Links a specified database to a specified container.', [
                self.client_id_argument, 
                self.cc_server_name, 
                self.mysql_host,
                self.database, 
                self.stack[0].get_params_copy()]),

            CLI_Command(self, 'list_database_users', '/cloud/db/user/list_all', 'Lists all database users under a specified client account.', [self.client_id_argument]),
            CLI_Command(self, 'list_server_database_users', '/cloud/db/user/list_all', 'Lists all database users on a specified server.', [self.client_id_argument, self.cc_server_name.get_filter_copy()]),
            CLI_Command(self, 'create_database_user', '/cloud/db/user/add', 'Creates a database user.', [
                self.client_id_argument, 
                self.cc_server_name, 
                self.mysql_host,
                CLI_Argument(self, 'mysql_user', 'username'), 
                CLI_Argument(self, 'password', 'password'), 
                self.database]),
            CLI_Command(self, 'delete_database_user', '/cloud/db/user/delete', 'Deletes a database user.', [
                self.client_id_argument, 
                self.cc_server_name, 
                self.mysql_host,
                self.mysql_user]),
            CLI_Command(self, 'get_database_user', '/cloud/db/user/get', 'Gets the details of a database user.', [
                self.client_id_argument, 
                self.cc_server_name, 
                self.mysql_host,
                self.mysql_user]),

            CLI_Command(self, 'list_stacks', '/cloud/stack/list_all', 'Gets a list of all the stacks.', [
                self.client_id_argument]),
            CLI_Command(self, 'list_server_stacks', '/cloud/stack/list_all', 'Gets a list of all the stacks for a specified server.', [
                self.client_id_argument,
                self.cc_server_name.get_filter_copy()]),
            # Why on earth is the stack server attribute "server" while everywhere else it's "server_name"?
            #CLI_Command(self, 'get_stack', '/cloud/stack/get', 'Gets the information about a specified stack.', [
            #    self.client_id_argument,
            #    self.cc_server_name.get_api_name_copy('server'),
            #    self.stack]),
            
        ])