import re
from typing import List
from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.app_service import AppServiceResource
from azure_iac.payloads.resources.application_insights import ApplicationInsightsResource
from azure_iac.payloads.resources.container_app import ContainerAppResource
from azure_iac.payloads.resources.cosmos_db import CosmosDBResource
from azure_iac.payloads.resources.function_app import FunctionAppResource
from azure_iac.payloads.resources.keyvault import KeyVaultResource
from azure_iac.payloads.resources.postgresql_db import PostgreSqlDbResource
from azure_iac.payloads.resources.redis import RedisResource
from azure_iac.payloads.resources.spring_app import SpringAppResource
from azure_iac.payloads.resources.sql_db import SqlDbResource
from azure_iac.payloads.resources.storage_account import StorageAccountResource
from azure_iac.payloads.resources.mysql_db import MySqlDbResource


RESOURCES = {
    ResourceType.AZURE_APP_SERVICE: AppServiceResource,
    ResourceType.AZURE_APPLICATION_INSIGHTS: ApplicationInsightsResource,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppResource,
    ResourceType.AZURE_COSMOS_DB: CosmosDBResource,
    ResourceType.AZURE_FUNCTION_APP: FunctionAppResource,
    ResourceType.AZURE_KEYVAULT: KeyVaultResource,
    ResourceType.AZURE_POSTGRESQL_DB: PostgreSqlDbResource,
    ResourceType.AZURE_REDIS_CACHE: RedisResource,
    ResourceType.AZURE_SQL_DB: SqlDbResource,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountResource,
    ResourceType.AZURE_MYSQL_DB: MySqlDbResource
}


class Resource():
    def from_json(json: dict) -> List['Resource']:
        if 'type' not in json:
            raise ValueError(f'`type` is not found for resource: {json}')

        resource = RESOURCES[json['type']]
        if 'instances' not in json:
            # single resource instance
            return [resource()]
        
        # multiple resource instances
        return [resource.from_json(json) for json in json.get('instances', [])]

    
    def from_expression(expression: str, all_resources: dict) -> 'Resource':
        # two expressions are supported: '${resource_type}' or '${resource_type.resource_name}'
        pattern = r'\$\{(.*?)\}'
        match = re.search(pattern, expression)
        if not match:
            raise ValueError(f'Invalid expression: {expression}. ' + 
                             'Supported expressions are: ${resource_type} or ${resource_type.resource_name}')

        if match.group(1) not in all_resources:
            raise ValueError(f'Resource not found: {expression}')

        return all_resources[match.group(1)]
