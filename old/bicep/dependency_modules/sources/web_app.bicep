// In order to make the templates more readable, we use only the mininal set of 
// parameters to create the resource. 

param name string = 'webapp-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param linuxFxVersion string = 'PYTHON|3.8'
param identityType string = 'SystemAssigned'
param appSettings array = []


module appServicePlan './source_dependencies/app_service_plan.bicep' = {
  name: 'app-service-plan-deployment'
  params: {
    location: location
  }
}

resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: name
  location: location
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

output appResource resource = appService
output id string = appService.id
output name string = appService.name
output identityPrincipalId string = appService.identity.principalId
output outboundIps string = appService.properties.outboundIpAddresses
