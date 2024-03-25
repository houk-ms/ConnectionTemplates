// The template to create a container registry

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
