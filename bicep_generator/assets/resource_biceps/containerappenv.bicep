// The template to create a container app environment

param name string = 'acaenv_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param logAnalyticsName string = 'log-${uniqueString(resourceGroup().id)}'


module logAnalyticsDeployment 'loganalytics.bicep' = {
  name: 'log-analytics-deployment'
  params: {
    location: location
  }
}

resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' existing = {
  name: logAnalyticsName
}

resource containerAppEnv 'Microsoft.Web/kubeEnvironments@2022-09-01' = {
  name: name
  location: location 
  kind: 'containerenvironment'
  properties: {
    environmentType: 'managed'
    internalLoadBalancerEnabled: false
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: logAnalytics.properties.customerId
        sharedKey: logAnalytics.listKeys().primarySharedKey
      }
    }
  }
}


output id string = containerAppEnv.id
