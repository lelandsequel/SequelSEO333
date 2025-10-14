# 🔑 API Setup Guide - Step by Step

**Status:** ✅ All API integrations coded and ready!  
**Your job:** Just add the API keys to `.env` file

---

## 🎯 Quick Summary

I've integrated **5 real APIs** into your SEO Lead Finder:

| API | Purpose | Cost | Priority |
|-----|---------|------|----------|
| **Google Places** | Real businesses | $200/mo free | 🔥 HIGH |
| **PageSpeed Insights** | Real SEO metrics | FREE | 🔥 HIGH |
| **SerpAPI** | Search volume | 100/mo free | 🟡 MEDIUM |
| **Hunter.io** | Email discovery | 25/mo free | 🟡 MEDIUM |
| **Ahrefs** | Traffic trends | $99/mo | 🔵 LOW |

**All APIs have fallbacks** - the app still works without any keys!

---

## 📋 Setup Checklist

- [ ] Google Places API Key
- [ ] PageSpeed Insights API Key
- [ ] SerpAPI Key (optional)
- [ ] Hunter.io API Key (optional)
- [ ] Ahrefs API Key (optional - expensive)

---

## 🚀 Phase 1: Google Cloud APIs (START HERE)

### What You Get:
- ✅ Real businesses from Google Maps
- ✅ Real page speed metrics
- ✅ Real SEO data (schema, meta tags, etc.)

### Cost:
- **$200/month FREE credit** from Google Cloud
- After that: ~$0.032 per Places API call
- PageSpeed Insights: **100% FREE**

### Setup Steps:

#### 1. Go to Google Cloud Console
🔗 https://console.cloud.google.com/

#### 2. Create a Project (or use existing)
- Click "Select a project" → "New Project"
- Name it: "SEO Lead Finder"
- Click "Create"

#### 3. Enable APIs
Click "APIs & Services" → "Enable APIs and Services"

**Enable these 2 APIs:**
- Search for "Places API (New)" → Click "Enable"
- Search for "PageSpeed Insights API" → Click "Enable"

#### 4. Create API Key
- Go to "APIs & Services" → "Credentials"
- Click "Create Credentials" → "API Key"
- Copy the key (looks like: `AIzaSyD...`)

#### 5. (Optional but Recommended) Restrict the Key
- Click on your API key
- Under "API restrictions" → "Restrict key"
- Select:
  - Places API (New)
  - PageSpeed Insights API
- Click "Save"

#### 6. Add to .env File
Open `seo_lead_finder/.env` and add:
```bash
GOOGLE_PLACES_API_KEY=AIzaSyD...your_key_here
PSI_API_KEY=AIzaSyD...your_key_here
```

**Note:** You can use the SAME key for both!

---

## 🔍 Phase 2: SerpAPI (Optional)

### What You Get:
- Real search volume data
- Better industry discovery
- Ad density metrics

### Cost:
- **100 searches/month FREE**
- $50/month for 5,000 searches

### Setup Steps:

#### 1. Sign Up
🔗 https://serpapi.com/users/sign_up

#### 2. Get API Key
- After signup, go to dashboard
- Copy your API key

#### 3. Add to .env File
```bash
SERPAPI_KEY=your_serpapi_key_here
```

---

## 📧 Phase 3: Hunter.io (Optional)

### What You Get:
- Email addresses for businesses
- Contact discovery

### Cost:
- **25 searches/month FREE**
- $49/month for 500 searches

### Setup Steps:

#### 1. Sign Up
🔗 https://hunter.io/users/sign_up

#### 2. Get API Key
- Go to API → API Keys
- Copy your key

#### 3. Add to .env File
```bash
HUNTER_API_KEY=your_hunter_key_here
```

---

## 📊 Phase 4: Ahrefs (Optional - Premium)

### What You Get:
- Real traffic trends
- Backlink data
- Domain authority

### Cost:
- **No free tier**
- $99/month minimum

### Setup Steps:

#### 1. Sign Up
🔗 https://ahrefs.com/api

#### 2. Get API Token
- Go to Account → API Access
- Generate token

#### 3. Add to .env File
```bash
AHREFS_API_KEY=your_ahrefs_token_here
```

---

## ✅ Testing Your Setup

### Test Without Any Keys (Stub Data)
```bash
python3 main.py --once --geo "Austin, TX"
# Should work with fake data
```

### Test With Google APIs
After adding Google keys:
```bash
python3 main.py --once --geo "Austin, TX"
# Should show:
# 🗺️  Google Places: Found X businesses
# 🔍 PageSpeed: Analyzing...
# ✅ PageSpeed: LCP=X.XXs, Score=XX
```

### Test With All APIs
After adding all keys:
```bash
python3 main.py --once --geo "Austin, TX"
# Should show:
# 📊 SerpAPI: industry in Austin, TX - X,XXX results
# 🗺️  Google Places: Found X businesses
# 🔍 PageSpeed: Analyzing...
# 📧 Hunter.io: Found email for domain.com
```

---

## 🎓 What Happens With/Without Keys

### Without Any Keys:
```
✅ Pipeline runs successfully
✅ Generates 150 leads
✅ Uses realistic stub data
✅ Saves to CSV
❌ Data is fake
```

### With Google Places + PageSpeed:
```
✅ REAL businesses from Google Maps
✅ REAL page speed metrics
✅ REAL SEO data (schema, meta tags)
✅ REAL tech stack detection
⚠️  Industry discovery still uses stub data
⚠️  No emails
```

### With All APIs:
```
✅ REAL search volume data
✅ REAL businesses
✅ REAL SEO metrics
✅ REAL email addresses
✅ 100% real data!
```

---

## 💰 Cost Breakdown

### Recommended Setup (Phase 1 + 2):
- Google Cloud: **FREE** ($200 credit)
- SerpAPI: **FREE** (100/month)
- **Total: $0/month** 🎉

### Full Setup (All APIs):
- Google Cloud: **FREE** ($200 credit)
- SerpAPI: $50/month (or free tier)
- Hunter.io: $49/month (or free tier)
- Ahrefs: $99/month
- **Total: ~$200/month** (or $0 with free tiers)

---

## 🔧 Troubleshooting

### "Google Places API error: REQUEST_DENIED"
- Make sure you enabled "Places API (New)" not the old one
- Check that your API key is not restricted to wrong APIs
- Verify billing is enabled on your Google Cloud project

### "PageSpeed timeout"
- This is normal for slow websites
- The app will use fallback data
- Try increasing timeout in code if needed

### "SerpAPI error: 403"
- Check your API key is correct
- Verify you haven't exceeded free tier (100/month)
- Check your account status

### "Hunter.io error"
- Verify API key is correct
- Check you haven't exceeded free tier (25/month)
- Some domains may not have emails in their database

---

## 📝 Your .env File Should Look Like:

```bash
# === API KEYS / CREDS ===
# Google Cloud APIs
GOOGLE_PLACES_API_KEY=AIzaSyD...your_key_here
PSI_API_KEY=AIzaSyD...your_key_here

# Search & SEO Data
SERPAPI_KEY=abc123...your_key_here

# Email Discovery
HUNTER_API_KEY=xyz789...your_key_here

# Traffic Analytics (Optional)
AHREFS_API_KEY=

# Google Sheets (Optional)
GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON_PATH=./secrets/google-service-account.json
GOOGLE_SHEETS_SPREADSHEET_ID=
GOOGLE_SHEETS_WORKSHEET_NAME=Leads

# Slack (Optional)
SLACK_WEBHOOK_URL=

# === DEFAULTS ===
DEFAULT_GEO=Houston, TX
MAX_INDUSTRIES=5
LEADS_PER_INDUSTRY=30
HOT_LEAD_THRESHOLD=70
```

---

## 🎯 Recommended Approach

### Week 1: Test with Stub Data
- Run without any API keys
- Understand the output format
- Verify the pipeline works

### Week 2: Add Google APIs
- Get Google Places + PageSpeed keys
- Test with real businesses
- See real SEO metrics

### Week 3: Add SerpAPI
- Get better industry discovery
- See real search volume

### Week 4: Add Hunter.io
- Get email addresses
- Complete contact info

### Later: Consider Ahrefs
- Only if you need traffic trends
- Expensive but powerful

---

## ✅ Next Steps

1. **Start with Google Cloud** (Phase 1)
   - Most important
   - Mostly free
   - Biggest impact

2. **Add SerpAPI** (Phase 2)
   - Free tier is generous
   - Better industry discovery

3. **Add Hunter.io** (Phase 3)
   - If you need emails
   - Free tier works for testing

4. **Skip Ahrefs for now** (Phase 4)
   - Expensive
   - Not critical
   - Add later if needed

---

**Ready to add your first API key?** Start with Google Cloud! 🚀

