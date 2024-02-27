// The template to create a keyvault

param name string = 'vault-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param skuName string = 'standard'
param skuFamily string = 'A'
param enableRbacAuthorization bool = false
param allowIps array = []


resource keyvault 'Microsoft.KeyVault/vaults@2023-02-01' = {
  name: name
  location: location
  properties: {
    tenantId: subscription().tenantId
    sku: {
      name: skuName
      family: skuFamily
    }
    enableRbacAuthorization: enableRbacAuthorization
    networkAcls: {
      ipRules: [for ip in allowIps : {
        value: ip
      }]
    }
  }
}


output id string = keyvault.id
output endpoint string = 'https://${keyvault.name}${environment().suffixes.keyvaultDns}'
output scope string = '${environment().resourceManager}/.default'
