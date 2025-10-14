#!/usr/bin/env python3
"""
Quick Test Script for SEO Lead Finder

Run this to test the pipeline with different cities and see results.
"""

import subprocess
import csv
import os
from datetime import datetime

def run_for_city(city):
    """Run the pipeline for a specific city and show results."""
    print(f"\n{'='*60}")
    print(f"🎯 Testing: {city}")
    print(f"{'='*60}\n")
    
    # Run the pipeline
    result = subprocess.run(
        ["python3", "main.py", "--once", "--geo", city],
        capture_output=True,
        text=True
    )
    
    # Find the output file
    output_lines = result.stdout.split('\n')
    csv_file = None
    for line in output_lines:
        if '✅ CSV saved:' in line:
            csv_file = line.split('✅ CSV saved:')[1].strip()
            break
    
    if not csv_file or not os.path.exists(csv_file):
        print("❌ No output file found!")
        return
    
    # Analyze results
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
    
    total = len(rows)
    hot = [r for r in rows if int(r['Score']) >= 70]
    industries = list(set(r['Industry'] for r in rows))
    
    print(f"✅ Results:")
    print(f"   📊 Total Leads: {total}")
    print(f"   🔥 Hot Leads (Score >= 70): {len(hot)}")
    print(f"   🏭 Industries: {', '.join(industries)}")
    print(f"   📁 Output: {csv_file}")
    
    if hot:
        print(f"\n   🌟 Top 3 Hot Leads:")
        for i, lead in enumerate(sorted(hot, key=lambda x: int(x['Score']), reverse=True)[:3], 1):
            print(f"      {i}. {lead['BusinessName']} - Score: {lead['Score']}")
            print(f"         Issues: {lead['Issues']}")

def main():
    """Run tests for multiple cities."""
    print("\n" + "="*60)
    print("🚀 SEO Lead Finder - Quick Test")
    print("="*60)
    
    cities = [
        "Austin, TX",
        "Nashville, TN",
        "Phoenix, AZ"
    ]
    
    for city in cities:
        run_for_city(city)
    
    print("\n" + "="*60)
    print("✅ All tests complete!")
    print("="*60)
    print("\n📁 Check the ./out/ directory for CSV files")
    print("💡 Try: python3 quick_test.py")
    print()

if __name__ == "__main__":
    main()

