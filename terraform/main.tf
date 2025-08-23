# 🚀 Terraform Configuration voor wimtilburgs.nl Platform
# Laatste update: 2025-08-23
# Doel: Scalable AI Health Platform met SSO en microservices

terraform {
  required_version = ">= 1.0"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~>3.0"
    }
    azuread = {
      source  = "hashicorp/azuread"
      version = "~>2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "~>3.0"
    }
  }

  # Remote state - gebruik jouw Terraform Cloud workspace
  backend "remote" {
    organization = "jlam-smarthealth"
    workspaces {
      name = "wimtilburgs-platform"
    }
  }
}

# Configure Azure Provider
provider "azurerm" {
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}

# Configure Azure AD Provider
provider "azuread" {}

# Random string for unique naming
resource "random_id" "main" {
  byte_length = 4
}

# Local values voor consistente naming
locals {
  project_name = "wimtilburgs"
  environment  = var.environment
  location     = var.azure_region
  
  # Naming convention: wimtilburgs-dev-rg-a1b2c3d4
  resource_suffix = random_id.main.hex
  
  common_tags = {
    Project     = "wimtilburgs.nl"
    Environment = var.environment
    ManagedBy   = "terraform"
    Owner       = "wim@jlam.nl"
    Purpose     = "AI Health Platform"
    CostCenter  = "JLAM-SmartHealth"
  }
}

# Main Resource Group
resource "azurerm_resource_group" "main" {
  name     = "${local.project_name}-${local.environment}-rg-${local.resource_suffix}"
  location = local.location
  tags     = local.common_tags
}

# Storage Account voor Terraform state en assets
resource "azurerm_storage_account" "main" {
  name                     = "${local.project_name}st${local.resource_suffix}"
  resource_group_name      = azurerm_resource_group.main.name
  location                = azurerm_resource_group.main.location
  account_tier            = "Standard"
  account_replication_type = var.environment == "prod" ? "GRS" : "LRS"
  
  # Security settings
  min_tls_version                = "TLS1_2"
  allow_nested_items_to_be_public = false
  
  tags = local.common_tags
}

# Container voor static assets
resource "azurerm_storage_container" "assets" {
  name                  = "assets"
  storage_account_name  = azurerm_storage_account.main.name
  container_access_type = "blob"
}

# Log Analytics Workspace voor monitoring
resource "azurerm_log_analytics_workspace" "main" {
  name                = "${local.project_name}-${local.environment}-logs-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku                = "PerGB2018"
  retention_in_days   = var.environment == "prod" ? 90 : 30
  
  tags = local.common_tags
}

# Application Insights voor monitoring
resource "azurerm_application_insights" "main" {
  name                = "${local.project_name}-${local.environment}-ai-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  workspace_id        = azurerm_log_analytics_workspace.main.id
  application_type    = "web"
  
  tags = local.common_tags
}

# Key Vault voor secrets (API keys, etc.)
resource "azurerm_key_vault" "main" {
  name                = "${local.project_name}-${local.environment}-kv-${local.resource_suffix}"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  tenant_id          = data.azurerm_client_config.current.tenant_id
  sku_name           = "standard"
  
  # Security settings
  purge_protection_enabled   = var.environment == "prod" ? true : false
  soft_delete_retention_days = 7
  
  tags = local.common_tags
}

# Current Azure configuration
data "azurerm_client_config" "current" {}

# Key Vault access policy voor Terraform service principal
resource "azurerm_key_vault_access_policy" "terraform" {
  key_vault_id = azurerm_key_vault.main.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = data.azurerm_client_config.current.object_id
  
  secret_permissions = [
    "Get",
    "Set",
    "List",
    "Delete",
    "Purge"
  ]
}

# Container Registry voor Docker images (toekomstige AI services)
resource "azurerm_container_registry" "main" {
  name                = "${local.project_name}cr${local.resource_suffix}"
  resource_group_name = azurerm_resource_group.main.name
  location           = azurerm_resource_group.main.location
  sku                = var.environment == "prod" ? "Premium" : "Basic"
  admin_enabled      = true
  
  tags = local.common_tags
}

# Virtual Network voor toekomstige microservices
resource "azurerm_virtual_network" "main" {
  name                = "${local.project_name}-${local.environment}-vnet-${local.resource_suffix}"
  address_space       = ["10.0.0.0/16"]
  location           = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  tags = local.common_tags
}

# Subnet voor Container Instances
resource "azurerm_subnet" "containers" {
  name                 = "containers"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.1.0/24"]
  
  delegation {
    name = "container-instances"
    service_delegation {
      name    = "Microsoft.ContainerInstance/containerGroups"
      actions = ["Microsoft.Network/virtualNetworks/subnets/action"]
    }
  }
}

# Network Security Group
resource "azurerm_network_security_group" "main" {
  name                = "${local.project_name}-${local.environment}-nsg-${local.resource_suffix}"
  location           = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  
  # Allow HTTPS inbound
  security_rule {
    name                       = "HTTPS"
    priority                   = 1001
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "443"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  
  # Allow HTTP inbound (redirect to HTTPS)
  security_rule {
    name                       = "HTTP"
    priority                   = 1002
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "80"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
  
  tags = local.common_tags
}