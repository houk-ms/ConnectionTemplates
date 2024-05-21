from typing import List

from azure_iac.payloads.binding import Binding
from azure_iac.payloads.resources.service_bus import ServiceBusResource

from azure_iac.terraform_engines.models.template import Template
from azure_iac.terraform_engines.models.appsetting import AppSetting, AppSettingType
from azure_iac.terraform_engines.modules.target_resource_engine import TargetResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation

# TODO: queue and topic
class ServiceBusEngine(TargetResourceEngine):

    ServiceBusDataOwnerRole = 'Azure Service Bus Data Owner'
    ServiceBusDataReceiverRole = 'Azure Service Bus Data Receiver'
    ServiceBusDataSenderRole = 'Azure Service Bus Data Sender'

    def __init__(self, resource: ServiceBusResource) -> None:
        super().__init__(Template.SERVICE_BUS_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.SERVICE_BUS.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.SERVICE_BUS.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('service', 'bus', self.resource.name, 'id'), 
                'azurerm_servicebus_namespace.{}.id'.format(self.module_name)),
            (string_helper.format_snake('service', 'bus', 'queue', self.resource.name, 'id'), 
                'azurerm_servicebus_queue.{}queue.id'.format(self.module_name))
        ]

    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_servicebus_namespace.{}.id'.format(self.module_name),
                ServiceBusEngine.ServiceBusDataOwnerRole)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.KeyValue, 'AZURE_SERVICEBUS_FULLYQUALIFIEDNAMESPACE', 'azurerm_servicebus_namespace.{}.endpoint'.format(self.module_name)),
        ]
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        custom_keys = dict() if binding.customKeys is None else binding.customKeys
        default_settings = [
            (AppSettingType.SecretReference, 'AZURE_SERVICEBUS_CONNECTIONSTRING', 'azurerm_servicebus_namespace.{}.default_primary_connection_string'.format(self.module_name)),
        ]
        return [AppSetting(_type, custom_keys.get(key, key), value) for _type, key, value in default_settings]
