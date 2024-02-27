resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' = {
  name: containerRegistryName
  location: containerRegistryLocation
  sku: {
    name: containerRegistrySku
  }
  properties: {
    adminUserEnabled: true
  }
}