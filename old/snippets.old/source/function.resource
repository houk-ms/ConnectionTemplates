resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: functionAppName
  location: functionAppLocation
  kind: 'functionapp'
  properties: {
    serverFarmId: appServicePlan.id
  }
  identity: {
    type: functionAppIdentityType
  }
}