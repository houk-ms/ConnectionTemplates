// In order to make the templates more readable, we use only the mininal set of 
// parameters to create the resource. 


param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'
param connectorName string = 'connector_${uniqueString(resourceGroup().id)}'
param connectorAuthType string = 'systemAssignedIdentity'
param connectorClientType string = 'python'
param connectorTargetResourceId string

resource webApp 'Microsoft.Web/sites@2022-09-01' existing = {
  name: webAppName
}

resource serviceConnector 'Microsoft.ServiceLinker/linkers@2022-05-01' = {
  name: connectorName
  scope: webApp
  properties: {
    clientType: connectorClientType
    targetService: {
      type: 'AzureResource'
      id: connectorTargetResourceId
    }
    authInfo: {
      authType: connectorAuthType
    }
  }
}


output id string = serviceConnector.id
