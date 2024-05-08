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

# Default configuration names for bindings per target, auth type and client type
# (attr, config_key, is_secret)
CONFIGURATION_NAMES = {
    "ComputeResource": {
		ConnectionType.HTTP: {
			ClientType.PYTHON: [
			    ("request_url", "SERVICE_URL", False),
            ],
            ClientType.NODE: [
                ("request_url", "SERVICE_URL", False),
            ],
            ClientType.JAVA: [
                ("request_url", "SERVICE_URL", False),
            ],
            ClientType.DOTNET: [
                ("request_url", "SERVICE_URL", False),
            ],
            ClientType.DEFAULT: [
               ("request_url", "SERVICE_URL", False),
            ]
		}
	},
    ResourceType.AZURE_APPLICATION_INSIGHTS: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', True)
			],
			ClientType.NODE: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', True)
			],
			ClientType.JAVA: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', True)
			],
			ClientType.DOTNET: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', True)
			],
			ClientType.DEFAULT: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', True)
			]
		},
		ConnectionType.SYSTEMIDENTITY: {
			ClientType.PYTHON: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', False)
			],
			ClientType.NODE: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', False)
			],
			ClientType.JAVA: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', False)
			],
			ClientType.DOTNET: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', False)
			],
			ClientType.DEFAULT: [
				('connection_string', 'APPLICATIONINSIGHTS_CONNECTION_STRING', False)
			]
		}
	},
    ResourceType.AZURE_BOT_SERVICE: {
		ConnectionType.BOTREGISTRATION:{
			ClientType.PYTHON: [
				("bot_id", "BOT_ID", False),
				("bot_password", "BOT_PASSWORD", True),
				("bot_domain", "BOT_DOMAIN", False)
			],
			ClientType.NODE: [
				("bot_id", "BOT_ID", False),
				("bot_password", "BOT_PASSWORD", True),
				("bot_domain", "BOT_DOMAIN", False)
			],
			ClientType.JAVA: [
				("bot_id", "BOT_ID", False),
				("bot_password", "BOT_PASSWORD", True),
				("bot_domain", "BOT_DOMAIN", False)
			],
			ClientType.DOTNET: [
				("bot_id", "BOT_ID", False),
				("bot_password", "BOT_PASSWORD", True),
				("bot_domain", "BOT_DOMAIN", False)
			],
			ClientType.DEFAULT: [
				("bot_id", "BOT_ID", False),
				("bot_password", "BOT_PASSWORD", True),
				("bot_domain", "BOT_DOMAIN", False)
			]
		}
	},
    ResourceType.AZURE_COSMOS_DB: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
                ('connection_string', 'AZURE_COSMOS_CONNECTIONSTRING', True)
            ],
            ClientType.NODE: [
                ('connection_string', 'AZURE_COSMOS_CONNECTIONSTRING', True)
            ],
            ClientType.JAVA: [
                ('connection_string', 'AZURE_COSMOS_CONNECTIONSTRING', True)
            ],
            ClientType.DOTNET: [
                ('connection_string', 'AZURE_COSMOS_CONNECTIONSTRING', True)
            ],
            ClientType.DEFAULT: [
                ('connection_string', 'AZURE_COSMOS_CONNECTIONSTRING', True)
            ]
		},
		ConnectionType.SYSTEMIDENTITY: {
			ClientType.PYTHON: [
			    ("resource_endpoint", "AZURE_COSMOS_RESOURCEENDPOINT", False),
            ],
            ClientType.NODE: [
                ("resource_endpoint", "AZURE_COSMOS_RESOURCEENDPOINT", False),
            ],
            ClientType.JAVA: [
                ("resource_endpoint", "AZURE_COSMOS_RESOURCEENDPOINT", False),
            ],
            ClientType.DOTNET: [
                ("resource_endpoint", "AZURE_COSMOS_RESOURCEENDPOINT", False),
            ],
            ClientType.DEFAULT: [
                ("resource_endpoint", "AZURE_COSMOS_RESOURCEENDPOINT", False),
            ]
        }
	},
    ResourceType.AZURE_KEYVAULT: {
		ConnectionType.SYSTEMIDENTITY: {
			ClientType.PYTHON: [
			    ("resource_endpoint", "AZURE_KEYVAULT_RESOURCEENDPOINT", False),
            ],
            ClientType.NODE: [
                ("resource_endpoint", "AZURE_KEYVAULT_RESOURCEENDPOINT", False),
            ],
            ClientType.JAVA: [
                ("resource_endpoint", "AZURE_KEYVAULT_RESOURCEENDPOINT", False),
            ],
            ClientType.DOTNET: [
                ("resource_endpoint", "AZURE_KEYVAULT_RESOURCEENDPOINT", False),
            ],
            ClientType.DEFAULT: [
                ("resource_endpoint", "AZURE_KEYVAULT_RESOURCEENDPOINT", False),
            ]
		}
	},
    ResourceType.AZURE_REDIS_CACHE: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
                ('connection_string', 'AZURE_REDIS_CONNECTIONSTRING', True)
            ],
            ClientType.NODE: [
                ('connection_string', 'AZURE_REDIS_CONNECTIONSTRING', True)
            ],
            ClientType.JAVA: [
                ('connection_string', 'AZURE_REDIS_CONNECTIONSTRING', True)
            ],
            ClientType.DOTNET: [
                ('connection_string', 'AZURE_REDIS_CONNECTIONSTRING', True)
            ],
            ClientType.DEFAULT: [
                ('host', 'AZURE_REDIS_HOST', False),
				('database', 'AZURE_REDIS_DATABASE', False),
				('password', 'AZURE_REDIS_PASSWORD', True),
				('port', 'AZURE_REDIS_PORT', False),
				('ssl', 'AZURE_REDIS_SSL', False)
            ]
		}
	},
    ResourceType.AZURE_STORAGE_ACCOUNT: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
                ('connection_string', 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING', True)
            ],
            ClientType.NODE: [
                ('connection_string', 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING', True)
            ],
            ClientType.JAVA: [
                ('connection_string', 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING', True)
            ],
            ClientType.DOTNET: [
                ('connection_string', 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING', True)
            ],
            ClientType.DEFAULT: [
                ('connection_string', 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING', True)
            ]
		},
		ConnectionType.SYSTEMIDENTITY: {
			ClientType.PYTHON: [
			    ("blob_endpoint", "AZURE_STORAGEACCOUNT_BLOBENDPOINT", False),
				("table_endpoint", "AZURE_STORAGEACCOUNT_TABLEENDPOINT", False),
				("queue_endpoint", "AZURE_STORAGEACCOUNT_QUEUEENDPOINT", False),
				("file_endpoint", "AZURE_STORAGEACCOUNT_FILEENDPOINT", False),
            ],
            ClientType.NODE: [
                ("blob_endpoint", "AZURE_STORAGEACCOUNT_BLOBENDPOINT", False),
				("table_endpoint", "AZURE_STORAGEACCOUNT_TABLEENDPOINT", False),
				("queue_endpoint", "AZURE_STORAGEACCOUNT_QUEUEENDPOINT", False),
				("file_endpoint", "AZURE_STORAGEACCOUNT_FILEENDPOINT", False),
            ],
            ClientType.JAVA: [
                ("blob_endpoint", "AZURE_STORAGEACCOUNT_BLOBENDPOINT", False),
				("table_endpoint", "AZURE_STORAGEACCOUNT_TABLEENDPOINT", False),
				("queue_endpoint", "AZURE_STORAGEACCOUNT_QUEUEENDPOINT", False),
				("file_endpoint", "AZURE_STORAGEACCOUNT_FILEENDPOINT", False),
            ],
            ClientType.DOTNET: [
                ("blob_endpoint", "AZURE_STORAGEACCOUNT_BLOBENDPOINT", False),
				("table_endpoint", "AZURE_STORAGEACCOUNT_TABLEENDPOINT", False),
				("queue_endpoint", "AZURE_STORAGEACCOUNT_QUEUEENDPOINT", False),
				("file_endpoint", "AZURE_STORAGEACCOUNT_FILEENDPOINT", False),
            ],
            ClientType.DEFAULT: [
                ("blob_endpoint", "AZURE_STORAGEACCOUNT_BLOBENDPOINT", False),
				("table_endpoint", "AZURE_STORAGEACCOUNT_TABLEENDPOINT", False),
				("queue_endpoint", "AZURE_STORAGEACCOUNT_QUEUEENDPOINT", False),
				("file_endpoint", "AZURE_STORAGEACCOUNT_FILEENDPOINT", False),
            ]
        }
    },
    ResourceType.AZURE_SERVICE_BUS: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
                ('connection_string', 'AZURE_SERVICEBUS_CONNECTIONSTRING', True)
            ],
            ClientType.NODE: [
                ('connection_string', 'AZURE_SERVICEBUS_CONNECTIONSTRING', True)
            ],
            ClientType.JAVA: [
                ('connection_string', 'AZURE_SERVICEBUS_CONNECTIONSTRING', True)
            ],
            ClientType.DOTNET: [
                ('connection_string', 'AZURE_SERVICEBUS_CONNECTIONSTRING', True)
            ],
            ClientType.DEFAULT: [
                ('connection_string', 'AZURE_SERVICEBUS_CONNECTIONSTRING', True)
            ]
		},
		ConnectionType.SYSTEMIDENTITY: {
			ClientType.PYTHON: [
			    ("namespace", "AZURE_SERVICEBUS_FULLYQUALIFIEDNAMESPACE", False),
            ],
            ClientType.NODE: [
                ("namespace", "AZURE_SERVICEBUS_FULLYQUALIFIEDNAMESPACE", False),
            ],
            ClientType.JAVA: [
                ("namespace", "AZURE_SERVICEBUS_FULLYQUALIFIEDNAMESPACE", False),
            ],
            ClientType.DOTNET: [
                ("namespace", "AZURE_SERVICEBUS_FULLYQUALIFIEDNAMESPACE", False),
            ],
            ClientType.DEFAULT: [
                ("namespace", "AZURE_SERVICEBUS_FULLYQUALIFIEDNAMESPACE", False),
            ]
        }
	},
	ResourceType.AZURE_SQL_DB: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
				('server', 'AZURE_SQL_SERVER', False),
				('database', 'AZURE_SQL_DATABASE', False),
				('user', 'AZURE_SQL_USER', False),
				('password', 'AZURE_SQL_PASSWORD', True)
			],
			ClientType.NODE: [
				('server', 'AZURE_SQL_SERVER', False),
				('database', 'AZURE_SQL_DATABASE', False),
				('user', 'AZURE_SQL_USERNAME', False),
				('password', 'AZURE_SQL_PASSWORD', True),
				('port', 'AZURE_SQL_PORT', False)
			],
			ClientType.JAVA: [
				('connection_string', "AZURE_SQL_CONNECTIONSTRING", True)
			],
			ClientType.DOTNET: [
				('connection_string', "AZURE_SQL_CONNECTIONSTRING", True)
			],
			ClientType.DEFAULT: [
				('server', 'AZURE_SQL_HOST', False),
				('database', 'AZURE_SQL_DATABASE', False),
				('user', 'AZURE_SQL_USERNAME', False),
				('password', 'AZURE_SQL_PASSWORD', True),
				('port', 'AZURE_SQL_PORT', False)
			]
		}
	},
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
	ResourceType.AZURE_POSTGRESQL_DB: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
				('connection_string', "AZURE_POSTGRESQL_CONNECTIONSTRING", True)
			],
			ClientType.NODE: [
				('server', 'AZURE_POSTGRESQL_HOST', False),
				('database', 'AZURE_POSTGRESQL_DATABASE', False),
				('user', 'AZURE_POSTGRESQL_USER', False),
				('password', 'AZURE_POSTGRESQL_PASSWORD', True),
				('port', 'AZURE_POSTGRESQL_PORT', False),
				('ssl', 'AZURE_POSTGRESQL_SSL', False)
			],
			ClientType.JAVA: [
				('connection_string', "AZURE_POSTGRESQL_CONNECTIONSTRING", True)
			],
			ClientType.DOTNET: [
				('connection_string', "AZURE_POSTGRESQL_CONNECTIONSTRING", True)
			],
			ClientType.DEFAULT: [
				('server', 'AZURE_POSTGRESQL_HOST', False),
				('database', 'AZURE_POSTGRESQL_DATABASE', False),
				('user', 'AZURE_POSTGRESQL_USERNAME', False),
				('password', 'AZURE_POSTGRESQL_PASSWORD', True),
				('port', 'AZURE_POSTGRESQL_PORT', False),
				('ssl', 'AZURE_POSTGRESQL_SSL', False)
			]
		}
	},
	ResourceType.AZURE_OPENAI:{
        ConnectionType.SECRET: {
            ClientType.PYTHON: [
                ('base', 'AZURE_OPENAI_BASE', False),
                ('key', 'AZURE_OPENAI_KEY', True)
            ],
            ClientType.NODE: [
                ('base', 'AZURE_OPENAI_BASE', False),
                ('key', 'AZURE_OPENAI_KEY', True)
            ],
            ClientType.JAVA: [
                ('base', 'AZURE_OPENAI_BASE', False),
                ('key', 'AZURE_OPENAI_KEY', True)
            ],
            ClientType.DOTNET: [
                ('base', 'AZURE_OPENAI_BASE', False),
                ('key', 'AZURE_OPENAI_KEY', True)
            ],
            ClientType.DEFAULT: [
                ('base', 'AZURE_OPENAI_BASE', False),
                ('key', 'AZURE_OPENAI_KEY', True)
            ]
        },
        ConnectionType.SYSTEMIDENTITY: {
            ClientType.PYTHON: [
                ('base', 'AZURE_OPENAI_BASE', False)
            ],
            ClientType.NODE: [
                ('base', 'AZURE_OPENAI_BASE', False)
            ],
            ClientType.JAVA: [
                ('base', 'AZURE_OPENAI_BASE', False)
            ],
            ClientType.DOTNET: [
                ('base', 'AZURE_OPENAI_BASE', False)
            ],
            ClientType.DEFAULT: [
                ('base', 'AZURE_OPENAI_BASE', False)
            ]
        }
	},
    ResourceType.AZURE_WEBPUBSUB: {
		ConnectionType.SECRET: {
			ClientType.PYTHON: [
				('connection_string', 'AZURE_WEBPUBSUB_CONNECTIONSTRING', True)
            ],
			ClientType.NODE: [
				('connection_string', 'AZURE_WEBPUBSUB_CONNECTIONSTRING', True)
            ],
			ClientType.JAVA: [
				('connection_string', 'AZURE_WEBPUBSUB_CONNECTIONSTRING', True)
            ],
			ClientType.DOTNET: [
                ('connection_string', 'AZURE_WEBPUBSUB_CONNECTIONSTRING', True)
            ],
			ClientType.DEFAULT: [
                ('connection_string', 'AZURE_WEBPUBSUB_CONNECTIONSTRING', True)
            ]
        },
		ConnectionType.SYSTEMIDENTITY: {
			ClientType.PYTHON: [
				('host', 'AZURE_WEBPUBSUB_HOST', False),
            ],
			ClientType.NODE: [
				('host', 'AZURE_WEBPUBSUB_HOST', False),
            ],
			ClientType.JAVA: [
				('host', 'AZURE_WEBPUBSUB_HOST', False),
            ],
			ClientType.DOTNET: [
				('host', 'AZURE_WEBPUBSUB_HOST', False),
            ],
			ClientType.DEFAULT: [
				('host', 'AZURE_WEBPUBSUB_HOST', False),
            ]
        }
    }
}
