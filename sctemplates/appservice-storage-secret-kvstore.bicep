targetScope = 'subscription'


param appServiceName string = ''
param appServicePlanName string = ''
param keyVaultName string = ''
param location string = ''
param resourceGroupName string = ''
param storageAccountName string = ''


// Scope: Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: resourceGroupName
  location: location
}

// Source: App Service Plan
module appServicePlan './source/appserviceplan.bicep' = {
  name: 'app-service-plan'
  scope: rg
  params: {
    name: appServicePlanName
    location: location
    sku: {
      name: 'B1'
    }
  }
}

// Source: App Service
module appService './source/appservice.bicep' = {
  name: 'app-service'
  scope: rg
  params: {
    name: appServiceName
    location: location
    appServicePlanId: appServicePlan.outputs.id
    keyVaultName: keyVaultName
    runtimeName: 'dotnetcore'
    runtimeVersion: '6.0'
  }
}

// Target: Storage Account
module storageAccount './target/storage/storage-account.bicep' = {
  name: 'storage-account'
  scope: rg
  params: {
    name: storageAccountName
    location: location
    keyVaultName: keyVaultName
  }
}

// Secret Store: Key Vault
module keyVault './auth/keyvault.bicep' = {
  name: 'keyvault'
  scope: rg
  params: {
    name: keyVaultName
    location: location
  }
}

// AppSettings
module webAppSettings './source/appservice-appsettings.bicep' = {
  name: 'app-settings'
  scope: rg
  params: {
    name: appServiceName
    appSettings: {
      StorageConnectionString: storageAccount.outputs.connectionStringKey
    }
  }
}

// RoleAssignment: AppService => KeyVault
module apiKeyVaultAccess './auth/keyvault-access.bicep' = {
  name: 'api-keyvault-access'
  scope: rg
  params: {
    keyVaultName: keyVault.outputs.name
    principalId: appService.outputs.identityPrincipalId
  }
}

