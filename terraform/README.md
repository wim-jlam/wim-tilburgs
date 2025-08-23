# 🏗️ Terraform Infrastructure - wimtilburgs.nl Platform

*AI Health Platform Infrastructure as Code*  
*Laatste update: 2025-08-23*

---

## 🎯 Overzicht

Deze Terraform configuratie bouwt een schaalbare Azure infrastructure voor het wimtilburgs.nl AI Health platform, inclusief:

- **Frontend**: Azure Static Web Apps (React TypeScript)
- **AI Services**: Container Instances voor GPT-5/AI workloads  
- **Database**: PostgreSQL Flexible Server
- **Security**: Key Vault, WAF, DDoS protection
- **Monitoring**: Application Insights, Log Analytics
- **Networking**: VNet met subnets voor microservices

---

## 📁 Project Structuur

```
terraform/
├── main.tf                    # Main infrastructure
├── variables.tf              # Variable definitions  
├── outputs.tf               # Output values
├── README.md                # This file
├── environments/
│   ├── dev/
│   │   └── terraform.tfvars  # Dev environment config
│   ├── staging/
│   │   └── terraform.tfvars  # Staging environment config
│   └── prod/
│       └── terraform.tfvars  # Production environment config
└── modules/
    ├── networking/          # VNet, subnets, NSG
    ├── compute/            # Container instances, AKS
    ├── database/           # PostgreSQL configuration
    └── security/           # Key Vault, certificates
```

---

## 🚀 Quick Start

### 1. Prerequisites

```bash
# Terraform geïnstalleerd
terraform --version  # >= 1.0

# Azure CLI geïnstalleerd en ingelogd
az login

# Terraform Cloud account (voor remote state)
# - Organisatie: jlam-smarthealth
# - Workspace: wimtilburgs-platform
```

### 2. Initialize Terraform

```bash
# Clone repository
cd /Users/wimtilburgs/Development/cia-app/terraform

# Initialize Terraform (eerste keer)
terraform init
```

### 3. Plan en Apply

```bash
# Development environment
terraform plan -var-file="environments/dev/terraform.tfvars"
terraform apply -var-file="environments/dev/terraform.tfvars"

# Production environment  
terraform plan -var-file="environments/prod/terraform.tfvars"
terraform apply -var-file="environments/prod/terraform.tfvars"
```

---

## 🏗️ Infrastructure Components

### 🔧 Core Resources

| Resource | Purpose | Environment |
|----------|---------|-------------|
| Resource Group | Container voor alle resources | alle |
| Storage Account | Static assets, Terraform state | alle |  
| Key Vault | API keys, secrets, certificates | alle |
| Log Analytics | Centralized logging | alle |
| Application Insights | APM, monitoring | alle |

### 🌐 Networking

| Resource | Purpose | Environment |
|----------|---------|-------------|
| Virtual Network | Isolated network voor services | alle |
| Subnet (containers) | Container instances | alle |
| Network Security Group | Firewall rules | alle |
| DDoS Protection | DDoS mitigation | prod only |

### 🐳 Compute (Toekomstig)

| Resource | Purpose | Environment |
|----------|---------|-------------|
| Container Registry | Docker images voor AI services | alle |
| Container Instances | AI workloads (GPT-5, etc.) | alle |
| App Service Plan | Backup compute | staging/prod |

### 🗄️ Database (Toekomstig)

| Resource | Purpose | Environment |
|----------|---------|-------------|
| PostgreSQL Flexible | Main database | alle |
| Private Endpoint | Secure database access | prod |
| Backup Vault | Database backups | prod |

---

## 🔒 Security & Compliance

### 🛡️ Security Features

- **Key Vault**: Alle secrets en certificates
- **Managed Identity**: No hardcoded credentials
- **Private Endpoints**: Database niet public accessible  
- **NSG Rules**: Network access control
- **SSL/TLS**: Encryption in transit
- **Disk Encryption**: Encryption at rest

### 📋 Compliance

- **GDPR**: EU data residency (West Europe)
- **HIPAA Ready**: Healthcare data protection patterns
- **SOC 2**: Logging en monitoring
- **Backup**: Automated backup strategies

---

## 💰 Cost Optimization

### 📊 Environment Costs (Geschat)

| Environment | Monthly Cost | Key Resources |
|------------|--------------|---------------|
| **Dev** | €50-75 | Basic tier, auto-shutdown | 
| **Staging** | €150-200 | Mid-tier, limited hours |
| **Prod** | €300-500 | High availability, 24/7 |

### 💡 Cost Saving Tips

```bash
# Auto-shutdown voor dev resources (add to terraform)
resource "azurerm_dev_test_global_vm_shutdown_schedule" "dev" {
  count = var.environment == "dev" ? 1 : 0
  # ... configuration
}

# Use Azure reservations voor prod (1-3 jaar commitment)
# Use spot instances voor non-critical workloads
# Monitor via Azure Cost Management
```

---

## 🔄 CI/CD Integration

### 🤖 GitHub Actions Workflow

```yaml
# .github/workflows/terraform.yml (voorbeeld)
name: Terraform Deploy

on:
  push:
    branches: [main]
    paths: ['terraform/**']

jobs:
  terraform:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Terraform
        uses: hashicorp/setup-terraform@v2
        with:
          terraform_version: 1.5.0
          
      - name: Terraform Plan
        run: |
          terraform init
          terraform plan -var-file="environments/${{ env.ENVIRONMENT }}/terraform.tfvars"
```

### 🔐 Required Secrets

In GitHub repository settings:

```bash
# Azure Service Principal
AZURE_CLIENT_ID=[service-principal-app-id]
AZURE_CLIENT_SECRET=[service-principal-secret]
AZURE_SUBSCRIPTION_ID=[subscription-id]
AZURE_TENANT_ID=[tenant-id]

# Terraform Cloud
TF_API_TOKEN=[terraform-cloud-api-token]
```

---

## 🛠️ Commands Reference

### 📝 Daily Operations

```bash
# Check current state
terraform show

# Plan changes
terraform plan -var-file="environments/dev/terraform.tfvars"

# Apply changes
terraform apply -var-file="environments/dev/terraform.tfvars"

# Destroy environment (BE CAREFUL!)
terraform destroy -var-file="environments/dev/terraform.tfvars"

# Format code
terraform fmt -recursive

# Validate configuration
terraform validate

# View outputs
terraform output
```

### 🔍 Troubleshooting

```bash
# Enable debug logging
export TF_LOG=DEBUG

# Check Azure resources
az resource list --resource-group [resource-group-name]

# Terraform state commands
terraform state list
terraform state show [resource-name]

# Import existing resources
terraform import [resource-type].[resource-name] [azure-resource-id]
```

---

## 🚦 Environments

### 🔧 Development
- **Purpose**: Feature development en testing
- **Resources**: Minimal, cost-optimized
- **Data**: Non-production, dummy data
- **Uptime**: Business hours only

### 🧪 Staging  
- **Purpose**: Pre-production testing
- **Resources**: Production-like maar smaller
- **Data**: Sanitized production data
- **Uptime**: Extended business hours

### 🚀 Production
- **Purpose**: Live platform
- **Resources**: High availability, scaled
- **Data**: Real user data, GDPR compliant
- **Uptime**: 24/7 with SLA

---

## 📞 Support & Troubleshooting

### 🆘 Common Issues

1. **"Backend configuration changed"**
   ```bash
   terraform init -reconfigure
   ```

2. **"Resource already exists"**
   ```bash
   terraform import [resource-type].[name] [azure-id]
   ```

3. **State lock issues**
   ```bash
   terraform force-unlock [lock-id]
   ```

### 📚 Documentation Links

- [Azure Provider Documentation](https://registry.terraform.io/providers/hashicorp/azurerm/latest/docs)
- [Terraform Cloud Documentation](https://www.terraform.io/cloud/docs)
- [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)

---

**🎯 Volgende Stappen:**

1. ✅ Terraform workspace configureren in Terraform Cloud
2. ✅ Azure Service Principal aanmaken voor CI/CD
3. ✅ Development environment deployen
4. ⏳ Database module toevoegen
5. ⏳ Container instances voor AI services
6. ⏳ Production environment setup

---

*"Infrastructure as Code = Reproducible, Scalable, Reliable"* 🚀