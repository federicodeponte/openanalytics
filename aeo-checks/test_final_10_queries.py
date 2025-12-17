#!/usr/bin/env python3
"""Final test: 10 queries with Gemini + Serper - production ready."""

import os
import asyncio
import sys
sys.path.append('/Users/federicodeponte/openanalytics/aeo-checks')

from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis, CompanyInfo, Competitor
from test_company_data import SCAILE_COMPANY_DATA

async def test_final_10_queries():
    """Final production test: 10 queries with full Gemini + Serper integration."""
    
    print("🏆 FINAL PRODUCTION TEST: 10 QUERIES + GEMINI + SERPER")
    print("=" * 70)
    
    # Create SCAILE request - production configuration
    company_data = SCAILE_COMPANY_DATA
    company_info = CompanyInfo(**company_data["companyInfo"])
    competitors = [Competitor(**comp) for comp in company_data["competitors"]]
    company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
    
    request = MentionsCheckRequest(
        companyName="SCAILE",
        companyAnalysis=company_analysis,
        language="english",
        country="US",
        numQueries=10,  # PRODUCTION STANDARD: 10 queries
        mode="fast",
        generateInsights=True,
        platforms=["gemini"]
    )
    
    print(f"🎯 PRODUCTION CONFIGURATION:")
    print(f"   📊 Company: SCAILE")
    print(f"   🔍 Queries: 10 (production standard)")
    print(f"   🤖 Platform: Gemini native SDK")
    print(f"   🌐 Web search: Serper API enhanced")
    print(f"   📈 Distribution: 70% unbranded, 20% competitive, 10% branded")
    print(f"   ⚡ Mode: Fast (aeo-leaderboard parity)")
    
    try:
        print(f"\n🚀 Running production mentions check...")
        start_time = asyncio.get_event_loop().time()
        
        result = await mentions_check_advanced(request)
        
        end_time = asyncio.get_event_loop().time()
        actual_time = end_time - start_time
        
        print(f"\n✅ PRODUCTION SUCCESS!")
        print(f"⏱️  Execution time: {result.execution_time_seconds:.2f}s (actual: {actual_time:.2f}s)")
        print(f"🎯 Queries processed: {result.actualQueriesProcessed}/10")
        print(f"📊 Visibility: {result.visibility:.1f}% ({result.band})")
        print(f"🏢 Total mentions: {result.mentions}")
        print(f"📈 Presence rate: {result.presence_rate:.1f}%")
        print(f"⭐ Quality score: {result.quality_score:.1f}/10")
        print(f"💰 Cost: ${result.total_cost:.4f}")
        
        # Detailed query breakdown
        print(f"\n🔍 COMPLETE QUERY RESULTS (10/10):")
        print("=" * 70)
        
        organic_mentions = 0
        competitive_mentions = 0
        branded_mentions = 0
        web_enhanced_count = 0
        
        for i, qr in enumerate(result.query_results, 1):
            mentions = qr.capped_mentions
            quality = qr.quality_score
            dimension = qr.dimension
            
            # Categorize by type
            if dimension.startswith("UNBRANDED"):
                organic_mentions += mentions
            elif "Competitive" in dimension:
                competitive_mentions += mentions
            elif "Branded" in dimension:
                branded_mentions += mentions
            
            # Check web enhancement
            if qr.response_text:
                web_indicators = ["according to", "based on", "search results", "sources"]
                has_web_content = any(indicator in qr.response_text.lower() for indicator in web_indicators)
                if has_web_content:
                    web_enhanced_count += 1
            
            status = "✅" if mentions > 0 else "❌"
            web_status = "🌐" if has_web_content else "📝"
            
            print(f"{i:2d}. {status}{web_status} '{qr.query[:50]}...' ({dimension})")
            print(f"     Mentions: {mentions} | Quality: {quality:.1f}/10 | Type: {qr.mention_type}")
            
            if mentions > 0 and qr.response_text:
                preview = qr.response_text[:100].replace('\n', ' ')
                print(f"     Preview: {preview}...")
        
        print(f"\n📊 PRODUCTION PERFORMANCE BREAKDOWN:")
        print("=" * 50)
        print(f"🎯 Organic (unbranded) mentions: {organic_mentions}")
        print(f"🥊 Competitive mentions: {competitive_mentions}")
        print(f"🏷️  Branded mentions: {branded_mentions}")
        print(f"🌐 Web-enhanced responses: {web_enhanced_count}/10 ({(web_enhanced_count/10)*100:.0f}%)")
        
        # Validate production standards
        print(f"\n✅ PRODUCTION STANDARDS VALIDATION:")
        print("=" * 50)
        
        checks = []
        checks.append(("10 queries processed", result.actualQueriesProcessed == 10))
        checks.append(("Hyperniche distribution", len([qr for qr in result.query_results if qr.dimension.startswith("UNBRANDED")]) >= 7))
        checks.append(("Web search enhancement", web_enhanced_count >= 8))  # At least 80%
        checks.append(("Real API responses", all(qr.response_text for qr in result.query_results)))
        checks.append(("Quality scoring", result.quality_score > 0 or result.mentions == 0))
        checks.append(("Execution under 3 minutes", actual_time < 180))
        
        for check_name, passed in checks:
            status = "✅" if passed else "❌"
            print(f"   {status} {check_name}")
        
        all_passed = all(passed for _, passed in checks)
        
        if all_passed:
            print(f"\n🎉 ALL PRODUCTION STANDARDS PASSED!")
            print(f"✅ Ready for openanalytics deployment")
            print(f"✅ Ready for aeo-leaderboard sync")
            print(f"✅ Ready for production use")
        else:
            print(f"\n⚠️  Some production standards need attention")
        
        return all_passed
        
    except Exception as e:
        print(f"\n❌ PRODUCTION TEST FAILED: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_final_10_queries())
    if success:
        print(f"\n🚀 READY FOR PRODUCTION DEPLOYMENT!")
    else:
        print(f"\n💥 PRODUCTION TEST FAILED - NEEDS FIXES")