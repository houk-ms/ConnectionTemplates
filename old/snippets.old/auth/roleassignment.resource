resource roleAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  scope: {{ROLE_ASSIGNMENT_SCOPE}}
  name: guid({{PRINCIPAL_ID}}, {{ROLE_DEFINITION_ID}}, resourceGroup().id)
  properties: {
    roleDefinitionId: resourceId('Microsoft.Authorization/roleDefinitions', {{ROLE_DEFINITION_ID}})
    principalId: {{PRINCIPAL_ID}}
  }
}