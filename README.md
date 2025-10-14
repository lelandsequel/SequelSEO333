# SEO Lead Finder — Hybrid Deep Research + Agentic Search

A production-ready scaffold to discover **the 5 industries most in need of SEO/AEO** each week in a target geography, then identify and score businesses, log them to Google Sheets, and notify you for hot leads.

- **Weekly schedule (Sundays)** via APScheduler (local run) or GitHub Actions (CI).
- **Industry Discovery**: Ranks industries by "SEO need" using multiple signals.
- **Lead Finder**: Enumerates businesses and runs light SEO/AEO checks.
- **Scoring**: Weighted score for buy signals.
- **Outputs**: Google Sheet + CSV archive.
- **Alerts**: Slack webhook for hot leads.

> Works great with VS Code + Augment Code. Fill in `.env`, keep coding, and ship.

---

## Quickstart

1. **Clone / unzip** this project.
2. Create and fill **.env** from `.env.example` (API keys & config).
3. Install deps:
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```
4. (Optional) Enable GitHub Actions with your secrets to run weekly.
5. Run once locally to test:
   ```bash
   python main.py --geo "Houston, TX"
   ```

### Required/Optional APIs
- **SERP**: SerpAPI or Google Custom Search (SERPAPI_KEY or GCS creds)
- **Traffic/Backlinks (optional)**: Ahrefs/Semrush API
- **PageSpeed/Lighthouse (optional)**: PSI API (PageSpeed Insights)
- **Contacts (optional)**: Hunter.io or Clearbit
- **Sheets**: Service Account JSON or OAuth; see `sheets_io.py`

> All integrations are **optional**. Stubs and fallbacks are provided so you can iterate safely.

---

## Scheduling

### APScheduler (local/server)
- `main.py` registers a weekly job **Sundays 9:00 America/Chicago** (default).

### GitHub Actions (CI)
- `workflows/weekly.yml` runs on Sundays at **15:00 UTC**. Adjust if needed.
  - During CDT (Mar–Nov), 15:00 UTC = 10:00 CT.
  - During CST (Nov–Mar), 15:00 UTC = 09:00 CT.

---

## Output Columns (Google Sheet)

```
[RunDate, Geo, Industry, BusinessName, Website, Email, Phone, City, TechStack,
 CoreWebVitals_LCP, HasSchema, HasFAQ, HasOrg, MetaTitleOK, MetaDescOK,
 ContentFreshMonths, TrafficTrend_90d, Issues, Score, Notes, Source]
```

---

## Extend

- Add vertical-specific checks (e.g., inventory pages for auto, service pages for law).
- Pipe into HubSpot/Notion: see `alerts.py` for a template.
- Use the `prompts/aeo_summary.md` template to auto-generate outreach blurbs.
