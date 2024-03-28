output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "container_app_id" {
  value = azurerm_container_app.aca.id
}

output "storage_account_id" {
  value = azurerm_storage_account.storage_account.id
}
