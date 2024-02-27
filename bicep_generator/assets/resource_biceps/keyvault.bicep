// The template to create a keyvault

param name string = 'vault-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param skuName string = 'standard'
param skuFamily string = 'A'
param enableRbacAuthorization bool = false


resource keyVault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: name
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      name: skuName
      family: skuFamily
    }
    enableRbacAuthorization: enableRbacAuthorization
  }
}


output id string = keyVault.id
output endpoint string = keyVault.properties.vaultUri
output scope string = '${environment().resourceManager}/.default'
