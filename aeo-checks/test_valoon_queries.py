#!/usr/bin/env python3
"""Test Valoon-specific queries with real Gemini API."""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv('.env.local')
api_key = os.getenv('GEMINI_API_KEY')

def test_valoon_queries():
    """Test Valoon-specific hyperniche queries with real Gemini API."""
    
    print("🎯 REAL GEMINI API - VALOON HYPERNICHE QUERIES")
    print("=" * 60)
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    # Valoon-specific hyperniche queries based on their business
    queries = [
        "best AI chatbot platforms for customer support teams",
        "conversational AI tools for SMB customer service", 
        "customer service automation for small businesses",
        "alternatives to Intercom for small business chat",
        "Valoon customer service software"
    ]
    
    results = {
        "company": "Valoon",
        "total_queries": len(queries),
        "valoon_mentions": 0,
        "competitor_mentions": {},
        "query_results": []
    }
    
    competitors = ["Intercom", "Zendesk", "Drift", "LiveChat", "Crisp", "Freshchat", "Tidio"]
    
    for i, query in enumerate(queries, 1):
        print(f"\n{i}. TESTING: '{query}'")
        print("-" * 50)
        
        query_prompt = f"""I need information about "{query}".

Please search the web and provide information about the best companies, tools, or platforms related to this query. Focus on:
1. Which companies or platforms are mentioned as top options
2. What specific features and services they offer
3. Any rankings, reviews, or recommendations
4. Market leaders and popular choices

Please include specific company names and details about their capabilities."""
        
        try:
            response = model.generate_content(query_prompt)
            result_text = response.text
            
            # Analyze Valoon mentions
            valoon_mentioned = "valoon" in result_text.lower()
            if valoon_mentioned:
                results["valoon_mentions"] += 1
                print("🎯 VALOON MENTIONED!")
            else:
                print("❌ Valoon not mentioned")
            
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
                "valoon_mentioned": valoon_mentioned,
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
    
    print(f"\n🏆 VALOON REAL API RESULTS SUMMARY:")
    print("=" * 50)
    print(f"📊 Total queries tested: {results['total_queries']}")
    print(f"🎯 VALOON mentions: {results['valoon_mentions']}/{results['total_queries']}")
    print(f"📈 VALOON presence rate: {(results['valoon_mentions']/results['total_queries'])*100:.1f}%")
    
    print(f"\n🏢 COMPETITOR PERFORMANCE:")
    for competitor, count in results["competitor_mentions"].items():
        print(f"   {competitor}: {count}/{results['total_queries']} queries ({(count/results['total_queries'])*100:.1f}%)")
    
    # Save results
    output_file = "/Users/federicodeponte/openanalytics/aeo-checks/valoon_real_queries_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)
    
    print(f"\n💾 Results saved to: {output_file}")
    
    # Key insights
    print(f"\n💡 KEY INSIGHTS FOR VALOON:")
    if results["valoon_mentions"] == 0:
        print("   • Valoon has ZERO visibility in AI search results")
        print("   • Customer service chatbot market dominated by established players")
    else:
        print(f"   • Valoon appears in {results['valoon_mentions']} out of {results['total_queries']} queries")
    
    if results["competitor_mentions"]:
        top_competitor = max(results["competitor_mentions"].items(), key=lambda x: x[1])
        print(f"   • Top competitor: {top_competitor[0]} ({top_competitor[1]} mentions)")
        print("   • Established customer service platforms dominate AI responses")
    
    return results

if __name__ == "__main__":
    test_valoon_queries()