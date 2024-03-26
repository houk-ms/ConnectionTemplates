import re
from typing import List
from payloads.models.resource_type import ResourceType
from payloads.resources.app_service import AppServiceResource
from payloads.resources.application_insights import ApplicationInsightsResource
from payloads.resources.container_app import ContainerAppResource
from payloads.resources.cosmos_db import CosmosDBResource
from payloads.resources.function_app import FunctionAppResource
from payloads.resources.keyvault import KeyVaultResource
from payloads.resources.postgresql_db import PostgreSqlDbResource
from payloads.resources.redis import RedisResource
from payloads.resources.spring_app import SpringAppResource
from payloads.resources.sql_db import SqlDbResource
from payloads.resources.storage_account import StorageAccountResource


RESOURCES = {
    ResourceType.AZURE_APP_SERVICE: AppServiceResource,
    ResourceType.AZURE_APPLICATION_INSIGHTS: ApplicationInsightsResource,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppResource,
    ResourceType.AZURE_COSMOS_DB: CosmosDBResource,
    ResourceType.AZURE_FUNCTION_APP: FunctionAppResource,
    ResourceType.AZURE_KEYVAULT: KeyVaultResource,
    ResourceType.AZURE_POSTGRESQL_DB: PostgreSqlDbResource,
    ResourceType.AZURE_REDIS_CACHE: RedisResource,
    ResourceType.AZURE_SPRING_APP: SpringAppResource,
    ResourceType.AZURE_SQL_DB: SqlDbResource,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountResource
}


class Resource():
    def from_json(json: dict) -> List['Resource']:
        if 'type' not in json:
            raise ValueError(f'`type` is not found for resource: {json}')

        resource = RESOURCES[json['type']]
        return [resource.from_json(json) for json in json['instances']]
    
    def from_expression(expression: dict, all_resources: dict) -> 'Resource':
        # two expressions are supported: '${resource_type}' or '${resource_type.resource_name}'
        pattern = r'\$\{(.*?)\}'
        match = re.search(pattern, expression)
        if not match:
            raise ValueError(f'Invalid expression: {expression}. ' + 
                             'Supported expressions are: ${resource_type} or ${resource_type.resource_name}')

        if match.group(1) not in all_resources:
            raise ValueError(f'Resource not found: {expression}')

        return all_resources[match.group(1)]