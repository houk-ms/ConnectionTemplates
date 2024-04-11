from typing import List
from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.bot_service import BotServiceResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation



class BotServiceEngine(TargetResourceEngine):

    StorageDataReaderAccessRole = 'Reader and Data Access'

    def __init__(self, resource: BotServiceResource) -> None:
        super().__init__(Template.BOT_SERVICE_TF.value)
        self.resource = resource

        # main.tf variables
        self.main_var_botaadappclientid = 'bot_aad_app_client_id'
        self.main_var_botaadappclientsecret = 'bot_aad_app_client_secret'

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.BOT_SERVICE.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.BOT_SERVICE.value) + '${var.resource_suffix}'
        self.module_params_microsoft_app_id = '${var.' + self.main_var_botaadappclientid + '}'
        self.module_params_endpoint = 'example.com'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('bot', 'service', self.resource.name, 'id'), 
                'azurerm_bot_channels_registration.{}.id'.format(self.module_name))
        ]


    def set_endpoint(self, endpoint: str) -> None:
        self.module_params_endpoint = endpoint

        # extra variables needed when binding with compute service
        self.main_variables.extend([
            (self.main_var_botaadappclientid, None),
            (self.main_var_botaadappclientsecret, None),
        ])


    def get_app_settings_bot(self, binding: Binding) -> List[AppSetting]:
        bot_app_settings = {
            'BOT_ID': '"${var.' + self.main_var_botaadappclientid + '}"',
            'BOT_PASSWORD': '"${var.' + self.main_var_botaadappclientsecret + '}"',
            'BOT_DOMAIN': '"' + self.module_params_endpoint + '"',
        }
        
        return [AppSetting(AppSettingType.KeyValue, key, value) for key, value in bot_app_settings.items()]