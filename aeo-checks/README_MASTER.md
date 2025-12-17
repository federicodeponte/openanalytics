# Master AEO Service - Advanced Analysis Platform

**Version 5.0.0** - Combines the best features from aeo-health-check and aeo-leaderboard implementations.

## 🚀 Features

### Health Check (v4.0)
- **29 checks** across 4 categories with tiered objective scoring
- **AI Access Gate**: Critical checks that block all AI platforms
- **Schema Gate**: Essential checks for AI entity identification  
- **Quality Gate**: Important optimization opportunities
- **Excellence Tier**: Full optimization potential

### Mentions Check (v5.0)
- **Hyperniche Targeting**: AI-assisted query generation with Gemini 2.5 Flash
- **Quality Scoring**: Advanced mention quality detection (primary recommendations, top options, listed mentions)
- **5 AI Platforms**: Perplexity, Claude, ChatGPT, Gemini, Mistral
- **Business Intelligence**: Brand confusion analysis, competitive positioning
- **Sophisticated TL;DR**: Actionable recommendations with strategic insights

### Master Analysis (NEW)
- **Combined Intelligence**: Integrated health + mentions analysis  
- **Strategic Recommendations**: High-level business guidance
- **Priority Actions**: Specific tactical steps
- **Weighted Scoring**: 60% health (foundation) + 40% visibility (performance)

## 🏗️ Architecture

```
Master AEO Service
├── Health Check Engine (from aeo-health-check)
│   ├── Technical SEO (16 checks)
│   ├── Structured Data (6 checks) 
│   ├── AI Crawler Access (4 checks)
│   └── Authority/E-E-A-T (3 checks)
├── Mentions Analysis Engine (from aeo-leaderboard)
│   ├── Hyperniche Query Generation
│   ├── Parallel AI Platform Querying
│   ├── Quality-Adjusted Scoring
│   └── Brand Confusion Detection
└── Master Intelligence Layer (NEW)
    ├── Combined Score Calculation
    ├── Strategic Recommendations
    └── Priority Action Planning
```

## 🔧 Installation & Deployment

### Local Development

```bash
# Install dependencies
pip install -r master_requirements.txt

# Install Playwright browsers
playwright install chromium

# Set environment variables
export OPENAI_API_KEY="your-openai-key"
export OPENROUTER_API_KEY="your-openrouter-key" 
export GEMINI_API_KEY="your-gemini-key"  # Optional

# Run locally
python master_aeo_service.py
```

### Modal Deployment

```bash
# Deploy to Modal
modal deploy master_deploy.py

# Test deployment
modal run master_deploy.py
```

**Deployment URL**: `https://clients--master-aeo-service-fastapi-app.modal.run`

## 📋 API Endpoints

### Health Check
```bash
POST /health/check
```

**Request:**
```json
{
  "url": "https://example.com",
  "include_performance": true,
  "include_accessibility": true
}
```

**Response:**
```json
{
  "url": "https://example.com",
  "overall_score": 78.5,
  "grade": "B",
  "visibility_band": "Moderate",
  "categories": [
    {
      "name": "Technical SEO",
      "score": 85.2,
      "max_score": 100,
      "grade": "A",
      "checks": [...],
      "summary": "Strong technical foundation..."
    }
  ],
  "recommendations": [
    "Essential: Add Organization schema markup",
    "Important: Enhance content quality"
  ]
}
```

### Mentions Check
```bash
POST /mentions/check
```

**Request:**
```json
{
  "companyName": "SCAILE",
  "companyAnalysis": {
    "companyInfo": {
      "name": "SCAILE",
      "industry": "SaaS",
      "products": ["AEO Consulting"],
      "services": ["AEO Strategy"],
      "target_audience": "B2B SaaS companies"
    },
    "competitors": [
      {"name": "BrightEdge"},
      {"name": "Conductor"}
    ]
  },
  "mode": "balanced",
  "numQueries": 25,
  "language": "english",
  "country": "US"
}
```

**Response:**
```json
{
  "companyName": "SCAILE",
  "visibility": 67.8,
  "band": "Strong",
  "mentions": 42,
  "presence_rate": 68.0,
  "quality_score": 6.8,
  "platform_stats": {
    "gemini": {
      "mentions": 12,
      "quality_score": 7.2,
      "responses": 25,
      "errors": 0
    }
  },
  "tldr": {
    "visibility_assessment": "Strong AI search visibility (67.8%)",
    "key_insights": [
      "Strongest performance on gemini (quality: 7.2/10)",
      "Best performing query type: Product-Industry"
    ],
    "brand_confusion_risk": "Low - clear brand recognition",
    "actionable_recommendations": [
      "Optimize: Enhance existing content quality",
      "Platform focus: Improve claude visibility"
    ]
  }
}
```

### Master Analysis
```bash
POST /analyze/master
```

**Request:**
```json
{
  "url": "https://scaile.tech",
  "companyName": "SCAILE", 
  "companyAnalysis": { ... },
  "mode": "balanced",
  "numQueries": 20
}
```

**Response:**
```json
{
  "url": "https://scaile.tech",
  "companyName": "SCAILE",
  "health": { ... },
  "mentions": { ... },
  "combined_score": 73.2,
  "combined_grade": "B",
  "strategic_recommendations": [
    "CONTENT STRATEGY: Excellent foundation but low visibility",
    "BALANCED APPROACH: Continue optimizing both areas"
  ],
  "priority_actions": [
    "OPTIMIZE: Complete schema implementation",
    "CONTENT: Develop AI-optimized FAQ content",
    "TARGETING: Focus content on weak dimensions"
  ]
}
```

## 🎯 Analysis Modes

| Mode | Queries | Platforms | Use Case |
|------|---------|-----------|----------|
| **fast** | 10 | Gemini + ChatGPT | Quick assessment |
| **balanced** | 25 | 4 platforms | Recommended default |
| **full** | 50 | All 5 platforms | Comprehensive analysis |

## 🏆 Scoring System

### Health Check (Tiered Objective Scoring)
- **Tier 0 (Critical)**: AI crawler access - blocks all if failed
- **Tier 1 (Essential)**: Organization schema - caps score at 45
- **Tier 2 (Important)**: Content quality - caps score at 75-85  
- **Tier 3 (Excellence)**: Full optimization potential

### Mentions Check (Quality-Adjusted Scoring)
- **Primary Recommendations** (9.5/10): "I recommend X"
- **Top Options** (7.5/10): "leading/best X"
- **Listed Options** (5.0/10): Appears in lists
- **Context Mentions** (3.5/10): Basic mentions

### Combined Score
- **60% Health**: Technical foundation
- **40% Visibility**: AI platform performance
- **Grades**: A+ (90+), A (80-89), B (70-79), C (60-69), D (50-59), F (<50)

## 💡 Key Improvements Over Individual Services

### From aeo-health-check:
✅ **Tiered Objective Scoring**: More realistic scoring system  
✅ **29 Comprehensive Checks**: Complete technical foundation  
✅ **AI Crawler Detection**: Critical for AEO success

### From aeo-leaderboard:
✅ **Hyperniche Targeting**: AI-assisted query generation  
✅ **Quality Scoring**: Sophisticated mention analysis  
✅ **Brand Confusion Analysis**: Business intelligence  
✅ **5 Platform Coverage**: Comprehensive visibility testing

### Master Enhancements:
🚀 **Combined Intelligence**: Health + visibility integration  
🚀 **Strategic Recommendations**: High-level business guidance  
🚀 **Priority Actions**: Tactical implementation steps  
🚀 **Unified API**: Single service for all AEO needs

## 🔍 Use Cases

### 1. Initial AEO Assessment
```bash
# Quick health + visibility overview
POST /analyze/master
{
  "url": "https://company.com",
  "companyName": "Company",
  "mode": "fast",
  "numQueries": 10
}
```

### 2. Comprehensive AEO Audit
```bash
# Complete analysis with full insights
POST /analyze/master
{
  "url": "https://company.com",
  "companyName": "Company", 
  "companyAnalysis": { ... },
  "mode": "full",
  "numQueries": 50
}
```

### 3. Monitoring & Tracking
```bash
# Regular balanced checks for monitoring
POST /analyze/master
{
  "url": "https://company.com",
  "companyName": "Company",
  "mode": "balanced",
  "numQueries": 25
}
```

## 🚨 Requirements

### Mandatory
- **Company Analysis Data**: Required for mentions check
- **Products/Services**: At least one product or service
- **Valid URL**: Accessible website for health check

### Optional  
- **Competitor Data**: Enhances competitive analysis
- **Target Audience**: Improves query targeting
- **Geographic Focus**: Enables location-based queries

## 🛠️ Integration Examples

### Python Client
```python
import httpx

async def run_master_analysis(url: str, company_name: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "https://clients--master-aeo-service-fastapi-app.modal.run/analyze/master",
            json={
                "url": url,
                "companyName": company_name,
                "companyAnalysis": {
                    "companyInfo": {
                        "name": company_name,
                        "products": ["Software"],
                        "industry": "Technology"
                    }
                },
                "mode": "balanced"
            }
        )
        return response.json()
```

### JavaScript/Node.js
```javascript
const analyzeCompany = async (url, companyName) => {
  const response = await fetch(
    'https://clients--master-aeo-service-fastapi-app.modal.run/analyze/master',
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        url,
        companyName,
        companyAnalysis: {
          companyInfo: {
            name: companyName,
            products: ['Software'],
            industry: 'Technology'
          }
        },
        mode: 'balanced'
      })
    }
  );
  return response.json();
};
```

## 📊 Performance Characteristics

- **Health Check**: ~30-60 seconds (depends on website complexity)
- **Mentions Check**: ~2-5 minutes (depends on mode and platforms)
- **Master Analysis**: ~3-6 minutes (combined execution)
- **Concurrent Limit**: 10 parallel requests
- **Timeout**: 30 minutes maximum per request

## 🔗 Related Services

- **OpenAnalytics Main**: Company analysis and data extraction
- **PDF Service**: Report generation from analysis results
- **Modal Workspace**: Cloud deployment and scaling

---

**Created by combining the best features from aeo-health-check and aeo-leaderboard implementations.**