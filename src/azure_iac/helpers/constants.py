from enum import Enum

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
	AUTHENTICATION = "Authentication"

	AUTHPWD = "Active Directory Password"

class SQL_CONSTANTS_JAVA(Enum):
	PROTOCOL = "jdbc:sqlserver://"
	USER = "user"
	PASSWORD = "password"
	DATABASE = "database"
	AUTHENTICATION = "authentication"

	AUTHPWD = "ActiveDirectoryPassword"

class SQL_CONSTANTS_PYTHON(Enum):
	DRIVER = "Driver"
	SERVER = "Server"
	DATABASE = "Database"
	USER = "UiD"
	PASSWORD = "Pwd"
	AUTHENTICATION = "Authentication"

	AUTHPWD = "ActiveDirectoryPassword"

class SQL_CONSTANTS(Enum):
	DOTNET = SQL_CONSTANTS_DOTNET
	JAVA = SQL_CONSTANTS_JAVA
	PYTHON = SQL_CONSTANTS_PYTHON
