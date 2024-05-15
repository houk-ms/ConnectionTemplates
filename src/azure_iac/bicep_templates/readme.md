# IaC Generator - Bicep

## Bicep files

Iac Generator uses modules.
the following files to the infrastructure:

1. Bicep templates of resources

    For each kind of resources, a Bicep file is generated as the module for the resource. The Bicep file for each resource is used once or for multiple times in the `main.bicep` for actual deployments. Each template contains the parameters that it takes from the `main.bicep` at the top, followed by the basic configurations of these files. Below is the brief introduction of the generated Bicep files for all resources and their dependency resources.

    - Compute services
      - Azure Container Apps

        `containerappenv.bicep` defines the Container Apps Environment and the Log Anayltics (for monitoring) that are prerequisites for the creation of the Container Apps. Only one Container Apps Environment is only created and is shared by all the Container Apps services.
        `containerappregistry.bicep` defines the Container Registry Registry that is also shared by all of the Container Apps services.
        `containerapp.bicep` defines a template of a Container App. System identity is enabled and the Container App Registry is referenced. Other environment variables and secrets for service bindings are passed through from the `main.bicep`.

      - Azure App Service
      
        `appservice.bicep`, `appserviceplan.bicep`, `appservice.settings.bicep`
        
      - Azure Functions
        `functionapp.bicep`, `storageaccount.bicep`, `functionapp.settings.bicep`
        
      - staticwebapp.bicep, staticwebapp.settings.bicep
        Azure Static Web App
    - Target resources and others
      - keyvault.bicep
        Azure Key Vault
      - cosmosdb.bicep
        Azure Cosmos DB for MongoDB
      - storageaccount.bicep
        Azure Storage Account
      - sqldb.bicep
        Azure SQL Database
      - postgresqldb.bicep
        Azure Database for PostgreSQL servers
      - mysql.bicep
        Azure Azure Database for MySQL servers
      - aiservices.bicep
        Azure AI Services
      - openai.bicep
        Azure OpenAI
      - botservice.bicep
        Azure AI Bot Service
      - servicebus.bicep
        Azure Service Bus
      - webpubsub.bicep
        Azure Web PubSub

1. main.bicep

    Note that the compute resources are deployed twice in the main.bicep. The configuration of app settings, environment variables and container app secrets takes place after the dependency resources (database, key vault, storage, etc.) are deployed.

    A diagram that shows the flow of deployments?

1. main.parameters.json

    This file contains the parameters that requires user input. 
    - Azure AI Bot Service
      An Azure AI Bot Service requires the client ID and the client secret of the registered app for Microsoft Entra identity provider.
    - Azure Database for PostgreSQL servers
      An Azure Database for PostgreSQL servers requires the user name and the password of the database administrator.
    - Azure SQL
      An Azure SQL Database requires the user name and the password of the database administrator.
    - Azure Azure Database for MySQL servers
      An Azure Database for MySQL servers requires the user name and the password of the database administrator.

## Next Step

1. Complete the input parameters.
1. Customize the configurations to the resources.
1. Provision the resources. Refer to [Deploy Bicep files from Visual Studio Code](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-vscode).
