import re
from typing import List
from azure_iac.helpers.constants import ClientType, POSTGRESQL_CONSTANTS, MYSQL_CONSTANTS, SQL_CONSTANTS, CONFIGURATION_NAMES
from azure_iac.payloads.models.connection_type import ConnectionType
from azure_iac.payloads.models.resource_type import ResourceType

def get_client_type(language: str) -> ClientType:
    if language == 'js' or language == 'ts':
        return ClientType.NODE
    if language == 'java':
        return ClientType.JAVA
    if language == 'python' or language == 'py':
        return ClientType.PYTHON
    if language == 'csharp' or language == 'dotnet':
        return ClientType.DOTNET
    return ClientType.DEFAULT

def join_segments(segments: tuple, kv_separator = "=", separator = ";") -> str:
        conn_str_segs = []
        for key, value in segments:
            conn_str_segs.append(key + kv_separator + value)
        return separator.join(conn_str_segs)

def decorate_var(value: str, iac_type: str) -> str:
    if iac_type == "tf":
        return f"\"{value}\""
    
    # bicep
    # `'${var}'` should be `${var}` directly
    if re.match(r'^\${[^}]*}$', value):
        return value[2:-1]
    else:
        return '\'{}\''.format(value)

class MySqlConnInfoHelper():
    def __init__(self, language: str, server: str, user: str, password: str, database: str, port = "3306"):
        self.client_type = get_client_type(language)
        self.server = server + ".mysql.database.azure.com"
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.ssl = "true" if self.client_type == ClientType.NODE else "Require"

	# return (config_key, value, is_secret)
    def get_configs(self, customKeys: dict, connection: ConnectionType, iac_type: str) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_MYSQL_DB].keys():
            print('Warning: Binding connection type {} is not supported for MySQL, using secret', connection) 

        connection = ConnectionType.SECRET

        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_MYSQL_DB][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            if key == "connection_string":
                config_value = self.get_conn_str()
            else:
                config_value = getattr(self, key)
            config_value = decorate_var(config_value, iac_type)
            configs.append((config_key, config_value, is_secret))
        return configs
	
    def get_conn_str(self) -> str:
        if self.client_type == ClientType.JAVA:
            return MYSQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{}/{}?".format(self.server, self.port, self.database) + \
                join_segments([
                    (MYSQL_CONSTANTS.JAVA.value.SERVERTIMEZONE.value, MYSQL_CONSTANTS.JAVA.value.UTC.value),
                    (MYSQL_CONSTANTS.JAVA.value.SSL.value, MYSQL_CONSTANTS.JAVA.value.REQUIRE.value),
                    (MYSQL_CONSTANTS.JAVA.value.USER.value, self.user),
                    (MYSQL_CONSTANTS.JAVA.value.PASSWORD.value, self.password),
            ], kv_separator = "=", separator = "&")
		
        elif self.client_type == ClientType.DOTNET:
            return join_segments([
                (MYSQL_CONSTANTS.DOTNET.value.SERVER.value, self.server),
                (MYSQL_CONSTANTS.DOTNET.value.DATABASE.value, self.database),
                (MYSQL_CONSTANTS.DOTNET.value.USER.value, self.user),
                (MYSQL_CONSTANTS.DOTNET.value.PASSWORD.value, self.password),
                (MYSQL_CONSTANTS.DOTNET.value.SSL.value, MYSQL_CONSTANTS.DOTNET.value.REQUIRE.value)
            ])
		
        else:
            raise ValueError("Invalid client type for MySQL connection string generation.")
	
class SqlConnInfoHelper():
    def __init__(self, language: str, server: str, user: str, password: str, database: str, port = "3306"):
        self.client_type = get_client_type(language)
        self.server = server + ".database.windows.net"
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    def get_configs(self, customKeys: dict, connection: ConnectionType, iac_type: str) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_SQL_DB].keys():
            print('Warning: Binding connection type {} is not supported for SQL, using secret', connection)
        
        connection = ConnectionType.SECRET
        
        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_SQL_DB][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            if key == "connection_string":
                config_value = self.get_conn_str()
            else:
                config_value = getattr(self, key)
            config_value = decorate_var(config_value, iac_type)
            configs.append((config_key, config_value, is_secret))
        return configs


    def get_conn_str(self) -> str:
        if self.client_type == ClientType.PYTHON:
            return join_segments([
                (SQL_CONSTANTS.PYTHON.value.DRIVER.value, "{ODBC Driver 18 for SQL Server}"),
                (SQL_CONSTANTS.PYTHON.value.SERVER.value, self.server + "," + self.port),
                (SQL_CONSTANTS.PYTHON.value.DATABASE.value, self.database),
                (SQL_CONSTANTS.PYTHON.value.USER.value, self.user),
                (SQL_CONSTANTS.PYTHON.value.PASSWORD.value, self.password),
                (SQL_CONSTANTS.PYTHON.value.AUTHENTICATION.value, SQL_CONSTANTS.PYTHON.value.AUTHPWD.value)
            ])
        elif self.client_type == ClientType.JAVA:
            return SQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{};".format(self.server, self.port) + \
                join_segments([
                    (SQL_CONSTANTS.JAVA.value.DATABASE.value, self.database),
                    (SQL_CONSTANTS.JAVA.value.USER.value, self.user),
                    (SQL_CONSTANTS.JAVA.value.PASSWORD.value, self.password),
                    (SQL_CONSTANTS.JAVA.value.AUTHENTICATION.value, SQL_CONSTANTS.JAVA.value.AUTHPWD.value)
            ])
        elif self.client_type == ClientType.DOTNET:
            return join_segments([
                (SQL_CONSTANTS.DOTNET.value.SERVER.value, "tcp:" + self.server + "," + self.port),
                (SQL_CONSTANTS.DOTNET.value.DATABASE.value, self.database),
                (SQL_CONSTANTS.DOTNET.value.USER.value, self.user),
                (SQL_CONSTANTS.DOTNET.value.PASSWORD.value, self.password),
                (SQL_CONSTANTS.DOTNET.value.AUTHENTICATION.value, SQL_CONSTANTS.DOTNET.value.AUTHPWD.value)
            ])
        else:
            raise ValueError("Invalid client type for SQL Server connection string generation.")

class PostgreSqlConnInfoHelper():
    def __init__(self, language: str, server: str, user: str, password: str, database: str, port = "5432"):
        self.client_type = get_client_type(language)
        self.server = server + ".postgres.database.azure.com"
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.ssl = "Require"
	
    def get_configs(self, customKeys: dict, connection: ConnectionType, iac_type: str) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_POSTGRESQL_DB].keys():
            print('Warning: Binding connection type {} is not supported for PostgreSQL, using secret', connection)
        
        connection = ConnectionType.SECRET
        
        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_POSTGRESQL_DB][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            if key == "connection_string":
                config_value = self.get_conn_str()
            else:
                config_value = getattr(self, key)
            config_value = decorate_var(config_value, iac_type)
            configs.append((config_key, config_value, is_secret))
        return configs

    def get_conn_str(self) -> str:
        if self.client_type == ClientType.PYTHON:
            return join_segments([
                (POSTGRESQL_CONSTANTS.PYTHON.value.SERVER.value, self.server),
                (POSTGRESQL_CONSTANTS.PYTHON.value.DATABASE.value, self.database),
                (POSTGRESQL_CONSTANTS.PYTHON.value.PORT.value, self.port),
                (POSTGRESQL_CONSTANTS.PYTHON.value.USER.value, self.user),
                (POSTGRESQL_CONSTANTS.PYTHON.value.PASSWORD.value, self.password),
                (POSTGRESQL_CONSTANTS.PYTHON.value.SSL.value, POSTGRESQL_CONSTANTS.PYTHON.value.REQUIRE.value)
            ], kv_separator = "=", separator = " ")
        
        elif self.client_type == ClientType.JAVA:
            return POSTGRESQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{}/{}?".format(self.server, self.port, self.database) + \
                join_segments([
                    (POSTGRESQL_CONSTANTS.JAVA.value.SSL.value, POSTGRESQL_CONSTANTS.JAVA.value.REQUIRE.value),
                    (POSTGRESQL_CONSTANTS.JAVA.value.USER.value, self.user),
                    (POSTGRESQL_CONSTANTS.JAVA.value.PASSWORD.value, self.password)
            ], kv_separator = "=", separator = "&")
        
        elif self.client_type == ClientType.DOTNET:
            return join_segments([
                (POSTGRESQL_CONSTANTS.DOTNET.value.SERVER.value, self.server),
                (POSTGRESQL_CONSTANTS.DOTNET.value.DATABASE.value, self.database),
                (POSTGRESQL_CONSTANTS.DOTNET.value.PORT.value, self.port),
                (POSTGRESQL_CONSTANTS.DOTNET.value.USER.value, self.user),
                (POSTGRESQL_CONSTANTS.DOTNET.value.PASSWORD.value, self.password),
                (POSTGRESQL_CONSTANTS.DOTNET.value.SSL.value, POSTGRESQL_CONSTANTS.DOTNET.value.REQUIRE.value)
            ])
        
        else:
            raise ValueError("Invalid client type for PostgreSQL connection string generation.")

class CosmosConnInfoHelper():
    def __init__(self, language: str, connection_string=None, resource_endpoint=None):
        self.client_type = get_client_type(language)
        self.connection_string = connection_string
        self.resource_endpoint = resource_endpoint

    def get_configs(self, customKeys: dict, connection: ConnectionType) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_COSMOS_DB].keys():
            print('Warning: Binding connection type {} is not supported for Comos DB')

        configs = []

        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_COSMOS_DB][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs

class StorageConnInfoHelper():
    def __init__(self, language: str, connection_string=None, blob_endpoint=None, table_endpoint=None, queue_endpoint=None, file_endpoint=None):
        self.client_type = get_client_type(language)
        self.connection_string = connection_string
        self.blob_endpoint = blob_endpoint
        self.table_endpoint = table_endpoint
        self.queue_endpoint = queue_endpoint
        self.file_endpoint = file_endpoint

    def get_configs(self, customKeys: dict, connection: ConnectionType) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_STORAGE_ACCOUNT].keys():
            print('Warning: Binding connection type {} is not supported for Storage Account')

        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_STORAGE_ACCOUNT][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs

class ServiceBusConnInfoHelper():
    def __init__(self, language: str, connection_string=None, namespace=None):
        self.client_type = get_client_type(language)
        self.connection_string = connection_string
        self.namespace = namespace

    def get_configs(self, customKeys: dict, connection: ConnectionType) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_SERVICE_BUS].keys():
            print('Warning: Binding connection type {} is not supported for Service Bus')

        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_SERVICE_BUS][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs

class RedisConnInfoHelper():
    def __init__(self, language: str, connection_string="", host: str="", password:str="", database:str="", port = "6380"):
        self.client_type = get_client_type(language)
        self.connection_string = connection_string
        self.host = host
        self.password = password
        self.database = database
        self.port = port
        self.ssl = "true"

    def get_configs(self, customKeys: dict, connection: ConnectionType, iac_type:str) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_REDIS_CACHE].keys():
            print('Warning: Binding connection type {} is not supported for Redis Cache')

        configs = []
        # for bicep, attribites are generated inside the template, 
        # which cannot be passed as a parameter to construct the connection string
        if iac_type == "bicep":
            print('Warning: IaC generator does not support Redis Cache connection string generation for Bicep. Use AZURE_REDIS_KEY instead')
            configs.append(("AZURE_REDIS_KEY", "", True))
            return configs
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_REDIS_CACHE][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs

class KeyVaultConnInfoHelper():
    def __init__(self, language: str, resource_endpoint=None):
        self.client_type = get_client_type(language)
        self.resource_endpoint = resource_endpoint

    def get_configs(self, customKeys: dict, connection: ConnectionType) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_KEYVAULT].keys():
            print('Warning: Binding connection type {} is not supported for Key Vault')

        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_KEYVAULT][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs

class ComputeResourceConnInfoHelper():
    def __init__(self, language: str, request_url=None, resource_name=None):
        self.client_type = get_client_type(language)
        self.request_url = request_url
        self.resource_name = resource_name

    def get_configs(self, customKeys: dict, connection: ConnectionType) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES["ComputeResource"].keys():
            print('Warning: Binding connection type {} is not supported for Compute Resource')

        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES["ComputeResource"][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            # reformat key with resource name
            if config_key == default_key:
                config_key = "SERVICE{}_URL".format(self.resource_name.upper())
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs

class AppInsightsConnInfoHelper():
    def __init__(self, language: str, connection_string=None):
        self.client_type = get_client_type(language)
        self.connection_string = connection_string

    def get_configs(self, customKeys: dict, connection: ConnectionType) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_APPLICATION_INSIGHTS].keys():
            print('Warning: Binding connection type {} is not supported for App Insights')

        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_APPLICATION_INSIGHTS][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs
 

class BotConnInfoHelper():
    def __init__(self, language: str, bot_id: str, bot_password: str, bot_domain: str):
        self.client_type = get_client_type(language)
        self.bot_id = bot_id
        self.bot_password = bot_password
        self.bot_domain = bot_domain

    def get_configs(self, customKeys: dict, connection: ConnectionType) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_BOT_SERVICE].keys():
            print('Warning: Binding connection type {} is not supported for Bot Service')

        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_BOT_SERVICE][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs
    

class OpenAIConnInfoHelper():
    def __init__(self, language: str, base: str, key: str=None):
        self.client_type = get_client_type(language)
        self.base = base
        self.key = key

    def get_configs(self, customKeys: dict, connection: ConnectionType) -> List[tuple]:
        if connection not in CONFIGURATION_NAMES[ResourceType.AZURE_OPENAI].keys():
            print('Warning: Binding connection type {} is not supported for OpenAI')

        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_OPENAI][connection][self.client_type]:
            config_key = customKeys.get(default_key, default_key)
            config_value = getattr(self, key)
            configs.append((config_key, config_value, is_secret))

        return configs
