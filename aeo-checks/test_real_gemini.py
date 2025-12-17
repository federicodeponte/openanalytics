#!/usr/bin/env python3
"""Test hyperniche queries with REAL Gemini API - no mocks!"""

import os
import asyncio
import json
from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis, CompanyInfo, Competitor
from test_company_data import SCAILE_COMPANY_DATA, VALOON_COMPANY_DATA

# Load environment variables
from dotenv import load_dotenv
load_dotenv('.env.local')

async def test_real_gemini_queries():
    """Test with REAL Gemini API - actual results!"""
    
    print("🔥 REAL GEMINI API TESTING - HYPERNICHE QUERIES")
    print("=" * 70)
    print(f"🔑 Using Gemini API Key: {os.getenv('GEMINI_API_KEY', 'NOT_SET')[:20]}...")
    
    # Test just SCAILE first to see real results
    company_data = SCAILE_COMPANY_DATA
    company_name = "SCAILE"
    
    print(f"\n🏢 TESTING: {company_name} (REAL API)")
    print("=" * 50)
    
    # Create company analysis
    company_info = CompanyInfo(**company_data["companyInfo"])
    competitors = [Competitor(**comp) for comp in company_data["competitors"]]
    company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
    
    print(f"📊 Company: {company_info.name}")
    print(f"📊 Industry: {company_info.industry}")
    print(f"📊 Products: {', '.join(company_info.products[:3])}")
    print(f"📊 Target: B2B SaaS companies, CMOs, enterprise companies")
    print(f"📊 Competitors: {', '.join([c.name for c in competitors[:3]])}")
    
    # Create mentions request - REAL API call
    request = MentionsCheckRequest(
        companyName=company_name,
        companyAnalysis=company_analysis,
        language="english",
        country="US",
        numQueries=5,  # Start small to test
        mode="fast",
        generateInsights=True,
        platforms=["gemini", "chatgpt"]  # Test both platforms
    )
    
    print(f"\n🎯 GENERATING REAL HYPERNICHE QUERIES...")
    print(f"⚡ Mode: Fast (5 queries, 2 platforms)")
    print(f"🤖 Platforms: Gemini + ChatGPT")
    
    try:
        # This will use REAL APIs
        result = await mentions_check_advanced(request)
        
        print(f"\n✅ REAL API TEST COMPLETE!")
        print(f"⏱️  Execution Time: {result.execution_time_seconds:.2f}s")
        print(f"🎯 Queries Processed: {result.actualQueriesProcessed}")
        
        print(f"\n🔍 REAL HYPERNICHE QUERIES GENERATED:")
        print("-" * 50)
        
        # Show actual queries generated
        unique_queries = {}
        for query_result in result.query_results:
            if query_result.query not in unique_queries:
                unique_queries[query_result.query] = {
                    "dimension": query_result.dimension,
                    "platforms": [],
                    "total_mentions": 0,
                    "avg_quality": 0,
                    "mention_types": set(),
                    "all_results": []
                }
            
            unique_queries[query_result.query]["platforms"].append(query_result.platform)
            unique_queries[query_result.query]["total_mentions"] += query_result.capped_mentions
            unique_queries[query_result.query]["avg_quality"] += query_result.quality_score
            unique_queries[query_result.query]["mention_types"].add(query_result.mention_type)
            unique_queries[query_result.query]["all_results"].append({
                "platform": query_result.platform,
                "mentions": query_result.capped_mentions,
                "quality": query_result.quality_score,
                "type": query_result.mention_type,
                "position": query_result.position,
                "response_preview": query_result.response_text[:200] + "..." if query_result.response_text else "No response"
            })
        
        # Average quality scores
        for query, data in unique_queries.items():
            data["avg_quality"] = data["avg_quality"] / len(data["platforms"])
            data["mention_types"] = list(data["mention_types"])
        
        # Display each unique query with REAL results
        for i, (query, data) in enumerate(unique_queries.items(), 1):
            print(f"\n{i}. QUERY: '{query}'")
            print(f"   Dimension: {data['dimension']}")
            print(f"   Total Mentions: {data['total_mentions']}")
            print(f"   Average Quality: {data['avg_quality']:.1f}/10")
            print(f"   Mention Types: {', '.join(data['mention_types'])}")
            
            # Show results per platform
            for result_data in data["all_results"]:
                platform = result_data["platform"]
                mentions = result_data["mentions"]
                quality = result_data["quality"]
                mention_type = result_data["type"]
                position = result_data["position"]
                
                status = "✅" if mentions > 0 else "❌"
                pos_str = f"#{position}" if position else "Not ranked"
                
                print(f"   {status} {platform.title()}: {mentions} mentions, {quality:.1f} quality, {mention_type}, {pos_str}")
                
                if mentions > 0:
                    print(f"      Preview: {result_data['response_preview'][:100]}...")
        
        print(f"\n🏆 REAL PERFORMANCE SUMMARY:")
        print(f"   Visibility: {result.visibility:.1f}% ({result.band})")
        print(f"   Total Mentions: {result.mentions}")
        print(f"   Presence Rate: {result.presence_rate:.1f}%")
        print(f"   Quality Score: {result.quality_score:.1f}/10")
        print(f"   Cost: ${result.total_cost:.4f}")
        print(f"   Tokens: {result.total_tokens}")
        
        # Platform comparison
        print(f"\n📱 REAL PLATFORM PERFORMANCE:")
        for platform, stats in result.platform_stats.items():
            if stats.responses > 0:
                print(f"   {platform.title()}: {stats.mentions} mentions, {stats.quality_score:.1f} avg quality")
        
        # Dimension analysis
        print(f"\n📊 DIMENSION PERFORMANCE:")
        for dimension, stats in result.dimension_stats.items():
            print(f"   {dimension}: {stats.mentions} mentions, {stats.quality_score:.1f} quality")
        
        # Real insights from TL;DR
        if result.tldr:
            print(f"\n💡 REAL AI INSIGHTS:")
            print(f"   Assessment: {result.tldr.visibility_assessment}")
            print(f"   Brand Risk: {result.tldr.brand_confusion_risk}")
            
            if result.tldr.key_insights:
                print(f"   Key Insights:")
                for insight in result.tldr.key_insights:
                    print(f"   • {insight}")
            
            if result.tldr.actionable_recommendations:
                print(f"   Recommendations:")
                for rec in result.tldr.actionable_recommendations:
                    print(f"   • {rec}")
        
        # Export real results
        real_results = {
            "company": company_name,
            "timestamp": "real_api_test",
            "execution_time": result.execution_time_seconds,
            "queries_processed": result.actualQueriesProcessed,
            "unique_queries": unique_queries,
            "performance": {
                "visibility": result.visibility,
                "band": result.band,
                "mentions": result.mentions,
                "presence_rate": result.presence_rate,
                "quality_score": result.quality_score,
                "cost": result.total_cost,
                "tokens": result.total_tokens
            },
            "platform_stats": {
                platform: {
                    "mentions": stats.mentions,
                    "quality": stats.quality_score,
                    "responses": stats.responses
                } for platform, stats in result.platform_stats.items()
            }
        }
        
        with open("/Users/federicodeponte/openanalytics/aeo-checks/real_gemini_results.json", "w") as f:
            json.dump(real_results, f, indent=2)
        
        print(f"\n💾 REAL RESULTS EXPORTED:")
        print(f"   File: real_gemini_results.json")
        print(f"   Contains: Actual API responses and performance data")
        
        return real_results
        
    except Exception as e:
        print(f"\n❌ ERROR IN REAL API TEST: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return None

if __name__ == "__main__":
    results = asyncio.run(test_real_gemini_queries())