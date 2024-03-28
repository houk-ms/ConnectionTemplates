from payloads.binding import Binding
from payloads.models.connection_type import ConnectionType
from terraform_engines.modules.source_resource_engine import SourceResourceEngine
from terraform_engines.modules.target_resource_engine import TargetResourceEngine
from terraform_engines.modules.store_resource_engine import StoreResourceEngine
from terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine
from terraform_engines.modules.role_resource_engine import RoleResourceEngine

class TerraformBindingHandler():
    def __init__(self, 
                 binding: Binding, 
                 source_engine: SourceResourceEngine,
                 target_engine: TargetResourceEngine,
                 store_engine: StoreResourceEngine,
                 role_engine: RoleResourceEngine,
                 firewall_engine: FirewallResourceEngine):
        self.binding = binding
        self.source_engine = source_engine
        self.target_engine = target_engine
        self.store_engine = store_engine
        self.role_engine = role_engine
        self.setting_engine = firewall_engine


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
            scope_props = self.target_engine.get_role_scope_props()
            self.role_engine.assign_role(principal_id, scope_props)

        elif self.binding.connection == ConnectionType.HTTP:
            # source engine depends on target engine (--> app settings)
            self.source_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_http(self.binding)
            self.source_engine.add_app_settings(app_settings)

        elif self.binding.connection == ConnectionType.SECRET:
            # store engine depends on target engine (--> secrets)
            if self.store_engine is not None:
                self.store_engine.add_dependency_engine(self.target_engine)
                secrets = self.target_engine.get_store_secrets(self.binding)
                self.store_engine.save_secret(secrets)

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
    