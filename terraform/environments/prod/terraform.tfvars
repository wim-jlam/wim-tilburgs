# 🚀 Production Environment Configuration
# terraform/environments/prod/terraform.tfvars

environment   = "prod"
azure_region  = "West Europe"
project_name  = "wimtilburgs"
custom_domain = "wimtilburgs.nl"

# Database configuration voor prod - high availability
database_config = {
  sku_name                     = "GP_Gen5_2"  # General Purpose, 2 vCores
  storage_mb                   = 51200        # 50GB
  backup_retention_days        = 35           # Lange retentie voor prod
  geo_redundant_backup_enabled = true         # Geo-redundancy voor disaster recovery
  auto_grow_enabled           = true
  ssl_enforcement_enabled     = true
}

# Container config - krachtige instances voor prod AI workloads
container_config = {
  cpu    = 2.0  # 2 vCPUs
  memory = 4.0  # 4GB RAM
}

# Static Web App - Standard tier voor prod features
static_web_app_config = {
  sku_tier = "Standard"  # Betaalde tier voor prod features
}

# AI Services configuratie voor prod
ai_services_config = {
  openai_model       = "gpt-5"     # GPT-5 voor prod (wanneer beschikbaar)
  max_tokens        = 4000        # Hogere limiet voor prod
  temperature       = 0.7
  enable_monitoring = true
}

# Monitoring - volledig voor prod
monitoring_config = {
  log_retention_days = 90          # Langere retentie voor compliance
  enable_alerts     = true         # Wel alerts voor prod
  alert_email       = "wim@jlam.nl"
}

# Security - maximaal voor prod
security_config = {
  enable_waf     = true   # Web Application Firewall voor prod
  enable_ddos    = true   # DDoS protection voor prod
  key_vault_sku  = "premium"  # Premium Key Vault voor HSM
  ssl_policy     = "TLS_1_2"
}

# Tags specifiek voor prod
common_tags = {
  Project      = "wimtilburgs.nl"
  Environment  = "prod"
  ManagedBy    = "terraform"
  Owner        = "wim@jlam.nl"
  Purpose      = "AI Health Platform Production"
  CostCenter   = "JLAM-SmartHealth"
  Compliance   = "GDPR"
  Backup       = "required"
  HighAvailability = "true"
}