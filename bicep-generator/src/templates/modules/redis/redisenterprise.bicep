// The template to create a redis for enterprise

param name string = 'redisep_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param skuName string = 'Enterprise_E10'
param SkuCapacity int = 2
param minimumTlsVersion string = '1.2'


resource redisEnterprise 'Microsoft.Cache/redisEnterprise@2023-07-01' = {
  name: name
  location: location
  sku: {
    name: skuName
    capacity: SkuCapacity
  }
  properties: {
    minimumTlsVersion: minimumTlsVersion
  }
}
