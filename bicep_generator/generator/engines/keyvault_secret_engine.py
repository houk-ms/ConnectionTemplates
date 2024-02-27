from .secret_engine import SecretEngine
from models.connector import SourceType

class KeyvaultSecretEngine(SecretEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'keyvault secret for {}'.format(self.connector.target_type)

        self.module_params = [
            ('keyVaultName', 'keyVaultName')
        ]

        self.module_symbolic_name = '{}KeyvaultSecretDeployment'.format(self.connector.target_type)
        self.module_bicep_file = 'keyvault.secret.bicep'
        self.module_deployment_name = '{}-keyvault-secret-deployment'.format(self.connector.target_type)


    def set_module_param_secret(self, secretName):
        if self.connector.source_type == 'webapp':
            self.module_params.append(('name', "'{}-secret'".format(self.connector.target_type)))
            self.module_params.append(('secretValue', secretName))


    def set_variables(self):
        if self.connector.source_type == SourceType.WebApp.value:
            self.main_variables.append(('{}SecretReference'.format(self.connector.target_type), '{}.outputs.appServiceSecretRefernece'.format(self.module_symbolic_name)))
        elif self.connector.source_type == SourceType.ContainerApp.value:
            self.main_variables.append(('{}SecretReference'.format(self.connector.target_type), '{}.outputs.containerAppSecretRefernece'.format(self.module_symbolic_name)))