resource "azurerm_container_app" "aca" {
  name                         = "${var.resource_prefix}-aca"
  container_app_environment_id = azurerm_container_app_environment.aca_env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  secret {
    name = "storage-key"
    value = azurerm_storage_account.storage_account.primary_access_key 
  }

  template {
    container {
      name   = "examplecontainerapp"
      image  = "mcr.microsoft.com/azuredocs/containerapps-helloworld:latest"
      cpu    = 0.25
      memory = "0.5Gi"

      env {
        name = "${var.env_var_prefix}_STORAGE_ACCESS_KEY"
        secret_name = "storage-key"
      }
    }
  }

  # identity {
  #   type = "SystemAssigned"
  # }
}