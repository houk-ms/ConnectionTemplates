// The template to create a container app

param name string = 'aca_${uniqueString(resourceGroup().id)}'
param location string = resourceGroup().location
param containerName string = 'helloworld'
param containerImage string = 'mcr.microsoft.com/azuredocs/containerapps-helloworld:latest'
param containerRegistryName string = 'acr_${uniqueString(resourceGroup().id)}'
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

resource containerApp 'Microsoft.Web/containerApps@2022-09-01' = {
  name: name
  location: location
  properties: {
    kubeEnvironmentId: containerAppEnvDeployment.outputs.id
    configuration: {
      ingress: {
        external: true
        targetPort: 80
      }
      registries: [
        {
          server: containerRegistry.name
          username: containerRegistry.properties.loginServer
          passwordSecretRef: 'ACR_PASSWORD'
        }
      ]
      secrets: [
        {
          name: 'ACR_PASSWORD'
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
