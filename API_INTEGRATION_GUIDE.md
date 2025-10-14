# 🔌 API Integration Guide

This guide shows you how to replace stub functions with real API integrations.

---

## Current Status: Stub vs Real Data

| Module | Current (Stub) | Real Integration | Priority |
|--------|---------------|------------------|----------|
| Industry Discovery | Hash-based scoring | SerpAPI search volume | High |
| Lead Finder | Fake businesses | Google Places API | High |
| SEO Checks | Random metrics | Real HTML + PSI API | Medium |
| Contact Discovery | Empty fields | Hunter.io API | Low |
| Traffic Data | Random trends | Ahrefs/Semrush API | Low |

---

## 1. Industry Discovery (SerpAPI)

### Current Implementation
<augment_code_snippet path="seo_lead_finder/modules/industry_discovery.py" mode="EXCERPT">
````python
def _serp_volume_proxy(geo: str, industry: str) -> float:
    # TODO: call SerpAPI or Google Custom Search
    seed = abs(hash((geo.lower(), industry.lower()))) % 1000
    return 100 + (seed % 300)  # 100-400
````
</augment_code_snippet>

### Real Implementation with SerpAPI

```python
import os
import requests

def _serp_volume_proxy(geo: str, industry: str) -> float:
    """Get real search volume using SerpAPI"""
    api_key = os.getenv("SERPAPI_KEY")
    if not api_key:
        # Fallback to stub
        seed = abs(hash((geo.lower(), industry.lower()))) % 1000
        return 100 + (seed % 300)
    
    try:
        # Search for "{industry} near me" in geo
        params = {
            "engine": "google",
            "q": f"{industry} near me",
            "location": geo,
            "api_key": api_key
        }
        
        response = requests.get("https://serpapi.com/search", params=params, timeout=10)
        data = response.json()
        
        # Extract metrics
        total_results = data.get("search_information", {}).get("total_results", 0)
        ads_count = len(data.get("ads", []))
        local_results = len(data.get("local_results", []))
        
        # Calculate demand score
        # More results + more ads + more local = higher demand
        score = (total_results / 1000) + (ads_count * 50) + (local_results * 20)
        
        return min(score, 1000)  # Cap at 1000
        
    except Exception as e:
        print(f"SerpAPI error: {e}, using fallback")
        seed = abs(hash((geo.lower(), industry.lower()))) % 1000
        return 100 + (seed % 300)
```

**Setup:**
1. Sign up at https://serpapi.com/
2. Get API key
3. Add to `.env`: `SERPAPI_KEY=your_key_here`

---

## 2. Lead Finder (Google Places API)

### Current Implementation
<augment_code_snippet path="seo_lead_finder/modules/lead_finder.py" mode="EXCERPT">
````python
def _fake_directory_search(geo: str, industry: str, max_results: int) -> List[Dict]:
    seeds = []
    for i in range(max_results):
        seeds.append({
            "name": f"{industry.title()} Biz {i+1}",
            "website": f"https://www.example-{industry.replace(' ', '-')}-{i+1}.com",
            ...
````
</augment_code_snippet>

### Real Implementation with Google Places

```python
import os
import requests
from typing import List, Dict

def _google_places_search(geo: str, industry: str, max_results: int) -> List[Dict]:
    """Find real businesses using Google Places API"""
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not api_key:
        return _fake_directory_search(geo, industry, max_results)
    
    try:
        # Text search for businesses
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": f"{industry} in {geo}",
            "key": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        leads = []
        for place in data.get("results", [])[:max_results]:
            place_id = place.get("place_id")
            
            # Get place details for website, phone, etc.
            details_url = "https://maps.googleapis.com/maps/api/place/details/json"
            details_params = {
                "place_id": place_id,
                "fields": "name,website,formatted_phone_number,formatted_address",
                "key": api_key
            }
            
            details_response = requests.get(details_url, params=details_params, timeout=10)
            details = details_response.json().get("result", {})
            
            leads.append({
                "name": details.get("name", ""),
                "website": details.get("website", ""),
                "phone": details.get("formatted_phone_number", ""),
                "address": details.get("formatted_address", ""),
                "city": geo.split(",")[0],
                "email": "",  # Will be filled by Hunter.io
                "source": "google_places"
            })
        
        return leads
        
    except Exception as e:
        print(f"Google Places error: {e}, using fallback")
        return _fake_directory_search(geo, industry, max_results)

def find_leads(geo: str, industry: str, max_results: int = 30) -> List[Dict]:
    # Try Google Places first, fallback to stub
    return _google_places_search(geo, industry, max_results)
```

**Setup:**
1. Enable Google Places API at https://console.cloud.google.com/
2. Create API key
3. Add to `.env`: `GOOGLE_PLACES_API_KEY=your_key_here`

---

## 3. SEO Checks (Real HTML Parsing + PageSpeed)

### Current Implementation
<augment_code_snippet path="seo_lead_finder/modules/seo_checks.py" mode="EXCERPT">
````python
def evaluate_site(url: str) -> Dict:
    # TODO: Replace with real fetch + parse + PSI/Ahrefs checks.
    issues: List[str] = []
    lcp = round(random.uniform(2.0, 5.5), 2)
    ...
````
</augment_code_snippet>

### Real Implementation

```python
import os
import requests
from bs4 import BeautifulSoup
from typing import Dict, List
import random

def _fetch_pagespeed_metrics(url: str) -> Dict:
    """Get real PageSpeed Insights metrics"""
    api_key = os.getenv("PSI_API_KEY")
    if not api_key:
        return {
            "lcp": round(random.uniform(2.0, 5.5), 2),
            "fcp": round(random.uniform(1.0, 3.0), 2),
            "cls": round(random.uniform(0.0, 0.3), 2)
        }
    
    try:
        psi_url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            "url": url,
            "key": api_key,
            "category": "performance"
        }
        
        response = requests.get(psi_url, params=params, timeout=30)
        data = response.json()
        
        metrics = data.get("lighthouseResult", {}).get("audits", {})
        lcp_audit = metrics.get("largest-contentful-paint", {})
        
        return {
            "lcp": lcp_audit.get("numericValue", 0) / 1000,  # Convert to seconds
            "score": data.get("lighthouseResult", {}).get("categories", {}).get("performance", {}).get("score", 0) * 100
        }
        
    except Exception as e:
        print(f"PSI error for {url}: {e}")
        return {"lcp": round(random.uniform(2.0, 5.5), 2)}

def _parse_html_seo(url: str) -> Dict:
    """Parse HTML for SEO elements"""
    try:
        response = requests.get(url, timeout=10, headers={
            "User-Agent": "Mozilla/5.0 (compatible; SEOBot/1.0)"
        })
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Check for Schema.org
        has_schema = bool(soup.find_all(attrs={"itemtype": True})) or \
                     bool(soup.find_all("script", type="application/ld+json"))
        
        # Check for FAQ schema
        has_faq = "FAQPage" in response.text or "Question" in response.text
        
        # Check for Organization schema
        has_org = "Organization" in response.text
        
        # Check meta tags
        title = soup.find("title")
        meta_title_ok = bool(title and 30 <= len(title.text) <= 60)
        
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc_ok = bool(meta_desc and 120 <= len(meta_desc.get("content", "")) <= 160)
        
        # Detect tech stack
        tech_stack = "Custom"
        if "wp-content" in response.text or "wordpress" in response.text.lower():
            tech_stack = "WordPress"
        elif "wix.com" in response.text:
            tech_stack = "Wix"
        elif "squarespace" in response.text.lower():
            tech_stack = "Squarespace"
        
        return {
            "has_schema": has_schema,
            "has_faq": has_faq,
            "has_org": has_org,
            "meta_title_ok": meta_title_ok,
            "meta_desc_ok": meta_desc_ok,
            "tech_stack": tech_stack
        }
        
    except Exception as e:
        print(f"HTML parse error for {url}: {e}")
        return {
            "has_schema": False,
            "has_faq": False,
            "has_org": False,
            "meta_title_ok": False,
            "meta_desc_ok": False,
            "tech_stack": "Unknown"
        }

def evaluate_site(url: str) -> Dict:
    """Evaluate site with real data"""
    if not url or "example" in url:
        # Stub data for fake URLs
        return _generate_stub_audit()
    
    # Get real metrics
    psi_metrics = _fetch_pagespeed_metrics(url)
    html_data = _parse_html_seo(url)
    
    issues = []
    lcp = psi_metrics.get("lcp", 3.0)
    if lcp > 3.0:
        issues.append("Slow LCP")
    
    if not html_data.get("has_schema"):
        issues.append("No Schema.org")
    
    # Combine all data
    return {
        "lcp": lcp,
        "has_schema": html_data.get("has_schema"),
        "has_faq": html_data.get("has_faq"),
        "has_org": html_data.get("has_org"),
        "meta_title_ok": html_data.get("meta_title_ok"),
        "meta_desc_ok": html_data.get("meta_desc_ok"),
        "tech_stack": html_data.get("tech_stack"),
        "content_fresh_months": 6,  # TODO: Add content freshness check
        "traffic_trend_90d": 0,  # TODO: Add Ahrefs integration
        "issues": issues,
        "notes": ""
    }
```

**Setup:**
1. Get PageSpeed Insights API key at https://console.cloud.google.com/
2. Add to `.env`: `PSI_API_KEY=your_key_here`

---

## 4. Email Discovery (Hunter.io)

```python
import os
import requests

def _find_email(domain: str, company_name: str) -> str:
    """Find email using Hunter.io"""
    api_key = os.getenv("HUNTER_API_KEY")
    if not api_key:
        return ""
    
    try:
        url = "https://api.hunter.io/v2/domain-search"
        params = {
            "domain": domain,
            "api_key": api_key,
            "limit": 1
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        emails = data.get("data", {}).get("emails", [])
        if emails:
            return emails[0].get("value", "")
        
        return ""
        
    except Exception as e:
        print(f"Hunter.io error: {e}")
        return ""

# Add to lead_finder.py after getting business data
for lead in leads:
    if lead.get("website"):
        domain = lead["website"].replace("https://", "").replace("http://", "").split("/")[0]
        lead["email"] = _find_email(domain, lead.get("name", ""))
```

**Setup:**
1. Sign up at https://hunter.io/
2. Get API key
3. Add to `.env`: `HUNTER_API_KEY=your_key_here`

---

## 5. Traffic Data (Ahrefs)

```python
import os
import requests

def _get_traffic_trend(domain: str) -> Dict:
    """Get traffic trend from Ahrefs"""
    api_key = os.getenv("AHREFS_API_KEY")
    if not api_key:
        return {"traffic_trend_90d": 0}
    
    try:
        url = "https://api.ahrefs.com/v3/site-explorer/metrics-history"
        params = {
            "target": domain,
            "mode": "domain",
            "history": "monthly",
            "token": api_key
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        # Calculate 90-day trend
        history = data.get("metrics", [])
        if len(history) >= 3:
            recent = sum([m.get("organic_traffic", 0) for m in history[:3]]) / 3
            older = sum([m.get("organic_traffic", 0) for m in history[3:6]]) / 3
            
            if older > 0:
                trend = ((recent - older) / older) * 100
                return {"traffic_trend_90d": round(trend, 1)}
        
        return {"traffic_trend_90d": 0}
        
    except Exception as e:
        print(f"Ahrefs error: {e}")
        return {"traffic_trend_90d": 0}
```

**Setup:**
1. Sign up at https://ahrefs.com/api
2. Get API key
3. Add to `.env`: `AHREFS_API_KEY=your_key_here`

---

## Integration Priority

### Phase 1: Core Data (Do First)
1. ✅ Google Places API - Real businesses
2. ✅ Basic HTML parsing - Schema, meta tags
3. ✅ PageSpeed Insights - Real performance metrics

### Phase 2: Enhanced Data
4. ⬜ SerpAPI - Real search volume
5. ⬜ Hunter.io - Email discovery
6. ⬜ Ahrefs - Traffic trends

### Phase 3: Advanced Features
7. ⬜ Content freshness detection
8. ⬜ Backlink analysis
9. ⬜ Competitor analysis
10. ⬜ Industry-specific checks

---

## Testing Real Integrations

```bash
# Test with one real business
python3 -c "
from modules import seo_checks
result = seo_checks.evaluate_site('https://example.com')
print(result)
"

# Test full pipeline with real data
python3 main.py --once --geo 'Austin, TX'
```

---

## Cost Estimates

| Service | Free Tier | Paid Plans |
|---------|-----------|------------|
| SerpAPI | 100 searches/month | $50/month for 5,000 |
| Google Places | $0 for first $200/month | ~$0.032 per request |
| PageSpeed Insights | Free | Free (rate limited) |
| Hunter.io | 25 searches/month | $49/month for 500 |
| Ahrefs | No free tier | $99/month minimum |

**Recommendation:** Start with Google Places + PageSpeed (mostly free), add others as needed.

---

## Error Handling Best Practices

Always include fallbacks:

```python
def api_call_with_fallback():
    try:
        # Try real API
        return real_api_call()
    except Exception as e:
        print(f"API error: {e}, using fallback")
        return stub_data()
```

This ensures the pipeline never breaks due to API issues.

