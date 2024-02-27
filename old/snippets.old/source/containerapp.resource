resource containerApp 'Microsoft.Web/containerApps@2022-09-01' = {
  name: containerAppName
  location: containerAppLocation
  properties: {
    kubeEnvironmentId: containerAppEnvironment.id
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
          name: containerAppContainerName
          image: containerAppContainerImage
        }
      ]
    }
  }
}