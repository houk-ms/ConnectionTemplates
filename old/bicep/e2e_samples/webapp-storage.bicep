// The template creates a webapp and a storage account.
// In order to make it more readable, we use only the mininal set of parameters to create the resources.

param location string = resourceGroup().location
// App service plan parameters
param planName string = 'plan_${uniqueString(resourceGroup().id)}'
param kind string = 'linux'
param reserved bool = true
param sku string = 'B1'
// Webapp parameters
param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'
param linuxFxVersion string = 'PYTHON|3.8'
param identityType string = 'SystemAssigned'
param appSettings array = []
// Storage account parameters
param storageAccountName string = 'account${uniqueString(resourceGroup().id)}'


// Create an app service plan 
resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: planName
  location: location
  kind: kind
  sku: {
    name: sku
  }
  properties: {
    reserved: reserved
  }
}


// Create a web app
resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: location
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      appSettings: appSettings
    }
  }
  identity: {
    type: identityType
  }
}


// Create a storage account
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}


output accountId string = storageAccount.id
output webAppId string = appService.id
output identityPrincipalId string = appService.identity.principalId
output outboundIps string = appService.properties.outboundIpAddresses
