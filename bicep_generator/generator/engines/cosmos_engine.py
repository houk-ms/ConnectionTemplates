from models.connector import Connector, AuthType
from .target_engine import TargetEngine


class CosmosEngine(TargetEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'Azure Cosmos Mongo DB'

        resource_name = self.connector.target_props.get('name') or 'database'
        resource_server = self.connector.target_props.get('server') or 'cosmos'

        self.main_params = [
            ('databaseName', 'string', "'{}".format(resource_name) + "-${uniqueString(resourceGroup().id)}'", None),
            ('accountName', 'string', "'{}".format(resource_server) + "-${uniqueString(resourceGroup().id)}'", None)
        ]

        self.module_params =  [
            ('location', 'location'),
            ('accountName', 'accountName'),
            ('databaseName', 'databaseName'),
        ]

        self.module_symbolic_name = 'cosmosDeployment'
        self.module_bicep_file = 'cosmos.bicep'
        self.module_deployment_name = 'cosmos-deployment'

        self.existing_resource_name = 'accountName'
        self.existing_resource_type = 'Microsoft.DocumentDB/databaseAccounts@2023-11-15'
        self.existing_resource_symbolic_name = 'cosmos'

        self.need_existing_resource = True

    def get_secret_name(self):
        return 'cosmosConnectionString'

    def get_app_settings(self):
        conn_key_name = self.connector.target_props.get('key')
        if self.connector.auth_type == AuthType.Secret.value:
            return [(conn_key_name if conn_key_name else 'AZURE_COSMOSDB_CONNECTIONSTRING', 'cosmosSecretReference' if self.connector.kv_store else 'cosmosConnectionString')]
    
    
    def get_target_resource_id(self):
        return 'cosmosDeployment.outputs.databaseId'
    

    def set_variables(self):
        if self.connector.auth_type == AuthType.Secret.value:
            self.main_variables.append(('cosmosConnectionString',
                "cosmos.listConnectionStrings().connectionStrings[0].connectionString"
            ))