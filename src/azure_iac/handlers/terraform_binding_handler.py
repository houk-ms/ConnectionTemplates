from azure_iac.payloads.binding import Binding
from azure_iac.payloads.models.connection_type import ConnectionType

from azure_iac.terraform_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.role_resource_engine import RoleResourceEngine


class TerraformBindingHandler():
    def __init__(self, 
                 binding: Binding, 
                 source_engine: SourceResourceEngine,
                 target_engine: TargetResourceEngine,
                 role_engine: RoleResourceEngine,
                 firewall_engine: FirewallResourceEngine):
        self.binding = binding
        self.source_engine = source_engine
        self.target_engine = target_engine
        self.role_engine = role_engine
        self.firewall_engine = firewall_engine


    def process_engines(self):

        if self.binding.connection == ConnectionType.SYSTEMIDENTITY:
            # source engine depends on target engine (--> app settings)
            self.source_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_identity(self.binding)
            self.source_engine.add_app_settings(app_settings)
            
            # firewall engine depends on source engine (--> outbound ips)
            # target may not support separated firewall settings
            if self.firewall_engine is not None:
                self.firewall_engine.add_dependency_engine(self.source_engine)
                public_ip = self.source_engine.get_outbound_ip()
                self.firewall_engine.allow_firewall(public_ip)
            
            # role engine depends on source and target engine (--> principal id, scope)
            self.role_engine.add_dependency_engine(self.source_engine)
            self.role_engine.add_dependency_engine(self.target_engine)
            principal_id = self.source_engine.get_identity_id()
            scope, role_def = self.target_engine.get_role_scope()
            self.role_engine.assign_role(principal_id, scope, role_def)

        elif self.binding.connection == ConnectionType.HTTP:
            # source engine depends on target engine (--> app settings)
            self.source_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_http(self.binding)
            self.source_engine.add_app_settings(app_settings)

        elif self.binding.connection == ConnectionType.SECRET:
            # source engine depends on target engine (--> app settings)
            self.source_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_secret(self.binding)
            self.source_engine.add_app_settings(app_settings)
            
            # firewall engine depends on source engine (--> outbound ips)
            # target may not support separated firewall settings
            if self.firewall_engine is not None:
                self.firewall_engine.add_dependency_engine(self.source_engine)
                public_ip = self.source_engine.get_outbound_ip()
                self.firewall_engine.allow_firewall(public_ip)
            
        else:
            raise ValueError('Invalid connection type: {}'.format(self.binding.connection_type))
    