// The template creates firewall rules for redis cache

param redisName string = 'redis_${uniqueString(resourceGroup().id)}'
param allowIps array = []


resource redis 'Microsoft.Cache/redis@2023-08-01' existing = {
  name: redisName
}

resource redisFirewall 'Microsoft.Cache/redis/firewallRules@2023-08-01' = [for ip in allowIps : {
  name: uniqueString(ip)
  parent: redis
  properties: {
    endIP: ip
    startIP: ip
  }
}]
