from typing import List

from azure_iac.helpers.connection_info import WebPubSubConnInfoHelper
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.web_pubsub import WebPubSubResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class WebPubSubEngine(TargetResourceEngine):

    def __init__(self, resource: WebPubSubResource) -> None:
        super().__init__(Template.WEBPUBSUB_BICEP.value,
                         Template.WEBPUBSUB_MODULE.value)
        self.resource = resource

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('webPubSub', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('webpubsub', self.resource.name)
        self.module_params_name = string_helper.format_camel('webPubSub', self.resource.name, "Name")
        self.module_params_secret_name = string_helper.format_kv_secret_name('webpubsub', self.resource.name)
        
        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', string_helper.get_location(), False),
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.WEB_PUBSUB.value)),
        ]
        self.main_outputs = [
            (string_helper.format_camel('webpubsub', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        connInfoHelper = WebPubSubConnInfoHelper("" if binding.source.service is None else binding.source.service.language,
                                                 connection_string=None,
                                                 host='{}.outputs.hostName'.format(self.module_name)
                                                )
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection)
        return self._get_app_settings(configs)
    
    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        # TODO: support key names for multiple targets of same type
        connInfoHelper = WebPubSubConnInfoHelper("" if binding.source.service is None else binding.source.service.language,
                                                 connection_string=''  # get in template
                                                )
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection)
        
        return self._get_app_settings(configs)
