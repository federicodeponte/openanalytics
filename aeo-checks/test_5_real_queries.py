#!/usr/bin/env python3
"""Test 5 key hyperniche queries with real Gemini API - comprehensive results."""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv('.env.local')
api_key = os.getenv('GEMINI_API_KEY')

def test_5_real_queries():
    """Test 5 key hyperniche queries with real Gemini API."""
    
    print("🎯 REAL GEMINI API - 5 KEY HYPERNICHE QUERIES")
    print("=" * 60)
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # 5 key hyperniche queries
    queries = [
        "best AEO consulting for B2B SaaS companies United States",
        "Answer Engine Optimization for CMOs in enterprise companies", 
        "AI search optimization tools for marketing teams",
        "alternatives to BrightEdge for SaaS companies",
        "SCAILE AEO consulting"
    ]
    
    results = {
        "total_queries": len(queries),
        "scaile_mentions": 0,
        "competitor_mentions": {},
        "query_results": []
    }
    
    competitors = ["BrightEdge", "Conductor", "Searchmetrics", "Semrush", "Moz", "Ahrefs"]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. TESTING: '{query}'")
        print("-" * 50)
        
        query_prompt = f"""I need information about "{query}".

Please search the web and provide information about the best companies, tools, or services related to this query. Focus on:
1. Which companies or consultants are mentioned as top options
2. What specific services they offer
3. Any rankings or recommendations
4. Market leaders and established players

Please include specific company names and details about their expertise."""
        
        try:
            response = model.generate_content(query_prompt)
            result_text = response.text
            
            # Analyze mentions
            scaile_mentioned = "scaile" in result_text.lower()
            if scaile_mentioned:
                results["scaile_mentions"] += 1
                print("🎯 SCAILE MENTIONED!")
            else:
                print("❌ SCAILE not mentioned")
            
            # Check competitor mentions
            query_competitors = []
            for competitor in competitors:
                if competitor.lower() in result_text.lower():
                    query_competitors.append(competitor)
                    if competitor not in results["competitor_mentions"]:
                        results["competitor_mentions"][competitor] = 0
                    results["competitor_mentions"][competitor] += 1
            
            print(f"🏢 Competitors mentioned: {', '.join(query_competitors) if query_competitors else 'None'}")
            print(f"📄 Response length: {len(result_text)} characters")
            print(f"📖 Preview: {result_text[:200]}...")
            
            results["query_results"].append({
                "query": query,
                "scaile_mentioned": scaile_mentioned,
                "competitors_mentioned": query_competitors,
                "response_length": len(result_text),
                "response_preview": result_text[:500]
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results["query_results"].append({
                "query": query,
                "error": str(e)
            })
    
    print(f"\n🏆 REAL API RESULTS SUMMARY:")
    print("=" * 50)
    print(f"📊 Total queries tested: {results['total_queries']}")
    print(f"🎯 SCAILE mentions: {results['scaile_mentions']}/{results['total_queries']}")
    print(f"📈 SCAILE presence rate: {(results['scaile_mentions']/results['total_queries'])*100:.1f}%")
    
    print(f"\n🏢 COMPETITOR PERFORMANCE:")
    for competitor, count in results["competitor_mentions"].items():
        print(f"   {competitor}: {count}/{results['total_queries']} queries ({(count/results['total_queries'])*100:.1f}%)")
    
    # Save results
    output_file = "/Users/federicodeponte/openanalytics/aeo-checks/5_real_queries_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Key insights
    print(f"\n💡 KEY INSIGHTS:")
    if results["scaile_mentions"] == 0:
        print("   • SCAILE has ZERO visibility in AI search results")
        print("   • This confirms the need for comprehensive AEO strategy")
    else:
        print(f"   • SCAILE appears in {results['scaile_mentions']} out of {results['total_queries']} queries")
    
    if results["competitor_mentions"]:
        top_competitor = max(results["competitor_mentions"].items(), key=lambda x: x[1])
        print(f"   • Top competitor: {top_competitor[0]} ({top_competitor[1]} mentions)")
        print("   • Established players dominate AI search results")
    
    return results

if __name__ == "__main__":
    test_5_real_queries()