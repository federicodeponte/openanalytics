#!/usr/bin/env python3
"""Complete real API test for both SCAILE and Valoon with native Gemini API."""

import os
import asyncio
import json
import google.generativeai as genai
from dotenv import load_dotenv
from test_company_data import SCAILE_COMPANY_DATA, VALOON_COMPANY_DATA

# Load environment variables
load_dotenv('.env.local')

async def test_complete_real_mentions():
    """Test both SCAILE and Valoon with complete real API calls."""
    
    print("🔥 COMPLETE REAL API TESTING - BOTH COMPANIES")
    print("=" * 70)
    
    # Configure Gemini with real API key
    api_key = os.getenv('GEMINI_API_KEY')
    print(f"🔑 Using Gemini API Key: {api_key[:20]}...")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    companies = {
        "SCAILE": SCAILE_COMPANY_DATA,
        "Valoon": VALOON_COMPANY_DATA
    }
    
    all_results = {}
    
    for company_name, company_data in companies.items():
        print(f"\n🏢 TESTING: {company_name}")
        print("=" * 50)
        
        company_info = company_data["companyInfo"]
        products = company_info["products"]
        target_audience = company_info["target_audience"]
        
        print(f"📊 Industry: {company_info['industry']}")
        print(f"📊 Products: {', '.join(products[:3])}")
        print(f"📊 Target: {target_audience[:100]}...")
        
        # Generate 10 hyperniche queries using the same logic as aeo-leaderboard
        query_prompt = f"""Generate 10 HYPERNICHE, highly targeted AEO visibility queries for {company_name}.

COMPANY DATA:
- Industry: {company_info['industry']}
- Products: {', '.join(products)}
- Target Audience: {target_audience}
- Target Roles: CMOs, Marketing Directors, Growth Leaders
- Geographic: United States
- Company Size: enterprise companies

QUERY DISTRIBUTION (follow exactly):
70% UNBRANDED_HYPERNICHE (no mention of {company_name}):
1. PRODUCT_INDUSTRY_GEO: "best [product] for [target_industry] United States"
2. SERVICE_INDUSTRY_GEO: "[service] for [target_industry] companies"
3. INDUSTRY_PRODUCT_ENTERPRISE: "enterprise [industry] [product] solutions"
4. TARGET_ROLE_SPECIFIC: "[product] for [specific_role] in [target_industry]"
5. PAIN_POINT_SOLUTION: "best tools for improving AI search visibility"
6. COMPETITIVE_CATEGORY: "top [product_category] companies for [target_industry]"
7. USE_CASE_SPECIFIC: "[product] to improve [specific_outcome] for [target_industry]"

20% COMPETITIVE_HYPERNICHE:
8. COMPETITOR_ALTERNATIVE: "alternatives to BrightEdge for [target_industry]"
9. COMPETITOR_VS: "BrightEdge vs other [product] for [target_industry]"

10% BRANDED_DIRECT:
10. BRANDED_PRODUCT: "{company_name} [main_product]"

CRITICAL REQUIREMENTS:
- 70% queries MUST NOT mention {company_name}
- Layer 2-3 targeting dimensions (Industry + Role + Geo, etc.)
- Use EXACT targeting data provided
- Make queries HYPER-SPECIFIC to B2B search patterns

Return exactly 10 queries as a JSON array:
[{{"query": "actual search query", "dimension": "HYPERNICHE_TYPE"}}]"""

        print(f"\n🎯 GENERATING HYPERNICHE QUERIES FOR {company_name}...")
        
        try:
            response = model.generate_content(query_prompt)
            queries_text = response.text
            
            # Parse JSON
            import re
            json_match = re.search(r'\[(.*?)\]', queries_text, re.DOTALL)
            if json_match:
                queries_text = json_match.group(0)
            
            queries = json.loads(queries_text)
            print(f"✅ Generated {len(queries)} hyperniche queries")
            
        except Exception as e:
            print(f"⚠️ Query generation failed: {e}")
            # Fallback hyperniche queries
            queries = [
                {"query": f"best AEO consulting for SaaS companies United States", "dimension": "PRODUCT_INDUSTRY_GEO"},
                {"query": f"Answer Engine Optimization for CMOs in enterprise companies", "dimension": "TARGET_ROLE_SPECIFIC"},
                {"query": f"AI search optimization tools for B2B companies", "dimension": "PAIN_POINT_SOLUTION"},
                {"query": f"alternatives to BrightEdge for SaaS companies", "dimension": "COMPETITOR_ALTERNATIVE"},
                {"query": f"{company_name} AEO consulting", "dimension": "BRANDED_PRODUCT"}
            ]
        
        # Test each query with real API
        company_results = {
            "company_name": company_name,
            "queries_tested": len(queries),
            "query_results": [],
            "summary": {
                "total_mentions": 0,
                "queries_with_mentions": 0,
                "avg_quality": 0.0
            }
        }
        
        print(f"\n🔍 TESTING QUERIES WITH REAL GEMINI API:")
        print("-" * 50)
        
        for i, query_data in enumerate(queries[:5], 1):  # Test first 5 to save API calls
            query = query_data["query"]
            dimension = query_data["dimension"]
            
            print(f"\n{i}. Testing: '{query}' ({dimension})")
            
            # Create search prompt
            search_prompt = f"""I need information about "{query}".

Please search the web and provide information about companies, tools, or services related to this query. Focus on:
1. Which companies or solutions are mentioned as top options
2. What specific services they offer
3. Any rankings or recommendations
4. Detailed information about market leaders

Include specific company names and details about their expertise."""
            
            try:
                search_response = model.generate_content(search_prompt)
                result_text = search_response.text
                
                # Analyze mentions
                company_mentioned = company_name.lower() in result_text.lower()
                mention_count = result_text.lower().count(company_name.lower())
                
                # Simple quality scoring based on content length and structure
                quality_score = min(10.0, len(result_text) / 200)  # Basic scoring
                
                print(f"   Company mentioned: {'✅' if company_mentioned else '❌'}")
                if company_mentioned:
                    print(f"   Mention count: {mention_count}")
                    print(f"   Quality score: {quality_score:.1f}/10")
                    print(f"   Preview: {result_text[:150]}...")
                else:
                    print(f"   No mentions found")
                    print(f"   Response length: {len(result_text)} chars")
                
                company_results["query_results"].append({
                    "query": query,
                    "dimension": dimension,
                    "mentioned": company_mentioned,
                    "mention_count": mention_count,
                    "quality_score": quality_score,
                    "response_preview": result_text[:300]
                })
                
                if company_mentioned:
                    company_results["summary"]["total_mentions"] += mention_count
                    company_results["summary"]["queries_with_mentions"] += 1
                
            except Exception as e:
                print(f"   ❌ Query failed: {e}")
                company_results["query_results"].append({
                    "query": query,
                    "dimension": dimension,
                    "error": str(e)
                })
        
        # Calculate summary stats
        if company_results["query_results"]:
            valid_results = [r for r in company_results["query_results"] if "error" not in r]
            if valid_results:
                company_results["summary"]["avg_quality"] = sum(r["quality_score"] for r in valid_results) / len(valid_results)
                presence_rate = (company_results["summary"]["queries_with_mentions"] / len(valid_results)) * 100
                company_results["summary"]["presence_rate"] = presence_rate
        
        print(f"\n📊 REAL RESULTS SUMMARY FOR {company_name}:")
        print(f"   Queries tested: {len(company_results['query_results'])}")
        print(f"   Total mentions: {company_results['summary']['total_mentions']}")
        print(f"   Queries with mentions: {company_results['summary']['queries_with_mentions']}")
        print(f"   Presence rate: {company_results['summary'].get('presence_rate', 0):.1f}%")
        print(f"   Average quality: {company_results['summary']['avg_quality']:.1f}/10")
        
        all_results[company_name] = company_results
    
    # Save complete results
    output_file = "/Users/federicodeponte/openanalytics/aeo-checks/complete_real_api_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 COMPLETE RESULTS EXPORTED:")
    print(f"   File: {output_file}")
    
    # Final comparison
    print(f"\n🏆 COMPANY COMPARISON:")
    print("-" * 50)
    for company_name, results in all_results.items():
        summary = results["summary"]
        print(f"{company_name}:")
        print(f"   Mentions: {summary['total_mentions']} | Presence: {summary.get('presence_rate', 0):.1f}% | Quality: {summary['avg_quality']:.1f}/10")
    
    return all_results

if __name__ == "__main__":
    results = asyncio.run(test_complete_real_mentions())