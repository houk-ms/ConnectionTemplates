from .firewall_engine import FirewallEngine


class KeyvaultFirewallEngine(FirewallEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'firewall rules for Azure Keyvault'


        self.module_params = [
            ('name', 'keyVaultName'),
            ('location', 'location')
        ]

        self.module_symbolic_name = 'keyvaultFirewallDeployment'
        self.module_bicep_file = 'keyvault.firewall.bicep'
        self.module_deployment_name = 'keyvault-firewall-deployment'


    def set_module_param_outbound_ip(self, outbound_ip):
        self.module_params.append(('allowIps', outbound_ip))
    

