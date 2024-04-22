from azure_iac.bicep_engines.models.template import Template
from azure_iac.bicep_engines.modules.base_resource_engine import BaseResourceEngine

from azure_iac.helpers import string_helper
from azure_iac.helpers.abbrevation import Abbreviation


class ResourceGroupEngine(BaseResourceEngine):
    def __init__(self) -> None:
        super().__init__(Template.RESOURCE_GROUP_BICEP.value,
                         Template.RESOURCE_GROUP_MODULE.value)
        self.resource = None

        # resource.module states and variables
        self.module_name = 'resourceGroup'

        # main.bicep states and variables
        self.main_params = [
            ('location', 'string', 'eastus'),
            ('resourceGroupName', 'string', 'rg-myenv'),
            ('resourceToken', 'string', 'toLower(uniqueString(subscription().id, location, resourceGroupName))', False)
        ]
