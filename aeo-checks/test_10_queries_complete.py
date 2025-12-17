#!/usr/bin/env python3
"""Test COMPLETE 10 queries for both SCAILE and Valoon with real Gemini API."""

import os
import json
import google.generativeai as genai
from dotenv import load_dotenv

# Load API key
load_dotenv('.env.local')
api_key = os.getenv('GEMINI_API_KEY')

def test_complete_10_queries():
    """Test complete 10 hyperniche queries for both companies with real Gemini API."""
    
    print("🎯 REAL GEMINI API - COMPLETE 10 QUERIES PER COMPANY")
    print("=" * 70)
    print(f"🔑 API Key: {api_key[:20]}...")
    
    # Configure Gemini
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    
    companies = {
        "SCAILE": {
            "queries": [
                # 70% UNBRANDED HYPERNICHE (7 queries)
                "best AEO consulting for B2B SaaS companies United States",
                "Answer Engine Optimization for CMOs in enterprise companies", 
                "AI search optimization tools for marketing teams",
                "enterprise Marketing Technology AEO solutions",
                "best tools for improving AI search visibility mentions",
                "top AEO companies for B2B SaaS United States",
                "AI platform optimization consultants for enterprise",
                # 20% COMPETITIVE HYPERNICHE (2 queries)
                "alternatives to BrightEdge for SaaS companies",
                "BrightEdge vs Conductor for enterprise AEO",
                # 10% BRANDED DIRECT (1 query)
                "SCAILE AEO consulting"
            ],
            "competitors": ["BrightEdge", "Conductor", "Searchmetrics", "Semrush", "Moz", "Ahrefs"]
        },
        "Valoon": {
            "queries": [
                # 70% UNBRANDED HYPERNICHE (7 queries)
                "best AI chatbot platforms for customer support teams",
                "conversational AI tools for SMB customer service", 
                "customer service automation for small businesses",
                "enterprise customer support software solutions",
                "AI chat tools for startup customer service",
                "top customer service platforms for SMB United States",
                "automated customer support for growing companies",
                # 20% COMPETITIVE HYPERNICHE (2 queries)
                "alternatives to Intercom for small business chat",
                "Intercom vs Zendesk for SMB customer service",
                # 10% BRANDED DIRECT (1 query)
                "Valoon customer service software"
            ],
            "competitors": ["Intercom", "Zendesk", "Drift", "LiveChat", "Crisp", "Freshchat", "Tidio"]
        }
    }
    
    all_results = {}
    
    for company_name, company_data in companies.items():
        print(f"\n🏢 TESTING: {company_name} (10 COMPLETE QUERIES)")
        print("=" * 60)
        
        queries = company_data["queries"]
        competitors = company_data["competitors"]
        
        results = {
            "company": company_name,
            "total_queries": len(queries),
            "company_mentions": 0,
            "competitor_mentions": {},
            "query_results": []
        }
        
        for i, query in enumerate(queries, 1):
            print(f"\n{i}/10. TESTING: '{query}'")
            print("-" * 50)
            
            # Determine query dimension
            if company_name.lower() in query.lower():
                dimension = "BRANDED_DIRECT"
            elif any(comp.lower() in query.lower() for comp in competitors):
                dimension = "COMPETITIVE_HYPERNICHE"
            else:
                dimension = "UNBRANDED_HYPERNICHE"
            
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
                
                # Analyze company mentions
                company_mentioned = company_name.lower() in result_text.lower()
                company_count = result_text.lower().count(company_name.lower())
                
                if company_mentioned:
                    results["company_mentions"] += 1
                    print(f"🎯 {company_name.upper()} MENTIONED! ({company_count} times)")
                else:
                    print(f"❌ {company_name} not mentioned")
                
                # Check competitor mentions
                query_competitors = []
                for competitor in competitors:
                    if competitor.lower() in result_text.lower():
                        query_competitors.append(competitor)
                        if competitor not in results["competitor_mentions"]:
                            results["competitor_mentions"][competitor] = 0
                        results["competitor_mentions"][competitor] += 1
                
                print(f"🏢 Competitors: {', '.join(query_competitors) if query_competitors else 'None'}")
                print(f"📊 Dimension: {dimension}")
                print(f"📄 Length: {len(result_text)} chars")
                
                results["query_results"].append({
                    "query": query,
                    "dimension": dimension,
                    "company_mentioned": company_mentioned,
                    "company_count": company_count,
                    "competitors_mentioned": query_competitors,
                    "response_length": len(result_text),
                    "response_preview": result_text[:300]
                })
                
            except Exception as e:
                print(f"❌ Error: {e}")
                results["query_results"].append({
                    "query": query,
                    "dimension": dimension,
                    "error": str(e)
                })
        
        # Calculate statistics
        presence_rate = (results["company_mentions"] / results["total_queries"]) * 100
        
        print(f"\n🏆 {company_name.upper()} COMPLETE RESULTS:")
        print("=" * 50)
        print(f"📊 Total queries: {results['total_queries']}")
        print(f"🎯 Company mentions: {results['company_mentions']}/{results['total_queries']}")
        print(f"📈 Presence rate: {presence_rate:.1f}%")
        
        # Break down by dimension
        dimensions = {"UNBRANDED_HYPERNICHE": [], "COMPETITIVE_HYPERNICHE": [], "BRANDED_DIRECT": []}
        for result in results["query_results"]:
            if "error" not in result:
                dimensions[result["dimension"]].append(result)
        
        print(f"\n📊 BREAKDOWN BY DIMENSION:")
        for dim, dim_results in dimensions.items():
            if dim_results:
                mentions = sum(1 for r in dim_results if r["company_mentioned"])
                rate = (mentions / len(dim_results)) * 100 if dim_results else 0
                print(f"   {dim}: {mentions}/{len(dim_results)} mentions ({rate:.1f}%)")
        
        print(f"\n🏢 TOP COMPETITOR PERFORMANCE:")
        sorted_competitors = sorted(results["competitor_mentions"].items(), key=lambda x: x[1], reverse=True)
        for competitor, count in sorted_competitors[:5]:
            comp_rate = (count / results["total_queries"]) * 100
            print(f"   {competitor}: {count}/{results['total_queries']} queries ({comp_rate:.1f}%)")
        
        all_results[company_name] = results
    
    # Save complete results
    output_file = "/Users/federicodeponte/openanalytics/aeo-checks/complete_10_queries_results.json"
    with open(output_file, "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 COMPLETE 10-QUERY RESULTS EXPORTED:")
    print(f"   File: {output_file}")
    
    # Final comparison
    print(f"\n🏆 FINAL COMPANY COMPARISON (10 QUERIES EACH):")
    print("=" * 60)
    for company_name, results in all_results.items():
        presence_rate = (results["company_mentions"] / results["total_queries"]) * 100
        top_competitor = max(results["competitor_mentions"].items(), key=lambda x: x[1])[0] if results["competitor_mentions"] else "None"
        top_comp_rate = (max(results["competitor_mentions"].values()) / results["total_queries"]) * 100 if results["competitor_mentions"] else 0
        
        print(f"{company_name}:")
        print(f"   Presence: {results['company_mentions']}/10 ({presence_rate:.1f}%)")
        print(f"   Top competitor: {top_competitor} ({top_comp_rate:.1f}%)")
        
        # Show organic vs branded performance
        organic_mentions = sum(1 for r in results["query_results"] if r.get("company_mentioned", False) and r.get("dimension") == "UNBRANDED_HYPERNICHE")
        branded_mentions = sum(1 for r in results["query_results"] if r.get("company_mentioned", False) and r.get("dimension") == "BRANDED_DIRECT")
        
        print(f"   Organic visibility: {organic_mentions}/7 unbranded queries")
        print(f"   Branded visibility: {branded_mentions}/1 branded query")
    
    return all_results

if __name__ == "__main__":
    test_complete_10_queries()