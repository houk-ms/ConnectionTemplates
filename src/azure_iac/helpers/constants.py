from enum import Enum

from azure_iac.payloads.models.connection_type import ConnectionType
from azure_iac.payloads.models.resource_type import ResourceType

class ClientType(str, Enum):
	NODE = "node"
	PYTHON = "python"
	JAVA = "java"
	DOTNET = "dotnet"
	DEFAULT = "none"

class POSTGRESQL_CONSTANTS_DOTNET(Enum):
	SERVER = "Server"
	DATABASE = "Database"
	PORT = "Port"
	USER = "User Id"
	PASSWORD = "Password"
	SSL = "Ssl Mode"

	REQUIRE = "Require"

class POSTGRESQL_CONSTANTS_PYTHON(Enum):
	SERVER = "host"
	DATABASE = "dbname"
	PORT = "port"
	USER = "user"
	PASSWORD = "password"
	SSL = "sslmode"
	
	REQUIRE = "require"

class POSTGRESQL_CONSTANTS_JDBC(Enum):
	PROTOCOL = "jdbc:postgresql://"
	USER = "user"
	PASSWORD = "password"
	SSL = "sslmode"

	REQUIRE = "require"

class POSTGRESQL_CONSTANTS(Enum):
	PYTHON = POSTGRESQL_CONSTANTS_PYTHON
	DOTNET = POSTGRESQL_CONSTANTS_DOTNET
	JAVA = POSTGRESQL_CONSTANTS_JDBC

class MYSQL_CONSTANTS_DOTNET(Enum):
	SERVER = "Server"
	DATABASE = "Database"
	USER = "User Id"
	PORT = "Port"
	PASSWORD = "Password"
	SSL = "SSL Mode"

	REQUIRE = "Required"

class MYSQL_CONSTANTS_JAVA(Enum):
	PROTOCOL = "jdbc:mysql://"
	USER = "user"
	PASSWORD = "password"
	SSL = "sslmode"
	SERVERTIMEZONE = "serverTimezone"

	REQUIRE = "required"
	UTC = "UTC"

class MYSQL_CONSTANTS(Enum):
	DOTNET = MYSQL_CONSTANTS_DOTNET
	JAVA = MYSQL_CONSTANTS_JAVA

class SQL_CONSTANTS_DOTNET(Enum):
	SERVER = "Data Source"
	DATABASE = "Initial Catalog"
	USER = "User ID"
	PASSWORD = "Password"

class SQL_CONSTANTS_JAVA(Enum):
	PROTOCOL = "jdbc:sqlserver://"
	USER = "user"
	PASSWORD = "password"
	DATABASE = "database"

class SQL_CONSTANTS_PYTHON(Enum):
	DRIVER = "Driver"
	SERVER = "Server"
	DATABASE = "Database"
	USER = "UiD"
	PASSWORD = "Pwd"

class SQL_CONSTANTS(Enum):
	DOTNET = SQL_CONSTANTS_DOTNET
	JAVA = SQL_CONSTANTS_JAVA
	PYTHON = SQL_CONSTANTS_PYTHON

# Default configuration names for bindings per target, auth type and client type
# (attr, config_key, is_secret)
CONFIGURATION_NAMES = {
	ResourceType.AZURE_APP_SERVICE: {},
    ResourceType.AZURE_APPLICATION_INSIGHTS: {},
    ResourceType.AZURE_BOT_SERVICE: {},
    ResourceType.AZURE_CONTAINER_APP: {},
    ResourceType.AZURE_COSMOS_DB: {},
    ResourceType.AZURE_FUNCTION_APP: {},
    ResourceType.AZURE_KEYVAULT: {},
    ResourceType.AZURE_REDIS_CACHE: {},
	ResourceType.AZURE_STORAGE_ACCOUNT: {},
    ResourceType.AZURE_SERVICE_BUS: {},
    ResourceType.AZURE_STATIC_WEB_APP: {},
	ResourceType.AZURE_SQL_DB: {},
    ResourceType.AZURE_MYSQL_DB: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
				('server', 'AZURE_MYSQL_HOST', False),
				('database', 'AZURE_MYSQL_DATABASE', False),
				('user', 'AZURE_MYSQL_USER', False),
				('password', 'AZURE_MYSQL_PASSWORD', True)
			],
			ClientType.NODE: [
				('server', 'AZURE_MYSQL_HOST', False),
				('database', 'AZURE_MYSQL_DATABASE', False),
				('user', 'AZURE_MYSQL_USER', False),
				('password', 'AZURE_MYSQL_PASSWORD', True),
				('port', 'AZURE_MYSQL_PORT', False),
				('ssl', 'AZURE_MYSQL_SSL', False)
			],
			ClientType.JAVA: [
				('connection_string', "AZURE_MYSQL_CONNECTIONSTRING", True)
			],
			ClientType.DOTNET: [
				('connection_string', "AZURE_MYSQL_CONNECTIONSTRING", True)
			],
			ClientType.DEFAULT: [
				('server', 'AZURE_MYSQL_HOST', False),
				('database', 'AZURE_MYSQL_DATABASE', False),
				('user', 'AZURE_MYSQL_USER', False),
				('password', 'AZURE_MYSQL_PASSWORD', True),
				('port', 'AZURE_MYSQL_PORT', False),
				('ssl', 'AZURE_MYSQL_SSL', False)
			]
		}
	},
	ResourceType.AZURE_POSTGRESQL_DB: {},
}
