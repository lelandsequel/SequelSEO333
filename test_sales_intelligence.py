#!/usr/bin/env python3
"""
Test the new sales intelligence features:
1. LLM-powered deep analysis
2. Sales report generation
"""

from dotenv import load_dotenv
load_dotenv()

from modules import llm_seo_analyzer, report_generator

def test_llm_analysis():
    """Test LLM analysis on a real website."""
    print("=" * 80)
    print("TESTING LLM SALES INTELLIGENCE ANALYSIS")
    print("=" * 80)
    print()
    
    # Test with a real business from our Denver results
    test_url = "http://www.dclc.co/"
    business_name = "Children's Learning Center"
    industry = "daycare"
    
    print(f"Analyzing: {business_name}")
    print(f"Industry: {industry}")
    print(f"Website: {test_url}")
    print()
    print("This will take ~10-15 seconds...")
    print()
    
    result = llm_seo_analyzer.analyze_website_with_llm(
        url=test_url,
        business_name=business_name,
        industry=industry
    )
    
    print("\n" + "=" * 80)
    print("RESULTS:")
    print("=" * 80)
    print()
    
    print(f"📊 SEO Score: {result.get('llm_seo_score', 'N/A')}/100")
    print()
    
    print("🚨 Critical Issues:")
    for issue in result.get('llm_critical_issues', []):
        print(f"  • {issue}")
    print()
    
    print(f"💰 Revenue Impact: {result.get('llm_revenue_impact', 'N/A')}")
    print()
    
    print("🎯 Opportunities:")
    for opp in result.get('llm_opportunities', []):
        print(f"  • {opp}")
    print()
    
    print("🔧 Services Offered:")
    services = result.get('llm_services_offered', [])
    if services:
        print(f"  {', '.join(services)}")
    else:
        print("  N/A")
    print()
    
    print(f"💡 Unique Selling Proposition: {result.get('llm_unique_selling_proposition', 'N/A')}")
    print()
    
    print(f"📞 Call-to-Action Quality: {result.get('llm_call_to_action_quality', 'N/A')}")
    print()
    
    print("🎯 Target Keywords:")
    for kw in result.get('llm_target_keywords', []):
        print(f"  • {kw}")
    print()
    
    print("❌ Missing Keywords:")
    for kw in result.get('llm_missing_keywords', []):
        print(f"  • {kw}")
    print()
    
    print("✅ Quick Wins:")
    for win in result.get('llm_quick_wins', []):
        print(f"  • {win}")
    print()
    
    print("🎯 Pitch Angle:")
    print(f"  {result.get('llm_pitch_angle', 'N/A')}")
    print()
    
    print("📝 Content Quality:")
    print(f"  {result.get('llm_content_quality', 'N/A')}")
    print()


def test_report_generation():
    """Test sales report generation with sample data."""
    print("\n" + "=" * 80)
    print("TESTING SALES REPORT GENERATION")
    print("=" * 80)
    print()
    
    # Create sample hot leads (simulating what main.py would generate)
    sample_leads = [
        {
            "RunDate": "2025-10-14",
            "Geo": "Denver, CO",
            "Industry": "daycare",
            "BusinessName": "Children's Learning Center",
            "Website": "http://www.dclc.co/",
            "Phone": "(303) 455-4865",
            "City": "Denver",
            "TechStack": "WordPress",
            "CoreWebVitals_LCP": 8.54,
            "HasSchema": False,
            "Issues": "Slow LCP, No Schema.org, Stale Content, Traffic Decline",
            "Score": 95,
            "LLM_SEOScore": 45,
            "LLM_CriticalIssues": [
                "8.5 second page load time on mobile",
                "Missing local business schema markup",
                "No clear call-to-action above the fold",
                "Content hasn't been updated in 18+ months"
            ],
            "LLM_RevenueImpact": "$5,000-8,000/month",
            "LLM_Opportunities": [
                "Implement local business schema to appear in Google's local pack",
                "Speed optimization could reduce bounce rate by 40%",
                "Add enrollment CTA above the fold",
                "Create blog content targeting 'daycare Denver' keywords",
                "Add parent testimonials and trust signals"
            ],
            "LLM_ServicesOffered": [
                "Infant care",
                "Toddler programs",
                "Preschool",
                "Before/after school care"
            ],
            "LLM_USP": "Family-owned for 25+ years, focus on early childhood development",
            "LLM_CTAQuality": "Weak",
            "LLM_TargetKeywords": ["daycare", "childcare", "Denver"],
            "LLM_MissingKeywords": [
                "daycare near me",
                "best daycare Denver",
                "infant care Denver",
                "preschool programs"
            ],
            "LLM_ContentQuality": "Basic information present but lacks depth. No blog, no parent resources, minimal trust signals.",
            "LLM_QuickWins": [
                "Add schema markup (1 day)",
                "Optimize images and enable caching (2 days)",
                "Add prominent enrollment CTA (1 day)",
                "Create 'Why Choose Us' section with testimonials (3 days)"
            ],
            "LLM_PitchAngle": "Your website takes 8.5 seconds to load - that's costing you enrollments. Parents searching for daycare won't wait that long. I can fix this in 2 weeks and get you showing up in Google's local results above your competitors."
        },
        {
            "RunDate": "2025-10-14",
            "Geo": "Denver, CO",
            "Industry": "plumbers",
            "BusinessName": "High 5 Plumbing",
            "Website": "https://high5plumbing.com/",
            "Phone": "(720) 340-3843",
            "City": "Denver",
            "TechStack": "WordPress",
            "CoreWebVitals_LCP": 22.24,
            "HasSchema": False,
            "Issues": "Slow LCP, No Schema.org, Stale Content",
            "Score": 95,
            "LLM_SEOScore": 38,
            "LLM_CriticalIssues": [
                "22 second page load time - losing 75% of mobile visitors",
                "Not appearing in Google's local service ads",
                "Missing emergency plumbing keywords"
            ],
            "LLM_RevenueImpact": "$12,000-18,000/month",
            "LLM_Opportunities": [
                "Emergency plumbing calls are high-value - optimize for 'emergency plumber Denver'",
                "Add click-to-call button prominently",
                "Create service area pages for nearby cities"
            ],
            "LLM_ServicesOffered": [
                "Emergency plumbing",
                "Water heater repair",
                "Drain cleaning",
                "Pipe repair"
            ],
            "LLM_USP": "24/7 emergency service, family-owned",
            "LLM_CTAQuality": "Missing",
            "LLM_TargetKeywords": ["plumber", "plumbing", "Denver"],
            "LLM_MissingKeywords": [
                "emergency plumber Denver",
                "24 hour plumber",
                "water heater repair Denver"
            ],
            "LLM_ContentQuality": "Minimal content, no service descriptions, no trust signals.",
            "LLM_QuickWins": [
                "Add emergency call button to header",
                "Speed optimization (critical)",
                "Add service area pages",
                "Implement local business schema"
            ],
            "LLM_PitchAngle": "Your website takes 22 seconds to load. When someone has a plumbing emergency, they're calling the first plumber they find - and it's not you. I can get you ranking #1 for 'emergency plumber Denver' in 30 days."
        }
    ]
    
    print(f"Generating report for {len(sample_leads)} hot leads...")
    print()
    
    report_path = report_generator.generate_sales_report(
        leads=sample_leads,
        geo="Denver, CO"
    )
    
    print()
    print(f"✅ Report generated: {report_path}")
    print()
    print("📄 You can now:")
    print("  1. Open the text file to review the report")
    print("  2. If Google credentials are configured, it will also create a Google Doc")
    print()


if __name__ == "__main__":
    print("\n🚀 SALES INTELLIGENCE SYSTEM TEST\n")
    
    # Test 1: LLM Analysis
    try:
        test_llm_analysis()
    except Exception as e:
        print(f"❌ LLM Analysis test failed: {e}")
        print()
    
    # Test 2: Report Generation
    try:
        test_report_generation()
    except Exception as e:
        print(f"❌ Report generation test failed: {e}")
        print()
    
    print("\n" + "=" * 80)
    print("✅ TESTING COMPLETE")
    print("=" * 80)
    print()
    print("💡 Next steps:")
    print("  1. Review the generated sales report")
    print("  2. Run the full pipeline: python3 main.py --once --geo 'Austin, TX'")
    print("  3. Check the ./out/ folder for CSV data and sales reports")
    print()

