from typing import List
from payloads.binding import Binding
from payloads.models.resource_type import ResourceType
from payloads.resources.sql_db import SqlDbResource

from engines.models.abbrevation import Abbreviation
from engines.models.template import Template
from engines.modules.target_resource_engine import TargetResourceEngine

from helpers import string_helper


class SqlDbEngine(TargetResourceEngine):

    def __init__(self, resource: SqlDbResource) -> None:
        super().__init__(Template.SQL_DB_BICEP.value,
                         Template.SQL_DB_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('sql', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('sql', self.resource.name)
        self.module_params_name = string_helper.format_camel('sql', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('sql', self.resource.name)
        
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.SQL_DB.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('sql', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_REDIS_CONNECTIONSTRING'

        if binding.source.type == ResourceType.AZURE_APP_SERVICE:
            return [
                (app_setting_key, '{}.outputs.appServiceSecretReference'.format(self.module_name))
            ]
        elif binding.source.type == ResourceType.AZURE_CONTAINER_APP:
            return [
                (app_setting_key, '{}.outputs.containerAppSecretReference'.format(self.module_name))
            ]