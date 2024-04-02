// The template to create Azure Storage Account with network ACLs, role assignments and Key Vault secret

param name string = 'sa${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param kind string = 'StorageV2'
param skuName string = 'Standard_LRS'
param allowIps array = []
param principalIds array = []
param roleDefinitionId string = 'c12c1c16-33a1-487b-954d-41c89c60f349'  // Reader and Data Access role
param keyVaultName string = ''
param secretName string = 'myvault/mysecret'


// create storage account with network ACLs
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
	name: name
	location: location
	kind: kind
	sku: {
		name: skuName
	}
	properties: {
	publicNetworkAccess: 'Enabled'
	networkAcls: {
		defaultAction: 'Deny'
		ipRules: [for ip in allowIps: {
			action: 'Allow'
			value: ip
		}]
	}
	}
}

// create role assignments for the specified principalIds
resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = [for principalId in principalIds: {
	scope: storageAccount
	name: guid(name, principalId)
	properties: {
		roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
		principalId: principalId
	}
}]

// create key vault and secret if keyVaultName is specified
resource keyVault 'Microsoft.KeyVault/vaults@2022-07-01' existing = if (keyVaultName != ''){
	name: keyVaultName
}

resource keyVaultSecret 'Microsoft.KeyVault/vaults/secrets@2022-07-01' = if (keyVaultName != ''){
	name: secretName
	parent: keyVault
	properties: {
		attributes: {
			enabled: true
		}
		contentType: 'string'
		value: 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};BlobEndpoint=${storageAccount.properties.primaryEndpoints.blob};FileEndpoint=${storageAccount.properties.primaryEndpoints.file};TableEndpoint=${storageAccount.properties.primaryEndpoints.table};QueueEndpoint=${storageAccount.properties.primaryEndpoints.queue};'
	}
}


output id string = storageAccount.id
output blobEndpoint string = storageAccount.properties.primaryEndpoints.blob
output fileEndpoint string = storageAccount.properties.primaryEndpoints.queue
output queueEndpoint string = storageAccount.properties.primaryEndpoints.file
output tableEndpoint string = storageAccount.properties.primaryEndpoints.table
output keyVaultSecretUri string = (keyVaultName != '' ? keyVaultSecret.properties.secretUriWithVersion : '')