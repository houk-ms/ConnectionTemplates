from typing import List

from azure_iac.helpers.connection_info import get_client_type, join_segments
from azure_iac.helpers.constants import ClientType, MYSQL_CONSTANTS
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
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:

        def get_conn_str(client_type, server, port, database, user, password) -> str:
            if client_type == ClientType.JAVA:
                return "\"" + \
                    MYSQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{}/{}?".format(server, port, database) + \
                    join_segments([
                        (MYSQL_CONSTANTS.JAVA.value.SERVERTIMEZONE.value, MYSQL_CONSTANTS.JAVA.value.UTC.value),
                        (MYSQL_CONSTANTS.JAVA.value.SSL.value, MYSQL_CONSTANTS.JAVA.value.REQUIRE.value),
                        (MYSQL_CONSTANTS.JAVA.value.USER.value, user),
                        (MYSQL_CONSTANTS.JAVA.value.PASSWORD.value, password),
                    ], kv_separator = "=", separator = "&") + "\""
                
            elif client_type == ClientType.DOTNET:
                return "\"" + \
                    join_segments([
                        (MYSQL_CONSTANTS.DOTNET.value.SERVER.value, server),
                        (MYSQL_CONSTANTS.DOTNET.value.DATABASE.value, database),
                        (MYSQL_CONSTANTS.DOTNET.value.USER.value, user),
                        (MYSQL_CONSTANTS.DOTNET.value.PASSWORD.value, password),
                        (MYSQL_CONSTANTS.DOTNET.value.SSL.value, MYSQL_CONSTANTS.DOTNET.value.REQUIRE.value)
                    ]) + "\""
                
            else:
                # use separate connection info instead of connection string
                return ''
        
        client_type = get_client_type(binding.source.service.language)
        server = self.module_params_name + ".mysql.database.azure.com"
        port = "3306"
        database = self.module_params_database_name
        user = self.module_params_administrator_login
        password = self.module_params_administrator_login_password
        conn_str = get_conn_str(client_type,
                                server=server,
                                port=port,
                                database=database,
                                user=user,
                                password=password)

        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = {
            ClientType.PYTHON: [
                (AppSettingType.KeyValue, 'AZURE_MYSQL_HOST', "\"{}\"".format(server)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_DATABASE', "\"{}\"".format(database)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_USER', "\"{}\"".format(user)),
                (AppSettingType.SecretReference, 'AZURE_MYSQL_PASSWORD', "\"{}\"".format(password)),
            ],
            ClientType.NODE: [
                (AppSettingType.KeyValue, 'AZURE_MYSQL_HOST', "\"{}\"".format(server)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_DATABASE', "\"{}\"".format(database)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_USER', "\"{}\"".format(user)),
                (AppSettingType.SecretReference, 'AZURE_MYSQL_PASSWORD', "\"{}\"".format(password)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_PORT', "\"{}\"".format(port)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_SSL', "\"true\"")
            ],
            ClientType.JAVA: [
                (AppSettingType.SecretReference, "AZURE_MYSQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DOTNET: [
                (AppSettingType.SecretReference, "AZURE_MYSQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DEFAULT: [
                (AppSettingType.KeyValue, 'AZURE_MYSQL_HOST', "\"{}\"".format(server)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_DATABASE', "\"{}\"".format(database)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_USER', "\"{}\"".format(user)),
                (AppSettingType.SecretReference, 'AZURE_MYSQL_PASSWORD', "\"{}\"".format(password)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_PORT', "\"{}\"".format(port)),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_SSL', "\"Require\"")
            ]
        }
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings[client_type]]
