resource appService 'Microsoft.Web/sites@2022-09-01' = {
  name: webAppName
  location: webAppLocation
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: webAppLinuxFxVersion
    }
  }
  identity: {
    type: webAppIdentityType
  }
}