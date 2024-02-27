// The template to create a redis enterprise database

param name string = 'database_${uniqueString(resourceGroup().id)}'
param redisEnterpriseName string = 'redisep_${uniqueString(resourceGroup().id)}'


resource redisEnterprise 'Microsoft.Cache/redisEnterprise@2023-07-01' existing = {
  name: redisEnterpriseName
}

resource redisEnterpriseDatabase 'Microsoft.Cache/redisEnterprise/databases@2022-01-01' = {
  name: name
  parent: redisEnterprise
}
