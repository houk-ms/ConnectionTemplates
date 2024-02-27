resource redisCache 'Microsoft.Cache/redis@2023-08-01' = {
  name: redisCacheName
  location: redisCacheLocation
  properties: {
    sku: {
      name: redisCacheSkuName
      family: redisCacheSkuFamily
      capacity: redisCacheSkuCapacity
    }
  }
}