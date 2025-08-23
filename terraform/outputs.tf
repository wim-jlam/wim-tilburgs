# 🔍 Terraform Outputs voor wimtilburgs.nl Platform
# Belangrijke waarden die andere systemen nodig hebben

# Resource Group information
output "resource_group_name" {
  description = "Name of the main resource group"
  value       = azurerm_resource_group.main.name
}

output "resource_group_location" {
  description = "Location of the main resource group"
  value       = azurerm_resource_group.main.location
}

# Storage Account information
output "storage_account_name" {
  description = "Name of the main storage account"
  value       = azurerm_storage_account.main.name
}

output "storage_account_primary_endpoint" {
  description = "Primary endpoint URL of the storage account"
  value       = azurerm_storage_account.main.primary_blob_endpoint
}

# Container Registry information (voor AI services)
output "container_registry_name" {
  description = "Name of the container registry"
  value       = azurerm_container_registry.main.name
}

output "container_registry_login_server" {
  description = "Login server URL of the container registry"
  value       = azurerm_container_registry.main.login_server
}

output "container_registry_admin_username" {
  description = "Admin username for container registry"
  value       = azurerm_container_registry.main.admin_username
  sensitive   = true
}

# Key Vault information
output "key_vault_name" {
  description = "Name of the Key Vault"
  value       = azurerm_key_vault.main.name
}

output "key_vault_uri" {
  description = "URI of the Key Vault"
  value       = azurerm_key_vault.main.vault_uri
}

# Monitoring information
output "log_analytics_workspace_id" {
  description = "Log Analytics Workspace ID"
  value       = azurerm_log_analytics_workspace.main.workspace_id
  sensitive   = true
}

output "application_insights_instrumentation_key" {
  description = "Application Insights instrumentation key"
  value       = azurerm_application_insights.main.instrumentation_key
  sensitive   = true
}

output "application_insights_connection_string" {
  description = "Application Insights connection string"
  value       = azurerm_application_insights.main.connection_string
  sensitive   = true
}

# Networking information
output "virtual_network_name" {
  description = "Name of the virtual network"
  value       = azurerm_virtual_network.main.name
}

output "containers_subnet_id" {
  description = "ID of the containers subnet"
  value       = azurerm_subnet.containers.id
}

# Environment information
output "environment" {
  description = "Current environment"
  value       = var.environment
}

output "project_name" {
  description = "Project name"
  value       = var.project_name
}

# URLs en endpoints voor GitHub Actions
output "github_actions_outputs" {
  description = "Important values for GitHub Actions workflows"
  value = {
    resource_group_name    = azurerm_resource_group.main.name
    storage_account_name   = azurerm_storage_account.main.name
    key_vault_name        = azurerm_key_vault.main.name
    app_insights_key      = azurerm_application_insights.main.instrumentation_key
    container_registry    = azurerm_container_registry.main.login_server
  }
  sensitive = true
}

# Connection strings voor applicaties
output "connection_strings" {
  description = "Connection strings for applications"
  value = {
    storage_account = azurerm_storage_account.main.primary_connection_string
    app_insights   = azurerm_application_insights.main.connection_string
  }
  sensitive = true
}

# Terraform state informatie
output "terraform_state_info" {
  description = "Information about Terraform state"
  value = {
    environment     = var.environment
    last_updated   = timestamp()
    resource_count = "calculated_at_apply"
    azure_region   = var.azure_region
  }
}