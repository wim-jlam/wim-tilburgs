# 🔷 Azure Deployment Plan - wimtilburgs.nl SmartHealth App

*Datum: 23 augustus 2025*  
*Azure Sponsorship: €3000/jaar beschikbaar*

---

## 📍 Huidige Azure Resources

### Databases:
- **jlampostgres** - Flexibele PostgreSQL server (ACTIEF)
- **jlam** - SQL Server (ACTIEF)
- **ZWEM** - SQL database (ACTIEF)

### Containers:
- **mijnleefstijlregister** - Container Registry
- **leefstijlkaart02-container** - Container Instances

### Resource Groups:
- **Stichting** - Hoofdgroep
- **myLeefstijlKaart** - App resources
- **hugo_rg_0309** - Test resources

---

## 🎯 Deployment Strategy voor wimtilburgs.nl

### Fase 1: Database Setup
```sql
-- Gebruik bestaande jlampostgres
-- Database: smarthealth_prod
-- Schema voor:
  - Users (transformatie verhalen)
  - Blog posts (Jalal & Jamal content)
  - AI interactions (GPT-5 logs)
  - Health metrics (glucose, gewicht, etc)
```

### Fase 2: Container Deployment
```dockerfile
# Dockerfile voor CIA/SmartHealth app
FROM python:3.9-slim

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy app
COPY . /app
WORKDIR /app

# Environment
ENV AZURE_POSTGRESQL_HOST=jlampostgres.postgres.database.azure.com
ENV AZURE_POSTGRESQL_USER=jlam_admin
ENV AZURE_POSTGRESQL_DB=smarthealth

# Run
CMD ["python", "app.py"]
```

### Fase 3: Azure Services Toevoegen

#### 1. Azure App Service
```bash
# Web App voor wimtilburgs.nl
az webapp create \
  --resource-group Stichting \
  --plan SmartHealthPlan \
  --name wimtilburgs \
  --runtime "PYTHON|3.9"
```

#### 2. Azure AI Services
```bash
# Cognitive Services voor AI features
az cognitiveservices account create \
  --name smarthealth-ai \
  --resource-group Stichting \
  --kind CognitiveServices \
  --sku F0 \
  --location westeurope
```

#### 3. Azure Storage
```bash
# Blob storage voor documents/images
az storage account create \
  --name smarthealthstorage \
  --resource-group Stichting \
  --sku Standard_LRS
```

---

## 🔐 Connection Strings

### PostgreSQL Connection:
```python
# Voor CIA app
AZURE_DB_CONFIG = {
    'host': 'jlampostgres.postgres.database.azure.com',
    'database': 'smarthealth',
    'user': 'jlam_admin@jlampostgres',
    'password': os.getenv('AZURE_DB_PASSWORD'),  # Uit 1Password
    'port': 5432,
    'sslmode': 'require'
}
```

### Container Registry:
```bash
# Login naar registry
az acr login --name mijnleefstijlregister

# Push image
docker tag cia-app mijnleefstijlregister.azurecr.io/smarthealth:latest
docker push mijnleefstijlregister.azurecr.io/smarthealth:latest
```

---

## 💰 Kosten Optimalisatie

### Gratis/Goedkoop met Sponsorship:
- **PostgreSQL**: ~€15/maand (Flexible Server)
- **App Service**: ~€10/maand (Basic tier)
- **Storage**: ~€5/maand (Standard)
- **AI Services**: F0 tier = GRATIS!

**Totaal: ~€30/maand = €360/jaar**  
**Budget: €3000/jaar**  
**Over: €2640/jaar voor groei!**

---

## 🚀 Quick Deploy Commands

### Stap 1: Resource Group Check
```bash
az group show --name Stichting
```

### Stap 2: PostgreSQL Database Maken
```bash
az postgres flexible-server db create \
  --resource-group Stichting \
  --server-name jlampostgres \
  --database-name smarthealth
```

### Stap 3: Web App Deployen
```bash
# Via GitHub Actions of Azure DevOps
az webapp deployment source config \
  --name wimtilburgs \
  --resource-group Stichting \
  --repo-url https://github.com/wimtilburgs/smarthealth \
  --branch main
```

### Stap 4: Custom Domain
```bash
az webapp config hostname add \
  --webapp-name wimtilburgs \
  --resource-group Stichting \
  --hostname wimtilburgs.nl
```

---

## 📊 Architecture Diagram

```
┌─────────────────────────────────────────┐
│          wimtilburgs.nl                 │
│         (Custom Domain)                 │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│      Azure App Service                  │
│      (SmartHealth Web App)              │
│      - Python/Flask                     │
│      - GPT-5, Gemini, Azure AI          │
└────────┬───────────────┬────────────────┘
         │               │
         ▼               ▼
┌──────────────┐  ┌─────────────────┐
│ PostgreSQL   │  │ Blob Storage    │
│ jlampostgres │  │ Documents/Media │
└──────────────┘  └─────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│        Azure AI Services                │
│  - Text Analytics                       │
│  - Translation                          │
│  - Computer Vision                      │
└─────────────────────────────────────────┘
```

---

## ✅ Next Steps

1. [ ] PostgreSQL database 'smarthealth' aanmaken
2. [ ] CIA app containerizen met Docker
3. [ ] Push naar Azure Container Registry
4. [ ] Deploy naar App Service
5. [ ] DNS configureren voor wimtilburgs.nl
6. [ ] SSL certificaat activeren
7. [ ] Monitoring opzetten

---

## 🎯 Eindresultaat

**wimtilburgs.nl** draait op Azure met:
- ✅ CIA Platform (GPT-5, Gemini, Azure AI)
- ✅ Blog met Jalal & Jamal content
- ✅ SmartHealth tools
- ✅ PostgreSQL database
- ✅ Schaalbaar tot 10,000+ users
- ✅ Binnen €3000/jaar budget

---

*"Van lokale app naar Azure cloud - SmartHealth goes global!"*