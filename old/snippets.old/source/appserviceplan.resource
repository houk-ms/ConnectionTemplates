resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: appServicePlanName
  location: appServicePlanLocation
  kind: appServicePlanKind
  sku: {
    name: appServicePlanSku
  }
  properties: {
    reserved: appServicePlanReserved
  }
}