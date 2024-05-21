from typing import List

from azure_iac.helpers.connection_info import get_client_type, join_segments
from azure_iac.helpers.constants import ClientType, POSTGRESQL_CONSTANTS
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.postgresql_db import PostgreSqlDbResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class PostgreSqlDbEngine(TargetResourceEngine):

    def __init__(self, resource: PostgreSqlDbResource) -> None:
        super().__init__(Template.POSTGRESQL_BICEP.value,
                         Template.POSTGRESQL_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('postgreSql', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('postgresql', self.resource.name)
        self.module_params_name = string_helper.format_camel('postgreSql', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('postgresql', self.resource.name)
        self.module_params_admin_name = string_helper.format_camel('postgreSql', self.resource.name, "AdminName")
        self.module_params_password = string_helper.format_camel('postgreSql', self.resource.name, "Password")
        self.module_params_database_name = string_helper.format_camel('postgreSql', self.resource.name, "DatabaseName")
        
        params_name = string_helper.format_resource_name(self.resource.name or Abbreviation.POSTGRESQL_DB.value)
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', params_name),
            (self.module_params_admin_name, 'string', None),
            (self.module_params_password, 'string', None, False, True),
            (self.module_params_database_name, 'string', "db_" + '${resourceToken}')
        ]
        self.main_outputs = [
            (string_helper.format_camel('postgreSql', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:      

        def get_conn_str(client_type, server, port, database, user, password) -> str:
            if client_type == ClientType.PYTHON:
                return "\'" + \
                    join_segments([
                        (POSTGRESQL_CONSTANTS.PYTHON.value.SERVER.value, server),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.DATABASE.value, database),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.PORT.value, port),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.USER.value, user),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.PASSWORD.value, password),
                        (POSTGRESQL_CONSTANTS.PYTHON.value.SSL.value, POSTGRESQL_CONSTANTS.PYTHON.value.REQUIRE.value)
                    ], kv_separator = "=", separator = " ") + "\'"
        
            elif client_type == ClientType.JAVA:
                return "\'" + \
                    POSTGRESQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{}/{}?".format(server, port, database) + \
                    join_segments([
                        (POSTGRESQL_CONSTANTS.JAVA.value.SSL.value, POSTGRESQL_CONSTANTS.JAVA.value.REQUIRE.value),
                        (POSTGRESQL_CONSTANTS.JAVA.value.USER.value, user),
                        (POSTGRESQL_CONSTANTS.JAVA.value.PASSWORD.value, password)
                    ], kv_separator = "=", separator = "&") + "\'"
        
            elif client_type == ClientType.DOTNET:
                return "\'" + \
                    join_segments([
                        (POSTGRESQL_CONSTANTS.DOTNET.value.SERVER.value, server),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.DATABASE.value, database),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.PORT.value, port),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.USER.value, user),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.PASSWORD.value, password),
                        (POSTGRESQL_CONSTANTS.DOTNET.value.SSL.value, POSTGRESQL_CONSTANTS.DOTNET.value.REQUIRE.value)
                    ]) + "\'"
                
            else:
                # use separate connection info instead of connection string
                return ''
        
        client_type = get_client_type(binding.source.service.language)
        conn_str = get_conn_str(client_type,
                                server="${" + self.module_params_name + "}.postgres.database.azure.com",
                                port="5432",
                                database="${" + self.module_params_database_name + "}",
                                user="${" + self.module_params_admin_name + "}",
                                password="${" + self.module_params_password + "}")

        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = {
            ClientType.PYTHON: [
                (AppSettingType.KeyVaultReference, 'AZURE_POSTGRESQL_CONNECTIONSTRING', conn_str),
            ],
            ClientType.NODE: [
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_HOST', "\'${" + self.module_params_name + "}.postgres.database.azure.com\'"),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_DATABASE', self.module_params_database_name),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_USER', self.module_params_admin_name),
                (AppSettingType.KeyVaultReference, 'AZURE_POSTGRESQL_PASSWORD', self.module_params_password),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_PORT', "\'5432\'"),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_SSL', "true")
            ],
            ClientType.JAVA: [
                (AppSettingType.KeyVaultReference, "AZURE_POSTGRESQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DOTNET: [
                (AppSettingType.KeyVaultReference, "AZURE_POSTGRESQL_CONNECTIONSTRING", conn_str),
            ],
            ClientType.DEFAULT: [
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_HOST', "\'${" + self.module_params_name + "}.postgres.database.azure.com\'"),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_DATABASE', self.module_params_database_name),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_USERNAME', self.module_params_admin_name),
                (AppSettingType.KeyVaultReference, 'AZURE_POSTGRESQL_PASSWORD', self.module_params_password),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_PORT', "\'5432\'"),
                (AppSettingType.KeyValue, 'AZURE_POSTGRESQL_SSL', "Require")
            ]
        }
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings[client_type]]