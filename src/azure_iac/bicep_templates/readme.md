# IaC Generator - Bicep

## Bicep files

Iac Generator uses modules.
the following files to the infrastructure:

1. Bicep templates of resources

    For each kind of resources, a Bicep file is generated as the module for the resource. If some dependency resources, e.g. App Service plan and Container Apps Environment, are required, the corresponding Bicep files are also created. Dependency resources are shared among the resources of the same kind. A Bicep file for app settings is also created for the compute resources. Below is the brief introduction of the generated Bicep files for all resources and their dependency resources.

    - containerapp.bicep, containerappenv.bicep, containerappregistry.bicep
      Azure Container Apps
    - appservice.bicep, appserviceplan.bicep, appservice.settings.bicep
      Azure App Service
    - functionapp.bicep, storageaccount.bicep, functionapp.settings.bicep
      Azure Functions
    - staticwebapp.bicep, staticwebapp.settings.bicep
    - keyvault.bicep
    - cosmosdb.bicep
    - storageaccount.bicep
    - sqldb.bicep
    - postgresqldb.bicep
    - mysql.bicep
    - openai.bicep
    - botservice.bicep
    - servicebus.bicep
    - webpubsub.bicep

1. main.bicep

    Note that the compute resources are deployed twice in the main.bicep. The configuration of app settings, environment variables and container app secrets takes place after the dependency resources (database, key vault, storage, etc.) are deployed.

    A diagram that shows the flow of deployments?

1. main.parameters.json

    This file contains the parameters that requires user input.

## Next Step

1. Complete the input parameters.
1. Customize the configurations to the resources.
1. Provision the resources. Refer to [Deploy Bicep files from Visual Studio Code](https://learn.microsoft.com/en-us/azure/azure-resource-manager/bicep/deploy-vscode).
