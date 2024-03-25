// The template to create a container app

param name string = 'aca_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param containerName string = 'helloworld'
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
param containerRegistryName string = 'acr${uniqueString(resourceGroup().id)}'
param containerEnv array = []


module containerAppEnvDeployment 'containerappenv.bicep' = {
  name: 'containerappenv-deployment'
  params: {
    location: location
  }
}

module containerRegistryDeployment 'containerregistry.bicep' = {
  name: 'containerregistry-deployment'
  params: {
    name: containerRegistryName
    location: location
  }
}

resource containerRegistry 'Microsoft.ContainerRegistry/registries@2023-07-01' existing = { 
  name: containerRegistryName
}

resource containerApp 'Microsoft.App/containerApps@2023-05-01' = {
  name: name
  location: location
  identity: {
    type: 'SystemAssigned'
  }
  properties: {
    environmentId: containerAppEnvDeployment.outputs.id
    configuration: {
      ingress: {
        external: true
        targetPort: 80
      }
      registries: [
        {
          server: containerRegistry.name
          username: containerRegistry.properties.loginServer
          passwordSecretRef: 'acr-password'
        }
      ]
      secrets: [
        {
          name: 'acr-password'
          value: containerRegistry.listCredentials().passwords[0].value
        }
      ]
    }
    template: {
      containers: [
        {
          name: containerName
          image: containerImage
          env: containerEnv
        }
      ]
    }
  }
}



output id string = containerApp.id
output name string = containerApp.name
output identityPrincipalId string = containerApp.identity.principalId
output outboundIps string[] = containerApp.properties.outboundIpAddresses
output fqdn string = containerApp.properties.configuration.ingress.fqdn
