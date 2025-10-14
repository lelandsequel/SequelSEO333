#!/usr/bin/env python3
"""Test all API integrations to see what's working."""

import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_pagespeed_api():
    """Test PageSpeed Insights API."""
    print("\n" + "=" * 60)
    print("🧪 Testing PageSpeed Insights API")
    print("=" * 60)
    
    api_key = os.getenv("PSI_API_KEY")
    
    if not api_key:
        print("❌ PSI_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        url = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        params = {
            "url": "https://example.com",
            "key": api_key,
            "category": "performance",
            "strategy": "mobile"
        }
        
        print("   Testing with: https://example.com")
        response = requests.get(url, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        
        score = data.get("lighthouseResult", {}).get("categories", {}).get("performance", {}).get("score", 0) * 100
        print(f"✅ SUCCESS! Performance Score: {score:.0f}/100")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_google_places_api():
    """Test Google Places API."""
    print("\n" + "=" * 60)
    print("🧪 Testing Google Places API")
    print("=" * 60)
    
    api_key = os.getenv("GOOGLE_PLACES_API_KEY")
    
    if not api_key:
        print("❌ GOOGLE_PLACES_API_KEY not found in .env file")
        return False
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        params = {
            "query": "coffee shop in Houston, TX",
            "key": api_key
        }
        
        print("   Testing with: 'coffee shop in Houston, TX'")
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        status = data.get("status")
        
        if status == "OK":
            results = data.get("results", [])
            print(f"✅ SUCCESS! Found {len(results)} businesses")
            if results:
                print(f"   Example: {results[0].get('name')}")
            return True
        elif status == "REQUEST_DENIED":
            print(f"❌ FAILED: API not enabled or invalid key")
            print(f"   Error: {data.get('error_message', 'No error message')}")
            print(f"\n   👉 Enable the API here:")
            print(f"   https://console.cloud.google.com/apis/library/places-backend.googleapis.com?project=SequelSEO333")
            return False
        else:
            print(f"❌ FAILED: Status = {status}")
            print(f"   Error: {data.get('error_message', 'No error message')}")
            return False
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_serpapi():
    """Test SerpAPI."""
    print("\n" + "=" * 60)
    print("🧪 Testing SerpAPI (Optional)")
    print("=" * 60)
    
    api_key = os.getenv("SERPAPI_KEY")
    
    if not api_key:
        print("⚠️  SERPAPI_KEY not found (optional)")
        print("   Get it at: https://serpapi.com/")
        print("   Free tier: 100 searches/month")
        return None
    
    print(f"✅ API Key found: {api_key[:20]}...")
    
    try:
        url = "https://serpapi.com/search"
        params = {
            "q": "test",
            "api_key": api_key,
            "engine": "google"
        }
        
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()
        
        if "error" in data:
            print(f"❌ FAILED: {data.get('error')}")
            return False
        
        print(f"✅ SUCCESS! SerpAPI is working")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_hunter_io():
    """Test Hunter.io API."""
    print("\n" + "=" * 60)
    print("🧪 Testing Hunter.io (Optional)")
    print("=" * 60)

    api_key = os.getenv("HUNTER_API_KEY")

    if not api_key:
        print("⚠️  HUNTER_API_KEY not found (optional)")
        print("   Get it at: https://hunter.io/")
        print("   Free tier: 25 searches/month")
        return None

    print(f"✅ API Key found: {api_key[:20]}...")

    try:
        url = "https://api.hunter.io/v2/domain-search"
        params = {
            "domain": "example.com",
            "api_key": api_key
        }

        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "errors" in data:
            print(f"❌ FAILED: {data.get('errors')}")
            return False

        print(f"✅ SUCCESS! Hunter.io is working")
        return True

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_claude_api():
    """Test Claude API for LLM-powered SEO analysis."""
    print("\n" + "=" * 60)
    print("🧪 Testing Claude API (Recommended for AI Analysis)")
    print("=" * 60)

    api_key = os.getenv("ANTHROPIC_API_KEY")

    if not api_key:
        print("⚠️  ANTHROPIC_API_KEY not found (optional but recommended)")
        print("   Get it at: https://console.anthropic.com/")
        print("   Cost: ~$1-2 per 1,000 website analyses")
        print("   Replaces expensive Ahrefs ($500/month)!")
        return None

    print(f"✅ API Key found: {api_key[:20]}...")

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json"
            },
            json={
                "model": "claude-3-haiku-20240307",
                "max_tokens": 100,
                "messages": [
                    {"role": "user", "content": "Say 'API test successful' in JSON format with a key 'status'"}
                ]
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        if "content" in data:
            print(f"✅ SUCCESS! Claude API is working")
            print(f"   Model: claude-3-haiku-20240307")
            return True
        else:
            print(f"❌ FAILED: Unexpected response")
            return False

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def test_openai_api():
    """Test OpenAI API for LLM-powered SEO analysis."""
    print("\n" + "=" * 60)
    print("🧪 Testing OpenAI API (Alternative to Claude)")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("⚠️  OPENAI_API_KEY not found (optional)")
        print("   Get it at: https://platform.openai.com/api-keys")
        print("   Cost: ~$2-3 per 1,000 website analyses")
        return None

    print(f"✅ API Key found: {api_key[:20]}...")

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "user", "content": "Say 'API test successful'"}
                ],
                "max_tokens": 20
            },
            timeout=30
        )

        response.raise_for_status()
        data = response.json()

        if "choices" in data:
            print(f"✅ SUCCESS! OpenAI API is working")
            print(f"   Model: gpt-3.5-turbo")
            return True
        else:
            print(f"❌ FAILED: Unexpected response")
            return False

    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False


def main():
    """Run all API tests."""
    print("\n" + "🔧" * 30)
    print("API INTEGRATION TEST SUITE")
    print("🔧" * 30)

    results = {
        "PageSpeed Insights (Required)": test_pagespeed_api(),
        "Google Places (Required)": test_google_places_api(),
        "Claude AI (Recommended)": test_claude_api(),
        "OpenAI GPT (Alternative)": test_openai_api(),
        "SerpAPI (Optional)": test_serpapi(),
        "Hunter.io (Optional)": test_hunter_io(),
    }

    print("\n" + "=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)

    for name, status in results.items():
        if status is True:
            print(f"✅ {name}")
        elif status is False:
            print(f"❌ {name}")
        else:
            print(f"⚠️  {name} - Not configured")

    print("\n" + "=" * 60)

    required_working = results["PageSpeed Insights (Required)"] and results["Google Places (Required)"]
    llm_working = results["Claude AI (Recommended)"] or results["OpenAI GPT (Alternative)"]

    if required_working:
        print("🎉 ALL REQUIRED APIs ARE WORKING!")

        if llm_working:
            print("🤖 AI-POWERED SEO ANALYSIS ENABLED!")
            print("   You'll get deep content insights for each lead")
        else:
            print("\n💡 TIP: Add Claude or OpenAI API for AI-powered analysis")
            print("   See LLM_SETUP_GUIDE.md for details")
            print("   Cost: ~$1-2 per 1,000 websites (vs $500/month for Ahrefs!)")

        print("\nYou can now run:")
        print("  python3 quick_test.py")
        print("  python3 main.py")
    else:
        print("⚠️  SOME REQUIRED APIs ARE NOT WORKING")
        print("\nFix the issues above before running the pipeline.")

    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

