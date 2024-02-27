// The template to create keyvault access policy

param keyVaultName string = 'vault-${uniqueString(resourceGroup().id)}'
param permissions object = { secrets: [ 'get', 'list' ] }
param principalId string


resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
  name: keyVaultName
}

resource keyVaultAccessPolicies 'Microsoft.KeyVault/vaults/accessPolicies@2022-07-01' = {
  parent: keyVault
  name: 'add'
  properties: {
    accessPolicies: [ {
        tenantId: subscription().tenantId
        objectId: principalId
        permissions: permissions
      } ]
  }
}
