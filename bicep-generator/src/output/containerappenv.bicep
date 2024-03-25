// The template to create an Azure Container App environment

param name string = 'acaenv_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param logAnalyticsName string = 'log-${uniqueString(resourceGroup().id)}'
param logAnalyticsSKU string = 'PerGB2018'


resource logAnalytics 'Microsoft.OperationalInsights/workspaces@2022-10-01' = {
	name: logAnalyticsName
	location: location
	properties: {
		sku: {
			name: logAnalyticsSKU
		}
	}
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