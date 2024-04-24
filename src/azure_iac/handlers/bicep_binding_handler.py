from azure_iac.payloads.binding import Binding
from azure_iac.payloads.models.connection_type import ConnectionType

from azure_iac.bicep_engines.modules.source_resource_engine import SourceResourceEngine
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine
from azure_iac.bicep_engines.modules.store_resource_engine import StoreResourceEngine
from azure_iac.bicep_engines.modules.setting_resource_engine import SettingResourceEngine


class BicepBindingHandler():
    def __init__(self, 
                 binding: Binding, 
                 source_engine: SourceResourceEngine,
                 target_engine: TargetResourceEngine,
                 store_engine: StoreResourceEngine,
                 setting_engine: SettingResourceEngine,
                 ):
        self.binding = binding
        self.source_engine = source_engine
        self.target_engine = target_engine
        self.store_engine = store_engine
        self.setting_engine = setting_engine


    def process_engines(self):

        if self.binding.connection == ConnectionType.SYSTEMIDENTITY:
            # target engine depends on source engine
            self.target_engine.add_dependency_engine(self.source_engine)
            principal_id = self.source_engine.get_identity_id()
            public_ip = self.source_engine.get_outbound_ip()
            self.target_engine.assign_role(principal_id)
            self.target_engine.allow_firewall(public_ip)
            
            # setting engine depends on target engine
            self.setting_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_identity(self.binding)
            self.setting_engine.add_app_settings(app_settings)

        elif self.binding.connection == ConnectionType.HTTP:
            # setting engine depends on target engine
            self.setting_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_http(self.binding)
            self.setting_engine.add_app_settings(app_settings)

        elif self.binding.connection == ConnectionType.SECRET:
            if self.store_engine is not None:
                # target engine depends on store engine
                self.target_engine.add_dependency_engine(self.store_engine)
                store = self.store_engine.get_store_name()
                self.target_engine.save_secret(store)

            # target engine depends on source engine
            self.target_engine.add_dependency_engine(self.source_engine)
            public_ip = self.source_engine.get_outbound_ip()
            self.target_engine.allow_firewall(public_ip)

            # setting engine depends on store engine
            self.setting_engine.add_dependency_engine(self.target_engine)
            app_settings = self.target_engine.get_app_settings_secret(self.binding)
            self.setting_engine.add_app_settings(app_settings)
        
        elif self.binding.connection == ConnectionType.BOTREGISTRATION:
            # target engine depends on source engine
            self.target_engine.add_dependency_engine(self.source_engine)
            endpoint = self.source_engine.get_endpoint()
            self.target_engine.set_endpoint(endpoint)

            # settings are static, no need to depend on target engine
            # TODO: get_app_settings_... method can be boundled
            app_settings = self.target_engine.get_app_settings_bot(self.binding)
            self.setting_engine.add_app_settings(app_settings)
            
        else:
            raise ValueError('Invalid connection type: {}'.format(self.binding.connection))
    