resource "azurerm_container_app_environment" "aca_env" {
  name                       = "${var.resource_prefix}-aca-env"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.log_analytics_workspace.id
}