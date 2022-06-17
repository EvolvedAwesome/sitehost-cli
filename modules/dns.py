from rich.columns import Columns

from sitehost_cli import CLI_Module, Generic_CLI_Argument, Smart_CLI_Argument, Client_ID_Arugment, CLI_Command
from sitehost_cli.exceptions import *

class DNS_Module(CLI_Module):
    def __init__(self, api_version, console):
        super(DNS_Module, self).__init__(api_version, console)
        self.title = "[green bold]SiteHost DNS Module"
        
        self.client_id_argument = Client_ID_Arugment(self, 'client_id', 'client_id'), 
        self.zone = Smart_CLI_Argument(self, 'zone', 'domain', '/dns/list_domains', '[*]..name')
        self.ip_address = Smart_CLI_Argument(self, 'ip_address', 'ip_addr', '/dns/list_ips', '$..ip_addr', dynamic_completion=True)
        self.record_type = Generic_CLI_Argument(self, 'record_type', 'type', ['A', 'AAAA', 'CNAME', 'SRV', 'MX', 'TXT', 'CAA']) 
        self.record_id = Smart_CLI_Argument(self, 'record_name', 'name', '/dns/list_records', '$..id', label_path='$..name', dynamic_completion=True, context_attributes=[('domain', False)])

        self.command_array = self._populate_command_array(additional_commands = [
            CLI_Command(self, "add_record", "/dns/add_record", "Add a DNS record to the specified zone", [self.client_id_argument, self.zone, self.record_type, 'name', 'content']),
            CLI_Command(self, "delete_record", "/dns/delete_record", "Delete the a DNS record from the specified zone", [self.client_id_argument, self.zone, self.record_id]),
            CLI_Command(self, "list_records", "/dns/list_records", "List all the DNS records in the specified zone", [self.client_id_argument, self.zone], render_callback=self._pretty_print_dns_records),
            CLI_Command(self, "list_zones", "/dns/list_domains", "List all the DNS zones in the specified account", [self.client_id_argument], render_callback=self._pretty_print_zones),
            CLI_Command(self, "list_ips", "/dns/list_ips", "List all the IP addresses in the specified account", [self.client_id_argument]),
            CLI_Command(self, "create_zone", "/dns/create_domain", "Create a DNS Zone with the specified name/domain", [self.client_id_argument, self.zone]),
            CLI_Command(self, "delete_zone", "/dns/delete_domain", "Delete the DNS Zone with the specified name/domain", [self.client_id_argument, self.zone]),
            CLI_Command(self, "reset_ptr", "/dns/reset_reverse_dns", "Reset the pointer record for an IP address to it's default", [self.client_id_argument, self.ip_address]),
            CLI_Command(self, "update_ptr", "/dns/update_reverse_dns", "Update the pointer record for an IP address to it's default", [self.client_id_argument, self.ip_address, 'rdns']),
            CLI_Command(self, "update_record", "/dns/update_record", "Updates the DNS record in the specified zone", [self.client_id_argument, self.zone, self.record_id, self.record_type, 'name', 'content']),
            CLI_Command(self, "update_soa", "/dns/update_soa", "Updates the SOA record for the specified zone", [self.client_id_argument, self.zone, 'ns', 'email', 'refresh', 'retry', 'expire', 'minimum']),
        ])

    def _pretty_print_dns_records(self, records):

        if records is not None:
            renderables = [f"[{r['id']} {r['change_date']} ({r['state']})]: {r['name']} {r['ttl']} {r['type']} {r['content']}" for r in records]
            self.console.print(Columns(renderables))

    def _pretty_print_zones(self, zones):

        if zones is not None:
            renderables = [f"{zone['name']} ({zone['template_id']})" for zone in zones['data']]
            self.console.print(Columns(renderables))