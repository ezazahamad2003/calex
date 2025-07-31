#!/usr/bin/env python3
"""
Main Orchestrator for AI Prospecting & Profile Enrichment
=========================================================
This script orchestrates the complete workflow:
1. Gets user input for company data and prospect search criteria
2. Uses prospecting_agent to find initial prospects
3. Uses profile_filling_agent to enrich each prospect with detailed information
4. Saves the final enriched results

Environment:
  • Requires PERPLEXITY_API_KEY in a .env file
Usage:
  $ python main.py
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Import functions from our agents
from prospecting_agent import find_prospects, save_prospects
from profile_filling_agent import enrich_prospects_data

def get_user_inputs():
    """Get the required inputs from user"""
    print("🎯 AI Prospecting & Enrichment Pipeline")
    print("=" * 50)
    
    print("\n1️⃣ Company Data (optional):")
    print("   Enter information about your company/service to help with targeting")
    company_data = input("   Company info: ").strip()
    
    print("\n2️⃣ Prospect Search Criteria:")
    print("   Describe what type of prospects you're looking for")
    search_prompt = input("   Search criteria: ").strip()
    
    if not search_prompt:
        print("❌ Prospect search criteria is required!")
        sys.exit(1)
    
    print("\n3️⃣ Enrichment Options:")
    enrich_choice = input("   Enrich profiles with detailed research? (y/n, default: y): ").lower().strip()
    do_enrichment = enrich_choice != 'n'
    
    return company_data, search_prompt, do_enrichment

def generate_filename(prefix="prospects"):
    """Generate timestamped filename"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.json"

def main():
    """Main orchestration function"""
    try:
        # Get user inputs
        company_data, search_prompt, do_enrichment = get_user_inputs()
        
        # Step 1: Find initial prospects
        print("\n" + "="*50)
        print("🔍 STEP 1: Finding prospects...")
        print("="*50)
        
        prospects_data = find_prospects(company_data, search_prompt)
        
        # Check for errors in prospecting
        if "error" in prospects_data and prospects_data["error"]:
            print(f"❌ Prospecting failed: {prospects_data['message']}")
            sys.exit(1)
        
        # Check if we got any prospects
        if not prospects_data.get("prospects"):
            print("❌ No prospects found matching your criteria")
            sys.exit(1)
        
        prospect_count = len(prospects_data["prospects"])
        print(f"✅ Found {prospect_count} initial prospects")
        
        # Step 2: Enrich prospects (if requested)
        if do_enrichment:
            print("\n" + "="*50)
            print("🔎 STEP 2: Enriching prospect profiles...")
            print("="*50)
            
            enriched_data = enrich_prospects_data(prospects_data)
            
            # Check for enrichment errors
            if "error" in enriched_data and enriched_data["error"]:
                print(f"❌ Enrichment failed: {enriched_data['message']}")
                print("💡 Saving original prospects without enrichment...")
                final_data = prospects_data
                filename_prefix = "prospects_basic"
            else:
                print(f"✅ Successfully enriched {len(enriched_data['prospects'])} prospects")
                final_data = enriched_data
                filename_prefix = "prospects_enriched"
        else:
            print("\n⏭️  Skipping enrichment as requested")
            final_data = prospects_data
            filename_prefix = "prospects_basic"
        
        # Step 3: Save results
        print("\n" + "="*50)
        print("💾 STEP 3: Saving results...")
        print("="*50)
        
        # Generate default filename
        default_filename = generate_filename(filename_prefix)
        
        # Ask user for filename
        filename = input(f"Enter filename (default: {default_filename}): ").strip()
        if not filename:
            filename = default_filename
        
        # Save the file
        save_prospects(final_data, filename)
        
        # Summary
        print("\n" + "="*50)
        print("🎉 PIPELINE COMPLETE!")
        print("="*50)
        print(f"📊 Total prospects: {len(final_data['prospects'])}")
        print(f"📁 Saved to: {filename}")
        
        if do_enrichment:
            print("✨ Profiles have been enriched with detailed research")
        
        # Display sample prospect
        if final_data["prospects"]:
            first_prospect = final_data["prospects"][0]
            print(f"\n📋 Sample prospect: {first_prospect.get('name', 'Unknown')}")
            if first_prospect.get('type') == 'company':
                print(f"   Industry: {first_prospect.get('industry', 'Unknown')}")
                print(f"   Website: {first_prospect.get('website', 'Unknown')}")
            
            print(f"\n💡 All contact details are saved in the JSON file: {filename}")
            print("   Open the file to see comprehensive contact information for each prospect!")
            
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()