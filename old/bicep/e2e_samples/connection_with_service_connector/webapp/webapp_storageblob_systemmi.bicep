// The template to connect a WebApp to a Storage Blob with Service Connector
// =======================================================
//   Source         :   Webapp
//   Target         :   Storage Blob
//   Connection     :   Service Connector
//   Authentication :   System Assigned Managed Identity
// =======================================================


param location string = resourceGroup().location
param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'
param storageAccountName string = 'account${uniqueString(resourceGroup().id)}'
param connectorName string = 'connector_${uniqueString(resourceGroup().id)}'


// Create a Storage Account as target service
module storageAccountDeployment '../../../dependency_modules/targets/storage_account.bicep' = {
  name: 'storage-deployment'
  params: {
    location: location
    name: storageAccountName
  }
}


// Create a WebApp as compute service
module webAppDeployment '../../../dependency_modules/sources/web_app.bicep' = {
  name: 'webapp-deployment'
  params: {
    location: location
    name: webAppName
  }
}


// Create a Service Connector resource to connect WebApp to Storage
module serviceConnectorDeployment '../../../dependency_modules/connectors/webapp_connector.bicep' = {
  name: 'service-connector-deployment'
  params: {
    webAppName: webAppName
    connectorName: connectorName
    connectorTargetResourceId: '${storageAccountDeployment.outputs.id}/blobServices/default'
    connectorAuthType: 'systemAssignedIdentity'
  }
}


output storageId string = storageAccountDeployment.outputs.id
output webAppId string = webAppDeployment.outputs.id
output connectorId string = serviceConnectorDeployment.outputs.id
