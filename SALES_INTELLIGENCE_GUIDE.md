# 🎯 Sales Intelligence System Guide

## Overview

Your SEO Lead Finder now includes **AI-powered sales intelligence** that transforms raw data into **actionable sales reports** ready to close deals.

---

## 🆕 What's New?

### **Before (Spreadsheet Only):**
```
BusinessName: High 5 Plumbing
Score: 95
Issues: Slow LCP, No Schema, Stale Content
```
**Problem:** You still had to figure out what to say!

### **After (Sales Intelligence):**
```
═══════════════════════════════════════════════════
HIGH 5 PLUMBING, HEATING, COOLING & ELECTRIC
Score: 95/100 (CRITICAL - Immediate Action Needed)
Phone: (720) 340-3843
═══════════════════════════════════════════════════

🚨 CRITICAL ISSUES:
1. Website Loads in 22 Seconds
   → 75% of mobile users abandon before seeing your services
   → Estimated loss: $12,000-18,000/month

💰 REVENUE IMPACT: $12,000-18,000/month

🎯 PITCH ANGLE:
"Your website takes 22 seconds to load. When someone has a 
plumbing emergency, they're calling the first plumber they 
find - and it's not you. I can get you ranking #1 for 
'emergency plumber Denver' in 30 days."

✅ QUICK WINS (First 2 Weeks):
Week 1: Add emergency call button to header
Week 1: Speed optimization (critical)
Week 2: Add service area pages
Week 2: Implement local business schema

📞 CALL SCRIPT:
"Hi, this is [YOUR NAME]. I was doing research on plumbers
in Denver and came across High 5 Plumbing. I noticed your
website takes 22 seconds to load on mobile - when someone
has a plumbing emergency, they won't wait that long..."
```

---

## 🚀 Features

### 1. **LLM-Powered Deep Analysis**
For each high-scoring lead (score >= 60), the system now:

- ✅ Analyzes actual website content
- ✅ Identifies specific technical issues with $ impact
- ✅ Extracts services offered and USP
- ✅ Finds missing keywords and opportunities
- ✅ Generates personalized pitch angles
- ✅ Creates ready-to-use call scripts
- ✅ Provides quick wins roadmap

### 2. **Professional Sales Reports**
Automatically generates:

- **Text Reports** (always created, saved to `./out/`)
- **Google Docs** (optional, if credentials configured)

Each report includes:
- Executive summary with stats
- 1/3 page per hot lead with full analysis
- Prioritized by urgency (Critical/High/Good)
- Ready-to-use pitch scripts
- Competitive intelligence
- Revenue impact calculations

### 3. **Smart Prioritization**
Leads are categorized by urgency:

- 🔴 **CRITICAL (90+)**: Immediate action needed
- 🟠 **HIGH PRIORITY (80-89)**: Strong opportunity
- 🟡 **GOOD OPPORTUNITY (70-79)**: Worth pursuing

---

## 💰 Cost Analysis

### **LLM Analysis Costs:**

| Provider | Model | Cost per Lead | Cost per 100 Leads |
|----------|-------|---------------|-------------------|
| **Claude (Anthropic)** | Haiku | ~$0.01-0.02 | ~$1-2 |
| **OpenAI** | GPT-3.5 Turbo | ~$0.02-0.03 | ~$2-3 |

**For weekly runs:**
- 100 businesses analyzed = **$2-3/week**
- **$8-12/month** for full sales intelligence

**vs. alternatives:**
- Hiring a VA to research each lead: **$150+/week**
- Using Ahrefs for traffic data: **$500/month**

---

## 🔧 Setup

### **1. Install Dependencies**
```bash
pip3 install -r requirements.txt
```

### **2. Configure API Keys**
Already done! Your `.env` file has:
- ✅ `ANTHROPIC_API_KEY` (Claude - recommended)
- ✅ `OPENAI_API_KEY` (GPT - backup)

### **3. (Optional) Google Docs Integration**
To create Google Docs reports instead of just text files:

1. Use the same service account JSON you have for Google Sheets
2. Enable Google Docs API in your Google Cloud project:
   - Go to: https://console.cloud.google.com/apis/library/docs.googleapis.com?project=SequelSEO333
   - Click "ENABLE"

That's it! The system will automatically create Google Docs when credentials are available.

---

## 📊 Usage

### **Run the Full Pipeline**
```bash
python3 main.py --once --geo "Austin, TX"
```

**What happens:**
1. Finds 150 businesses across 5 industries
2. Analyzes each with PageSpeed + HTML parsing
3. **NEW:** For high-scoring leads (60+), runs LLM analysis
4. Scores and ranks all leads
5. Saves CSV with all data
6. **NEW:** Generates sales intelligence report for hot leads (70+)

**Output:**
- `./out/leads_YYYYMMDD_HHMMSS.csv` - Full data
- `./out/sales_report_Austin_TX_YYYY-MM-DD.txt` - Sales intelligence report
- (Optional) Google Doc with formatted report

### **Test the New Features**
```bash
python3 test_sales_intelligence.py
```

This will:
1. Test LLM analysis on a real website
2. Generate a sample sales report
3. Show you what the output looks like

---

## 📈 What You Get

### **CSV Data (Enhanced)**
Now includes LLM fields:
- `LLM_SEOScore` - AI-assessed SEO quality (0-100)
- `LLM_CriticalIssues` - Specific technical problems
- `LLM_RevenueImpact` - Estimated monthly loss
- `LLM_Opportunities` - Improvement opportunities
- `LLM_ServicesOffered` - What they do
- `LLM_USP` - Their unique selling proposition
- `LLM_CTAQuality` - Call-to-action assessment
- `LLM_TargetKeywords` - Keywords they're targeting
- `LLM_MissingKeywords` - Keywords they're missing
- `LLM_ContentQuality` - Content assessment
- `LLM_QuickWins` - Fast improvements
- `LLM_PitchAngle` - Best approach angle

### **Sales Report**
Professional report with:
- Executive summary
- Detailed analysis per lead
- Revenue impact calculations
- Pitch scripts
- Call scripts
- Quick wins roadmap
- Competitive insights

---

## 🎯 Workflow

### **Sunday Night (Automated):**
```bash
# Runs automatically at 9 AM Sunday (configured in .env)
# Or run manually:
python3 main.py --once --geo "Your City, State"
```

### **Monday Morning:**
1. Open `./out/sales_report_*.txt` (or Google Doc)
2. Review hot leads (sorted by priority)
3. Start calling from the top
4. Use the provided pitch scripts
5. Reference specific issues from the report

### **During Calls:**
- Mention specific technical issues (e.g., "22 second load time")
- Quote revenue impact (e.g., "$12K-18K/month loss")
- Offer quick wins (e.g., "I can fix this in 2 weeks")
- Use the provided call scripts as templates

---

## 🔥 Pro Tips

### **1. Focus on Critical Leads First**
Leads with score 90+ have the most obvious problems = easiest to close

### **2. Use Specific Numbers**
Don't say "your site is slow" - say "your site takes 22 seconds to load"

### **3. Lead with Revenue Impact**
"This is costing you $12K/month" is more compelling than "you need SEO"

### **4. Offer Quick Wins**
"I can fix X, Y, Z in the first 2 weeks" builds confidence

### **5. Reference Their Competitors**
The report shows how they compare to competitors in the same area

---

## 🛠️ Customization

### **Adjust LLM Analysis Threshold**
In `main.py`, line 48:
```python
if score >= 60 and lead.get("website"):  # Change 60 to your threshold
```

Lower = more LLM analysis (more cost)
Higher = less LLM analysis (less cost, but fewer insights)

### **Adjust Hot Lead Threshold**
In `.env`:
```bash
HOT_LEAD_THRESHOLD=70  # Change to 80 for stricter filtering
```

### **Change Report Format**
Edit `modules/report_generator.py` to customize:
- Section order
- Content included
- Formatting
- Urgency thresholds

---

## 📞 Example Call Flow

**Opening:**
> "Hi, this is [NAME]. I was doing research on [INDUSTRY] in [CITY] and came across [BUSINESS]. I noticed a few things on your website that might be costing you customers. Do you have 2 minutes?"

**Hook (use specific issue from report):**
> "Your website takes 22 seconds to load on mobile. Industry data shows you're losing about 75% of potential customers before they even see your services."

**Value Proposition:**
> "I specialize in fixing these exact issues for [INDUSTRY] businesses. I can get your site loading in under 3 seconds and ranking above [COMPETITOR] in about 30 days."

**Quick Wins:**
> "In the first 2 weeks alone, I can [QUICK WIN 1] and [QUICK WIN 2], which should start bringing in more calls immediately."

**Close:**
> "Would you be open to a 15-minute call where I can show you exactly what I found and how we can fix it?"

---

## 🎉 Results

With this system, you now have:

✅ **Automated lead discovery** (Google Places)
✅ **Technical SEO analysis** (PageSpeed, HTML parsing)
✅ **AI-powered insights** (Claude/GPT)
✅ **Revenue impact calculations**
✅ **Personalized pitch angles**
✅ **Ready-to-use call scripts**
✅ **Professional sales reports**
✅ **Competitive intelligence**

**All running autonomously every Sunday, ready Monday morning!**

---

## 🆘 Troubleshooting

### **"No LLM API key configured"**
- Check that `ANTHROPIC_API_KEY` or `OPENAI_API_KEY` is set in `.env`
- Run `python3 test_all_apis.py` to verify

### **"Google credentials not found"**
- Sales reports will still be created as text files
- To enable Google Docs, add service account JSON to `./secrets/`

### **LLM analysis is slow**
- Normal! Each analysis takes 10-15 seconds
- Only runs for high-scoring leads (60+)
- Adjust threshold in `main.py` if needed

### **Reports are too long**
- Adjust `HOT_LEAD_THRESHOLD` in `.env` to filter more strictly
- Edit `report_generator.py` to shorten sections

---

## 📚 Additional Resources

- `LLM_SETUP_GUIDE.md` - Detailed LLM API setup
- `API_STATUS.md` - Current API status
- `test_sales_intelligence.py` - Test the new features
- `test_all_apis.py` - Verify all APIs are working

---

**Questions? Issues? Check the output logs - they're very detailed!**

