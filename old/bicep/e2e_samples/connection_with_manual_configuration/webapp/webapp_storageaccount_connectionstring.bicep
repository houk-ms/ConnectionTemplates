// The template to connect a WebApp to a Storage Account with manual configurations
// =======================================================
//   Source         :   Webapp
//   Target         :   Storage Account
//   Connection     :   Manual Configuration
//   Authentication :   Connection String
// =======================================================


param location string = resourceGroup().location
param storageAccountName string = 'account${uniqueString(resourceGroup().id)}'
param appServiceName string = 'webapp-${uniqueString(resourceGroup().id)}'


// Create a Storage Account as target service
// Public network access is enabled by default
module storageAccountDeployment '../../../dependency_modules/targets/storage_account.bicep' = {
  name: 'storage-account-deployment'
  params: {
    location: location
    name: storageAccountName
  }
}
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
  name: storageAccountName
}
var storageConnectionString = '''
  DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};
  BlobEndpoint=${storageAccount.properties.primaryEndpoints.blob};FileEndpoint=${storageAccount.properties.primaryEndpoints.file};
  TableEndpoint=${storageAccount.properties.primaryEndpoints.table};QueueEndpoint=${storageAccount.properties.primaryEndpoints.queue};
'''


// Create a WebApp as compute service
// Save storage account connection string into the app settings
module appServiceDeployment '../../../dependency_modules/sources/web_app.bicep' = {
  name: 'app-service-deployment'
  params: {
  location: location
  name: appServiceName
  appSettings: [{
    name: 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING'
    value: storageConnectionString
  }]
  }
}


output storageId string = storageAccount.id
output webAppId string = appServiceDeployment.outputs.id
