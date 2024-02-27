// The template to create a postgresql database

param name string = 'database_${uniqueString(resourceGroup().id)}'
param postgresqlName string = 'postgresql_${uniqueString(resourceGroup().id)}'
param charset string = 'UTF8'
param collation string = 'en_US.UTF-8'


resource postgresql 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' existing = {
  name: postgresqlName
}

resource postgresqlDatabase 'Microsoft.DBforPostgreSQL/flexibleServers/databases@2022-12-01' = {
  name: name
  parent: postgresql
  properties: {
    charset: charset
    collation: collation
  }
}
