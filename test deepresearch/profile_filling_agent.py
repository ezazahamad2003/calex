#!/usr/bin/env python3
"""
Profile Filling (Enrichment) Agent
------------------------------------------------
Takes an existing prospects JSON file (output from prospecting_agent.py) and, for each
prospect, performs deep-research enrichment using Perplexity's 'sonar-deep-research' model.
The agent outputs an enriched prospects JSON with the same structure but filled/updated
fields.

Environment:
  • Requires PERPLEXITY_API_KEY in a .env file (same as prospecting_agent.py).
Usage:
  $ python profile_filling_agent.py prospects.json
  If no argument is supplied, the script will prompt for a file path (default: prospects.json).
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List
import requests
from dotenv import load_dotenv

# -------------------------------------------------------------
# Configuration / Setup
# -------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("PERPLEXITY_API_KEY")
if not API_KEY:
    print("❌ PERPLEXITY_API_KEY not found in .env file!")
    sys.exit(1)

PROMPT_TEMPLATE_PATH = Path(__file__).with_name("profile_filling_template.txt")

# -------------------------------------------------------------
# Helper Functions
# -------------------------------------------------------------

def load_prompt_template() -> str:
    """Load the profile-filling prompt template"""
    if not PROMPT_TEMPLATE_PATH.exists():
        print(f"❌ {PROMPT_TEMPLATE_PATH.name} not found!")
        sys.exit(1)
    return PROMPT_TEMPLATE_PATH.read_text(encoding="utf-8")


def create_profile_prompt(prospect: Dict[str, Any]) -> str:
    """Insert the prospect JSON into the template"""
    template = load_prompt_template()
    prospect_json_str = json.dumps(prospect, ensure_ascii=False, indent=2)
    prompt = template.replace("{prospect_data}", prospect_json_str)
    return prompt


def deep_research(query: str) -> Dict[str, Any]:
    """Call Perplexity API with deep research reasoning"""
    url = "https://api.perplexity.ai/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": "sonar-deep-research",
        "messages": [{"role": "user", "content": query}],
        "reasoning_effort": "high",
    }
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=90)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print("❌ API request failed:", e)
        return {"error": str(e)}


def parse_json_from_content(content: str) -> Dict[str, Any]:
    """Extract first valid JSON object found in content string"""
    content = content.strip()
    # Remove markdown fencing if present
    if content.startswith("```json"):
        content = content[7:]
    if content.endswith("```"):
        content = content[:-3]
    # Try direct parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Fallback: find first { … } block balancing braces
    start = content.find("{")
    if start == -1:
        raise ValueError("No JSON object found")
    brace_count = 0
    for idx in range(start, len(content)):
        if content[idx] == "{":
            brace_count += 1
        elif content[idx] == "}":
            brace_count -= 1
            if brace_count == 0:
                json_str = content[start: idx + 1]
                return json.loads(json_str)
    raise ValueError("Incomplete JSON object")


def enrich_prospect(prospect: Dict[str, Any]) -> Dict[str, Any]:
    """Send prospect to API and return enriched version (fallback to original on failure)"""
    prompt = create_profile_prompt(prospect)
    api_response = deep_research(prompt)
    if "error" in api_response:
        print("⚠️  Skipping enrichment due to API error for prospect:", prospect.get("name"))
        return prospect
    content = api_response["choices"][0]["message"]["content"]
    try:
        enriched = parse_json_from_content(content)
        return enriched
    except Exception as e:
        print("⚠️  Failed to parse enrichment result for", prospect.get("name"), "- returning original. Error:", e)
        return prospect

# -------------------------------------------------------------
# Main Routine
# -------------------------------------------------------------

def enrich_prospects_data(prospects_data):
    """Main function to enrich prospects data - returns enriched JSON data"""
    if "prospects" not in prospects_data or not isinstance(prospects_data["prospects"], list):
        return {
            "error": True,
            "message": "Input data missing 'prospects' list",
            "prospects": []
        }

    prospects: List[Dict[str, Any]] = prospects_data["prospects"]
    enriched_list: List[Dict[str, Any]] = []

    # Iterate & enrich
    for idx, prospect in enumerate(prospects, 1):
        print(f"\n🔎 Enriching prospect {idx}/{len(prospects)}: {prospect.get('name', 'Unknown')}")
        enriched = enrich_prospect(prospect)
        enriched_list.append(enriched)

    return {"prospects": enriched_list}


def main():
    # Determine input file
    if len(sys.argv) > 1:
        input_path = Path(sys.argv[1])
    else:
        user_in = input("Enter prospects JSON file path (default: prospects.json): ").strip()
        input_path = Path(user_in) if user_in else Path("prospects.json")

    if not input_path.exists():
        print(f"❌ File not found: {input_path}")
        sys.exit(1)

    # Load prospects
    prospects_data = json.loads(input_path.read_text(encoding="utf-8"))
    
    # Enrich prospects
    enriched_data = enrich_prospects_data(prospects_data)
    
    if "error" in enriched_data:
        print(f"❌ {enriched_data['message']}")
        sys.exit(1)
    
    # Save output
    out_file = input_path.with_stem(input_path.stem + "_enriched")
    out_file.write_text(json.dumps(enriched_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n✅ Enrichment complete. Saved to {out_file}")


if __name__ == "__main__":
    main()
