output "container_app_url" {
  description = "URL of the deployed container app"
  value       = azurerm_container_app.gpteasers.latest_revision_fqdn
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.gpteasers.name
}

output "container_app_environment_name" {
  description = "Name of the container app environment"
  value       = azurerm_container_app_environment.gpteasers.name
}