// The template to create storage firewall rules

param name string = 'account${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param kind string = 'StorageV2'
param skuName string = 'Standard_LRS'
param allowIps array = []


resource storageAccount 'Microsoft.Storage/storageAccounts@2022-09-01' = {
  name: name
  location: location
  kind: kind
  sku: {
    name: skuName
  }
  properties: {
    publicNetworkAccess: 'Enabled'
    networkAcls: {
      defaultAction: 'Deny'
      ipRules: [for ip in allowIps: {
        action: 'Allow'
        value: ip
      }]
    }
  }
}
