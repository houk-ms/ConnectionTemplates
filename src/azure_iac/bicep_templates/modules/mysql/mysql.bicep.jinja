// The template to create a mysql server

param name string = 'mysql_${uniqueString(resourceGroup().id)}'
param databaseName string = 'database_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param skuName string = 'Standard_D4ds_v4'
param skuTier string = 'GeneralPurpose'
param version string = '8.0.21'
@allowed(['Default', 'GeoRestore', 'PointInTimeRestore', 'Replica'])
param createMode string = 'Default'
param adminName string = ''
@secure()
param adminPassword string = ''
param availabilityZone string = '1'
param allowIps array = []
param keyVaultName string = ''
param secretName string = ''
@secure()
param secretValue string = ''

// create a mysql server
resource mysqlServer 'Microsoft.DBforMySQL/flexibleServers@2023-10-01-preview' = {
	name: name
	location: location
	sku: {
		name: skuName
		tier: skuTier
	}
	properties: {
		administratorLogin: adminName
		administratorLoginPassword: adminPassword
		availabilityZone: availabilityZone
		createMode: createMode
		version: version
	}
}

// create a mysql database
resource mysqlDatabase 'Microsoft.DBforMySQL/flexibleServers/databases@2023-06-30' = {
	name: databaseName
	parent: mysqlServer
}

// create firewall rules
resource mysqlFirewall 'Microsoft.DBforMySQL/flexibleServers/firewallRules@2023-06-30' = [for ip in allowIps : {
	name: uniqueString(ip)
	parent: mysqlServer
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

output id string = mysqlServer.id
output keyVaultSecretUri string = keyVaultSecret.properties.secretUriWithVersion
