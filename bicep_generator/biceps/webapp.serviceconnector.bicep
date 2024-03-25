// The template to create a service connector resource on a webapp
param name string = 'connector_${uniqueString(resourceGroup().id)}'
param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'
param clientType string = 'python'
param targetResourceId string
param authType string = 'secret'

resource webApp 'Microsoft.Web/sites@2022-09-01' existing = {
  name: webAppName
}

resource serviceConnector 'Microsoft.ServiceLinker/linkers@2022-05-01' = {
  name: name
  scope: webApp
  properties: {
    clientType: clientType
    targetService: {
      type: 'AzureResource'
      id: targetResourceId
    }
    authInfo: {
      authType: authType
    }
  }
}
