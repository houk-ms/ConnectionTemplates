// The template to create Azure Key Vault with network ACLs and role assignments 

param name string = 'vault-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param skuName string = 'standard'
param skuFamily string = 'A'
param enableRbacAuthorization bool = true
param allowIps array = []
param principalIds array = []
param roleDefinitionId string = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'  // storage blob data contributor role


// create keyvault with network ACLs
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

// create role assignments for the specified principalIds
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principalId in principalIds: {
	scope: keyvault
	name: guid(name, principalId)
	properties: {
		roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
		principalId: principalId
	}
}]


output id string = keyvault.id
output endpoint string = 'https://${keyvault.name}${environment().suffixes.keyvaultDns}'