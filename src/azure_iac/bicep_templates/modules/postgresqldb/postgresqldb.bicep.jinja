// The template to create a postgresql server

param name string = 'psql_${uniqueString(resourceGroup().id)}'
param databaseName string = 'database_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param skuName string = 'Standard_D4ds_v4'
param skuTier string = 'GeneralPurpose'
param version string = '12'
@allowed(['Create', 'Default', 'GeoRestore', 'PointInTimeRestore', 'Replica', 'ReviveDropped', 'Update'])
param createMode string = 'Default'
param adminName string = 'administrator_${uniqueString(resourceGroup().id)}'
@secure()
param adminPassword string = 'Aa0!${newGuid()}'
param storageSizeGb int = 128
param availabilityZone string = '1'
param charset string = 'UTF8'
param allowIps array = []
param keyVaultName string = ''
param secretName string = 'myvault/mysecret'
@secure()
param secretValue string = ''


// create a postgresql server
resource postgresqlServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
	name: name
	location: location
	sku: {
		name: skuName
		tier: skuTier
	}
	properties: {
		version: version
		createMode: createMode
		administratorLogin: adminName
		administratorLoginPassword: adminPassword
		storage: {
			storageSizeGB: storageSizeGb
		}
		availabilityZone: availabilityZone
	}
}

// create a postgresql database
resource postgresqlDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
	name: databaseName
	parent: postgresqlServer
	properties: {
		charset: charset
	}
}

// create firewall rules
resource postgresqlFirewall 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2022-12-01' = [for ip in allowIps : {
	name: uniqueString(ip)
	parent: postgresqlServer
	properties: {
		endIpAddress: ip
		startIpAddress: ip
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
		value: secretValue
	}
}


output id string = postgresqlServer.id
output keyVaultSecretUri string = (keyVaultName != '' ? keyVaultSecret.properties.secretUriWithVersion : '')
