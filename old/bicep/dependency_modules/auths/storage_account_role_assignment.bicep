// In order to make the templates more readable, we use only the mininal set of 
// parameters to create the resource. 

param storageAccountName string = 'account${uniqueString(resourceGroup().id)}'
param roleAssignmentName string = guid(resourceGroup().id, roleDefinitionId)
param principalId string
param roleDefinitionId string


resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' existing = {
  name: storageAccountName
}

resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: storageAccount
  name: roleAssignmentName
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', roleDefinitionId)
    principalId: principalId
  }
}


output id string = roleAssignment.id
