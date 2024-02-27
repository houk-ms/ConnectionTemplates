from models.connector import AuthType
from .target_engine import TargetEngine


class KeyvaultEngine(TargetEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'Azure Keyvault'

        self.main_params = [
            ('keyVaultName', 'string', "'vault-${uniqueString(resourceGroup().id)}'", None)
        ]

        self.module_params = [
            ('location', 'location'),
            ('name', 'keyVaultName')
        ]

        self.module_symbolic_name = 'keyvaultDeployment'
        self.module_bicep_file = 'keyvault.bicep'
        self.module_deployment_name = 'keyvault-deployment'


    def get_app_settings(self):
        if self.connector.auth_type == AuthType.SystemIdentity.value:
            return [
                ('AZURE_KEYVAULT_RESOURCEENDPOINT', 'keyvaultEndpoint'),
                ('AZURE_KEYVAULT_SCOPE', 'keyvaultScope')
            ]
        elif self.connector.auth_type == AuthType.UserIdentity.value:
            return [
                ('AZURE_KEYVAULT_RESOURCEENDPOINT', 'keyvaultEndpoint'),
                ('AZURE_KEYVAULT_SCOPE', 'keyvaultScope'),
                ('AZURE_KEYVAULT_CLIENTID', 'userMIClientId'),
            ]
        else:
            raise NotImplemented('Unexpected code path!')
    
    
    def get_target_resource_id(self):
        return 'keyvaultDeployment.outputs.id'
    

    def set_variables(self):
        if self.connector.auth_type == AuthType.SystemIdentity.value:
            self.main_variables.append(('keyvaultEndpoint', 'keyvaultDeployment.outputs.endpoint'))
            self.main_variables.append(('keyvaultScope', 'keyvaultDeployment.outputs.scope'))
