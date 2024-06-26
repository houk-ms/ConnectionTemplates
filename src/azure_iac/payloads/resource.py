import re
from typing import List
from azure_iac.payloads.models.resource_type import ResourceType
from azure_iac.payloads.resources.aisearch import AISearchResource
from azure_iac.payloads.resources.aiservices import AIServicesResource
from azure_iac.payloads.resources.aks import AKSResource
from azure_iac.payloads.resources.app_service import AppServiceResource
from azure_iac.payloads.resources.application_insights import ApplicationInsightsResource
from azure_iac.payloads.resources.bot_service import BotServiceResource
from azure_iac.payloads.resources.container_app import ContainerAppResource
from azure_iac.payloads.resources.cosmos_db import CosmosDBResource
from azure_iac.payloads.resources.function_app import FunctionAppResource
from azure_iac.payloads.resources.keyvault import KeyVaultResource
from azure_iac.payloads.resources.mysql_db import MySqlDbResource
from azure_iac.payloads.resources.openai import OpenAIResource
from azure_iac.payloads.resources.postgresql_db import PostgreSqlDbResource
from azure_iac.payloads.resources.redis import RedisResource
from azure_iac.payloads.resources.service_bus import ServiceBusResource
from azure_iac.payloads.resources.sql_db import SqlDbResource
from azure_iac.payloads.resources.static_web_app import StaticWebAppResource
from azure_iac.payloads.resources.openai import OpenAIResource
from azure_iac.payloads.resources.web_pubsub import WebPubSubResource
from azure_iac.payloads.resources.storage_account import StorageAccountResource


RESOURCES = {
    ResourceType.AZURE_AI_SEARCH: AISearchResource,
    ResourceType.AZURE_AI_SERVICES: AIServicesResource,
    ResourceType.AZURE_KUBERNETES_SERVICE: AKSResource, 
    ResourceType.AZURE_APP_SERVICE: AppServiceResource,
    ResourceType.AZURE_APPLICATION_INSIGHTS: ApplicationInsightsResource,
    ResourceType.AZURE_BOT_SERVICE: BotServiceResource,
    ResourceType.AZURE_CONTAINER_APP: ContainerAppResource,
    ResourceType.AZURE_COSMOS_DB: CosmosDBResource,
    ResourceType.AZURE_FUNCTION_APP: FunctionAppResource,
    ResourceType.AZURE_KEYVAULT: KeyVaultResource,
    ResourceType.AZURE_OPENAI: OpenAIResource,
    ResourceType.AZURE_POSTGRESQL_DB: PostgreSqlDbResource,
    ResourceType.AZURE_REDIS_CACHE: RedisResource,
    ResourceType.AZURE_SQL_DB: SqlDbResource,
    ResourceType.AZURE_STORAGE_ACCOUNT: StorageAccountResource,
    ResourceType.AZURE_MYSQL_DB: MySqlDbResource,
    ResourceType.AZURE_SERVICE_BUS: ServiceBusResource,
    ResourceType.AZURE_STATIC_WEB_APP: StaticWebAppResource,
    ResourceType.AZURE_OPENAI: OpenAIResource,
    ResourceType.AZURE_WEBPUBSUB: WebPubSubResource,
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
