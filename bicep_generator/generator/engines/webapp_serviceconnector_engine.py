from .base_engine import BaseEngine
from models.connector import AuthType

class WebAppServiceConnectorEngine(BaseEngine):
    def __init__(self, connector):
        super().__init__(connector)

        # base parameters
        self.service_brand_name = 'Azure Service Connector'

        self.main_params = [
            ('{}ConnectorName'.format(self.connector.target_type), 'string', "'connector_${uniqueString(resourceGroup().id)}'", None)
        ]
        self.module_params = [
            ('webAppName', 'webAppName'),
            ('name', '{}ConnectorName'.format(self.connector.target_type)),
            ('authType', "'systemAssignedIdentity'" if self.connector.auth_type == AuthType.SystemIdentity.value else "'secret'")
        ]
        self.module_symbolic_name = '{}ConnectorDeployment'.format(self.connector.target_type)
        self.module_bicep_file = 'webapp.serviceconnector.bicep'
        self.module_deployment_name = '{}-service-connector-deployment'.format(self.connector.target_type)



    def generate_module(self, target_resource_id):
        self.module_params.append(('targetResourceId', target_resource_id))
        return super().generate_module()
