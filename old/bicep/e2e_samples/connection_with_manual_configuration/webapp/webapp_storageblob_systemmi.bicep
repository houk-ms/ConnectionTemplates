// The template to connect a WebApp to a Storage Blob with manual configurations
// =======================================================
//   Source         :   Webapp
//   Target         :   Storage Blob
//   Connection     :   Manual Configuration
//   Authentication :   System Assigned Managed Identity
// =======================================================


param location string = resourceGroup().location
param storageAccountName string = 'account${uniqueString(resourceGroup().id)}'
param appServiceName string = 'webapp-${uniqueString(resourceGroup().id)}'
param storageBlobDataContributorRole string  = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'


// Create a Storage Account as target service
// Public network access is enabled by default
module storageAccountDeployment '../../../dependency_modules/targets/storage_account.bicep' = {
	name: 'storage-account-deployment'
	params: {
		location: location
		name: storageAccountName
	}
}
resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
	name: storageAccountName
}
var storageBlobEndpoint = storageAccount.properties.primaryEndpoints.blob


// Create a WebApp as compute service
// Save storage blob endpoint into the app settings
module appServiceDeployment '../../../dependency_modules/sources/web_app.bicep' = {
	name: 'app-service-deployment'
	params: {
	location: location
	name: appServiceName
	appSettings: [{
		name: 'AZURE_STORAGEBLOB_RESOURCEENDPOINT'
		value: storageBlobEndpoint
	}]
	}
}
var appSystemIdentityPrinciaplId = appServiceDeployment.outputs.identityPrincipalId


// Create a Role Assignment
// for the WebApp to access the Storage
module roleAssignmentDeployment '../../../dependency_modules/auths/storage_account_role_assignment.bicep' = {
  name: 'role-assignment-deployment'
  params: {
    roleAssignmentName: guid(appServiceName, storageBlobDataContributorRole, resourceGroup().id)
    principalId: appSystemIdentityPrinciaplId
    roleDefinitionId: storageBlobDataContributorRole
  }
}


output storageId string = storageAccount.id
output webAppId string = appServiceDeployment.outputs.id
