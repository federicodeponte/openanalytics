#!/usr/bin/env python3
"""Extract detailed hyperniche queries and complete results for SCAILE and Valoon."""

import asyncio
import json
from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis, CompanyInfo, Competitor
from test_company_data import SCAILE_COMPANY_DATA, VALOON_COMPANY_DATA
from run_local_tests import create_mock_ai_client

async def extract_detailed_results():
    """Extract complete hyperniche queries and detailed results."""
    
    print("🔍 DETAILED HYPERNICHE QUERIES & RESULTS")
    print("=" * 80)
    
    # Mock the AI client
    import master_aeo_service
    master_aeo_service.get_ai_client = lambda: create_mock_ai_client()
    
    companies = {
        "SCAILE": SCAILE_COMPANY_DATA,
        "Valoon": VALOON_COMPANY_DATA
    }
    
    detailed_results = {}
    
    for company_name, company_data in companies.items():
        print(f"\n🏢 {company_name.upper()} - DETAILED ANALYSIS")
        print("=" * 60)
        
        # Create company analysis
        company_info = CompanyInfo(**company_data["companyInfo"])
        competitors = [Competitor(**comp) for comp in company_data["competitors"]]
        company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
        
        # Company context summary
        print(f"🎯 BUSINESS CONTEXT:")
        print(f"   Industry: {company_info.industry}")
        print(f"   Products: {', '.join(company_info.products[:3]) if company_info.products else 'None'}")
        print(f"   Target: {company_info.target_audience}")
        print(f"   Competitors: {', '.join([c.name for c in competitors[:3]])}")
        
        # Create mentions request (FAST MODE with hyperniche generation)
        request = MentionsCheckRequest(
            companyName=company_name,
            companyAnalysis=company_analysis,
            language="english",
            country="US",
            numQueries=10,
            mode="fast",
            generateInsights=True,
            platforms=["gemini", "chatgpt"]
        )
        
        # Run mentions check with hyperniche queries
        result = await mentions_check_advanced(request)
        
        print(f"\n🎯 HYPERNICHE QUERIES GENERATED ({result.actualQueriesProcessed} total):")
        print("-" * 50)
        
        # Extract and display each query with complete results
        queries_with_results = []
        
        for i, query_result in enumerate(result.query_results, 1):
            query_data = {
                "query_number": i,
                "query": query_result.query,
                "dimension": query_result.dimension,
                "platform": query_result.platform,
                "results": {
                    "raw_mentions": query_result.raw_mentions,
                    "capped_mentions": query_result.capped_mentions,
                    "quality_score": query_result.quality_score,
                    "mention_type": query_result.mention_type,
                    "position": query_result.position,
                    "source_urls": query_result.source_urls,
                    "competitor_mentions": query_result.competitor_mentions,
                    "response_length": len(query_result.response_text)
                }
            }
            queries_with_results.append(query_data)
            
            # Display query details
            targeting_elements = []
            query_lower = query_result.query.lower()
            if "for " in query_lower:
                targeting_elements.append("🎯 Targeted")
            if "enterprise" in query_lower or "b2b" in query_lower:
                targeting_elements.append("🏢 Enterprise")
            if "united states" in query_lower:
                targeting_elements.append("🌍 Geographic")
            if any(product.lower() in query_lower for product in (company_info.products or [])):
                targeting_elements.append("📦 Product-Specific")
            if any(comp.name.lower() in query_lower for comp in competitors):
                targeting_elements.append("⚔️ Competitive")
            if "cmo" in query_lower or "director" in query_lower or "manager" in query_lower:
                targeting_elements.append("👥 Role-Specific")
            
            targeting_str = " ".join(targeting_elements) if targeting_elements else "❌ Generic"
            
            print(f"\n{i:2d}. QUERY: '{query_result.query}'")
            print(f"     Dimension: {query_result.dimension}")
            print(f"     Targeting: {targeting_str}")
            print(f"     Platform: {query_result.platform}")
            print(f"     Results: {query_result.capped_mentions} mentions, {query_result.quality_score:.1f} quality")
            print(f"     Type: {query_result.mention_type}")
            if query_result.position:
                print(f"     Position: #{query_result.position}")
        
        # Unique queries (since each runs on 2 platforms)
        unique_queries = {}
        for qr in result.query_results:
            if qr.query not in unique_queries:
                unique_queries[qr.query] = {
                    "dimension": qr.dimension,
                    "platforms": [],
                    "total_mentions": 0,
                    "avg_quality": 0,
                    "mention_types": set()
                }
            unique_queries[qr.query]["platforms"].append(qr.platform)
            unique_queries[qr.query]["total_mentions"] += qr.capped_mentions
            unique_queries[qr.query]["avg_quality"] += qr.quality_score
            unique_queries[qr.query]["mention_types"].add(qr.mention_type)
        
        # Average quality scores
        for query, data in unique_queries.items():
            data["avg_quality"] = data["avg_quality"] / len(data["platforms"])
            data["mention_types"] = list(data["mention_types"])
        
        print(f"\n📊 UNIQUE QUERIES SUMMARY ({len(unique_queries)} unique):")
        print("-" * 50)
        
        for i, (query, data) in enumerate(unique_queries.items(), 1):
            print(f"{i:2d}. '{query}'")
            print(f"     → {data['dimension']} | {data['total_mentions']} mentions | {data['avg_quality']:.1f} quality")
            print(f"     → Platforms: {', '.join(data['platforms'])} | Types: {', '.join(data['mention_types'])}")
        
        # Overall results summary
        print(f"\n🏆 OVERALL PERFORMANCE:")
        print(f"   Visibility: {result.visibility:.1f}% ({result.band})")
        print(f"   Total Mentions: {result.mentions}")
        print(f"   Presence Rate: {result.presence_rate:.1f}%")
        print(f"   Quality Score: {result.quality_score:.1f}/10")
        print(f"   Execution Time: {result.execution_time_seconds:.2f}s")
        
        # Platform performance
        print(f"\n📱 PLATFORM PERFORMANCE:")
        for platform, stats in result.platform_stats.items():
            if stats.responses > 0:
                print(f"   {platform.title()}: {stats.mentions} mentions, {stats.quality_score:.1f} quality, {stats.responses} responses")
        
        # Dimension performance
        print(f"\n📋 DIMENSION PERFORMANCE:")
        for dimension, stats in result.dimension_stats.items():
            print(f"   {dimension}: {stats.mentions} mentions, {stats.quality_score:.1f} quality, {stats.queries} queries")
        
        # TL;DR insights
        if result.tldr:
            print(f"\n💡 KEY INSIGHTS:")
            print(f"   Assessment: {result.tldr.visibility_assessment}")
            print(f"   Brand Risk: {result.tldr.brand_confusion_risk}")
            if result.tldr.key_insights:
                print(f"   Top Insights:")
                for insight in result.tldr.key_insights[:3]:
                    print(f"   • {insight}")
            if result.tldr.actionable_recommendations:
                print(f"   Recommendations:")
                for rec in result.tldr.actionable_recommendations[:2]:
                    print(f"   • {rec}")
        
        # Store detailed results
        detailed_results[company_name] = {
            "company_context": {
                "name": company_info.name,
                "industry": company_info.industry,
                "products": company_info.products,
                "target_audience": company_info.target_audience,
                "competitors": [c.name for c in competitors]
            },
            "unique_queries": dict(unique_queries),
            "complete_query_results": [
                {
                    "query": qr.query,
                    "dimension": qr.dimension,
                    "platform": qr.platform,
                    "mentions": qr.capped_mentions,
                    "quality": qr.quality_score,
                    "type": qr.mention_type,
                    "position": qr.position
                } for qr in result.query_results
            ],
            "performance_summary": {
                "visibility": result.visibility,
                "band": result.band,
                "total_mentions": result.mentions,
                "presence_rate": result.presence_rate,
                "quality_score": result.quality_score,
                "execution_time": result.execution_time_seconds
            },
            "platform_stats": {
                platform: {
                    "mentions": stats.mentions,
                    "quality": stats.quality_score,
                    "responses": stats.responses
                } for platform, stats in result.platform_stats.items()
            },
            "dimension_stats": {
                dimension: {
                    "mentions": stats.mentions,
                    "quality": stats.quality_score,
                    "queries": stats.queries
                } for dimension, stats in result.dimension_stats.items()
            }
        }
    
    # Export complete results
    with open("/Users/federicodeponte/openanalytics/aeo-checks/detailed_hyperniche_results.json", "w") as f:
        json.dump(detailed_results, f, indent=2)
    
    print(f"\n💾 COMPLETE RESULTS EXPORTED:")
    print(f"   File: detailed_hyperniche_results.json")
    print(f"   Contains: All 10 queries + complete results for both companies")
    
    return detailed_results

if __name__ == "__main__":
    results = asyncio.run(extract_detailed_results())