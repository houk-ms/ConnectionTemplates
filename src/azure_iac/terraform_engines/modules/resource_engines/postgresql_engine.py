from typing import List

from azure_iac.helpers.connection_info import get_client_type, join_segments
from azure_iac.helpers.constants import ClientType, POSTGRESQL_CONSTANTS
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
        self.module_params_database_name = (self.resource.name or Abbreviation.POSTGRESQL_DB.value) + '-db'
        
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
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:

        def get_conn_str(client_type, server, port, database, user, password) -> str:
            if client_type == ClientType.PYTHON:
                return "\"" + \
                    join_segments([
                        (POSTGRESQL_CONSTANTS.PYTHON.value.SERVER.value, server),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.DATABASE.value, database),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.PORT.value, port),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.USER.value, user),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.PASSWORD.value, password),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.SSL.value, POSTGRESQL_CONSTANTS.PYTHON.value.REQUIRE.value)
                    ], kv_separator = "=", separator = " ") + "\""
        
            elif client_type == ClientType.JAVA:
                return "\"" + \
                    POSTGRESQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{}/{}?".format(server, port, database) + \
                    join_segments([
                        (POSTGRESQL_CONSTANTS.JAVA.value.SSL.value, POSTGRESQL_CONSTANTS.JAVA.value.REQUIRE.value),
                        (POSTGRESQL_CONSTANTS.JAVA.value.USER.value, user),
                        (POSTGRESQL_CONSTANTS.JAVA.value.PASSWORD.value, password)
                    ], kv_separator = "=", separator = "&") + "\""
        
            elif client_type == ClientType.DOTNET:
                return "\"" + \
                    join_segments([
                        (POSTGRESQL_CONSTANTS.DOTNET.value.SERVER.value, server),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.DATABASE.value, database),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.PORT.value, port),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.USER.value, user),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.PASSWORD.value, password),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.SSL.value, POSTGRESQL_CONSTANTS.DOTNET.value.REQUIRE.value)
                    ]) + "\""
                
            else:
                # use separate connection info instead of connection string
                return ''
        
        client_type = get_client_type(binding.source.service.language)
        server = self.module_params_name + ".postgres.database.azure.com"
        port = "5432"
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
                (AppSettingType.SecretReference, 'AZURE_POSTGRESQL_CONNECTIONSTRING', conn_str),
            ],
            ClientType.NODE: [
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_HOST', "\"{}\"".format(server)),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_DATABASE', "\"{}\"".format(database)),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_USER', "\"{}\"".format(user)),
                (AppSettingType.SecretReference, 'AZURE_POSTGRESQL_PASSWORD', "\"{}\"".format(password)),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_PORT', "\"{}\"".format(port)),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_SSL', "\"true\"")
            ],
            ClientType.JAVA: [
                (AppSettingType.SecretReference, "AZURE_POSTGRESQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DOTNET: [
                (AppSettingType.SecretReference, "AZURE_POSTGRESQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DEFAULT: [
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_HOST', "\"{}\"".format(server)),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_DATABASE', "\"{}\"".format(database)),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_USERNAME', "\"{}\"".format(user)),
                (AppSettingType.SecretReference, 'AZURE_POSTGRESQL_PASSWORD', "\"{}\"".format(password)),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_PORT', "\"{}\"".format(port)),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_SSL', "\"Require\"")
            ]
        }
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings[client_type]]
