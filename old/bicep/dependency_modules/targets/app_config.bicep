// In order to make the templates more readable, we use only the mininal set of 
// parameters to create the resource. 

param name string = 'sctest_appconfig'
param location string = resourceGroup().location


resource appConfig 'Microsoft.AppConfiguration/configurationStores@2023-03-01' = {
  name: name
  location: location
  sku: {
    name: 'standard'
  }
}

output name string = appConfig.name
output id string = appConfig.id
