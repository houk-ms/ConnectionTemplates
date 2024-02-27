// The main bicep to create compute and target services with connections

param storageAccountName string = 'account${uniqueString(resourceGroup().id)}'
param keyVaultName string = 'vault-${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param webAppName string = 'webapp-${uniqueString(resourceGroup().id)}'


// Create target service: Azure Storage Account

module storageAccountDeployment 'storageaccount.bicep' = {
    name: 'storage-account-deployment'
    params: {
        location: location
        name: storageAccountName
    }
}
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
    name: storageAccountName
}
var storageConnectionString = 'DefaultEndpointsProtocol=https;AccountName=${storageAccount.name};AccountKey=${storageAccount.listKeys().keys[0].value};BlobEndpoint=${storageAccount.properties.primaryEndpoints.blob};FileEndpoint=${storageAccount.properties.primaryEndpoints.file};TableEndpoint=${storageAccount.properties.primaryEndpoints.table};QueueEndpoint=${storageAccount.properties.primaryEndpoints.queue};'


// Create keyvault secret for: Azure Storage Account

module storageKeyvaultSecretDeployment 'keyvault.secret.bicep' = {
    name: 'storage-keyvault-secret-deployment'
    params: {
        keyVaultName: keyVaultName
        name: 'storage-secret'
        secretValue: storageConnectionString
    }
}
var storageSecretReference = storageKeyvaultSecretDeployment.outputs.appServiceSecretRefernece


// Create target service: Azure Keyvault

module keyvaultDeployment 'keyvault.bicep' = {
    name: 'keyvault-deployment'
    params: {
        location: location
        name: keyVaultName
    }
}
var keyvaultEndpoint = keyvaultDeployment.outputs.endpoint
var keyvaultScope = keyvaultDeployment.outputs.scope


// Create compute service: Azure WebApp

module appServiceDeployment 'webapp.bicep' = {
    name: 'app-service-deployment'
    params: {
        location: location
        name: webAppName
        appSettings: [{
            name: 'AZURE_STORAGEACCOUNT_CONNECTIONSTRING'
            value: storageSecretReference
        },{
            name: 'AZURE_KEYVAULT_RESOURCEENDPOINT'
            value: keyvaultEndpoint
        },{
            name: 'AZURE_KEYVAULT_SCOPE'
            value: keyvaultScope
        }]
    }
}
var appSystemIdentityPrinciaplId = appServiceDeployment.outputs.identityPrincipalId
var outboundIps = split(appServiceDeployment.outputs.outboundIps, ',')


// Create access policy for Azure Keyvault

module keyvaultAccessPolicyDeployment 'keyvault.accesspolicy.bicep' = {
    name: 'keyvault-access-policy-deployment'
    params: {
        principalId: appSystemIdentityPrinciaplId
    }
}


// Create firewall rules for Azure Storage Account

module storageFirewallDeployment 'storageaccount.firewall.bicep' = {
    name: 'storage-firewall-deployment'
    params: {
        name: storageAccountName
        location: location
        allowIps: outboundIps
    }
}


// Create firewall rules for Azure Keyvault

module keyvaultFirewallDeployment 'keyvault.firewall.bicep' = {
    name: 'keyvault-firewall-deployment'
    params: {
        name: keyVaultName
        location: location
        allowIps: outboundIps
    }
}