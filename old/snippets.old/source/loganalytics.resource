resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
  name: logAnalyticsName
  location: logAnalyticsLocation
  properties: {
    sku: {
      name: logAnalyticsSku
    }
  }
}