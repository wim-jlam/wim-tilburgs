# 🔒 SECURITY CHECKLIST - VERPLICHT VOOR ALLE DOCUMENTEN

*Created: 23 augustus 2025*  
*Reason: Security incident - API keys exposed in documentation*

## ⚠️ VOOR ELKE FILE DIE JE SCHRIJFT/UPDATET:

### 1. SCAN voor gevoelige data:
- [ ] Geen API keys (sk-, AIza, Bearer tokens)
- [ ] Geen passwords of wachtwoorden
- [ ] Geen database connection strings
- [ ] Geen private IP adressen
- [ ] Geen SSH keys of certificates
- [ ] Geen email adressen (tenzij publiek)
- [ ] Geen service account tokens

### 2. VERVANG met placeholders:
```bash
# GOED ✅
OPENAI_API_KEY=[VERVANG MET KEY UIT 1PASSWORD]
DATABASE_PASSWORD=[CHECK 1PASSWORD VAULT]
SERVER_IP=[VRAAG AAN ADMIN]

# FOUT ❌
OPENAI_API_KEY=sk-proj-abc123...
DATABASE_PASSWORD=MyS3cr3tP@ss
SERVER_IP=192.168.1.100
```

### 3. CHECK git history:
```bash
# Voor commit - check of geen secrets in staging
git diff --staged | grep -E "(sk-|AIza|password|token|secret)"

# Check hele history
git log -p | grep -E "(sk-|AIza|password|token|secret)"
```

### 4. USE security tools:
```bash
# Installeer gitleaks
brew install gitleaks

# Scan huidige directory
gitleaks detect --source . -v

# Pre-commit hook
gitleaks protect --staged -v
```

## 🚨 ALS JE EEN SECRET VINDT:

1. **STOP** - Commit/push niet!
2. **VERWIJDER** - Vervang met placeholder
3. **ROTEER** - Vraag om key rotation
4. **MELD** - Informeer team/eigenaar
5. **DOCUMENTEER** - Log het incident

## 📋 VEILIGE PATTERNS:

### Voor Documentatie:
```markdown
## API Configuratie
- API Key opslaan in 1Password onder "ChatGPT Teams"
- Kopieer key naar .env file (NOOIT in code!)
- Format: OPENAI_API_KEY=sk-proj-[rest van key]
```

### Voor Code:
```python
# GOED ✅
import os
api_key = os.getenv('OPENAI_API_KEY')

# FOUT ❌
api_key = "sk-proj-abc123..."
```

### Voor Config Files:
```yaml
# GOED ✅
database:
  host: ${DATABASE_HOST}
  password: ${DATABASE_PASSWORD}

# FOUT ❌  
database:
  host: prod.database.com
  password: MyPassword123
```

## 🎯 GOLDEN RULES:

1. **WANNEER TWIJFEL** → Gebruik placeholder
2. **PRODUCTIE SECRETS** → NOOIT in repo
3. **DEVELOPMENT SECRETS** → Alleen in .env (met .gitignore)
4. **DOCUMENTATIE** → Alleen WHERE, niet WHAT
5. **CODE REVIEWS** → Check altijd voor secrets

## 🔄 REGULAR AUDITS:

Weekly:
```bash
# Full repo scan
gitleaks detect --source . -v

# Check all markdown files
grep -r "sk-\|AIza\|password" *.md
```

## 💡 REMEMBER:

> "Een exposed secret is als een sleutel onder de deurmat - 
> iedereen kan binnen komen!"

**Deze checklist is gemaakt na een security incident op 23-08-2025**
**waar API keys per ongeluk in documentatie terecht kwamen.**

---

*GEBRUIK DEZE CHECKLIST. ALTIJD. GEEN EXCUSES.*