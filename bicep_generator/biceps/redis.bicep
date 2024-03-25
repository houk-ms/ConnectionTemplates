// The template to create a redis cache

param name string = 'redis_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param skuName string = 'Basic'
param SkuFamily string = 'C'
param SkuCapacity int = 0


resource redis 'Microsoft.Cache/redis@2023-08-01' = {
  name: name
  location: location
  properties: {
    sku: {
      name: skuName
      family: SkuFamily
      capacity: SkuCapacity
    }
  }
}
