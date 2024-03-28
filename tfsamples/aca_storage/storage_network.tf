resource "azurerm_storage_account_network_rules" "storage_network" {
  storage_account_id = azurerm_storage_account.storage_account.id

  default_action             = "Deny"
  ip_rules                   = azurerm_container_app.aca.outbound_ip_addresses
}