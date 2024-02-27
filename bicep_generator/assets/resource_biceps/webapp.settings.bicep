// The template to create webapp settings
param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'
param webAppSettings object = {}

resource webApp 'Microsoft.Web/sites@2022-09-01' existing = {
  name: webAppName
}

resource appSettings 'Microsoft.Web/sites/config@2022-09-01' = {
  name: 'appsettings'
  parent: webApp
  properties: webAppSettings
}
