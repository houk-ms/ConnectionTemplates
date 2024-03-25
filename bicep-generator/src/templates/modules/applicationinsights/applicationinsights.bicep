// The template to create an application insights

param name string = 'insights_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param kind string = 'web'
param applicationType string = 'web'
param requestSource string = 'rest'


resource applicationInsights 'Microsoft.Insights/components@2020-02-02' = {
	name: name
	location: location
	kind: kind
	properties: {
		Application_Type: applicationType
		Request_Source: requestSource
	}
}
