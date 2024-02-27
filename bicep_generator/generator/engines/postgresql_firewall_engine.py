from .firewall_engine import FirewallEngine


class PostgresqlFirewallEngine(FirewallEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'firewall rules for Azure Database for PostgreSQL'


        self.module_params = [
            ('postgresqlName', 'serverName'),
        ]

        self.module_symbolic_name = 'postgresqlFirewallDeployment'
        self.module_bicep_file = 'postgresql.firewall.bicep'
        self.module_deployment_name = 'postgresql-firewall-deployment'


    def set_module_param_outbound_ip(self, outbound_ip):
        self.module_params.append(('allowIps', outbound_ip))
    

