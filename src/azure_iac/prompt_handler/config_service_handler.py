import json
import os
from openai import AzureOpenAI
from azure_iac.payloads.models.resource_type import ResourceType

DB_RESOURCES = [ResourceType.AZURE_SQL_DB.value, ResourceType.AZURE_POSTGRESQL_DB.value, ResourceType.AZURE_MYSQL_DB.value]
COMPUTE_RESOURCES = [ResourceType.AZURE_APP_SERVICE.value, ResourceType.AZURE_CONTAINER_APP.value, ResourceType.AZURE_FUNCTION_APP.value, ResourceType.AZURE_STATIC_WEB_APP.value]

class ConfigServiceHandler:
    def __init__(self):
        self.OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
        self.OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
        self.client = AzureOpenAI(
            azure_endpoint=self.OPENAI_ENDPOINT, 
            api_key=self.OPENAI_API_KEY,  
            api_version="2024-02-01"
        )

    def configure_resources(self, message: str):
        response = self.client.chat.completions.create(
            model="gpt4",
            messages=[
                {"role": "system", "content": "You are an assistant that knows about Azure resources and services.\
                                                Your job is to determine what Azure services are needed from either app architecture or infrastructure design.\
                                                \
                                                [Response Rules]\
                                                1. Response with a table of Azure resources and their amounts in the following format:\
                                                    | Resource Type                     | Amount      |\
                                                    | ----------------------------------|-------------|\
                                                    | Azure resource type               | number      |\
                                                    | ...                               | ...         |\
                                                2. Do not contain ANY OTHER words except the table.\
                                                3. Use the most similar resource type name from below:\
                                                    Azure App Service, Azure Container Apps, Azure Static Web Apps, Azure Functions,\
                                                    Azure Cosmos DB, Azure Storage Account,\
                                                    Azure SQL DB, Azure PostgreSQL DB, Azure MySQL DB,\
                                                    Azure Service Bus, Azure Key Vault, Azure Cache for Redis,\
                                                    Azure Web PubSub, Azure OpenAI Service, Azure AI Services, Azure AI Search,\
                                                    Azure Application Insights, Azure Bot Service\
                                                [Response Rules]"},
                {"role": "user", "content": message}
            ]
        )
        resource_table = response.choices[0].message.content
        resource_list= self.parse_resource_table(resource_table)
        return resource_list
    
    def parse_resource_table(self, resource_table: str):
        resource_list = []
        for row in resource_table.split("\n")[2:]:
            resource, amount = row.split("|")[1:3]
            resource = resource.strip().upper()
            try:
                resource_type = self.get_resource_type(resource)
                for i in range(int(amount)):
                    name = f"{resource_type}{i+1}"
                    resource_list.append(f"{resource_type}.{name}")
            except:
                print(f"Resource type {resource} is not found.")
        return resource_list

    def get_resource_type(self, resource: str):
        resource_type_dict = {
            "AZURE AI SEARCH": ResourceType.AZURE_AI_SEARCH,
            "AZURE AI SERVICES": ResourceType.AZURE_AI_SERVICES,
            "AZURE APPLICATION INSIGHTS": ResourceType.AZURE_APPLICATION_INSIGHTS,
            "AZURE APP SERVICE": ResourceType.AZURE_APP_SERVICE,
            "AZURE BOT SERVICE": ResourceType.AZURE_BOT_SERVICE,
            "AZURE CACHE FOR REDIS": ResourceType.AZURE_REDIS_CACHE,
            "AZURE CONTAINER APPS": ResourceType.AZURE_CONTAINER_APP,
            "AZURE COSMOS DB": ResourceType.AZURE_COSMOS_DB,
            "AZURE FUNCTIONS": ResourceType.AZURE_FUNCTION_APP,
            "AZURE KEY VAULT": ResourceType.AZURE_KEYVAULT,
            "AZURE MYSQL DB": ResourceType.AZURE_MYSQL_DB,
            "AZURE OPENAI SERVICE": ResourceType.AZURE_OPENAI,
            "AZURE POSTGRESQL DB": ResourceType.AZURE_POSTGRESQL_DB,
            "AZURE SERVICE BUS": ResourceType.AZURE_SERVICE_BUS,
            "AZURE STATIC WEB APPS": ResourceType.AZURE_STATIC_WEB_APP,
            "AZURE STORAGE ACCOUNT": ResourceType.AZURE_STORAGE_ACCOUNT,
            "AZURE SQL DB": ResourceType.AZURE_SQL_DB,
            "AZURE WEB PUBSUB": ResourceType.AZURE_WEBPUBSUB,
        }
        return resource_type_dict[resource].value

    def configure_bindings(self, message: str, resource_list):
        response = self.client.chat.completions.create(
            model="gpt4",
            messages=[
                {"role": "system", "content": "You are an assistant that knows about Azure resources and services.\
                                                Your job is to determine the relationship among given Azure resource list, picking out the 1-to-1 connections.\
                                                Here is the **Azure resource list**:\
                                                {resource_list}\
                                                Determine the authentication type if it is specified. Possible values are secret, system-identity, http, and none. None means not specified. http is the type between two compute services (azureappservice, azurecontainerapps, azurefunctions, and azurestaticwebapp).\
                                                \
                                                [Response Rules]\
                                                1. Response with a table of connections between Azure services and their connection type in the following format:\
                                                    | Connection                                                                        | Type                                  |\
                                                    | source resource-->target resource                                                 | authentication type                   |\
                                                    | ...                                                                               | ...                                   |\
                                                2. Do not contain ANY OTHER words except the table.\
                                                3. Use the name directly from the **Azure resource list**.\
                                                4. The type of the source resources should be one of **azureappservice, azurecontainerapps, or azurefunctions**\
                                                [Response Rules]".format(resource_list=resource_list)},
                {"role": "user", "content": message}
            ]
        )

        binding_table = response.choices[0].message.content
        binding_list = self.parse_binding_table(binding_table)
        return binding_list
    
    def parse_binding_table(self, binding_table: str):
        binding_list = []
        for row in binding_table.split("\n")[2:]:
            binding, auth_type = row.split("|")[1:3]
            binding = binding.strip()
            source, target = binding.split("-->")
            auth_type = auth_type.strip()

            # check if auth type is available
            source_type = source.split(".")[0]
            target_type = target.split(".")[0]
            if ((auth_type == "system-identity" and target_type not in COMPUTE_RESOURCES + DB_RESOURCES) or \
                (auth_type == "http" and target_type in COMPUTE_RESOURCES and source in COMPUTE_RESOURCES) or \
                (auth_type == "secret" and target_type != ResourceType.AZURE_KEYVAULT)) and target_type != ResourceType.AZURE_BOT_SERVICE:
                binding_list.append((source, target, auth_type))
            else:
                binding_list.append((source, target, "none"))
        return binding_list

    def transform_to_json(self, resource_list, binding_list):
        json_output = {
            "resources": [],
            "bindings": [],
            "services": []
        }
        existing_types = []
        for resource in resource_list:
            resource_type, resource_name = resource.split(".")
            if resource_type not in existing_types:
                json_output["resources"].append({
                    "type": resource_type,
                    "instances": [
                        {
                            "name": resource_name
                        }
                    ]
                })
                existing_types.append(resource_type)
            else:
                json_output["resources"][existing_types.index(resource_type)]["instances"].append({
                    "name": resource_name
                })
            
            if resource_type in [ResourceType.AZURE_APP_SERVICE.value, ResourceType.AZURE_CONTAINER_APP.value, ResourceType.AZURE_FUNCTION_APP.value]:
                json_output["services"].append({
                    "host": '${' + resource + '}',
                    "language": "python",
                    "project": '.'
                })

        for binding in binding_list:
            source, target, auth_type = binding
            if auth_type != "none":
                json_output["bindings"].append({
                    "source": '${' + source + '}',
                    "target": '${' + target + '}',
                    "connection": "secret" if target in [ResourceType.AZURE_MYSQL_DB, ResourceType.AZURE_POSTGRESQL_DB, ResourceType.AZURE_SQL_DB] else auth_type,
                })
            else:
                json_output["bindings"].append({
                    "source": '${' + source + '}',
                    "target": '${' + target + '}'
                })
            
        return json_output

    def config_services(self, message: str):
        resource_list = self.configure_resources(message)
        binding_list = self.configure_bindings(message, resource_list)
        json_output = self.transform_to_json(resource_list, binding_list)
        print("\n----------------------------------------\n")
        print("resouces:", resource_list)
        print("bindings:", binding_list)
        print(json_output)
        print("\n----------------------------------------\n")
        return json_output
