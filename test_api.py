#!/usr/bin/env python3
"""Quick test to verify API keys are working."""

import os
from dotenv import load_dotenv
from modules.seo_checks import _fetch_pagespeed_metrics

# Load environment variables
load_dotenv()

def test_pagespeed_api():
    """Test PageSpeed Insights API."""
    print("=" * 60)
    print("🧪 Testing PageSpeed Insights API")
    print("=" * 60)
    
    api_key = os.getenv("PSI_API_KEY")
    
    if not api_key:
        print("❌ PSI_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    print()
    
    # Test with a simple website
    test_url = "https://example.com"
    print(f"Testing with: {test_url}")
    print()
    
    try:
        result = _fetch_pagespeed_metrics(test_url)
        
        if result:
            print()
            print("=" * 60)
            print("✅ SUCCESS! PageSpeed API is working!")
            print("=" * 60)
            print(f"LCP: {result.get('lcp')}s")
            print(f"Performance Score: {result.get('performance_score')}/100")
            print()
            return True
        else:
            print("❌ No result returned")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_pagespeed_api()
    
    if success:
        print("🎉 Your API is ready to use!")
        print()
        print("Next steps:")
        print("  1. Run: python3 quick_test.py")
        print("  2. Or run full pipeline: python3 main.py")
    else:
        print("⚠️  API test failed. Check your API key in .env file")

