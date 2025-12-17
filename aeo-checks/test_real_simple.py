#!/usr/bin/env python3
"""Simple test with real Gemini API - just query generation and one platform test."""

import os
import asyncio
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv('.env.local')
api_key = os.getenv('GEMINI_API_KEY')

async def test_real_gemini_simple():
    """Test real Gemini API for query generation and one simple query."""
    
    print("🔥 REAL GEMINI API - SIMPLE TEST")
    print("=" * 50)
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    print("\n1️⃣ TESTING HYPERNICHE QUERY GENERATION")
    print("-" * 40)
    
    # Test sophisticated query generation
    prompt = """Generate 5 HYPERNICHE, highly targeted AEO visibility queries for SCAILE, an Answer Engine Optimization consulting company.

HYPERNICHE TARGETING DATA:
- Industry: Marketing Technology
- Products: AEO Consulting, Answer Engine Optimization, AI Search Optimization
- Services: AEO Strategy Development, Content Optimization for AI
- Target Industries: B2B SaaS companies
- Company Size: enterprise companies
- Roles: CMOs, Marketing Directors
- Geographic: United States
- Competitors: BrightEdge, Conductor, Searchmetrics
- Pain Points: Low AI search visibility, Poor mentions in AI platform responses

QUERY DISTRIBUTION (follow this exact ratio):
70% UNBRANDED_HYPERNICHE (organic visibility test):
1. PRODUCT_INDUSTRY_GEO: "best [product] for [target_industry] United States"
2. SERVICE_INDUSTRY_GEO: "[service] for [target_industry] companies"
3. INDUSTRY_PRODUCT_ENTERPRISE: "enterprise [industry] [product] solutions"
4. TARGET_ROLE_SPECIFIC: "[product] for [specific_role] in [target_industry]"
5. PAIN_POINT_SOLUTION: "best tools for [key_phrase_from_pain_point]"

20% COMPETITIVE_HYPERNICHE:
6. COMPETITOR_ALTERNATIVE: "alternatives to [competitor] for [target_industry]"

10% BRANDED_DIRECT:
7. BRANDED_PRODUCT: "SCAILE [main_product]"

CRITICAL HYPERNICHE REQUIREMENTS:
- 70% MUST NOT mention SCAILE at all
- Layer 2-3 targeting dimensions per query (Industry + Role + Geo, Product + Company_Size + Pain_Point, etc.)
- Use EXACT target industries, roles, company sizes from the data
- Include geographic qualifiers when available
- Make queries HYPER-SPECIFIC to actual B2B search patterns

EXAMPLES:
✅ HYPERNICHE: "AEO consulting for SaaS companies United States", "Answer Engine Optimization for CMOs in enterprise companies"
❌ GENERIC: "best AEO consulting", "SEO services"

Return exactly 5 queries as a JSON array:
[{"query": "actual search query", "dimension": "HYPERNICHE_TYPE"}]"""

    try:
        response = model.generate_content(prompt)
        queries_text = response.text
        
        print(f"✅ Gemini Response:")
        print(queries_text)
        
        # Try to parse JSON
        try:
            import json
            queries = json.loads(queries_text)
            print(f"\n📊 PARSED {len(queries)} QUERIES:")
            for i, q in enumerate(queries, 1):
                print(f"{i}. '{q['query']}' ({q['dimension']})")
        except:
            print("⚠️  Could not parse as JSON, but got response")
        
    except Exception as e:
        print(f"❌ Query generation failed: {e}")
        queries = [
            {"query": "AEO consulting for SaaS companies United States", "dimension": "PRODUCT_INDUSTRY_GEO"},
            {"query": "Answer Engine Optimization for CMOs", "dimension": "TARGET_ROLE_SPECIFIC"}
        ]
    
    print(f"\n2️⃣ TESTING REAL QUERY EXECUTION")
    print("-" * 40)
    
    # Test one real query
    test_query = "AEO consulting for SaaS companies United States"
    print(f"🎯 Query: '{test_query}'")
    
    query_prompt = f"""I need information about "{test_query}". 

Please search the web and provide information about the best AEO (Answer Engine Optimization) consulting companies that specialize in helping SaaS companies in the United States improve their visibility in AI-powered search platforms like ChatGPT, Perplexity, Claude, and Gemini.

Focus on:
1. Which companies or consultants are mentioned as top options
2. What specific AEO services they offer
3. Their expertise with SaaS companies
4. Any rankings or recommendations

Please include specific company names and details about their AEO expertise."""
    
    try:
        print("🔍 Querying Gemini with search...")
        response = model.generate_content(query_prompt)
        result_text = response.text
        
        print(f"✅ REAL GEMINI RESPONSE:")
        print("-" * 30)
        print(result_text[:500] + "..." if len(result_text) > 500 else result_text)
        
        # Analyze mentions
        print(f"\n📊 MENTION ANALYSIS:")
        scaile_mentioned = "scaile" in result_text.lower()
        brightedge_mentioned = "brightedge" in result_text.lower()
        conductor_mentioned = "conductor" in result_text.lower()
        
        print(f"   SCAILE mentioned: {'✅' if scaile_mentioned else '❌'}")
        print(f"   BrightEdge mentioned: {'✅' if brightedge_mentioned else '❌'}")
        print(f"   Conductor mentioned: {'✅' if conductor_mentioned else '❌'}")
        
        # Simple scoring
        if scaile_mentioned:
            print(f"   🎯 SCAILE found in results!")
        else:
            print(f"   ⚠️  SCAILE not mentioned in AI response")
        
        return {
            "query_generation": "success",
            "test_query": test_query,
            "scaile_mentioned": scaile_mentioned,
            "response_length": len(result_text),
            "response_preview": result_text[:200]
        }
        
    except Exception as e:
        print(f"❌ Query execution failed: {e}")
        return {"error": str(e)}

if __name__ == "__main__":
    result = asyncio.run(test_real_gemini_simple())