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

def join_segments(segments: tuple[str], kv_separator = "=", separator = ";") -> str:
        conn_str_segs = []
        for key, value in segments:
            conn_str_segs.append(key + kv_separator + value)
        return separator.join(conn_str_segs)


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
    def get_secret_configs(self, customKeys: dict) -> list[tuple]:
        configs = []
        for key, default_key, is_secret in CONFIGURATION_NAMES[ResourceType.AZURE_MYSQL_DB][ConnectionType.SECRET][self.client_type]:
            config_key = customKeys.get(key, default_key)
            if key == "connection_string":
                config_value = self.get_conn_str()
            else:
                config_value = getattr(self, key)
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
        self.ssl = "Required"

    def get_conn_str(self) -> str:
        if self.client_type == ClientType.PYTHON:
            return join_segments([
                (SQL_CONSTANTS.PYTHON.value.DRIVER.value, "{ODBC Driver 18 for SQL Server}")
                (SQL_CONSTANTS.PYTHON.value.SERVER.value, self.server + "," + self.port),
                (SQL_CONSTANTS.PYTHON.value.DATABASE.value, self.database),
                (SQL_CONSTANTS.PYTHON.value.USER.value, self.user),
                (SQL_CONSTANTS.PYTHON.value.PASSWORD.value, self.password)
            ])
        elif self.client_type == ClientType.JAVA:
            return SQL_CONSTANTS.JAVA.value.PROTOCOL.value + "{}:{};".format(self.server, self.port) + \
                join_segments([
                    (SQL_CONSTANTS.JAVA.value.DATABASE.value, self.database),
                    (SQL_CONSTANTS.JAVA.value.USER.value, self.user),
                    (SQL_CONSTANTS.JAVA.value.PASSWORD.value, self.password),
            ])
        elif self.client_type == ClientType.DOTNET:
            return join_segments([
                (SQL_CONSTANTS.DOTNET.value.SERVER.value, self.server + "," + self.port),
                (SQL_CONSTANTS.DOTNET.value.DATABASE.value, self.database),
                (SQL_CONSTANTS.DOTNET.value.USER.value, self.user),
                (SQL_CONSTANTS.DOTNET.value.PASSWORD.value, self.password)
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
                    (POSTGRESQL_CONSTANTS.JAVA.value.SSL.value, POSTGRESQL_CONSTANTS.JAVA.value.REQUIRE.value)
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

