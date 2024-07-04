from azure_iac.payloads.binding import Binding
from azure_iac.payloads.models.connection_type import ConnectionType
from azure_iac.payloads.models.resource_type import ResourceType

from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.terraform_engines.modules.firewall_resource_engine import FirewallResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.role_resource_engine import RoleResourceEngine
from azure_iac.terraform_engines.modules.resource_engines.keyvaultsecret_engine import KeyVaultSecretEngine
from azure_iac.terraform_engines.modules.resource_engines.useridentity_engine import UserIdentityEngine


class TerraformBindingHandler():

    ALLOW_AZURE_RESOURCES = [ResourceType.AZURE_POSTGRESQL_DB, ResourceType.AZURE_SQL_DB, ResourceType.AZURE_MYSQL_DB, ResourceType.AZURE_REDIS_CACHE]

    def __init__(self, 
                 binding: Binding, 
                 source_engine: SourceResourceEngine,
                 target_engine: TargetResourceEngine,
                 role_engine: RoleResourceEngine,
                 firewall_engine: FirewallResourceEngine,
                 key_vault_secret_engine: KeyVaultSecretEngine,
                 user_identity_engine: UserIdentityEngine
                 ):
        self.binding = binding
        self.source_engine = source_engine
        self.target_engine = target_engine
        self.role_engine = role_engine
        self.firewall_engine = firewall_engine
        self.key_vault_secret_engine = key_vault_secret_engine
        self.user_identity_engine = user_identity_engine


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
                # for DB. use allow azure rule
                if self.firewall_engine.resource.type not in TerraformBindingHandler.ALLOW_AZURE_RESOURCES:
                    public_ip = self.source_engine.get_outbound_ip()
                    self.firewall_engine.allow_firewall(public_ip)
            
            # role engine depends on source and target engine (--> principal id, scope)
            self.role_engine.add_dependency_engine(self.source_engine)
            self.role_engine.add_dependency_engine(self.target_engine)
            principal_id = self.source_engine.get_identity_id()
            scope, role_def = self.target_engine.get_role_scope()
            self.role_engine.assign_role(principal_id, scope, role_def)

        elif self.binding.connection == ConnectionType.USERIDENTITY:
            # enable user identity for source engine
            self.source_engine.enable_user_identity(self.user_identity_engine.get_identity_id())

            # role engine depends on user identity and target engine (--> principal id, scope)
            self.role_engine.add_dependency_engine(self.source_engine)
            self.role_engine.add_dependency_engine(self.target_engine)
            principal_id = self.user_identity_engine.get_principal_id()
            scope, role_def = self.target_engine.get_role_scope()
            self.role_engine.assign_role(principal_id, scope, role_def)

            # source engine depends on target engine (--> app settings)
            self.source_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_identity(self.binding)
            # client id key for user identity
            custom_keys = dict() if self.binding.customKeys is None else self.binding.customKeys
            app_settings.append(AppSetting(AppSettingType.KeyValue,
                                           custom_keys.get('AZURE_CLIENT_ID', 'AZURE_CLIENT_ID'),
                                           self.user_identity_engine.get_client_id()))
            self.source_engine.add_app_settings(app_settings)
            
            # firewall engine depends on source engine (--> outbound ips)
            # target may not support separated firewall settings
            if self.firewall_engine is not None:
                self.firewall_engine.add_dependency_engine(self.source_engine)
                # for DB. use allow azure rule
                if self.firewall_engine.resource.type not in TerraformBindingHandler.ALLOW_AZURE_RESOURCES:
                    public_ip = self.source_engine.get_outbound_ip()
                    self.firewall_engine.allow_firewall(public_ip)

        elif self.binding.connection == ConnectionType.HTTP:
            # source engine depends on target engine (--> app settings)
            self.source_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_http(self.binding)
            self.source_engine.add_app_settings(app_settings)

        elif self.binding.connection == ConnectionType.SECRET:
            # source engine depends on target engine (--> app settings)
            self.source_engine.add_dependency_engine(self.target_engine)
            
            app_settings = self.target_engine.get_app_settings_secret(self.binding)
            if self.binding.store is not None and self.key_vault_secret_engine is not None:
                self.key_vault_secret_engine.change_appsettings_for_secret_reference(self.binding, app_settings)
            self.source_engine.add_app_settings(app_settings)
            
            # firewall engine depends on source engine (--> outbound ips)
            # target may not support separated firewall settings
            if self.firewall_engine is not None:
                self.firewall_engine.add_dependency_engine(self.source_engine)
                # for DB. use allow azure rule
                if self.firewall_engine.resource.type not in TerraformBindingHandler.ALLOW_AZURE_RESOURCES:
                    public_ip = self.source_engine.get_outbound_ip()
                    self.firewall_engine.allow_firewall(public_ip)
        
        elif self.binding.connection == ConnectionType.BOTREGISTRATION:
            # target engine depends on source engine
            self.target_engine.add_dependency_engine(self.source_engine)
            endpoint = self.source_engine.get_endpoint()
            self.target_engine.set_endpoint(endpoint)

            # settings are static, no need to depend on target engine
            # TODO: get_app_settings_... method can be boundled
            app_settings = self.target_engine.get_app_settings_bot(self.binding)
            self.source_engine.add_app_settings(app_settings)

        else:
            raise ValueError('Invalid connection type: {}'.format(self.binding.connection_type))
    