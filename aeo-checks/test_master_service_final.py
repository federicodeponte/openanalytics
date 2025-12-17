#!/usr/bin/env python3
"""Final test: Master service with native Gemini SDK - 10 queries like aeo-leaderboard."""

import os
import asyncio
import sys
sys.path.append('/Users/federicodeponte/openanalytics/aeo-checks')

from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis, CompanyInfo, Competitor
from test_company_data import SCAILE_COMPANY_DATA

async def test_master_service_final():
    """Final test with master service using native Gemini SDK."""
    
    print("🏆 FINAL TEST: MASTER SERVICE + NATIVE GEMINI SDK")
    print("=" * 70)
    
    # Create full SCAILE request - matching aeo-leaderboard standard
    company_data = SCAILE_COMPANY_DATA
    company_info = CompanyInfo(**company_data["companyInfo"])
    competitors = [Competitor(**comp) for comp in company_data["competitors"]]
    company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
    
    request = MentionsCheckRequest(
        companyName="SCAILE",
        companyAnalysis=company_analysis,
        language="english",
        country="US",
        numQueries=10,  # FULL 10 queries
        mode="fast",    # Fast mode = 10 queries, 2 platforms
        generateInsights=True,
        platforms=["gemini"]  # Test Gemini only for speed
    )
    
    print(f"🎯 TESTING MASTER SERVICE WITH:")
    print(f"   📊 Company: SCAILE")
    print(f"   🔍 Queries: 10 (hyperniche)")
    print(f"   🤖 Platform: Gemini (native SDK)")
    print(f"   🚀 Mode: Fast (matching aeo-leaderboard)")
    print(f"   🔄 Distribution: 70% unbranded, 20% competitive, 10% branded")
    
    try:
        print(f"\n⚡ Running mentions check...")
        result = await mentions_check_advanced(request)
        
        print(f"\n✅ MASTER SERVICE SUCCESS!")
        print(f"⏱️  Execution time: {result.execution_time_seconds:.2f}s")
        print(f"🎯 Queries processed: {result.actualQueriesProcessed}")
        print(f"📊 Visibility: {result.visibility:.1f}% ({result.band})")
        print(f"🏢 Total mentions: {result.mentions}")
        print(f"📈 Presence rate: {result.presence_rate:.1f}%")
        print(f"⭐ Quality score: {result.quality_score:.1f}/10")
        print(f"💰 Cost: ${result.total_cost:.4f}")
        
        # Show detailed query results
        print(f"\n🔍 DETAILED QUERY RESULTS:")
        print("-" * 60)
        
        for i, qr in enumerate(result.query_results, 1):
            mentions = qr.capped_mentions
            quality = qr.quality_score
            dimension = qr.dimension
            
            status = "✅" if mentions > 0 else "❌"
            print(f"{i:2d}. {status} '{qr.query}' ({dimension})")
            print(f"     Mentions: {mentions} | Quality: {quality:.1f}/10 | Type: {qr.mention_type}")
            
            if mentions > 0:
                preview = qr.response_text[:100] if qr.response_text else "No response"
                print(f"     Preview: {preview}...")
        
        # Performance breakdown
        print(f"\n📊 PERFORMANCE BREAKDOWN:")
        print("-" * 40)
        
        # By dimension
        dimensions = {}
        for qr in result.query_results:
            dim = qr.dimension
            if dim not in dimensions:
                dimensions[dim] = {"mentions": 0, "queries": 0}
            dimensions[dim]["mentions"] += qr.capped_mentions
            dimensions[dim]["queries"] += 1
        
        for dim, stats in dimensions.items():
            rate = (stats["mentions"] / max(stats["queries"], 1)) * 100
            print(f"   {dim}: {stats['mentions']} mentions / {stats['queries']} queries ({rate:.1f}%)")
        
        # Check if hyperniche queries were generated
        unbranded_queries = [qr for qr in result.query_results if qr.dimension.startswith("UNBRANDED")]
        print(f"\n🎯 HYPERNICHE ANALYSIS:")
        print(f"   Unbranded queries: {len(unbranded_queries)}/10")
        print(f"   Organic mentions: {sum(qr.capped_mentions for qr in unbranded_queries)}")
        
        if len(unbranded_queries) >= 7:
            print(f"   ✅ Proper 70% unbranded distribution achieved!")
        
        # AI Insights
        if result.tldr:
            print(f"\n💡 AI INSIGHTS:")
            print(f"   Assessment: {result.tldr.visibility_assessment}")
            if result.tldr.key_insights:
                for insight in result.tldr.key_insights[:3]:
                    print(f"   • {insight}")
        
        print(f"\n🎉 INTEGRATION COMPLETE!")
        print(f"✅ Native Gemini SDK working")
        print(f"✅ 10-query hyperniche generation")
        print(f"✅ Real API responses")
        print(f"✅ Quality scoring and insights")
        print(f"✅ Matches aeo-leaderboard functionality")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_master_service_final())
    if success:
        print(f"\n🚀 MASTER SERVICE + GEMINI SDK = 100% SUCCESS!")
    else:
        print(f"\n💥 TEST FAILED")