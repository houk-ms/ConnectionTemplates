// The template to create an Azure Container Registry

param name string = 'acr_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param sku string = 'Basic'

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
	name: name
	location: location
	sku: {
		name: sku
	}
	properties: {
		adminUserEnabled: true
	}
}