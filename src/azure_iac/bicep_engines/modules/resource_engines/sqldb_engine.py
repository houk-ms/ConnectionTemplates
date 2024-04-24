from typing import List

from azure_iac.helpers.connection_info import SqlConnInfoHelper
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.sql_db import SqlDbResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


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
        self.module_params_admin_name = string_helper.format_camel('sql', self.resource.name, "AdminName")
        self.module_params_password = string_helper.format_camel('sql', self.resource.name, "Password")
        self.module_params_database_name = string_helper.format_camel('sql', self.resource.name, "DatabaseName")
        
        params_name = string_helper.format_resource_name(self.resource.name or Abbreviation.SQL_DB.value)
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', params_name),
            (self.module_params_admin_name, 'string', "administrator_" + params_name),
            (self.module_params_password, 'string', "\'Aa0!${newGuid()}\'", False, True),
            (self.module_params_database_name, 'string', "database_" + params_name)
        ]
        self.main_outputs = [
            (string_helper.format_camel('sql', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding, language: str) -> List[tuple]:
        connInfoHelper = SqlConnInfoHelper(language,
                                           server="${" + self.module_params_name + "}",
                                           user="${" + self.module_params_admin_name + "}",
                                           password="${" + self.module_params_password + "}",
                                           database="${" + self.module_params_database_name + "}"
                                           )
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection,
                                             "bicep")
        
        return self._get_app_settings(configs)