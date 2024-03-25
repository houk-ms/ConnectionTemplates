from models.connector import AuthType
from .source_engine import SourceEngine

class ContainerAppEngine(SourceEngine):
    def __init__(self, connector):
        super().__init__(connector)

        # base parameters
        self.dependency_bicep_files = ['containerappenv.bicep', 'containerregistry.bicep', 'loganalytics.bicep']
        self.service_brand_name = 'Azure Container App'

        resource_name = self.connector.source_props.get('name') or 'aca'

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

        if resource_name == 'web':
            self.module_depends = "[apiAppDeployment]"

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
        self.main_variables.append(('appSystemIdentityPrinciaplId', '{}.outputs.identityPrincipalId'.format(self.module_symbolic_name)))

    
    def set_variable_outbound_ip(self):
        self.main_variables.append(('outboundIps', "{}.outputs.outboundIps".format(self.module_symbolic_name)))
    
    def set_module_param_app_settings(self, app_settings):
        app_settings_template = ''
        for key, value in app_settings:
            app_settings_template += (self.app_settings_template.format(key=key, value=value).strip() + ',')
        app_settings_template = '[{}]'.format(app_settings_template.strip(',').strip())
        self.module_params.append(('containerEnv', app_settings_template))