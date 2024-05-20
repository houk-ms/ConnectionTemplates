from typing import List

from azure_iac.helpers.connection_info import BotConnInfoHelper
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.bot_service import BotServiceResource

from azure_iac.bicep_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class BotServiceEngine(TargetResourceEngine):

    def __init__(self, resource: BotServiceResource) -> None:
        super().__init__(Template.BOT_SERVICE_BICEP.value,
                         Template.BOT_SERVICE_MODULE.value)
        self.resource = resource

        # main.bicep states and variables
        self.main_var_botaadappclientid = 'botAadAppClientId'
        self.main_var_botaadappclientsecret = 'botAadAppClientSecret'

        # resource.module states and variables
        self.module_name = string_helper.format_module_name('bot', self.resource.name)
        self.module_deployment_name = string_helper.format_deployment_name('bot', self.resource.name)
        self.module_params_name = string_helper.format_camel('bot', self.resource.name, "Name")
        self.module_params_botaadappclientid = self.main_var_botaadappclientid
        
        # main.bicep states and variables
        self.main_params = [
            (self.module_params_name, 'string', 
                string_helper.format_resource_name(self.resource.name or Abbreviation.BOT_SERVICE.value)),
            (self.main_var_botaadappclientid, 'string', None, False),
        ]
        self.main_outputs = [
            (string_helper.format_camel('bot', self.resource.name, "Id"), 
             'string', '{}.outputs.id'.format(self.module_name))]


    def set_endpoint(self, endpoint: str) -> None:
        self.module_params_botappdomain = endpoint

        # extra variables needed when binding with compute service
        self.main_params.extend([
            (self.main_var_botaadappclientsecret, 'string', None, False, True),
        ])


    def get_app_settings_bot(self, binding: Binding) -> List[AppSetting]:
        if binding.store:
            print('Warning: IaC generator does not support secret store for Bot Service.')
        
        connInfoHelper = BotConnInfoHelper("" if binding.source.service is None else binding.source.service.language,
                                           bot_id=self.main_var_botaadappclientid,
                                           bot_password=self.main_var_botaadappclientsecret,
                                           bot_domain=self.module_params_botappdomain)
        configs = connInfoHelper.get_configs({} if binding.customKeys is None else binding.customKeys,
                                             binding.connection)
        
        app_settings = []
        for app_setting_key, value, _ in configs:
            app_settings.append(
                AppSetting(AppSettingType.KeyValue, app_setting_key, value)
            )
        return app_settings
