from typing import List

from azure_iac.helpers.connection_info import get_client_type, join_segments
from azure_iac.helpers.constants import ClientType, MYSQL_CONSTANTS
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.mysql_db import MySqlDbResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class MySqlDbEngine(TargetResourceEngine):

    def __init__(self, resource: MySqlDbResource) -> None:
        super().__init__(Template.MYSQL_BICEP.value,
                         Template.MYSQL_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('mysql', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('mysql', self.resource.name)
        self.module_params_name = string_helper.format_camel('mysql', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('mysql', self.resource.name)
        self.module_params_admin_name = string_helper.format_camel('mysql', self.resource.name, "AdminName")
        self.module_params_password = string_helper.format_camel('mysql', self.resource.name, "Password")
        self.module_params_database_name = string_helper.format_camel('mysql', self.resource.name, "DatabaseName")
        
        params_name = string_helper.format_resource_name(self.resource.name or Abbreviation.MYSQL_DB.value)
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', params_name),
            (self.module_params_admin_name, 'string', None),
            (self.module_params_password, 'string', None, False, True),
            (self.module_params_database_name, 'string', "db" + '${resourceToken}')
        ]
        self.main_outputs = [
            (string_helper.format_camel('mysql', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:

        def get_conn_str(client_type, server, port, database, user, password) -> str:
            if client_type == ClientType.JAVA:
                return "\'" + \
                    MYSQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{}/{}?".format(server, port, database) + \
                    join_segments([
                        (MYSQL_CONSTANTS.JAVA.value.SERVERTIMEZONE.value, MYSQL_CONSTANTS.JAVA.value.UTC.value),
                        (MYSQL_CONSTANTS.JAVA.value.SSL.value, MYSQL_CONSTANTS.JAVA.value.REQUIRE.value),
                        (MYSQL_CONSTANTS.JAVA.value.USER.value, user),
                        (MYSQL_CONSTANTS.JAVA.value.PASSWORD.value, password),
                    ], kv_separator = "=", separator = "&") + "\'"
                
            elif client_type == ClientType.DOTNET:
                return "\'" + \
                    join_segments([
                        (MYSQL_CONSTANTS.DOTNET.value.SERVER.value, server),
                        (MYSQL_CONSTANTS.DOTNET.value.DATABASE.value, database),
                        (MYSQL_CONSTANTS.DOTNET.value.USER.value, user),
                        (MYSQL_CONSTANTS.DOTNET.value.PASSWORD.value, password),
                        (MYSQL_CONSTANTS.DOTNET.value.SSL.value, MYSQL_CONSTANTS.DOTNET.value.REQUIRE.value)
                    ]) + "\'"
                
            else:
                # use separate connection info instead of connection string
                return ''
        
        client_type = get_client_type(binding.source.service.language)
        conn_str = get_conn_str(client_type,
                                server="${" + self.module_params_name + "}.mysql.database.azure.com",
                                port="3306",
                                database="${" + self.module_params_database_name + "}",
                                user="${" + self.module_params_admin_name + "}",
                                password="${" + self.module_params_password + "}")
        print(conn_str)
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = {
            ClientType.PYTHON: [
                (AppSettingType.KeyValue, 'AZURE_MYSQL_HOST', "\'${" + self.module_params_name + "}.mysql.database.azure.com\'"),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_DATABASE', self.module_params_database_name),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_USER', self.module_params_admin_name),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_PASSWORD', self.module_params_password),
            ],
            ClientType.NODE: [
                (AppSettingType.KeyValue, 'AZURE_MYSQL_HOST', "\'${" + self.module_params_name + "}.mysql.database.azure.com\'"),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_DATABASE', self.module_params_database_name),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_USER', self.module_params_admin_name),
                (AppSettingType.KeyVaultReference, 'AZURE_MYSQL_PASSWORD', self.module_params_password),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_PORT', "\'3306\'"),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_SSL', "true")
            ],
            ClientType.JAVA: [
                (AppSettingType.KeyVaultReference, "AZURE_MYSQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DOTNET: [
                (AppSettingType.KeyVaultReference, "AZURE_MYSQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DEFAULT: [
                (AppSettingType.KeyValue, 'AZURE_MYSQL_HOST', "\'${" + self.module_params_name + "}.mysql.database.azure.com\'"),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_DATABASE', self.module_params_database_name),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_USER', self.module_params_admin_name),
                (AppSettingType.KeyVaultReference, 'AZURE_MYSQL_PASSWORD', self.module_params_password),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_PORT', "\'3306\'"),
                (AppSettingType.KeyValue, 'AZURE_MYSQL_SSL', "Require")
            ]
        }
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings[client_type]]