// The template creates firewall rules for postgresql

param postgresqlName string = 'redis_${uniqueString(resourceGroup().id)}'
param allowIps array = []


resource postgresql 'Microsoft.DBforPostgreSQL/flexibleServers@2022-12-01' existing = {
  name: postgresqlName
}

resource postgresqlFirewall 'Microsoft.DBforPostgreSQL/flexibleServers/firewallRules@2022-12-01' = [for ip in allowIps : {
  name: uniqueString(ip)
  parent: postgresql
  properties: {
    endIpAddress: ip
    startIpAddress: ip
  }
}]
