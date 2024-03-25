// The main bicep to create compute and target services with connections

param databaseName string = 'mongodb1-${uniqueString(resourceGroup().id)}'
param accountName string = 'cosmos-${uniqueString(resourceGroup().id)}'
param appInsightsName string = 'appinsights1-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param keyVaultName string = 'keyvault1-${uniqueString(resourceGroup().id)}'
param apiAppName string = 'api-${uniqueString(resourceGroup().id)}'
param webAppName string = 'web-${uniqueString(resourceGroup().id)}'


// Create target service: Azure Cosmos Mongo DB

module cosmosDeployment 'cosmos.bicep' = {
    name: 'cosmos-deployment'
    params: {
        location: location
        accountName: accountName
        databaseName: databaseName
    }
    dependsOn: []
}
resource cosmos 'Microsoft.DocumentDB/databaseAccounts@2023-11-15' existing = {
    name: accountName
}
var cosmosConnectionString = cosmos.listConnectionStrings().connectionStrings[0].connectionString


// Create target service: Azure Application Insights

module appInsightsDeployment 'appinsights.bicep' = {
    name: 'appinsights-deployment'
    params: {
        location: location
        name: appInsightsName
    }
    dependsOn: []
}
resource appInsights 'Microsoft.Insights/components@2020-02-02' existing = {
    name: appInsightsName
}
var appInsightsConnectionString = appInsights.properties.ConnectionString


// Create target service: Azure Keyvault

module keyvaultDeployment 'keyvault.bicep' = {
    name: 'keyvault-deployment'
    params: {
        location: location
        name: keyVaultName
    }
    dependsOn: []
}
var keyvaultEndpoint = keyvaultDeployment.outputs.endpoint
var keyvaultScope = keyvaultDeployment.outputs.scope


// Create compute service: Azure Container App

module apiAppDeployment 'containerapp.bicep' = {
    name: 'api-app-deployment'
    params: {
        location: location
        name: apiAppName
        containerEnv: [{
            name: 'AZURE_COSMOS_CONNECTION_STRING'
            value: cosmosConnectionString
        },{
            name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
            value: appInsightsConnectionString
        },{
            name: 'AZURE_KEY_VAULT_ENDPOINT'
            value: keyvaultEndpoint
        },{
            name: 'AZURE_KEYVAULT_SCOPE'
            value: keyvaultScope
        }]
    }
    dependsOn: []
}
var appSystemIdentityPrinciaplId = apiAppDeployment.outputs.identityPrincipalId


// Create compute service: Azure Container App

module webAppDeployment 'containerapp.bicep' = {
    name: 'web-app-deployment'
    params: {
        location: location
        name: webAppName
        containerEnv: [{
            name: 'REACT_APP_APPLICATIONINSIGHTS_CONNECTION_STRING'
            value: appInsightsConnectionString
        }]
    }
    dependsOn: [apiAppDeployment]
}


// Create access policy for Azure Keyvault

module keyvaultAccessPolicyDeployment 'keyvault.accesspolicy.bicep' = {
    name: 'keyvault-access-policy-deployment'
    params: {
        keyVaultName: keyVaultName
        principalId: appSystemIdentityPrinciaplId
    }
    dependsOn: [keyvaultDeployment]
}