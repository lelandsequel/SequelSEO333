# 🎯 C&L Page Services - Lead Finder UI Guide

## 🚀 Quick Start

### Launch the UI

```bash
streamlit run app.py
```

The UI will open automatically in your browser at `http://localhost:8501`

---

## 📱 UI Overview

The UI has **3 main tabs**:

### 1️⃣ **Manual Search** - Find leads on-demand
- Enter a location (e.g., "Austin, TX")
- Choose industry mode:
  - **Auto-discover**: AI finds top industries
  - **Manual**: You specify industries
  - **Hybrid**: Auto-discover + your additions
- Click "Find Leads" to run the search
- View results with hot leads highlighted
- Download CSV or sales report

### 2️⃣ **Automation** - Configure weekly runs
- Enable/disable weekly automation
- Set schedule (day of week, time)
- Configure locations to search
- Choose industry discovery mode
- Enable Slack notifications
- Save settings to generate GitHub Actions workflow
- Test automation immediately

### 3️⃣ **Results Dashboard** - View past results
- Browse all previous searches
- View metrics and charts
- Filter by industry, score, LCP
- Download filtered results
- Access sales reports

---

## ⚙️ Automation Setup

### How It Works

1. **Configure in UI**: Set your schedule, locations, and industries
2. **Save Settings**: Generates `.github/workflows/weekly.yml`
3. **Commit & Push**: Push the workflow file to GitHub
4. **Automatic Runs**: GitHub Actions runs on your schedule
5. **Get Results**: Results saved as artifacts + Slack notifications

### GitHub Secrets Required

Go to your GitHub repo → **Settings** → **Secrets and variables** → **Actions**

Add these secrets:

**Required:**
- `GOOGLE_PLACES_API_KEY`
- `PAGESPEED_API_KEY`
- `ANTHROPIC_API_KEY` or `OPENAI_API_KEY`
- `DATAFORSEO_LOGIN`
- `DATAFORSEO_PASSWORD`

**Optional:**
- `SLACK_WEBHOOK_URL` (for notifications)
- `GOOGLE_SERVICE_ACCOUNT_JSON` (for Sheets integration)

### Example Automation Config

**Schedule:** Every Monday at 9:00 AM UTC

**Locations:**
```
Houston, TX
Austin, TX
Dallas, TX
```

**Mode:** Auto-discover (finds top 5 industries per location)

**Result:** 15 searches per week (3 locations × 5 industries)

---

## 🎨 Features

### Manual Search Tab

✅ **Real-time search** - Run searches on-demand  
✅ **Live progress** - See what's happening  
✅ **Hot leads highlighted** - Scores ≥60 shown prominently  
✅ **AI analysis** - View LLM summaries for hot leads  
✅ **Filters** - Filter by industry, score, LCP  
✅ **Export** - Download CSV or sales report  

### Automation Tab

✅ **Visual scheduler** - Pick day and time  
✅ **Multi-location** - Search multiple cities  
✅ **Flexible modes** - Auto, manual, or hybrid  
✅ **Git integration** - Auto-generates workflow  
✅ **Test button** - Run automation immediately  
✅ **Setup guide** - Built-in help  

### Results Dashboard

✅ **Historical data** - View all past searches  
✅ **Metrics** - Total, hot, warm, cold leads  
✅ **Charts** - Industry distribution, score breakdown  
✅ **Advanced filters** - Multi-select industries, score ranges  
✅ **Bulk export** - Download filtered results  

---

## 📊 Understanding Results

### Lead Categories

| Category | Score | Description |
|----------|-------|-------------|
| 🔥 **Hot** | 60-100 | High SEO opportunity, ready to contact |
| 🌡️ **Warm** | 40-59 | Moderate opportunity, worth considering |
| ❄️ **Cold** | 0-39 | Low opportunity, may not be worth pursuing |

### Key Metrics

- **SEO Score**: Overall SEO opportunity (0-100)
- **LCP Score**: Largest Contentful Paint (seconds) - lower is better
- **Schema**: Whether site has structured data
- **Tech Stack**: Website platform (WordPress, Custom, etc.)

### Hot Lead Indicators

A lead is "hot" (score ≥60) when it has:
- ✅ Slow page speed (LCP > 2.5s)
- ✅ Missing schema markup
- ✅ Poor mobile optimization
- ✅ Outdated design
- ✅ Missing SEO basics

---

## 🔧 Troubleshooting

### UI won't start

```bash
# Install dependencies
pip3 install -r requirements.txt

# Try running again
streamlit run app.py
```

### No results showing

1. Check that `.env` file has API keys
2. Run a manual search first
3. Check `out/` directory for CSV files

### Automation not working

1. Verify GitHub Secrets are set
2. Check `.github/workflows/weekly.yml` exists
3. Go to GitHub Actions tab to see run history
4. Make sure workflow file is committed and pushed

### "Module not found" errors

```bash
# Make sure you're in the right directory
cd seo_lead_finder

# Install all dependencies
pip3 install -r requirements.txt
```

---

## 🎯 Best Practices

### For Manual Searches

1. **Start small**: Test with 1-2 industries first
2. **Use auto-discover**: Let AI find the best industries
3. **Check hot leads**: Focus on scores ≥60
4. **Read AI summaries**: Understand why each lead is valuable

### For Automation

1. **Start weekly**: Don't over-automate at first
2. **Monitor results**: Check GitHub Actions runs
3. **Adjust schedule**: Find the best day/time for your workflow
4. **Use Slack**: Get instant notifications
5. **Review regularly**: Check results dashboard weekly

### For Sales Outreach

1. **Prioritize hot leads**: Start with scores ≥60
2. **Read AI analysis**: Understand their specific needs
3. **Personalize outreach**: Mention specific issues (slow LCP, missing schema)
4. **Track conversions**: Note which industries convert best
5. **Refine targeting**: Adjust automation based on results

---

## 📈 Deployment Options

### Option 1: Local (Current)

```bash
streamlit run app.py
```

**Pros:** Free, full control  
**Cons:** Must keep computer running

### Option 2: Streamlit Cloud (Recommended)

1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Deploy!

**Pros:** Free, always online, auto-updates  
**Cons:** Public URL (can add authentication)

### Option 3: Self-hosted Server

Deploy to AWS, DigitalOcean, etc.

```bash
# Install on server
pip install -r requirements.txt

# Run with nohup
nohup streamlit run app.py --server.port 8501 &
```

**Pros:** Full control, private  
**Cons:** Costs money, requires maintenance

---

## 🎨 Customization

### Change Colors

Edit `app.py` and modify the CSS in the `st.markdown()` section:

```python
st.markdown("""
<style>
    .hot-lead {
        background-color: #your-color;
        border-left: 4px solid #your-border-color;
    }
</style>
""", unsafe_allow_html=True)
```

### Add More Metrics

Edit the metrics section in each tab to add custom calculations.

### Change Default Values

Modify the default values in text inputs and selectors.

---

## 💡 Tips & Tricks

1. **Bookmark the UI**: Add `http://localhost:8501` to bookmarks
2. **Use keyboard shortcuts**: Streamlit has built-in shortcuts (press `?` to see)
3. **Auto-refresh**: Enable in Streamlit settings for live updates
4. **Download regularly**: Export results to keep historical data
5. **Share results**: Use the share button to send to team members

---

## 🆘 Support

- **Documentation**: See `README.md` for full setup guide
- **API Setup**: See `API_SETUP_GUIDE.md` for API configuration
- **GitHub Issues**: Report bugs at [GitHub repo](https://github.com/lelandsequel/SequelSEO333/issues)

---

## 🚀 Next Steps

1. ✅ Launch the UI: `streamlit run app.py`
2. ✅ Run a manual search to test
3. ✅ Configure automation for weekly runs
4. ✅ Set up GitHub Secrets
5. ✅ Deploy to Streamlit Cloud (optional)
6. ✅ Start finding leads! 🎯

