# 🚀 SEO Lead Finder - Quick Start Guide

## TL;DR - Get Running in 2 Minutes

```bash
# 1. Install dependencies
pip3 install -r requirements.txt

# 2. Run it!
python3 main.py --once --geo "Houston, TX"

# 3. Check results
cat ./out/leads_*.csv | head -20
```

**That's it!** No API keys needed for testing. Results saved to `./out/` directory.

---

## What Just Happened?

The pipeline:
1. ✅ Discovered 5 industries with highest SEO need in Houston
2. ✅ Found 30 businesses per industry (150 total)
3. ✅ Ran SEO audits on each business
4. ✅ Scored each lead (0-100)
5. ✅ Saved results to CSV
6. ✅ Identified hot leads (score >= 70)

---

## Command Reference

### Run Once (Test Mode)
```bash
python3 main.py --once --geo "Austin, TX"
```

### Run Weekly Scheduler
```bash
python3 main.py --geo "Houston, TX"
# Runs every Sunday at 9:00 AM
# Press Ctrl+C to stop
```

### Run Test Suite
```bash
python3 test_pipeline.py
```

### Change Settings
```bash
# Edit .env file
nano .env

# Or use command line
python3 main.py --once --geo "Miami, FL"
```

---

## Understanding the Output

### CSV Columns
- **RunDate**: When the scan was performed
- **Geo**: Target geography
- **Industry**: Business industry
- **BusinessName**: Company name
- **Website**: Company website
- **Score**: Lead quality score (0-100)
- **Issues**: SEO problems found
- **TechStack**: Website platform (WordPress, Wix, etc.)
- **CoreWebVitals_LCP**: Largest Contentful Paint (speed metric)
- **HasSchema**: Schema.org markup present
- **TrafficTrend_90d**: Traffic change % over 90 days

### Score Breakdown
- **70-100**: 🔥 Hot lead (immediate outreach)
- **50-69**: 🟡 Warm lead (follow up)
- **0-49**: 🟢 Cold lead (nurture)

### Scoring Factors
| Factor | Points | Threshold |
|--------|--------|-----------|
| Traffic declining | 30 | -20% or worse |
| No Schema.org | 25 | Missing |
| Stale content | 15 | 12+ months old |
| Slow page speed | 15 | LCP > 3.0s |
| Easy tech stack | +10 | WordPress/Wix/Squarespace |

---

## Current Status (Stub Mode)

### ✅ What Works Now (No API Keys)
- Industry discovery (heuristic scoring)
- Lead generation (stub data)
- SEO auditing (randomized metrics)
- Lead scoring (full algorithm)
- CSV output
- Slack alerts (if webhook configured)

### 🔑 What Needs API Keys (Optional)
- Google Sheets output
- Real SERP data (SerpAPI)
- Real traffic data (Ahrefs)
- Real contact data (Hunter.io)
- Real PageSpeed data (PSI API)

---

## Adding Real Data (Optional)

### 1. Google Sheets Integration

```bash
# Create service account at Google Cloud Console
# Download JSON credentials
mkdir -p secrets
mv ~/Downloads/service-account.json secrets/google-service-account.json

# Update .env
GOOGLE_SHEETS_SPREADSHEET_ID=your_spreadsheet_id_here
```

### 2. Slack Alerts

```bash
# Create webhook at https://api.slack.com/messaging/webhooks
# Update .env
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

### 3. Real API Integrations (Future)

Edit the module files to replace stub functions:
- `modules/industry_discovery.py` - Add SerpAPI calls
- `modules/lead_finder.py` - Add Google Places API
- `modules/seo_checks.py` - Add real HTML parsing + PSI API

---

## Troubleshooting

### "ModuleNotFoundError"
```bash
pip3 install -r requirements.txt
```

### "Google Sheets credentials not found"
This is normal! CSV output still works. To enable Sheets:
1. Create service account JSON
2. Update `GOOGLE_SHEETS_SERVICE_ACCOUNT_JSON_PATH` in `.env`

### "No hot leads found"
Adjust threshold in `.env`:
```bash
HOT_LEAD_THRESHOLD=50  # Lower threshold
```

### Change number of leads
```bash
# Edit .env
LEADS_PER_INDUSTRY=50  # More leads per industry
MAX_INDUSTRIES=10      # More industries
```

---

## Scheduling Options

### Option 1: Local Scheduler (APScheduler)
```bash
# Runs in foreground
python3 main.py --geo "Houston, TX"

# Or use screen/tmux for background
screen -S seo_leads
python3 main.py --geo "Houston, TX"
# Press Ctrl+A, D to detach
```

### Option 2: Cron Job
```bash
# Edit crontab
crontab -e

# Add line (runs Sundays at 9 AM)
0 9 * * 0 cd /path/to/seo_lead_finder && python3 main.py --once --geo "Houston, TX"
```

### Option 3: GitHub Actions
Already configured in `.github/workflows/weekly.yml`
- Runs Sundays at 15:00 UTC (9-10 AM Central)
- Add secrets to GitHub repo settings

---

## Next Steps

1. ✅ **Test it** - Run `python3 test_pipeline.py`
2. ✅ **Try it** - Run `python3 main.py --once --geo "Your City"`
3. ⬜ **Review output** - Check `./out/leads_*.csv`
4. ⬜ **Add Google Sheets** - For persistent storage
5. ⬜ **Add Slack alerts** - For hot lead notifications
6. ⬜ **Customize scoring** - Edit `modules/scoring.py`
7. ⬜ **Add real APIs** - Replace stub functions

---

## Examples

### Find leads in multiple cities
```bash
python3 main.py --once --geo "Austin, TX"
python3 main.py --once --geo "Dallas, TX"
python3 main.py --once --geo "San Antonio, TX"
```

### Analyze output
```bash
# Count hot leads
grep -c ",7[0-9]," ./out/leads_*.csv
grep -c ",8[0-9]," ./out/leads_*.csv
grep -c ",9[0-9]," ./out/leads_*.csv

# Find highest scores
sort -t',' -k19 -nr ./out/leads_*.csv | head -10

# Filter by industry
grep "auto dealers" ./out/leads_*.csv
```

### Import to Excel/Google Sheets
Just open the CSV file in `./out/` directory!

---

## Support

- 📖 Full docs: See `README.md`
- 🧪 Test results: See `TEST_RESULTS.md`
- 💬 Issues: Check code comments for TODOs
- 🔧 Customize: All modules are well-documented

---

**Happy lead hunting! 🎯**

