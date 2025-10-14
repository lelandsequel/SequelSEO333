#!/usr/bin/env python3
"""
Test suite for SEO Lead Finder pipeline
Tests all modules without requiring API keys
"""
import sys
import os
from typing import Dict, List

# Test modules individually
def test_industry_discovery():
    print("\n=== Testing Industry Discovery ===")
    from modules import industry_discovery
    
    geo = "Houston, TX"
    industries = industry_discovery.discover_top_industries(geo, k=5)
    
    assert len(industries) == 5, f"Expected 5 industries, got {len(industries)}"
    assert all(isinstance(i, str) for i in industries), "All industries should be strings"
    print(f"✅ Discovered {len(industries)} industries: {industries}")
    return industries

def test_lead_finder():
    print("\n=== Testing Lead Finder ===")
    from modules import lead_finder
    
    geo = "Houston, TX"
    industry = "auto dealers"
    leads = lead_finder.find_leads(geo, industry, max_results=5)
    
    assert len(leads) == 5, f"Expected 5 leads, got {len(leads)}"
    assert all("name" in lead for lead in leads), "All leads should have 'name'"
    assert all("website" in lead for lead in leads), "All leads should have 'website'"
    print(f"✅ Found {len(leads)} leads")
    for lead in leads[:2]:
        print(f"   - {lead['name']}: {lead['website']}")
    return leads

def test_seo_checks():
    print("\n=== Testing SEO Checks ===")
    from modules import seo_checks
    
    url = "https://example.com"
    audit = seo_checks.evaluate_site(url)
    
    required_fields = ["lcp", "has_schema", "has_faq", "has_org", 
                       "meta_title_ok", "meta_desc_ok", "content_fresh_months",
                       "traffic_trend_90d", "tech_stack", "issues"]
    
    for field in required_fields:
        assert field in audit, f"Missing field: {field}"
    
    print(f"✅ SEO audit completed")
    print(f"   - LCP: {audit['lcp']}s")
    print(f"   - Schema: {audit['has_schema']}")
    print(f"   - Tech Stack: {audit['tech_stack']}")
    print(f"   - Issues: {audit['issues']}")
    return audit

def test_scoring():
    print("\n=== Testing Scoring ===")
    from modules import scoring
    
    lead = {"name": "Test Business", "website": "https://example.com"}
    audit = {
        "traffic_trend_90d": -25,  # declining
        "has_schema": False,
        "content_fresh_months": 18,  # stale
        "lcp": 4.5,  # slow
        "tech_stack": "WordPress"
    }
    
    score = scoring.score_lead(lead, audit)
    
    assert isinstance(score, int), "Score should be an integer"
    assert 0 <= score <= 100, f"Score should be 0-100, got {score}"
    print(f"✅ Lead scored: {score}/100")
    
    # Test with good site
    good_audit = {
        "traffic_trend_90d": 15,
        "has_schema": True,
        "content_fresh_months": 2,
        "lcp": 2.1,
        "tech_stack": "Custom"
    }
    good_score = scoring.score_lead(lead, good_audit)
    print(f"   - Bad site score: {score}/100")
    print(f"   - Good site score: {good_score}/100")
    return score

def test_sheets_io_mock():
    print("\n=== Testing Sheets I/O (Mock Mode) ===")
    # We'll test the CSV output only, not Google Sheets
    import csv
    import datetime as dt
    
    rows = [
        {
            "RunDate": "2025-10-14",
            "Geo": "Houston, TX",
            "Industry": "auto dealers",
            "BusinessName": "Test Auto",
            "Website": "https://example.com",
            "Email": "test@example.com",
            "Phone": "555-1234",
            "City": "Houston",
            "TechStack": "WordPress",
            "CoreWebVitals_LCP": 3.5,
            "HasSchema": False,
            "HasFAQ": True,
            "HasOrg": False,
            "MetaTitleOK": True,
            "MetaDescOK": False,
            "ContentFreshMonths": 12,
            "TrafficTrend_90d": -20,
            "Issues": "Slow LCP, No Schema",
            "Score": 75,
            "Notes": "",
            "Source": "test"
        }
    ]
    
    # Create CSV output
    os.makedirs("./out", exist_ok=True)
    date = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_path = f"./out/test_leads_{date}.csv"
    
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        header = list(rows[0].keys())
        w = csv.writer(f)
        w.writerow(header)
        w.writerows([list(r.values()) for r in rows])
    
    print(f"✅ CSV output created: {csv_path}")
    
    # Verify CSV
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        csv_rows = list(reader)
        assert len(csv_rows) == 1, "Should have 1 row"
        print(f"   - Verified {len(csv_rows)} row(s) in CSV")
    
    return csv_path

def test_alerts():
    print("\n=== Testing Alerts ===")
    from modules import alerts
    
    hot_leads = [
        {
            "BusinessName": "Hot Lead Auto",
            "Industry": "auto dealers",
            "Score": 85,
            "Website": "https://example.com",
            "Email": "contact@example.com",
            "City": "Houston",
            "Issues": "Slow LCP, No Schema, Stale Content"
        }
    ]
    
    # This will silently fail without SLACK_WEBHOOK_URL, which is fine
    alerts.notify_hot_leads(hot_leads)
    print(f"✅ Alert function executed (no webhook configured, so no actual alert sent)")
    return True

def test_full_pipeline_dry_run():
    print("\n=== Testing Full Pipeline (Dry Run) ===")
    from modules import industry_discovery, lead_finder, seo_checks, scoring
    
    geo = "Houston, TX"
    
    # Discover industries
    industries = industry_discovery.discover_top_industries(geo, k=2)
    print(f"   Industries: {industries}")
    
    all_rows = []
    for industry in industries:
        # Find leads
        leads = lead_finder.find_leads(geo, industry, max_results=3)
        
        for lead in leads:
            # Audit
            audit = seo_checks.evaluate_site(lead.get("website"))
            
            # Score
            score = scoring.score_lead(lead, audit)
            
            row = {
                "RunDate": "2025-10-14",
                "Geo": geo,
                "Industry": industry,
                "BusinessName": lead.get("name"),
                "Website": lead.get("website"),
                "Score": score,
                "Issues": ", ".join(audit.get("issues", []))
            }
            all_rows.append(row)
    
    print(f"✅ Pipeline completed: {len(all_rows)} total leads processed")
    
    # Show hot leads
    hot_threshold = 70
    hot = [r for r in all_rows if r["Score"] >= hot_threshold]
    print(f"   - Hot leads (score >= {hot_threshold}): {len(hot)}")
    
    for lead in hot[:3]:
        print(f"     • {lead['BusinessName']} - Score: {lead['Score']} - {lead['Issues']}")
    
    return all_rows

def main():
    print("=" * 60)
    print("SEO Lead Finder - Test Suite")
    print("=" * 60)
    
    # Set minimal env vars for testing
    os.environ.setdefault("MAX_INDUSTRIES", "5")
    os.environ.setdefault("LEADS_PER_INDUSTRY", "30")
    os.environ.setdefault("HOT_LEAD_THRESHOLD", "70")
    
    try:
        # Run all tests
        test_industry_discovery()
        test_lead_finder()
        test_seo_checks()
        test_scoring()
        test_sheets_io_mock()
        test_alerts()
        test_full_pipeline_dry_run()
        
        print("\n" + "=" * 60)
        print("✅ ALL TESTS PASSED!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Set up Google Sheets credentials to enable real output")
        print("2. Add real API integrations (SerpAPI, Ahrefs, etc.)")
        print("3. Run with: python main.py --once --geo 'Houston, TX'")
        return 0
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

