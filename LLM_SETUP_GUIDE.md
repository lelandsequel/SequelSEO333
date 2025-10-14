# 🤖 LLM-Powered SEO Analysis Setup

## Why Use LLMs Instead of Ahrefs?

**Ahrefs API:** $500+/month 💸  
**Claude API:** ~$3 per 1M tokens (analyze 1,000+ websites for $5-10) 🎉

### What You Get:

| Feature | Ahrefs | Claude/GPT |
|---------|--------|------------|
| Traffic estimates | ✅ | ❌ |
| Backlink data | ✅ | ❌ |
| **Content quality analysis** | ❌ | ✅ |
| **SEO recommendations** | ❌ | ✅ |
| **Missing opportunities** | ❌ | ✅ |
| **Technical SEO issues** | ❌ | ✅ |
| **Call-to-action analysis** | ❌ | ✅ |

---

## 🚀 Quick Setup

### Option 1: Claude API (Recommended - Cheaper & Better)

1. **Go to:** https://console.anthropic.com/
2. **Sign up** for an Anthropic account
3. **Add credits:** $5 minimum (will last for thousands of analyses)
4. **Create API key:**
   - Click "API Keys" in the left sidebar
   - Click "Create Key"
   - Copy the key (starts with `sk-ant-...`)
5. **Add to `.env`:**
   ```bash
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

**Cost:** ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens  
**Model used:** `claude-3-haiku-20240307` (fastest, cheapest)

---

### Option 2: OpenAI API (Alternative)

1. **Go to:** https://platform.openai.com/api-keys
2. **Sign up** for an OpenAI account
3. **Add credits:** $5 minimum
4. **Create API key:**
   - Click "+ Create new secret key"
   - Copy the key (starts with `sk-...`)
5. **Add to `.env`:**
   ```bash
   OPENAI_API_KEY=sk-your-key-here
   ```

**Cost:** ~$0.50 per 1M input tokens, ~$1.50 per 1M output tokens  
**Model used:** `gpt-3.5-turbo`

---

## 📊 Cost Breakdown

### Analyzing 1,000 Websites:

**With Claude Haiku:**
- Input: ~3,000 tokens per site × 1,000 = 3M tokens = $0.75
- Output: ~500 tokens per site × 1,000 = 500K tokens = $0.63
- **Total: ~$1.38** 🎉

**With GPT-3.5-turbo:**
- Input: ~3,000 tokens per site × 1,000 = 3M tokens = $1.50
- Output: ~500 tokens per site × 1,000 = 500K tokens = $0.75
- **Total: ~$2.25** 👍

**With Ahrefs:**
- **$500/month** minimum 💸

---

## 🧪 Test Your Setup

After adding your API key to `.env`, run:

```bash
python3 -m modules.llm_seo_analyzer
```

This will test the LLM integration with example.com.

---

## 🎯 What the LLM Analyzes

For each website, the LLM provides:

1. **SEO Score (0-100):** Overall content quality
2. **Top 3 Issues:** Specific problems found
   - Example: "Missing H1 tag", "No meta description", "Thin content"
3. **Top 3 Opportunities:** Actionable improvements
   - Example: "Add FAQ schema", "Improve CTA", "Add testimonials"
4. **Content Quality:** Brief assessment
   - Example: "Generic content, lacks local focus"
5. **Call-to-Action:** Does it have a clear CTA?

---

## 🔧 Integration with Pipeline

The LLM analysis is **automatically integrated** into the scoring system:

```python
# In modules/scoring.py
score = (
    pagespeed_score * 0.3 +      # 30% - Technical performance
    seo_basics_score * 0.2 +     # 20% - Basic SEO
    llm_content_score * 0.3 +    # 30% - AI content analysis ⭐
    engagement_score * 0.2       # 20% - Engagement signals
)
```

---

## 💡 Pro Tips

### 1. Start with Claude Haiku
- Cheapest option
- Fast responses
- Great for this use case

### 2. Set Budget Alerts
- In Anthropic Console: Settings → Billing → Set monthly limit
- Recommended: $10/month for testing

### 3. Rate Limiting
- The code already includes delays between requests
- Claude: 50 requests/minute (plenty for our use)
- OpenAI: 60 requests/minute

### 4. Fallback Behavior
- If no LLM API key is set, the pipeline still works
- It just skips the AI analysis
- You still get PageSpeed + basic SEO data

---

## 🆚 Claude vs OpenAI

| Feature | Claude Haiku | GPT-3.5-turbo |
|---------|--------------|---------------|
| **Cost** | ✅ Cheaper | More expensive |
| **Speed** | ✅ Faster | Slower |
| **Quality** | ✅ Better for analysis | Good |
| **JSON output** | ✅ More reliable | Sometimes messy |
| **Setup** | Easy | Easy |

**Recommendation:** Use Claude Haiku

---

## 🔒 Security

- Never commit your `.env` file (already in `.gitignore`)
- Rotate API keys regularly
- Set spending limits in the console
- Monitor usage in the dashboard

---

## 📈 Expected Results

With LLM analysis enabled, you'll see output like:

```
🤖 LLM: Analyzing https://example-plumber.com...
🤖 Claude: Score=65/100

Issues found:
  - No clear call-to-action above the fold
  - Missing local service area pages
  - Outdated blog content (last post 2 years ago)

Opportunities:
  - Add emergency service CTA
  - Create neighborhood-specific pages
  - Add customer testimonials with schema
```

This gives you **actionable insights** to pitch to potential clients!

---

## ❓ FAQ

**Q: Do I need both Claude AND OpenAI?**  
A: No! Pick one. Claude is recommended.

**Q: What if I don't want to pay for LLM?**  
A: The tool still works! You just won't get AI content analysis.

**Q: Can I use GPT-4 instead?**  
A: Yes, but it's 10x more expensive. Not worth it for this use case.

**Q: How do I know it's working?**  
A: Run `python3 test_all_apis.py` to test all integrations.

---

## 🎉 Ready to Go!

Once you've added your API key:

1. Install dependencies: `pip3 install -r requirements.txt`
2. Test: `python3 -m modules.llm_seo_analyzer`
3. Run pipeline: `python3 main.py`

Your leads will now include AI-powered SEO insights! 🚀

