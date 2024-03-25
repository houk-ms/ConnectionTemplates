// The template to create a role assignment on storage

param storageAccountName string = 'account${uniqueString(resourceGroup().id)}'
param name string = guid(resourceGroup().id, storageAccountName, roleDefinitionId)
param roleDefinitionId string = 'ba92f5b4-2d11-453d-a403-e96b0029c9fe'  // storage blob data contributor role
param principalId string


resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
  name: storageAccountName
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: name
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
    principalId: principalId
  }
}


output id string = roleAssignment.id
