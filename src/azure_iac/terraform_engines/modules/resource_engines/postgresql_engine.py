from typing import List
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.postgresql_db import PostgreSqlDbResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class PostgreSqlDbEngine(TargetResourceEngine):
    def __init__(self, resource: PostgreSqlDbResource) -> None:
        super().__init__(Template.POSTGRESQL_TF.value)
        self.resource = resource

        self.main_var_administrator_login = (self.resource.name or Abbreviation.POSTGRESQL_DB.value) + '_administrator_login'
        self.main_var_administrator_login_password = (self.resource.name or Abbreviation.POSTGRESQL_DB.value) + '_administrator_login_password'

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.POSTGRESQL_DB.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.POSTGRESQL_DB.value) + '${var.resource_suffix}'
        self.module_params_administrator_login = '${var.' + self.main_var_administrator_login + '}'
        self.module_params_administrator_login_password = '${var.' + self.main_var_administrator_login_password + '}'
        
        # main.tf variables and outputs
        self.main_variables = [
            (self.main_var_administrator_login, None),
            (self.main_var_administrator_login_password, None, True)
        ]
        self.main_outputs = [
            (string_helper.format_snake('postgresql', 'server', self.resource.name, 'id'), 
             'azurerm_postgresql_flexible_server.{}.id'.format(self.module_name)),
            (string_helper.format_snake('postgresql', 'db', self.resource.name, 'id'),
             'azurerm_postgresql_flexible_server_database.{}.id'.format(self.module_name + "db"))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return None

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        return None

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding, language: str) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_POSTGRESQLDB_CONNECTIONSTRING'
        # hard code to .NET connection string
        conn_string = '\"Server=\'{}.postgres.database.azure.com\';Port=5432;UserID=\'{}\';Password=\'{}\';Database=\'{}\';SslMode=Required;\"'.format(
                          self.module_params_name, 
                          self.module_params_administrator_login, 
                          self.module_params_administrator_login_password, 
                          self.module_params_name + "-db"
                      )

        return [
            AppSetting(AppSettingType.SecretReference, app_setting_key, conn_string)
        ]
