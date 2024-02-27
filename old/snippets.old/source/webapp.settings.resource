resource appSettings 'Microsoft.Web/sites/config@2022-09-01' = {
  name: '{{APP_CONFIG_NAME}}'
  parent: webApp
  properties: {
    {{APP_CONFIGS}}
  }
}