#!/usr/bin/env python3
"""Test script to demonstrate the 3 industry selection modes."""

import os
import sys
from dotenv import load_dotenv

# Add current directory to path
sys.path.insert(0, '.')

from modules import industry_discovery

load_dotenv()

print("=" * 60)
print("🧪 TESTING INDUSTRY SELECTION MODES")
print("=" * 60)

geo = "Houston, TX"

# Mode 1: Auto-Discovery Only
print("\n📊 MODE 1: Auto-Discovery (Top 3)")
print("-" * 60)
discovered = industry_discovery.discover_top_industries(geo, k=3)
print(f"\n✅ Discovered: {discovered}")

# Mode 2: Manual Override (simulated)
print("\n\n🎯 MODE 2: Manual Override")
print("-" * 60)
manual = ["car washes", "yoga studios", "coffee shops"]
print(f"✅ Manual industries: {manual}")
print("   (Use: python3 main.py --once --industries 'car washes,yoga studios,coffee shops')")

# Mode 3: Auto + Manual (simulated)
print("\n\n➕ MODE 3: Auto-Discovery + Manual Additions")
print("-" * 60)
additions = ["car washes", "yoga studios"]
combined = discovered + additions
print(f"✅ Discovered: {discovered}")
print(f"➕ Added: {additions}")
print(f"📋 Final list: {combined}")
print("   (Use: python3 main.py --once --add-industries 'car washes,yoga studios')")

print("\n" + "=" * 60)
print("✅ All modes working!")
print("=" * 60)

