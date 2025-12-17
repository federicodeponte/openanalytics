#!/usr/bin/env python3
"""Extract actual queries and results for SCAILE and Valoon in fast mode."""

import asyncio
import json
from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis, CompanyInfo, Competitor
from test_company_data import SCAILE_COMPANY_DATA, VALOON_COMPANY_DATA
from run_local_tests import create_mock_ai_client

async def extract_queries_and_results():
    """Extract actual queries and mock results for both companies in fast mode."""
    
    print("🔍 EXTRACTING QUERIES AND RESULTS FOR FAST MODE")
    print("=" * 70)
    
    # Mock the AI client to get consistent results
    import master_aeo_service
    master_aeo_service.get_ai_client = lambda: create_mock_ai_client()
    
    companies = {
        "SCAILE": SCAILE_COMPANY_DATA,
        "Valoon": VALOON_COMPANY_DATA
    }
    
    all_results = {}
    
    for company_name, company_data in companies.items():
        print(f"\n🏢 COMPANY: {company_name}")
        print("=" * 50)
        
        # Create company analysis
        company_info = CompanyInfo(**company_data["companyInfo"])
        competitors = [Competitor(**comp) for comp in company_data["competitors"]]
        company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
        
        # Show company context
        print(f"📊 Industry: {company_info.industry}")
        print(f"📊 Products: {company_info.products}")
        print(f"📊 Services: {company_info.services[:2] if company_info.services else []}")  # Show first 2
        print(f"📊 Top Competitors: {[c.name for c in competitors[:3]]}")
        
        # Create mentions request (FAST MODE)
        request = MentionsCheckRequest(
            companyName=company_name,
            companyAnalysis=company_analysis,
            language="english",
            country="US",
            numQueries=10,  # Fast mode
            mode="fast",
            generateInsights=True,
            platforms=["gemini", "chatgpt"]  # Fast mode platforms
        )
        
        # Run mentions check
        result = await mentions_check_advanced(request)
        
        # Extract query results
        queries_by_dimension = {}
        for query_result in result.query_results:
            dimension = query_result.dimension
            if dimension not in queries_by_dimension:
                queries_by_dimension[dimension] = []
            
            queries_by_dimension[dimension].append({
                "query": query_result.query,
                "platform": query_result.platform,
                "mentions": query_result.capped_mentions,
                "quality_score": query_result.quality_score,
                "mention_type": query_result.mention_type,
                "position": query_result.position
            })
        
        # Display results
        print(f"\n🎯 FAST MODE RESULTS:")
        print(f"   Visibility: {result.visibility:.1f}% ({result.band})")
        print(f"   Total Mentions: {result.mentions}")
        print(f"   Presence Rate: {result.presence_rate:.1f}%")
        print(f"   Quality Score: {result.quality_score:.1f}/10")
        print(f"   Queries Processed: {result.actualQueriesProcessed}")
        
        print(f"\n🔍 GENERATED QUERIES BY DIMENSION:")
        unique_queries = set()
        for dimension, queries in queries_by_dimension.items():
            print(f"\n   📋 {dimension.upper()} ({len(queries)//2} unique queries):")  # Divide by 2 since each query runs on 2 platforms
            seen_queries = set()
            for query_data in queries:
                query = query_data["query"]
                if query not in seen_queries:
                    print(f"      • '{query}'")
                    unique_queries.add(query)
                    seen_queries.add(query)
        
        print(f"\n📊 PLATFORM PERFORMANCE:")
        for platform, stats in result.platform_stats.items():
            if stats.responses > 0:
                print(f"   • {platform}: {stats.mentions} mentions, {stats.quality_score:.1f} avg quality, {stats.responses} responses")
        
        print(f"\n🎯 TOP INSIGHTS:")
        if result.tldr and result.tldr.key_insights:
            for i, insight in enumerate(result.tldr.key_insights[:3], 1):
                print(f"   {i}. {insight}")
        
        # Store results
        all_results[company_name] = {
            "company_context": {
                "name": company_info.name,
                "industry": company_info.industry,
                "products": company_info.products,
                "services": company_info.services,
                "competitors": [c.name for c in competitors]
            },
            "fast_mode_config": {
                "platforms": ["gemini", "chatgpt"],
                "num_queries": 10,
                "mode": "fast"
            },
            "unique_queries": list(unique_queries),
            "results_summary": {
                "visibility": result.visibility,
                "band": result.band,
                "mentions": result.mentions,
                "presence_rate": result.presence_rate,
                "quality_score": result.quality_score,
                "queries_processed": result.actualQueriesProcessed
            },
            "platform_stats": {
                platform: {
                    "mentions": stats.mentions,
                    "quality_score": stats.quality_score,
                    "responses": stats.responses
                } for platform, stats in result.platform_stats.items() if stats.responses > 0
            },
            "dimension_performance": {
                dimension: {
                    "mentions": stats.mentions,
                    "quality_score": stats.quality_score,
                    "queries": stats.queries
                } for dimension, stats in result.dimension_stats.items()
            },
            "top_insights": result.tldr.key_insights[:3] if result.tldr and result.tldr.key_insights else [],
            "visibility_assessment": result.tldr.visibility_assessment if result.tldr else "",
            "brand_confusion_risk": result.tldr.brand_confusion_risk if result.tldr else ""
        }
    
    # Comparison analysis
    print(f"\n🔥 FAST MODE COMPARISON ANALYSIS")
    print("=" * 50)
    
    scaile_results = all_results["SCAILE"]
    valoon_results = all_results["Valoon"]
    
    print(f"📈 VISIBILITY COMPARISON:")
    print(f"   SCAILE: {scaile_results['results_summary']['visibility']:.1f}% ({scaile_results['results_summary']['band']})")
    print(f"   Valoon: {valoon_results['results_summary']['visibility']:.1f}% ({valoon_results['results_summary']['band']})")
    
    print(f"\n📊 MENTIONS COMPARISON:")
    print(f"   SCAILE: {scaile_results['results_summary']['mentions']} total mentions")
    print(f"   Valoon: {valoon_results['results_summary']['mentions']} total mentions")
    
    print(f"\n🎯 QUALITY COMPARISON:")
    print(f"   SCAILE: {scaile_results['results_summary']['quality_score']:.1f}/10 avg quality")
    print(f"   Valoon: {valoon_results['results_summary']['quality_score']:.1f}/10 avg quality")
    
    print(f"\n🔍 QUERY GENERATION COMPARISON:")
    print(f"   SCAILE: {len(scaile_results['unique_queries'])} unique queries generated")
    print(f"   Valoon: {len(valoon_results['unique_queries'])} unique queries generated")
    
    # Export results
    with open("/Users/federicodeponte/openanalytics/aeo-checks/queries_and_results_fast_mode.json", "w") as f:
        json.dump(all_results, f, indent=2)
    
    print(f"\n💾 COMPLETE RESULTS EXPORTED:")
    print(f"   File: queries_and_results_fast_mode.json")
    print(f"   Contains: Company context, queries, results, platform stats, insights")
    
    return all_results

if __name__ == "__main__":
    results = asyncio.run(extract_queries_and_results())