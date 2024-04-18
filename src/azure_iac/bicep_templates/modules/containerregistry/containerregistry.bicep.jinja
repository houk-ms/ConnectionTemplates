// The template to create an Azure Container Registry

param name string = 'acr_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param sku string = 'Standard'

// 2022-02-01-preview needed for anonymousPullEnabled
resource containerRegistry 'Microsoft.ContainerRegistry/registries@2022-02-01-preview' = {
	name: name
	location: location
	sku: {
		name: sku
	}
	properties: {
		adminUserEnabled: true
		anonymousPullEnabled: true
	}
}

output id string = containerRegistry.id
output loginServer string = containerRegistry.properties.loginServer
