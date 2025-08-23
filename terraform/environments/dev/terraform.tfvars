# 🔧 Development Environment Configuration
# terraform/environments/dev/terraform.tfvars

environment   = "dev"
azure_region  = "West Europe"
project_name  = "wimtilburgs"
custom_domain = "dev.wimtilburgs.nl"

# Database configuration voor dev
database_config = {
  sku_name                     = "B_Gen5_1"  # Basic tier - goedkoop voor dev
  storage_mb                   = 5120        # 5GB
  backup_retention_days        = 7           # Korte retentie voor dev
  geo_redundant_backup_enabled = false       # Geen geo-redundancy voor dev
  auto_grow_enabled           = true
  ssl_enforcement_enabled     = true
}

# Container config - kleine instances voor dev
container_config = {
  cpu    = 0.5  # Half vCPU
  memory = 1.0  # 1GB RAM
}

# Static Web App - Free tier
static_web_app_config = {
  sku_tier = "Free"
}

# AI Services configuratie voor dev
ai_services_config = {
  openai_model       = "gpt-4"  # Start met GPT-4, upgrade later naar GPT-5
  max_tokens        = 1500      # Lager voor dev om kosten te sparen
  temperature       = 0.7
  enable_monitoring = true
}

# Monitoring - basis voor dev
monitoring_config = {
  log_retention_days = 30
  enable_alerts     = false      # Geen alerts voor dev
  alert_email       = "wim@jlam.nl"
}

# Security - minimaal voor dev
security_config = {
  enable_waf     = false  # Geen WAF voor dev
  enable_ddos    = false  # Geen DDoS protection voor dev
  key_vault_sku  = "standard"
  ssl_policy     = "TLS_1_2"
}

# Tags specifiek voor dev
common_tags = {
  Project     = "wimtilburgs.nl"
  Environment = "dev"
  ManagedBy   = "terraform"
  Owner       = "wim@jlam.nl"
  Purpose     = "AI Health Platform Development"
  CostCenter  = "JLAM-SmartHealth"
  AutoShutdown = "true"  # Voor cost optimization
}