from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.web_pubsub import WebPubSubResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


# Web PubSub network ACL is not for Ip rules
class WebPubSubEngine(TargetResourceEngine):

    WebPubSubContributorRole = 'SignalR/Web PubSub Contributor'

    def __init__(self, resource: WebPubSubResource) -> None:
        super().__init__(Template.WEB_PUBSUB_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.WEB_PUBSUB.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.WEB_PUBSUB.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('web', 'pubsub', self.resource.name, 'id'),
             'azurerm_web_pubsub.{}.id'.format(self.module_name))
        ]

    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_web_pubsub.{}.id'.format(self.module_name),
                WebPubSubEngine.WebPubSubContributorRole)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.KeyValue, 'AZURE_WEBPUBSUB_HOST', 'azurerm_web_pubsub.{}.hostname'.format(self.module_name)),
        ]
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.SecretReference, 'AZURE_WEBPUBSUB_CONNECTIONSTRING', 'azurerm_web_pubsub.{}.primary_connection_string'.format(self.module_name)),
        ]
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]