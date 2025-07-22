#!/usr/bin/env python3
"""
Simple AI Prospecting Agent
Takes company data and search prompt, returns JSON list of prospects
"""

import requests
import json
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv('PERPLEXITY_API_KEY')
if not api_key:
    print("❌ PERPLEXITY_API_KEY not found in .env file!")
    sys.exit(1)

def get_inputs():
    """Get the two required inputs from user"""
    print("🎯 AI Prospecting Agent")
    print("=" * 40)
    
    print("\n1️⃣ Company Data:")
    company_data = input("Enter your company information: ").strip()
    
    print("\n2️⃣ Prospect Search:")
    search_prompt = input("Enter what prospects you're looking for: ").strip()
    
    if not company_data or not search_prompt:
        print("❌ Both inputs are required!")
        sys.exit(1)
    
    return company_data, search_prompt

def load_prompt_template():
    """Load the prompt template from external file"""
    try:
        with open('prompt_template.txt', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print("❌ prompt_template.txt not found!")
        print("💡 Make sure prompt_template.txt is in the same directory as this script")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error loading prompt template: {e}")
        sys.exit(1)

def create_prospecting_prompt(company_data, search_prompt):
    """Create the specialized prompt for prospect research"""
    template = load_prompt_template()
    # Use string replacement instead of .format() to avoid conflicts with JSON braces
    prompt = template.replace("{company_data}", company_data).replace("{search_prompt}", search_prompt)
    return prompt

def deep_research(query, api_key):
    """Send query to Perplexity Deep Research API"""
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "sonar-deep-research",
        "messages": [
            {"role": "user", "content": query}
        ],
        "reasoning_effort": "medium"
    }
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        print("🔍 Searching for prospects...")
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    except requests.exceptions.RequestException as e:
        error_response = {
            "error": True,
            "message": str(e),
            "status_code": getattr(e.response, 'status_code', None) if hasattr(e, 'response') else None
        }
        if hasattr(e, 'response') and e.response is not None:
            try:
                error_details = e.response.json()
                error_response["details"] = error_details
            except:
                error_response["response_text"] = e.response.text
        return error_response

def extract_prospects_json(content):
    """Extract and validate the prospects JSON from the response"""
    try:
        # First, try to parse the content as-is
        content = content.strip()
        
        # Remove any markdown formatting
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        # Try to parse directly first
        try:
            prospects_data = json.loads(content)
            if "prospects" in prospects_data:
                return prospects_data
        except json.JSONDecodeError:
            pass
        
        # If that fails, look for JSON within the content
        # Find the first { and last } to extract JSON
        start_idx = content.find('{')
        if start_idx == -1:
            raise ValueError("No JSON object found in response")
        
        # Find the matching closing brace
        brace_count = 0
        end_idx = -1
        for i in range(start_idx, len(content)):
            if content[i] == '{':
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
        
        if end_idx == -1:
            raise ValueError("No complete JSON object found")
        
        # Extract the JSON substring
        json_content = content[start_idx:end_idx + 1]
        
        # Parse the extracted JSON
        prospects_data = json.loads(json_content)
        
        # Validate structure
        if "prospects" not in prospects_data:
            raise ValueError("No 'prospects' key found in response")
        
        return prospects_data
    
    except (json.JSONDecodeError, ValueError) as e:
        # If JSON parsing fails, create error structure
        return {
            "error": "Failed to parse prospects JSON",
            "details": str(e),
            "raw_content": content[:1000] + "..." if len(content) > 1000 else content
        }

def save_prospects(prospects_data, filename="prospects.json"):
    """Save results to file"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(prospects_data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved to {filename}")

def main():
    """Main function"""
    # Get inputs
    company_data, search_prompt = get_inputs()
    
    # Create prospecting prompt
    prospecting_prompt = create_prospecting_prompt(company_data, search_prompt)
    
    # Perform research
    result = deep_research(prospecting_prompt, api_key)
    
    # Check for API errors
    if "error" in result and result["error"]:
        error_output = {
            "error": True,
            "message": result["message"],
            "prospects": []
        }
        print(json.dumps(error_output, indent=2))
        return
    
    # Extract content
    content = result["choices"][0]["message"]["content"]
    
    # Parse prospects JSON
    prospects_json = extract_prospects_json(content)
    
    # Output final JSON
    print(json.dumps(prospects_json, indent=2, ensure_ascii=False))
    
    # Ask user if they want to save to file
    if "error" not in prospects_json:
        save_choice = input("\n💾 Save prospects to file? (y/n): ").lower().strip()
        if save_choice in ['y', 'yes']:
            # Generate filename with timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_filename = f"prospects_{timestamp}.json"
            
            filename = input(f"Enter filename (default: {default_filename}): ").strip()
            if not filename:
                filename = default_filename
            
            save_prospects(prospects_json, filename)

if __name__ == "__main__":
    main()