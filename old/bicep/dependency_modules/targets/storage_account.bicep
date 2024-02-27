// In order to make the templates more readable, we use only the mininal set of 
// parameters to create the resource. 

param name string = 'account${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location


resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: name
  location: location
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}


output name string = storageAccount.name
output id string = storageAccount.id
