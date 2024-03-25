from models.connector import Connector, AuthType
from .target_engine import TargetEngine


class ContainerAppTargetEngine(TargetEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'Azure Container App'

        resource_name = self.connector.target_props.get('name')
        
        self.main_params = [
            ('{}AppName'.format(resource_name), 'string', "'{}".format(resource_name) + "-${uniqueString(resourceGroup().id)}'", None)
        ]

        self.module_params = [
            ('location', 'location'),
            ('name', '{}AppName'.format(resource_name))
        ]
        self.module_symbolic_name = '{}AppDeployment'.format(resource_name.lower())
        self.module_bicep_file = 'containerapp.bicep'
        self.module_deployment_name = '{}-app-deployment'.format(resource_name.lower())


    def get_app_settings(self):
        conn_key_name = self.connector.target_props.get('key')
        if self.connector.auth_type == AuthType.Http.value:
            return [(conn_key_name if conn_key_name else 'SERVICE_URL', '{}.outputs.fqdn'.format(self.module_symbolic_name))]
    
    def set_variables(self):
        pass