// The template to create an storage account

param name string = 'account${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param kind string = 'StorageV2'
param skuName string = 'Standard_LRS'


resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: name
  location: location
  kind: kind
  sku: {
    name: skuName
  }
}


output id string = storageAccount.id
