// In order to make the templates more readable, we use only the mininal set of 
// parameters to create the resource, and we provide default value for every parameter. 

param name string = 'plan_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param kind string = 'linux'
param reserved bool = true
param sku string = 'B1'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {
  name: name
  location: location
  kind: kind
  sku: {
    name: sku
  }
  properties: {
    reserved: reserved
  }
}

output id string = appServicePlan.id
output name string = appServicePlan.name
