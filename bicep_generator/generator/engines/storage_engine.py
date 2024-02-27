from models.connector import Connector, AuthType
from .target_engine import TargetEngine


class StorageEngine(TargetEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'Azure Storage Account'

        self.main_params = [
            ('storageAccountName', 'string', "'account${uniqueString(resourceGroup().id)}'", None)
        ]

        self.module_params = [
            ('location', 'location'),
            ('name', 'storageAccountName')
        ]

        self.module_symbolic_name = 'storageAccountDeployment'
        self.module_bicep_file = 'storageaccount.bicep'
        self.module_deployment_name = 'storage-account-deployment'

        self.existing_resource_name = 'storageAccountName'
        self.existing_resource_type = 'Microsoft.Storage/storageAccounts@2023-01-01'
        self.existing_resource_symbolic_name = 'storageAccount'

        self.need_existing_resource = True


    def get_secret_name(self):
        return 'storageConnectionString'


    def get_app_settings(self):
        if self.connector.auth_type == AuthType.Secret.value:
            return [('AZURE_STORAGEACCOUNT_CONNECTIONSTRING', 'storageSecretReference' if self.connector.kv_store else 'storageConnectionString')]
        elif self.connector.auth_type == AuthType.SystemIdentity.value:
            return [('AZURE_STORAGEBLOB_RESOURCEENDPOINT', 'storageBlobEndpoint')]
    
    
    def get_target_resource_id(self):
        return 'storageAccountDeployment.outputs.id'
    

    def set_variables(self):
        if self.connector.auth_type == AuthType.Secret.value:
            self.main_variables.append(('storageConnectionString', 
                """'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};BlobEndpoint=${storageAccount.properties.primaryEndpoints.blob};FileEndpoint=${storageAccount.properties.primaryEndpoints.file};TableEndpoint=${storageAccount.properties.primaryEndpoints.table};QueueEndpoint=${storageAccount.properties.primaryEndpoints.queue};'"""
            ))
        elif self.connector.auth_type == AuthType.SystemIdentity.value:
            self.main_variables.append(('storageBlobEndpoint', 'storageAccount.properties.primaryEndpoints.blob'))