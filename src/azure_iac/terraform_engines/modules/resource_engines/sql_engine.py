from typing import List
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.sql_db import SqlDbResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class SqlDbEngine(TargetResourceEngine):
    def __init__(self, resource: SqlDbResource) -> None:
        super().__init__(Template.SQL_DB_TF.value)
        self.resource = resource

        self.main_var_administrator_login = (self.resource.name or Abbreviation.SQL_DB.value) + '_administrator_login'
        self.main_var_administrator_login_password = (self.resource.name or Abbreviation.SQL_DB.value) + '_administrator_login_password'

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.SQL_DB.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.SQL_DB.value) + '${var.resource_suffix}'
        self.module_params_administrator_login = '${var.' + self.main_var_administrator_login + '}'
        self.module_params_administrator_login_password = '${var.' + self.main_var_administrator_login_password + '}'
        
        # main.tf variables and outputs
        self.main_variables = [
            (self.main_var_administrator_login, None),
            (self.main_var_administrator_login_password, None, True)
        ]
        self.main_outputs = [
            (string_helper.format_snake('sql', 'server', self.resource.name, 'id'), 
             'azurerm_mssql_server.{}.id'.format(self.module_name)),
            (string_helper.format_snake('sql', 'db', self.resource.name, 'id'),
             'azurerm_mssql_database.{}.id'.format(self.module_name + "db"))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return None

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        return None

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_MYSQLDB_CONNECTIONSTRING'
        # hard code to .NET connection string
        conn_string = '\"Server=tcp:{}.database.windows.net,1433;User ID=\'{}\';Password=\'{}\';Initial Catalog=\'{}\';SslMode=Required;Persist Security Info=False;MultipleActiveResultSets=False;Encrypt=True;TrustServerCertificate=False;Authentication=\\"Active Directory Password\\";\"'.format(
                          self.module_params_name, 
                          self.module_params_administrator_login, 
                          self.module_params_administrator_login_password, 
                          self.module_params_name + "-db"
                      )

        return [
            AppSetting(AppSettingType.SecretReference, app_setting_key, conn_string)
        ]
