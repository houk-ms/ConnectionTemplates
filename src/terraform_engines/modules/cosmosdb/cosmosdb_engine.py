from typing import List
from payloads.binding import Binding
from payloads.resources.cosmos_db import CosmosDBResource

from terraform_engines.models.template import Template
from terraform_engines.models.appsetting import AppSetting, AppSettingType
from terraform_engines.modules.target_resource_engine import TargetResourceEngine

from helpers import string_helper
from helpers.abbrevation import Abbreviation


# TODO: enable firewall when creating resource
class CosmosDbEngine(TargetResourceEngine):

    CosmosAccountContributorRole = 'DocumentDB Account Contributor'

    def __init__(self, resource: CosmosDBResource) -> None:
        super().__init__(Template.COSMOS_DB_TF.value)
        self.resource = resource

        # resource module states and variables
        self.module_name = string_helper.format_snake(Abbreviation.COSMOS_DB.value, self.resource.name)
        self.module_params_name = (self.resource.name or Abbreviation.COSMOS_DB.value) + '${var.resource_suffix}'
        
        # main.tf variables and outputs
        self.main_outputs = [
            (string_helper.format_snake('cosmos', 'account', self.resource.name, 'id'), 
                'azurerm_cosmosdb_account.{}.id'.format(self.module_name))
        ]


    # return the current resource scope and role for role assignment
    def get_role_scope(self) -> tuple:
        return ('azurerm_cosmosdb_account.{}.id'.format(self.module_name),
                CosmosDbEngine.CosmosAccountContributorRole)

    # return the app settings needed by identity connection
    def get_app_settings_identity(self, binding: Binding) -> List[tuple]:
        return [
            AppSetting(AppSettingType.KeyValue, 'AZURE_COSMOS_RESOURCEENDPOINT', 
                       'azurerm_cosmosdb_account.{}.endpoint'.format(self.module_name))
        ]

    # return the app settings needed by secret connection
    def get_app_settings_secret(self, binding: Binding) -> List[tuple]:
        app_setting_key = binding.key if binding.key else 'AZURE_COSMOS_CONNECTIONSTRING'

        if binding.store is not None:
            return [
                AppSetting(AppSettingType.KeyVaultReference, app_setting_key, 
					'azurerm_cosmosdb_account.{}.primary_mongodb_connection_string'.format(self.module_name))
			]

        return [
            AppSetting(AppSettingType.SecretReference, app_setting_key, 
                'azurerm_cosmosdb_account.{}.primary_mongodb_connection_string'.format(self.module_name))
        ]