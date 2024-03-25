from payloads.binding import Binding
from payloads.models.connection_type import ConnectionType
from payloads.models.resource_type import ResourceType
from engines.modules.source_resource_engine import SourceResourceEngine
from engines.modules.target_resource_engine import TargetResourceEngine
from engines.modules.store_resource_engine import StoreResourceEngine
from engines.modules.setting_resource_engine import SettingResourceEngine

class BindingHandler():
    def __init__(self, 
                 binding: Binding, 
                 source_engine: SourceResourceEngine,
                 target_engine: TargetResourceEngine,
                 store_engine: StoreResourceEngine,
                 setting_engine: SettingResourceEngine):
        self.binding = binding
        self.source_engine = source_engine
        self.target_engine = target_engine
        self.store_engine = store_engine
        self.setting_engine = setting_engine


    def process_engines(self):

        if self.binding.connection == ConnectionType.SYSTEMIDENTITY:
            # target engine depends on source engine
            self.target_engine.add_module_dependency(self.source_engine.get_as_module_dependency())
            principal_id = self.source_engine.get_identity_id()
            public_ip = self.source_engine.get_outbound_ip()
            self.target_engine.assign_role(principal_id)
            self.target_engine.allow_firewall(public_ip)
            
            # setting engine depends on target engine
            self.setting_engine.add_module_dependency(self.target_engine.get_as_module_dependency())
            app_settings = self.target_engine.get_app_settings_identity()
            self.setting_engine.add_app_settings(app_settings)

        elif self.binding.connection == ConnectionType.HTTP:
            # target engine depends on source engine
            # setting engine depends on target engine
            self.target_engine.add_module_dependency(self.source_engine.get_as_module_dependency())
            app_settings = self.target_engine.get_app_settings_http()
            self.setting_engine.add_app_settings(app_settings)

        elif self.binding.connection == ConnectionType.SECRET:
            # target engine depends on store engine
            self.target_engine.add_module_dependency(self.store_engine.get_as_module_dependency())
            store = self.store_engine.get_store_name()
            self.target_engine.save_secret(store)

            # target engine depends on source engine
            self.target_engine.add_module_dependency(self.source_engine.get_as_module_dependency())
            public_ip = self.source_engine.get_outbound_ip()
            self.target_engine.allow_firewall(public_ip)

            # setting engine depends on store engine
            self.setting_engine.add_module_dependency(self.target_engine.get_as_module_dependency())
            app_settings = self.target_engine.get_app_settings_secret(self.source_engine.resource.type)
            self.setting_engine.add_app_settings(app_settings)
            
        else:
            raise ValueError('Invalid connection type: {}'.format(self.binding.connection_type))
    