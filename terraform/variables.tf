# 🔧 Terraform Variables voor wimtilburgs.nl Platform
# Environment-specific configuratie

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
  default     = "dev"
  
  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Environment must be one of: dev, staging, prod."
  }
}

variable "azure_region" {
  description = "Azure region for resources"
  type        = string
  default     = "West Europe"
}

variable "project_name" {
  description = "Project name for resource naming"
  type        = string
  default     = "wimtilburgs"
}

# Database configuration
variable "database_config" {
  description = "PostgreSQL database configuration"
  type = object({
    sku_name                     = string
    storage_mb                   = number
    backup_retention_days        = number
    geo_redundant_backup_enabled = bool
    auto_grow_enabled           = bool
    ssl_enforcement_enabled     = bool
  })
  
  default = {
    sku_name                     = "B_Gen5_1"  # Basic tier for dev
    storage_mb                   = 5120        # 5GB
    backup_retention_days        = 7
    geo_redundant_backup_enabled = false
    auto_grow_enabled           = true
    ssl_enforcement_enabled     = true
  }
}

# Container configuration voor AI services
variable "container_config" {
  description = "Container instances configuration"
  type = object({
    cpu    = number
    memory = number
  })
  
  default = {
    cpu    = 1    # 1 vCPU
    memory = 1.5  # 1.5 GB RAM
  }
}

# Static Web App configuration
variable "static_web_app_config" {
  description = "Azure Static Web Apps configuration"
  type = object({
    sku_tier = string
  })
  
  default = {
    sku_tier = "Free"  # Free tier voor dev
  }
}

# Domain configuration
variable "custom_domain" {
  description = "Custom domain name"
  type        = string
  default     = "wimtilburgs.nl"
}

# AI Services configuration
variable "ai_services_config" {
  description = "Configuration for AI services"
  type = object({
    openai_model        = string
    max_tokens         = number
    temperature        = number
    enable_monitoring  = bool
  })
  
  default = {
    openai_model       = "gpt-4"  # Will upgrade to GPT-5 when available
    max_tokens        = 2000
    temperature       = 0.7
    enable_monitoring = true
  }
}

# Monitoring and logging
variable "monitoring_config" {
  description = "Monitoring and alerting configuration"
  type = object({
    log_retention_days = number
    enable_alerts     = bool
    alert_email       = string
  })
  
  default = {
    log_retention_days = 30
    enable_alerts     = true
    alert_email       = "wim@jlam.nl"
  }
}

# Security configuration
variable "security_config" {
  description = "Security and compliance settings"
  type = object({
    enable_waf           = bool
    enable_ddos         = bool
    key_vault_sku       = string
    ssl_policy         = string
  })
  
  default = {
    enable_waf     = false  # Enable in staging/prod
    enable_ddos    = false  # Enable in prod
    key_vault_sku  = "standard"
    ssl_policy     = "TLS_1_2"
  }
}

# Tags
variable "common_tags" {
  description = "Common tags for all resources"
  type        = map(string)
  
  default = {
    Project     = "wimtilburgs.nl"
    ManagedBy   = "terraform"
    Owner       = "wim@jlam.nl"
    Purpose     = "AI Health Platform"
    CostCenter  = "JLAM-SmartHealth"
  }
}