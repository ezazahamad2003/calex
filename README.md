# AI Prospecting & Profile Enrichment System

A comprehensive AI-powered prospecting system that finds potential customers and enriches their profiles with detailed contact information using Perplexity AI's deep research capabilities.

## 🎯 Features

### **Two-Stage Pipeline**
- **🔍 Prospect Discovery**: Find ideal prospects matching your criteria
- **🔎 Profile Enrichment**: Deep-dive research to fill missing contact details

### **Comprehensive Contact Capture**
- **📧 Multiple Emails**: Work, personal, department-specific emails
- **📞 Phone Numbers**: Direct, mobile, office, toll-free, international
- **🏢 Addresses**: Headquarters, offices, mailing addresses
- **📠 Fax Numbers**: When available
- **📱 Social Media**: LinkedIn, Twitter/X, Facebook, Instagram, YouTube
- **💬 Messaging**: WhatsApp, Telegram, Signal, Slack, Discord
- **🔗 Other Methods**: Contact forms, chat widgets, Skype, etc.

### **Smart Targeting**
- **Perfect-Fit Priority**: Focuses on prospects that exactly match criteria
- **Intent Inference**: Identifies prospects likely to need your product/service
- **Decision-Maker Identification**: Finds key contacts within companies
- **High-Signal Platforms**: Prioritizes LinkedIn, Twitter/X, Glassdoor, Reddit, Crunchbase, etc.

### **Flexible Output**
- **JSON Structure**: Clean, structured data ready for CRM import
- **Timestamped Files**: Automatic file naming with timestamps
- **Enrichment Options**: Choose basic or detailed research
- **Error Handling**: Graceful fallbacks and detailed error reporting

## 🚀 Quick Start

### 1. **Setup Environment**
```bash
# Clone the repository
git clone https://github.com/ezazahamad2003/calex.git
cd calex

# Install dependencies
pip install requests python-dotenv

# Create .env file with your API key
echo "PERPLEXITY_API_KEY=your_api_key_here" > "test deepresearch/.env"
```

### 2. **Run the Pipeline**
```bash
python "test deepresearch/main.py"
```

### 3. **Follow the Prompts**
```
🎯 AI Prospecting & Enrichment Pipeline
==================================================

1️⃣ Company Data (optional):
   Enter information about your company/service to help with targeting
   Company info: [Your company details]

2️⃣ Prospect Search Criteria:
   Describe what type of prospects you're looking for
   Search criteria: [Your target criteria]

3️⃣ Enrichment Options:
   Enrich profiles with detailed research? (y/n, default: y): [y/n]
```

## 📁 Project Structure

```
test deepresearch/
├── main.py                    # 🎯 Main orchestrator (run this!)
├── prospecting_agent.py       # 🔍 Prospect discovery engine
├── profile_filling_agent.py   # 🔎 Profile enrichment engine
├── prompt_template.txt        # 📝 Prospecting instructions template
├── profile_filling_template.txt # 📝 Enrichment instructions template
└── .env                       # 🔑 API key (create this!)
```

## 🔧 Individual Components

### **Main Orchestrator** (`main.py`)
- Coordinates the entire workflow
- Handles user input and file management
- Provides progress updates and summaries

### **Prospecting Agent** (`prospecting_agent.py`)
- Finds initial prospects matching criteria
- Uses `prompt_template.txt` for research instructions
- Returns structured JSON with basic information

### **Profile Filling Agent** (`profile_filling_agent.py`)
- Enriches prospect profiles with detailed research
- Uses `profile_filling_template.txt` for enrichment instructions
- Fills missing contact information and details

## 📊 Output Format

The system generates comprehensive JSON files with detailed prospect information:

```json
{
  "prospects": [
    {
      "type": "company",
      "name": "TechCorp Inc",
      "website": "techcorp.com",
      "industry": "Software",
      "contact_info": {
        "emails": ["info@techcorp.com", "sales@techcorp.com"],
        "phones": ["+1-555-123-4567", "+1-800-TECHCORP"],
        "addresses": {
          "headquarters": "123 Tech Street, San Francisco, CA 94105"
        },
        "social_media": {
          "linkedin": "linkedin.com/company/techcorp",
          "twitter": "@techcorp"
        }
      },
      "key_contacts": [
        {
          "name": "John Smith",
          "title": "CEO",
          "contact_info": {
            "emails": ["john@techcorp.com"],
            "phones": ["+1-555-123-4570"],
            "linkedin": "linkedin.com/in/johnsmith"
          }
        }
      ],
      "opportunity_assessment": {
        "fit_score": "8",
        "why_good_fit": "Perfect match for our B2B SaaS solution..."
      }
    }
  ]
}
```

## 🎯 Use Cases

### **B2B Sales Teams**
- Find decision-makers at target companies
- Get comprehensive contact information
- Understand prospect fit and opportunity

### **Recruiters**
- Find candidates with specific skills
- Get detailed professional backgrounds
- Access multiple contact methods

### **Business Development**
- Identify partnership opportunities
- Research potential clients
- Map industry landscapes

### **Market Research**
- Understand target markets
- Identify industry trends
- Find key players in specific sectors

## 🔑 API Requirements

- **Perplexity AI API Key**: Required for deep research capabilities
- **Model**: Uses `sonar-deep-research` for comprehensive analysis
- **Rate Limits**: Respects Perplexity's API usage limits

## 📈 Advanced Features

### **Smart Targeting Logic**
- Prioritizes perfect-fit prospects first
- Falls back to high-likelihood prospects if needed
- Infers product-market fit from company attributes

### **Comprehensive Research**
- Scans multiple high-signal platforms
- Verifies information across sources
- Includes data verification dates for older information

### **Flexible Contact Capture**
- No restrictions on contact types
- Captures ALL discovered contact methods
- Supports multiple entries per contact type

## 🛠️ Customization

### **Templates**
- `prompt_template.txt`: Customize prospecting instructions
- `profile_filling_template.txt`: Customize enrichment instructions

### **Output Options**
- Basic prospecting only (no enrichment)
- Full enrichment with detailed research
- Custom filename generation

## 📝 Example Usage

```bash
# Run complete pipeline
python "test deepresearch/main.py"

# Example session:
Company info: We're a B2B SaaS company selling project management software
Search criteria: Find SaaS companies with 50-500 employees that might need project management tools
Enrichment: y

# Output: prospects_enriched_20241210_143052.json
```

## 🔒 Security

- API keys stored in `.env` file (not committed to repo)
- No sensitive data logged or stored
- Clean JSON output without API keys

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

---

**Ready to find your next customers?** 🚀

Run `python "test deepresearch/main.py"` and start discovering prospects! 