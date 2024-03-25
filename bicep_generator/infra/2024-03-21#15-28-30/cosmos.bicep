param accountName string = 'cosmos_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param databaseName string = 'database_${uniqueString(resourceGroup().id)}'


resource cosmosAccount 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' = {
  name: accountName
  location: location
  kind: 'MongoDB'
  properties: {
    databaseAccountOfferType: 'Standard'
    locations: [
      {
        locationName: location
        failoverPriority: 0
      }
    ]
    ipRules: [
      {
        ipAddressOrRange: '0.0.0.0'
      }
    ]
    consistencyPolicy: {
      defaultConsistencyLevel: 'Session'
    }
    enableAutomaticFailover: true
  }
}

resource mongoDB 'Microsoft.DocumentDB/databaseAccounts/mongodbDatabases@2023-11-15' = {
  parent: cosmosAccount
  name: databaseName
  properties: {
    resource: {
      id: databaseName
    }
    options: {}
  }
}


output accountId string = cosmosAccount.id
output databaseId string = mongoDB.id
