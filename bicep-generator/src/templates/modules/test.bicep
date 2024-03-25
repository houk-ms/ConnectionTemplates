module appServiceDeployment 'appservice/appservice.bicep' = {
  name: 'appservice-deployment'
  params: {
      location: location
      name: webAppName
      appSettings: [{
          name: 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING'
          value: storageSecretReference
      },{
          name: 'AZURE_KEYVAULT_RESOURCEENDPOINT'
          value: keyvaultEndpoint
      },{
          name: 'AZURE_KEYVAULT_SCOPE'
          value: keyvaultScope
      }]
  }
}
var appSystemIdentityPrinciaplId = appServiceDeployment.outputs.identityPrincipalId
var outboundIps = split(appServiceDeployment.outputs.outboundIps, ',')
