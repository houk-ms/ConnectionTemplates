// The template to creat a log analytics

param name string = 'log-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param sku string = 'PerGB2018'


resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: name
  location: location
  properties: {
    sku: {
      name: sku
    }
  }
}
