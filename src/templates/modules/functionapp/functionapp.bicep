// The template to create a function app

param name string = 'functionapp-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param linuxFxVersion string = 'PYTHON|3.8'
param identityType string = 'SystemAssigned'
param appSettings array = []


module appServicePlan '../appserviceplan/appserviceplan.bicep' = {
  name: 'appserviceplan-deployment'
  params: {
    location: location
  }
}

resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: name
  location: location
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.outputs.id
    siteConfig: {
      linuxFxVersion: linuxFxVersion
      appSettings: appSettings
    }
  }
  identity: {
    type: identityType
  }
}


output id string = appService.id
output name string = appService.name
output identityPrincipalId string = appService.identity.principalId
output outboundIps string = appService.properties.outboundIpAddresses
