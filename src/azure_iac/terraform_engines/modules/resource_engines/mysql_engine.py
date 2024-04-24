from typing import List
from azure_iac.helpers.connection_info import MySqlConnInfoHelper
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.mysql_db import MySqlDbResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class MySqlDbEngine(TargetResourceEngine):
    def __init__(self, resource: MySqlDbResource) -> None:
        super().__init__(Template.MYSQL_DB_TF.value)
        self.resource = resource

        self.main_var_administrator_login = (self.resource.name or Abbreviation.MYSQL_DB.value) + '_administrator_login'
        self.main_var_administrator_login_password = (self.resource.name or Abbreviation.MYSQL_DB.value) + '_administrator_login_password'

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.MYSQL_DB.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.MYSQL_DB.value) + '${var.resource_suffix}'
        self.module_params_administrator_login = '${var.' + self.main_var_administrator_login + '}'
        self.module_params_administrator_login_password = '${var.' + self.main_var_administrator_login_password + '}'
        self.module_params_database_name = (self.resource.name or Abbreviation.MYSQL_DB.value) + '-db'
        
        # main.tf variables and outputs
        self.main_variables = [
            (self.main_var_administrator_login, None),
            (self.main_var_administrator_login_password, None, True)
        ]
        self.main_outputs = [
            (string_helper.format_snake('mysql', 'server', self.resource.name, 'id'), 
             'azurerm_mysql_flexible_server.{}.id'.format(self.module_name)),
            (string_helper.format_snake('mysql', 'db', self.resource.name, 'id'),
             'azurerm_mysql_flexible_database.{}.id'.format(self.module_name + "db"))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return None

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        return None

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding, language="") -> List[tuple]:
        connInfoHelper = MySqlConnInfoHelper(language,
                                             server=self.module_params_name,
                                             user=self.module_params_administrator_login,
                                             password=self.module_params_administrator_login_password,
                                             database=self.module_params_database_name)
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys, binding.connection)
        return self._get_app_settings(configs)
