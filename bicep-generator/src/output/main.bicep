param location string = resourceGroup().location
param storageAccountHoukName string = 'houk${uniqueString(resourceGroup().id)}'
param containerAppHoukName string = 'houk${uniqueString(resourceGroup().id)}'
param containerAppHouk2Name string = 'houk2${uniqueString(resourceGroup().id)}'
param keyVaultHoukName string = 'houk${uniqueString(resourceGroup().id)}'
param containerAppEnvName string = 'houk${uniqueString(resourceGroup().id)}'
param containerRegistryName string = 'houk${uniqueString(resourceGroup().id)}'


// Deploy an Azure Container App environment

module containerAppEnv 'containerappenv.bicep' = {
	name: 'container-app-env-deployment'
	params: {
		location: location
		name: containerAppEnvName
	}
}
var containerAppEnvId = containerAppEnv.outputs.id


// Deploy an Azure Container Registry

module containerRegistry 'containerregistry.bicep' = {
	name: 'container-registry-deployment'
	params: {
		location: location
		name: containerRegistryName
	}
}


// Deploy an Azure Storage Account

module storageAccountHoukDeployment 'storageaccount.bicep' = {
    name: 'storage-account-houk-deployment'
    params: {
        location: location
        name: storageAccountHoukName 
        allowIps: concat(containerAppHoukOutboundIp)
        keyVaultName: keyVaultHoukName
        secretName: 'storage-account-houk-secret'
    }
    dependsOn: [
        keyVaultHoukDeployment
        containerAppHoukDeployment
    ]
    
}


// Deploy an Azure Container App

module containerAppHoukDeployment 'containerapp.bicep' = {
	name: 'container-app-houk-deployment'
	params: {
		location: location
		name: containerAppHoukName
		containerAppEnvId: containerAppEnvId
		containerRegistryName: containerRegistryName 
	}
}
var containerAppHoukPrincipalId = containerAppHoukDeployment.outputs.identityPrincipalId
var containerAppHoukOutboundIp = containerAppHoukDeployment.outputs.outboundIps


// Deploy an Azure Container App

module containerAppHouk2Deployment 'containerapp.bicep' = {
	name: 'container-app-houk2-deployment'
	params: {
		location: location
		name: containerAppHouk2Name
		containerAppEnvId: containerAppEnvId
		containerRegistryName: containerRegistryName 
	}
}


// Deploy an Azure Keyvault

module keyVaultHoukDeployment 'keyvault.bicep' = {
    name: 'key-vault-houk-deployment'
    params: {
        location: location
        name: keyVaultHoukName
        principalIds: [
            containerAppHoukPrincipalId
        ] 
        allowIps: concat(containerAppHoukOutboundIp)
    }
    dependsOn: [
        containerAppHoukDeployment
    ]
    
}


// Deploy an Azure Container App

module containerAppSettingsHoukDeployment 'containerapp.bicep' = {
	name: 'container-app-settings-houk-deployment'
	params: {
		location: location
		name: containerAppHoukName
		containerAppEnvId: containerAppEnvId
		containerRegistryName: containerRegistryName 
		containerEnv: [
			{
				name: 'AZURE_STORAGE_CONNECTION_STRING'
				value: storageAccountHoukDeployment.outputs.containerAppSecretReference
			}
			{
				name: 'AZURE_KEYVAULT_ENDPOINT'
				value: keyVaultHoukDeployment.outputs.endpoint
			}
		]
		
	}
	dependsOn: [
		storageAccountHoukDeployment
		keyVaultHoukDeployment
	]
	
}


output storageAccountHoukId string = storageAccountHoukDeployment.outputs.id
output containerAppHoukId string = containerAppHoukDeployment.outputs.id
output containerAppHouk2Id string = containerAppHouk2Deployment.outputs.id
output keyVaultHoukId string = keyVaultHoukDeployment.outputs.id
