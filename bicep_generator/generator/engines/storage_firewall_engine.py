from .firewall_engine import FirewallEngine


class StorageFirewallEngine(FirewallEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'firewall rules for Azure Storage Account'


        self.module_params = [
            ('name', 'storageAccountName'),
            ('location', 'location')
        ]

        self.module_symbolic_name = 'storageFirewallDeployment'
        self.module_bicep_file = 'storageaccount.firewall.bicep'
        self.module_deployment_name = 'storage-firewall-deployment'


    def set_module_param_outbound_ip(self, outbound_ip):
        self.module_params.append(('allowIps', outbound_ip))
    

