// The template to create a postgresql server

param serverName string = 'postgresql_${uniqueString(resourceGroup().id)}'
param databaseName string = 'postgresql_${uniqueString(resourceGroup().id)}'
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


resource postgresqlServer 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' = {
  name: serverName
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

resource postgresqlDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  name: databaseName
  parent: postgresqlServer
  properties: {
    charset: charset
  }
}


output serverId string = postgresqlServer.id
output databaseId string = postgresqlDatabase.id
