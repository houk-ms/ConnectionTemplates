// The template to create a keyvault secret

param keyVaultName string = 'vault-${uniqueString(resourceGroup().id)}'
param name string
@secure()
param secretValue string


resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = {
  name: keyVaultName
}

resource keyVaultSecret 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = {
  name: name
  parent: keyVault
  properties: {
    attributes: {
      enabled: true
    }
    contentType: 'string'
    value: secretValue
  }
}


output appServiceSecretRefernece string = '@Microsoft.KeyVault(SecretUri=${keyVaultSecret.properties.secretUriWithVersion})'
output containerAppSecretRefernece string = keyVaultSecret.properties.secretUriWithVersion
