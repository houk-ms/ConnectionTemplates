// The template builds a connection between a webapp and a storage account 
// with system assigned identity without using Service Connector

param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'
param storageAccountName string = 'account${uniqueString(resourceGroup().id)}'
param storageBlobDataContributorRole string  = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'

// Get an existing webapp
resource webApp 'Microsoft.Web/sites@2022-09-01' existing = {
  name: webAppName
}

// Get an existig storage
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
  name: storageAccountName
}

// Operation: Enable system assigned identity on the source service
// Nothing need to do as it is enabled when creating the webapp

// Operation: Configure the target service's endpoint on the source service's app settings
resource appSettings 'Microsoft.Web/sites/config@2022-09-01' = {
  name: 'appsettings'
  parent: webApp
  properties: {
    AZURE_STORAGEBLOB_RESOURCEENDPOINT: storageAccount.properties.primaryEndpoints.blob
  }
}

// Operation: Configure firewall on the target service to allow the source service's outbound ips
// Nothing need to do as storage account allows all ips by default

// Operation: Create role assignment for the source service's identity on the target service
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: guid(resourceGroup().id, storageBlobDataContributorRole)
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', storageBlobDataContributorRole)
    principalId: webApp.identity.principalId
  }
}
