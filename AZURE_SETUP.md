# 🚀 Azure Setup Guide - wimtilburgs.nl

*Laatste update: 2025-08-23*  
*Voor: Wim Tilburgs - Smart Health AI Consultant Platform*

---

## 🎯 Azure Deployment Overzicht

### Gekozen Azure Services:
- **Azure Static Web Apps** - Frontend hosting
- **Azure Database voor PostgreSQL** - Database
- **GitHub Actions** - CI/CD pipeline  
- **Azure CDN** - Global content delivery
- **Azure Application Insights** - Monitoring

---

## 📋 Stap-voor-stap Setup

### 1. Azure Static Web App Aanmaken

```bash
# Via Azure CLI (indien geïnstalleerd)
az staticwebapp create \
  --name "wimtilburgs-nl" \
  --resource-group "rg-wimtilburgs" \
  --source "https://github.com/[USERNAME]/wimtilburgs-nl" \
  --location "West Europe" \
  --branch "main" \
  --app-location "/" \
  --output-location "build"
```

**Of via Azure Portal:**
1. Ga naar [Azure Portal](https://portal.azure.com)
2. Create Resource > Static Web App
3. **Details invullen:**
   - Subscription: Je Microsoft non-profit subscription
   - Resource Group: `rg-wimtilburgs` (nieuw aanmaken)
   - Name: `wimtilburgs-nl`
   - Plan: `Free`
   - Region: `West Europe`

4. **Deployment details:**
   - Source: `GitHub`  
   - Organization: Je GitHub account
   - Repository: `wimtilburgs-nl` (wordt aangemaakt)
   - Branch: `main`
   - Build Presets: `React`
   - App location: `/`
   - Output location: `build`

### 2. GitHub Repository Setup

```bash
# Create GitHub repository (via web interface of CLI)
gh repo create wimtilburgs-nl --public --description "🤖 AI Motor platform voor Smart Health Consulting - Gebouwd volledig met AI"

# Connect local repository
git remote add origin https://github.com/[USERNAME]/wimtilburgs-nl.git
git push -u origin main
```

### 3. Environment Secrets Configureren

**In GitHub Repository Settings > Secrets and Variables > Actions:**

#### Required Secrets:
```
AZURE_STATIC_WEB_APPS_API_TOKEN=[wordt automatisch toegevoegd door Azure]
REACT_APP_API_URL=https://api.wimtilburgs.nl
OPENAI_API_KEY=[jouw OpenAI API key]
GOOGLE_AI_API_KEY=[jouw Google AI key]
DATABASE_URL=[Azure PostgreSQL connection string]
```

#### Optional Secrets:
```
GOOGLE_ANALYTICS_ID=G-XXXXXXXXXX
MICROSOFT_CLARITY_ID=[clarity tracking]
SMTP_USER=[email configuration]
SMTP_PASSWORD=[app password]
```

### 4. Custom Domain Setup

**In Azure Static Web App:**
1. Custom domains > Add
2. Domain: `wimtilburgs.nl`
3. Subdomain: `www.wimtilburgs.nl`
4. Validation: DNS TXT record
5. SSL: Automatic (gratis)

**DNS Records bij domain provider:**
```
Type: CNAME
Name: www
Value: [azure-static-web-app-url]

Type: TXT  
Name: @
Value: [azure-verification-code]
```

---

## 🗄️ Database Configuration

### Azure Database for PostgreSQL

```bash
# Create PostgreSQL server
az postgres server create \
  --resource-group "rg-wimtilburgs" \
  --name "wimtilburgs-postgres" \
  --location "West Europe" \
  --admin-user "wimadmin" \
  --admin-password "[STRONG_PASSWORD]" \
  --sku-name "B_Gen5_1" \
  --version "13"

# Create database
az postgres db create \
  --resource-group "rg-wimtilburgs" \
  --server-name "wimtilburgs-postgres" \
  --name "wimtilburgs_prod"
```

**Connection String Format:**
```
postgresql://wimadmin:[PASSWORD]@wimtilburgs-postgres.postgres.database.azure.com:5432/wimtilburgs_prod?sslmode=require
```

### Database Schema Deployment

```bash
# Connect to Azure database
psql "postgresql://wimadmin:[PASSWORD]@wimtilburgs-postgres.postgres.database.azure.com:5432/wimtilburgs_prod?sslmode=require"

# Run schema
\i database.sql
```

---

## 🔧 GitHub Actions Workflow

Bestand is al aangemaakt: `.github/workflows/azure-static-web-apps.yml`

**Workflow doet:**
1. ✅ Checkout code
2. ✅ Setup Node.js 18
3. ✅ Install dependencies (`npm ci`)
4. ✅ Build React app (`npm run build`)
5. ✅ Deploy naar Azure Static Web Apps
6. ✅ Handle pull request previews

---

## 🌍 SEO & Performance Optimalisaties

### Azure CDN Setup
```bash
# Create CDN profile
az cdn profile create \
  --resource-group "rg-wimtilburgs" \
  --name "wimtilburgs-cdn" \
  --location "West Europe" \
  --sku "Standard_Microsoft"
```

### Application Insights
```bash
# Create Application Insights
az monitor app-insights component create \
  --resource-group "rg-wimtilburgs" \
  --app "wimtilburgs-insights" \
  --location "West Europe" \
  --kind "web"
```

---

## 📊 Monitoring & Analytics

### Performance Monitoring
- **Azure Application Insights** - Server-side monitoring
- **Microsoft Clarity** - User behavior analytics  
- **Google Analytics 4** - Website analytics
- **Azure Monitor** - Infrastructure monitoring

### Health Checks
```javascript
// Endpoint voor health check
app.get('/api/health', (req, res) => {
  res.json({
    status: 'healthy',
    timestamp: new Date().toISOString(),
    version: process.env.REACT_APP_VERSION
  });
});
```

---

## 💰 Cost Optimization

### Geschatte Maandelijkse Kosten:
- **Azure Static Web Apps**: €0 (gratis tier)
- **PostgreSQL Basic**: ~€20/maand
- **CDN**: ~€5/maand
- **Application Insights**: €0 (1GB gratis)
- **Total**: ~€25/maand

### Microsoft Non-Profit Credits:
- **Azure Credits**: $3,500/jaar
- **GitHub Copilot**: Gratis
- **Power Platform**: Included

---

## 🔐 Security Checklist

### ✅ Implemented:
- HTTPS enforced (Azure SSL certificates)
- Environment variables voor secrets
- .env files in .gitignore
- Database SSL connections required
- GitHub Actions secrets encrypted

### 🔄 To Configure:
- Azure Key Vault voor production secrets
- Database firewall rules
- Azure Active Directory integration
- Content Security Policy headers
- Rate limiting via Azure Front Door

---

## 🚀 Deployment Commands

### Lokale Test:
```bash
# Install dependencies
npm install

# Start development server
npm start

# Build voor production
npm run build

# Test production build lokaal
npx serve -s build
```

### Production Deployment:
```bash
# Commit changes
git add .
git commit -m "feat: nieuwe feature beschrijving"

# Push naar main branch (triggert deployment)
git push origin main

# Monitor deployment
gh run list --repo [USERNAME]/wimtilburgs-nl
```

---

## 🆘 Troubleshooting

### Common Issues:

#### Build Fails:
```bash
# Check build logs in GitHub Actions
# Common fixes:
npm run build --verbose
npm audit fix
```

#### Environment Variables:
```bash
# Verify in Azure Static Web App > Configuration
# Check GitHub Secrets are set
```

#### Custom Domain Issues:
```bash
# Check DNS propagation
nslookup wimtilburgs.nl
dig wimtilburgs.nl
```

---

## 📞 Support Resources

- **Azure Support**: Microsoft non-profit support
- **GitHub Actions**: GitHub community support  
- **Documentation**: Azure Static Web Apps docs
- **Monitoring**: Application Insights dashboards

---

**🎯 Next Steps:**
1. Create GitHub repository
2. Setup Azure Static Web App via portal
3. Configure custom domain
4. Test deployment pipeline
5. Setup monitoring & analytics

**💡 Pro Tip:** Test alles eerst met een staging environment (branch deploy) voordat je naar production gaat!