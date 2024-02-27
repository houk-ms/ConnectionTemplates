resource storageAccount 'Microsoft.Storage/storageAccounts@2023-01-01' = {
  name: storageAccountName
  location: storageAccountLocation
  sku: {
    name: storageAccountSku
  }
  kind: storageAccountKind
}