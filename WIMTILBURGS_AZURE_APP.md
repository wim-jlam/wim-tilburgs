# 🚀 wimtilburgs.nl - Azure Native SmartHealth Platform

*Direct bouwen op Azure - Geen lokale deployment*  
*Datum: 23 augustus 2025*

---

## 🎯 De App die we gaan bouwen op Azure

### wimtilburgs.nl Features:
1. **Homepage** - Jouw transformatie verhaal (125kg → medicijnvrij)
2. **Blog** - Jalal & Jamal mystieke content (tweetalig)
3. **AI Assistant** - Powered by GPT-5, Gemini, Azure AI
4. **Health Tracker** - Glucose, gewicht, medicatie monitoring
5. **Coaching Portal** - Voor je 1-on-1 clients
6. **Knowledge Base** - GPT-5 discoveries, health protocols

---

## 🔷 Stap-voor-Stap Azure Setup

### Stap 1: Web App Aanmaken in Portal

1. Ga naar **"Een resource maken"** (+ icoon)
2. Kies **"Web App"**
3. Vul in:
   ```
   Subscription: Microsoft Azure Sponsorship
   Resource Group: Stichting
   Name: wimtilburgs
   Publish: Code
   Runtime stack: Python 3.9
   Operating System: Linux
   Region: West Europe
   Plan: Create new → SmartHealthPlan (B1: ~€10/maand)
   ```
4. Klik **"Review + create"** → **"Create"**

### Stap 2: Database Setup (gebruik jlampostgres)

In Azure Portal:
1. Ga naar **jlampostgres** 
2. Klik **"Databases"** → **"+ Add"**
3. Database naam: `smarthealth`
4. Klik **"Save"**

### Stap 3: Application Settings

In je Web App (wimtilburgs):
1. Ga naar **"Configuration"**
2. Voeg toe onder **"Application settings"**:
   ```
   AZURE_POSTGRESQL_HOST = jlampostgres.postgres.database.azure.com
   AZURE_POSTGRESQL_DB = smarthealth
   AZURE_POSTGRESQL_USER = [jouw admin user]
   AZURE_POSTGRESQL_PASSWORD = [uit 1Password]
   
   OPENAI_API_KEY = [je ChatGPT Teams key]
   GOOGLE_API_KEY = [VERVANG MET ECHTE KEY UIT GOOGLE CLOUD]
   
   SECRET_KEY = [genereer random string]
   FLASK_ENV = production
   ```

---

## 📁 App Structuur voor Azure

```
wimtilburgs-app/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── .deployment           # Azure deployment config
├── startup.txt           # Azure startup commands
├── static/
│   ├── css/
│   │   └── style.css     # SmartHealth styling
│   ├── js/
│   │   └── app.js        # Frontend logic
│   └── images/
│       └── wim.jpg       # Hero image
├── templates/
│   ├── index.html        # Homepage
│   ├── blog.html         # Blog listing
│   ├── article.html      # Blog article
│   ├── tracker.html      # Health tracker
│   └── ai-coach.html     # AI Assistant
├── models/
│   ├── database.py       # PostgreSQL models
│   └── ai_service.py     # AI integrations
└── content/
    └── jalal_jamal/      # Je boek content
```

---

## 🐍 Main App Code (app.py)

```python
from flask import Flask, render_template, request, jsonify
import os
import psycopg2
from azure.storage.blob import BlobServiceClient
import openai
import google.generativeai as genai

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

# Database connection
def get_db():
    return psycopg2.connect(
        host=os.environ.get('AZURE_POSTGRESQL_HOST'),
        database=os.environ.get('AZURE_POSTGRESQL_DB'),
        user=os.environ.get('AZURE_POSTGRESQL_USER'),
        password=os.environ.get('AZURE_POSTGRESQL_PASSWORD'),
        sslmode='require'
    )

# Routes
@app.route('/')
def home():
    return render_template('index.html', 
                         title="Wim Tilburgs - SmartHealth Consultant")

@app.route('/blog')
def blog():
    # Load Jalal & Jamal content
    return render_template('blog.html')

@app.route('/ai-coach', methods=['GET', 'POST'])
def ai_coach():
    if request.method == 'POST':
        question = request.json.get('question')
        # Use GPT-5, Gemini, or Azure AI
        response = get_ai_response(question)
        return jsonify({'response': response})
    return render_template('ai-coach.html')

@app.route('/tracker')
def health_tracker():
    return render_template('tracker.html')

def get_ai_response(question):
    # Smart routing between AI models
    if is_simple_query(question):
        return use_gpt5(question)  # GPT-5 for simple
    elif needs_translation(question):
        return use_gemini(question)  # Gemini FREE
    else:
        return use_azure_ai(question)  # Azure cognitive

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
```

---

## 🎨 Homepage Template (templates/index.html)

```html
<!DOCTYPE html>
<html lang="nl">
<head>
    <meta charset="UTF-8">
    <title>Wim Tilburgs - SmartHealth Consultant</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, sans-serif;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .hero {
            padding: 100px 20px;
            text-align: center;
        }
        .hero h1 {
            font-size: 3rem;
            margin-bottom: 20px;
        }
        .transformation {
            font-size: 1.5rem;
            margin: 30px 0;
        }
        .cta-button {
            background: gold;
            color: black;
            padding: 15px 30px;
            border-radius: 30px;
            text-decoration: none;
            font-weight: bold;
            display: inline-block;
            margin: 10px;
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>Wim Tilburgs</h1>
        <p class="subtitle">SmartHealth Consultant</p>
        
        <div class="transformation">
            <p>Van 125kg diabeet → Medicijnvrij Pioneer</p>
            <p>Van Libanon Veteraan → GPT-5 Ontdekker</p>
            <p>Van Ziekenzorg → Gezondheidszorg</p>
        </div>
        
        <div class="cta">
            <a href="/blog" class="cta-button">📚 Lees mijn Verhaal</a>
            <a href="/ai-coach" class="cta-button">🤖 AI Health Coach</a>
            <a href="/tracker" class="cta-button">📊 Health Tracker</a>
        </div>
        
        <div class="stats">
            <h2>Impact</h2>
            <p>9000+ mensen geholpen</p>
            <p>2000+ diabetes reversals</p>
            <p>Eerste GPT-5 documentatie ter wereld</p>
        </div>
    </div>
</body>
</html>
```

---

## 📦 requirements.txt

```
flask==2.3.0
psycopg2-binary==2.9.6
azure-storage-blob==12.17.0
azure-cognitiveservices-language-textanalytics==0.2.0
openai==1.0.0
google-generativeai==0.3.0
gunicorn==21.2.0
```

---

## 🚀 Deploy naar Azure

### Via Azure Portal (Deployment Center):

1. Ga naar je **wimtilburgs** Web App
2. Klik **"Deployment Center"** in linker menu
3. Kies **"GitHub"** als source
4. Autoriseer en selecteer:
   - Organization: wimtilburgs
   - Repository: smarthealth-azure
   - Branch: main
5. Klik **"Save"**

### Of via Azure CLI:

```bash
# Login
az login

# Deploy ZIP
az webapp deployment source config-zip \
  --resource-group Stichting \
  --name wimtilburgs \
  --src app.zip
```

---

## 🌐 Custom Domain Setup

1. Ga naar **"Custom domains"** in Web App
2. Klik **"+ Add custom domain"**
3. Voer in: `wimtilburgs.nl`
4. Volg DNS instructies:
   - CNAME: www → wimtilburgs.azurewebsites.net
   - A record: @ → [Azure IP]
5. Enable **HTTPS Only**

---

## 📊 Monitoring & Analytics

In Azure Portal voor je app:
- **Application Insights** - Performance monitoring
- **Log stream** - Real-time logs
- **Metrics** - Traffic, errors, response times
- **Alerts** - Notifications bij problemen

---

## 💰 Kosten Overzicht

| Service | Kosten/maand | Binnen Sponsorship? |
|---------|--------------|---------------------|
| Web App (B1) | €10 | ✅ Ja |
| PostgreSQL | €15 | ✅ Ja |
| Storage | €5 | ✅ Ja |
| Custom Domain | €10/jaar | ✅ Ja |
| **TOTAAL** | **€30/maand** | **✅ Ruim binnen €3000/jaar** |

---

## ✅ Checklist

- [ ] Web App aanmaken in Azure Portal
- [ ] Database 'smarthealth' toevoegen aan jlampostgres
- [ ] Application Settings configureren
- [ ] Code naar GitHub pushen
- [ ] Deployment Center koppelen
- [ ] Custom domain configureren
- [ ] SSL certificaat activeren
- [ ] Application Insights enablen

---

*"Direct op Azure bouwen - geen gedoe met deployment, alles cloud-native!"* 🚀