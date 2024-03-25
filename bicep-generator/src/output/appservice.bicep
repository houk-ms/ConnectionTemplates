// The template to create an app service

param name string = 'app-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param linuxFxVersion string = 'PYTHON|3.8'
param identityType string = 'SystemAssigned'
param appServicePlanId string
param appSettings array = []


resource appService 'Microsoft.Web/sites@2022-09-01' = {
	name: name
	location: location
	properties: {
		serverFarmId: appServicePlanId
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