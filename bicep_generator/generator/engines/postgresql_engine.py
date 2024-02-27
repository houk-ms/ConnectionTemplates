from models.connector import Connector, AuthType
from .target_engine import TargetEngine


class PostgresqlEngine(TargetEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'Azure Database for PostgreSQL'

        self.main_params = [
            ('serverName', 'string', "'postgresql-${uniqueString(resourceGroup().id)}'", None),
            ('databaseName', 'string', "'database_${uniqueString(resourceGroup().id)}'", None),
            ('adminName', 'string', "'administrator_${uniqueString(resourceGroup().id)}'", None),
            ('adminPassword', 'string', "'Aa0!${newGuid()}'", "@secure()"),
        ]

        self.module_params = [
            ('location', 'location'),
            ('serverName', 'serverName'),
            ('databaseName', 'databaseName'),
            ('adminName', 'adminName'),
            ('adminPassword', 'adminPassword'),
        ]

        self.module_symbolic_name = 'postgresqlDeployment'
        self.module_bicep_file = 'postgresql.bicep'
        self.module_deployment_name = 'postgresql-deployment'

        self.existing_resource_name = 'serverName'
        self.existing_resource_type = 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01'
        self.existing_resource_symbolic_name = 'postgresql'


    def get_app_settings(self):
        if self.connector.auth_type == AuthType.Secret.value:
            return [('AZURE_POSTGRESQL_CONNECTIONSTRING', 'postgresqlConnectionString')]
    
    
    def get_target_resource_id(self):
        return 'postgresqlDeployment.outputs.databaseId'
    

    def set_variables(self):
        if self.connector.auth_type == AuthType.Secret.value:
            self.main_variables.append(('postgresqlConnectionString',
                "'dbname=${databaseName} host=${serverName}.postgres.database.azure.com port=5432 sslmode=require user=${adminName} password=${adminPassword}'"
            ))