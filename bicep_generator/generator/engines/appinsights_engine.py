from models.connector import Connector, AuthType
from .target_engine import TargetEngine


class AppInsightsEngine(TargetEngine):
    def __init__(self, connector):
        super().__init__(connector)
        self.service_brand_name = 'Azure Application Insights'

        resource_name = self.connector.target_props.get('name') or 'insights'

        self.main_params = [
            ('appInsightsName', 'string', "'{}".format(resource_name) + "-${uniqueString(resourceGroup().id)}'", None)
        ]

        self.module_params = [
            ('location', 'location'),
            ('name', 'appInsightsName')
        ]

        self.module_symbolic_name = 'appInsightsDeployment'
        self.module_bicep_file = 'appinsights.bicep'
        self.module_deployment_name = 'appinsights-deployment'

        self.existing_resource_name = 'appInsightsName'
        self.existing_resource_type = 'Microsoft.Insights/components@2020-02-02'
        self.existing_resource_symbolic_name = 'appInsights'

        self.need_existing_resource = True


    def get_secret_name(self):
        return 'appInsightsConnectionString'


    def get_app_settings(self):
        conn_key_name = self.connector.target_props.get('key')
        if self.connector.auth_type == AuthType.Secret.value:
            return [(conn_key_name if conn_key_name else 'AZURE_APPINSIGHTS_CONNECTIONSTRING', 'appInsightsConnectionString')]
    

    def get_target_resource_id(self):
        return 'appInsightsDeployment.outputs.id'
    

    def set_variables(self):
        if self.connector.auth_type == AuthType.Secret.value:
            self.main_variables.append(('appInsightsConnectionString', 
                """appInsights.properties.ConnectionString"""
            ))