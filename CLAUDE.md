# 🤖 CLAUDE.md - WIM TILBURGS PLATFORM PROJECT
*Laatste update: 24 augustus 2025 - 07:40*  
*Versie: 2.1.0*

---

## 🎯 STATUS UPDATE - 24 AUGUSTUS 2025

### ✅ DEPLOYMENT CRISIS VOLLEDIG OPGELOST!

**Probleem:** Na repository hernaming werkte wimtilburgs.nl niet meer - React app bleef hangen op loading screen.

**Oplossing:** Volledige Azure Static Web App herconfiguratie uitgevoerd:
1. ✅ Nieuwe repository `wim-jlam/wim-tilburgs` aangemaakt
2. ✅ Azure Static Web App geconnecteerd aan juiste repository
3. ✅ GitHub Actions secret `AZURE_STATIC_WEB_APPS_API_TOKEN` geconfigureerd  
4. ✅ Azure Static Web Apps config (`staticwebapp.config.json`) toegevoegd
5. ✅ Webpack build process geoptimaliseerd
6. ✅ DNS ongewijzigd - alles werkt via `wimtilburgs.nl`

**Resultaat:** 
- 🌐 **https://wimtilburgs.nl** - ✅ VOLLEDIG OPERATIONEEL
- 🌐 **https://black-hill-03e334903.2.azurestaticapps.net** - ✅ VOLLEDIG OPERATIONEEL
- 🚀 **React app laadt correct** met nieuwe tagline "Van Patiënt naar Actiënt® - Een Veteraan met een Missie"
- 🔒 **SSL certificaat actief** - Secure HTTPS verbinding
- ⚡ **CI/CD pipeline werkend** - GitHub Actions deployt automatisch

### 🔧 TECHNISCHE DETAILS VOOR MORGEN:

**Repository Setup:**
```
Huidige repository: https://github.com/wim-jlam/wim-tilburgs
Azure Static Web App: wimtilburgs-nl (resource group: rg-wimtilburgs-platform)
Domain: wimtilburgs.nl → black-hill-03e334903.2.azurestaticapps.net
```

**Deployment Process:**
- Git push naar `main` branch triggert automatisch Azure Static Web Apps CI/CD
- Build process: `npm ci` → `npm run build` → Azure deployment
- Output location: `dist/` folder
- Build time: ~2 minuten per deployment

**Belangrijke Files:**
- `webpack.config.js` - Build configuratie met copy-webpack-plugin
- `public/staticwebapp.config.json` - Azure routing en MIME type config
- `.github/workflows/azure-static-web-apps.yml` - CI/CD pipeline
- `src/i18n/locales/` - Nederlandse en Engelse vertalingen

**Content Updates Voltooid:**
- ✅ Verwijderd: Alle gewichtsverlies referenties (125kg → 85kg)
- ✅ Toegevoegd: Nieuwe tagline "Van Patiënt naar Actiënt® - Een Veteraan met een Missie"
- ✅ Updated: Meta tags en SEO beschrijvingen
- ✅ Behouden: AI-first filosofie en smart health focus

### 📋 WHAT'S NEXT - VOLGENDE SESSIE PLANNING:

**Prioriteiten voor morgen:**
1. **Content Development** - Meer pagina's uitbouwen (About, Services, Blog)
2. **AI Features** - AI Motor functionaliteit implementeren
3. **Database Integration** - PostgreSQL connectie opzetten
4. **Performance** - Bundle size optimalisatie (huidige waarschuwing: 343 KiB)
5. **SEO Enhancement** - Structured data en sitemap toevoegen

**Mogelijke Uitbreidingen:**
- Multi-language blog posts toevoegen
- AI chatbot integratie voor bezoekers
- Contact formulier met email functionaliteit  
- Analytics tracking (Google Analytics 4)
- Progressive Web App (PWA) features

**Development Workflow:**
```bash
# Voor nieuwe features:
git checkout -b feature/naam-van-feature
# Ontwikkel, test lokaal
npm run build && open dist/index.html
# Commit en push naar branch
git push -u origin feature/naam-van-feature
# Merge naar main voor deployment
```

### 🚨 BELANGRIJKE OPMERKINGEN:

**DNS & SSL:**
- DNS wijzigt NOOIT meer - `wimtilburgs.nl` blijft altijd werken
- SSL certificaat automatisch beheerd door Azure
- Custom domain volledig geconfigureerd

**Repository Management:**
- Hoofdrepository: `wim-jlam/wim-tilburgs` 
- Oude repository `jlam-smarthealth/wim-tilburgs` kan verwijderd worden
- Alle secrets correct geconfigureerd in nieuwe repo

**Deployment Success Indicatoren:**
- ✅ GitHub Actions toont "success" status
- ✅ `gh run list` toont completed workflows  
- ✅ Both URLs (wimtilburgs.nl + azurestaticapps.net) serve React app
- ✅ New tagline visible in browser title and meta tags

### 🎉 SESSION RECAP:

**Start:** Website down - React app stuck on loading screen na repository rename
**Probleem:** Azure Static Web App connected aan verkeerde repository 
**Tijd besteed:** ~5 uur troubleshooting en fixing
**Oplossing:** Complete infrastructure herconfiguratie
**Eindresultaat:** 100% werkende website met nieuwe branding

**Lessons Learned:**
- Repository renames vereisen Azure Static Web App reconfiguratie
- GitHub Secrets moeten opnieuw geconfigureerd worden bij nieuwe repos
- DNS blijft stabiel, alleen repository connections veranderen
- Azure CDN cache kan 5-10 minuten duren voor nieuwe content

---

---

## 🔴 !IMPORTANT: CRITICAL SECURITY INCIDENT - 23-08-2025

**!IMPORTANT: API KEYS WAREN EXPOSED IN DOCUMENTATIE**
**!IMPORTANT: DIT MAG NOOIT MEER GEBEUREN**
**!IMPORTANT: CHECK ALTIJD SECURITY_CHECKLIST.md VOOR HET SCHRIJVEN**

### Wat er gebeurde:
- Google API key was volledig zichtbaar in WIMTILBURGS_AZURE_APP.md
- OpenAI key gedeeltelijk exposed in meerdere documenten
- Security breach door slechte documentatie praktijken

### Lessons Learned:
1. **NOOIT** echte credentials in documentatie
2. **ALTIJD** placeholders gebruiken
3. **ALTIJD** security checklist volgen
4. **ALTIJD** gitleaks draaien voor commit

---

## 🔒 SECURITY FIRST - ABSOLUTE REGELS

### ❌ VERBODEN:
```
NOOIT schrijven in ENIGE file:
- API keys (sk-proj-..., AIza...)
- Passwords of tokens
- Database credentials
- Private IP adressen
- Email adressen (tenzij publiek)
```

### ✅ VERPLICHT:
```
ALTIJD gebruiken:
- Environment variables (.env file)
- Placeholders in documentatie
- 1Password voor credential opslag
- GitHub Secrets voor CI/CD
- Gitleaks voor pre-commit checks
```

### 🛡️ Security Tools:
```bash
# Voor ELKE commit:
gitleaks detect --source . -v

# Check specific file:
grep -E "(sk-|AIza|password|token)" filename.md

# Pre-commit hook installeren:
cp .gitleaks.toml .git/hooks/pre-commit
```

---

## 📁 Project Overview

### Wat is CIA App:
- **Command Intelligence Agency** - Multi-AI Orchestrator
- **Doel**: "Palantir Killer" voor AI orchestration
- **Status**: Production met GPT-5 access!
- **Owner**: Wim Tilburgs (65jr, JLAM founder)

### Tech Stack:
```python
# Core
- Python 3.9+ met Flask
- Async AI calls met asyncio
- Multiple AI providers (OpenAI, Google, Azure)

# Special Features
- GPT-5 production access (wereldprimeur!)
- DALL-E 3 image generation
- Gemini Pro (gratis voor non-profits)
- 1Password integration zonder Touch ID
```

### File Structure:
```
/cia-app/
├── .env                    # NOOIT committen! (in .gitignore)
├── .env.example           # Veilige dummy waarden
├── .gitleaks.toml         # Secret scanning config
├── SECURITY_CHECKLIST.md  # Verplicht checken!
├── cia.py                 # Core orchestration engine
├── app.py                 # Flask web interface (port 8080)
├── templates/             # Web templates met DALL-E graphics
├── static/                # CSS, JS, images
├── knowledge/             # GPT-5 documentatie (60k+ woorden)
└── venv/                  # Virtual environment
```

---

## 🎯 Development Guidelines

### Voor ELKE wijziging:
1. **Check SECURITY_CHECKLIST.md**
2. **Scan voor secrets**: `gitleaks detect`
3. **Test lokaal eerst**
4. **Gebruik .env voor credentials**
5. **Documenteer met placeholders**

### Port Configuration:
```python
# Port 5000 werkt NIET (AirPlay conflict op macOS)
app.run(host='0.0.0.0', port=8080, debug=True)
```

### API Integration:
```python
# GOED ✅
api_key = os.getenv('OPENAI_API_KEY')

# FOUT ❌
api_key = "sk-proj-abc123..."  # NOOIT!
```

---

## 🚀 Quick Start

### Check status:
```bash
# Is Flask running?
lsof -i :8080

# Restart app
source venv/bin/activate
python app.py

# Open in browser
open http://localhost:8080
```

### Test GPT-5:
```python
from cia import CIA
import asyncio

cia = CIA()
result = asyncio.run(cia.execute_mission("What is 2+2?"))
print(result)  # Should return "4"
```

---

## 📚 Important Documents

1. **SECURITY_CHECKLIST.md** - ALTIJD eerst lezen!
2. **CLAUDE_BRIEFING.md** - Context voor nieuwe sessies
3. **knowledge/GPT5_FINAL_SUMMARY.md** - GPT-5 ontdekkingen
4. **WIM_APP_CLAUDE_ACCESS.md** - Azure deployment plan (check: geen secrets!)

---

## 💡 Wim's Preferences

### Waardeert:
- ✅ Security first mentaliteit
- ✅ Uitgebreid testen
- ✅ Proactief meedenken
- ✅ Werkende code
- ✅ Goede documentatie

### Irritaties:
- ❌ Exposed secrets (BIGGEST NO!)
- ❌ Niet checken security
- ❌ Half werk
- ❌ Aannames maken
- ❌ Niet testen

---

## 🔴 EMERGENCY PROTOCOL

### Als je een secret vindt:
1. **STOP** alles
2. **VERWIJDER** direct
3. **VERVANG** met placeholder
4. **MELD** aan Wim
5. **ROTEER** de exposed key
6. **DOCUMENTEER** incident

### Recovery commands:
```bash
# Remove from git history
git filter-branch --force --index-filter \
  "git rm --cached --ignore-unmatch path/to/file" \
  --prune-empty --tag-name-filter cat -- --all

# Or use BFG Repo-Cleaner
bfg --delete-files file-with-secrets.md
```

---

## 📋 Current TODO

- [ ] Rotate Google API key (was exposed)
- [ ] Check all files for remaining secrets
- [ ] Implement pre-commit hooks
- [ ] Train all Claude sessions on security
- [ ] Document security incident fully

---

**REMEMBER**: 
> "Een exposed secret is een open deur voor hackers.
> Check, double-check, en check nog een keer!"

*Dit document is gemaakt na het security incident van 23-08-2025.*
*We leren van onze fouten en worden elke dag beter.*

---

END OF CLAUDE.md - SECURITY FIRST, ALTIJD! 🔒