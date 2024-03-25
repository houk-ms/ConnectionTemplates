from payloads.models.resource_type import ResourceType
from payloads.resources.app_service import AppServiceResource
from payloads.resources.application_insights import ApplicationInsightsResource
from payloads.resources.container_app import ContainerAppResource
from payloads.resources.cosmos_db import CosmosDBResource
from payloads.resources.function_app import FunctionAppResource
from payloads.resources.keyvault import KeyVaultResource
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
    ResourceType.AZURE_SPRING_APP: SpringAppResource,
    ResourceType.AZURE_SQL_DB: SqlDbResource,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountResource
}


class Resource():
    def from_json(json):
        resource = RESOURCES[json['type']]
        return [resource.from_json(json) for json in json['instances']]
    
    def from_expression(expression, resources):
        # expression is like '${resource_type.resource_name}'
        if expression is None:
            return None
        
        expression = expression.replace('${', '').replace('}', '')
        pieces = expression.split('.')
        if len(pieces) != 2:
            raise Exception(f'Invalid resource expression: {expression}')
        resource_type, resource_name = ResourceType(pieces[0]), pieces[1]
        
        for resource in resources:
            if resource.type == resource_type and resource.name == resource_name:
                return resource
        return None