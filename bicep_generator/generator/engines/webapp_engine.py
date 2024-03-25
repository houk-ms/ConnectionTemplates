from models.connector import AuthType
from .source_engine import SourceEngine

class WebAppEngine(SourceEngine):
    def __init__(self, connector):
        super().__init__(connector)

        # base parameters
        self.dependency_bicep_files = ['appserviceplan.bicep']
        self.service_brand_name = 'Azure WebApp'

        self.main_params = [
            ('location', 'string', 'resourceGroup().location', None),
            ('webAppName', 'string', "'webapp-${uniqueString(resourceGroup().id)}'", None)
        ]
        self.module_params = [
            ('location', 'location'),
            ('name', 'webAppName')
        ]

        self.module_symbolic_name = 'appServiceDeployment'
        self.module_bicep_file = 'webapp.bicep'
        self.module_deployment_name = 'app-service-deployment'

        self.app_settings_template = \
"""「
            name: '{key}'
            value: {value}
        」
"""

    def get_principal_id(self):
        return 'appSystemIdentityPrinciaplId'
    

    def get_outbound_ip(self):
        return 'outboundIps'


    def set_variable_principal_id(self):
        self.main_variables.append(('appSystemIdentityPrinciaplId', 'appServiceDeployment.outputs.identityPrincipalId'))

    
    def set_variable_outbound_ip(self):
        self.main_variables.append(('outboundIps', "split(appServiceDeployment.outputs.outboundIps, ',')"))
    
    def set_module_param_app_settings(self, app_settings):
        app_settings_template = ''
        for key, value in app_settings:
            app_settings_template += (self.app_settings_template.format(key=key, value=value).strip() + ',')
        app_settings_template = '[{}]'.format(app_settings_template.strip(',').strip())
        self.module_params.append(('appSettings', app_settings_template))