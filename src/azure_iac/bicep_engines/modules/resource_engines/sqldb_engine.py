from typing import List

from azure_iac.helpers.connection_info import get_client_type, join_segments
from azure_iac.helpers.constants import ClientType, SQL_CONSTANTS
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
            (self.module_params_admin_name, 'string', None),
            (self.module_params_password, 'string', None, False, True),
            (self.module_params_database_name, 'string', "db_" + '${resourceToken}')
        ]
        self.main_outputs = [
            (string_helper.format_camel('sql', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        
        def get_conn_str(client_type, server, port, database, user, password) -> str:
            if client_type == ClientType.PYTHON:
                return "\'" + \
                    join_segments([
                        (SQL_CONSTANTS.PYTHON.value.DRIVER.value, "{ODBC Driver 18 for SQL Server}"),
                        (SQL_CONSTANTS.PYTHON.value.SERVER.value, server + "," + port),
                        (SQL_CONSTANTS.PYTHON.value.DATABASE.value, database),
                        (SQL_CONSTANTS.PYTHON.value.USER.value, user),
                        (SQL_CONSTANTS.PYTHON.value.PASSWORD.value, password),
                        (SQL_CONSTANTS.PYTHON.value.AUTHENTICATION.value, SQL_CONSTANTS.PYTHON.value.AUTHPWD.value)
                    ]) + "\'"
            elif client_type == ClientType.JAVA:
                return "\'" + \
                    SQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{};".format(server, port) + \
                        join_segments([
                            (SQL_CONSTANTS.JAVA.value.DATABASE.value, database),
                            (SQL_CONSTANTS.JAVA.value.USER.value, user),
                            (SQL_CONSTANTS.JAVA.value.PASSWORD.value, password),
                            (SQL_CONSTANTS.JAVA.value.AUTHENTICATION.value, SQL_CONSTANTS.JAVA.value.AUTHPWD.value)
                    ]) + "\'"
            elif client_type == ClientType.DOTNET:
                return "\'" + \
                    join_segments([
                        (SQL_CONSTANTS.DOTNET.value.SERVER.value, "tcp:" + server + "," + port),
                        (SQL_CONSTANTS.DOTNET.value.DATABASE.value, database),
                        (SQL_CONSTANTS.DOTNET.value.USER.value, user),
                        (SQL_CONSTANTS.DOTNET.value.PASSWORD.value, password),
                        (SQL_CONSTANTS.DOTNET.value.AUTHENTICATION.value, SQL_CONSTANTS.DOTNET.value.AUTHPWD.value)
                    ]) + "\'"
                
            else:
                # use separate connection info instead of connection string
                return ''
        
        client_type = get_client_type(binding.source.service.language)
        conn_str = get_conn_str(client_type,
                                server="${" + self.module_params_name + "}.database.windows.net",
                                port="1433",
                                database="${" + self.module_params_database_name + "}",
                                user="${" + self.module_params_admin_name + "}",
                                password="${" + self.module_params_password + "}")

        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = {
            ClientType.PYTHON: [
                (AppSettingType.KeyValue, 'AZURE_SQL_SERVER', "\'${" + self.module_params_name + "}.database.windows.net\'"),
                (AppSettingType.KeyValue, 'AZURE_SQL_DATABASE', self.module_params_database_name),
                (AppSettingType.KeyValue, 'AZURE_SQL_USER', self.module_params_admin_name),
                (AppSettingType.KeyVaultReference, 'AZURE_SQL_PASSWORD', self.module_params_password)
            ],
            ClientType.NODE: [
                (AppSettingType.KeyValue, 'AZURE_SQL_SERVER', "\'${" + self.module_params_name + "}.database.windows.net\'"),
                (AppSettingType.KeyValue, 'AZURE_SQL_DATABASE', self.module_params_database_name),
                (AppSettingType.KeyValue, 'AZURE_SQL_USERNAME', self.module_params_admin_name),
                (AppSettingType.KeyVaultReference, 'AZURE_SQL_PASSWORD', self.module_params_password),
                (AppSettingType.KeyValue, 'AZURE_SQL_PORT', "\'1433\'")
            ],
            ClientType.JAVA: [
                (AppSettingType.KeyVaultReference, "AZURE_SQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DOTNET: [
                (AppSettingType.KeyVaultReference, "AZURE_SQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DEFAULT: [
                (AppSettingType.KeyValue, 'AZURE_SQL_HOST', "\'${" + self.module_params_name + "}.database.windows.net\'"),
                (AppSettingType.KeyValue, 'AZURE_SQL_DATABASE', self.module_params_database_name),
                (AppSettingType.KeyValue, 'AZURE_SQL_USERNAME', self.module_params_admin_name),
                (AppSettingType.KeyVaultReference, 'AZURE_SQL_PASSWORD', self.module_params_password),
                (AppSettingType.KeyValue, 'AZURE_SQL_PORT', "\'1433\'")
            ]
        }
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings[client_type]]