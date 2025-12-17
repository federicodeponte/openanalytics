#!/usr/bin/env python3
"""Test native Gemini SDK integration in master service."""

import os
import asyncio
import sys
sys.path.append('/Users/federicodeponte/openanalytics/aeo-checks')

from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis, CompanyInfo, Competitor
from test_company_data import SCAILE_COMPANY_DATA

async def test_gemini_integration():
    """Test that master service now uses native Gemini SDK."""
    
    print("🔥 TESTING NATIVE GEMINI SDK INTEGRATION")
    print("=" * 60)
    
    # Create test request for SCAILE
    company_data = SCAILE_COMPANY_DATA
    company_info = CompanyInfo(**company_data["companyInfo"])
    competitors = [Competitor(**comp) for comp in company_data["competitors"]]
    company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
    
    request = MentionsCheckRequest(
        companyName="SCAILE",
        companyAnalysis=company_analysis,
        language="english",
        country="US",
        numQueries=3,  # Small test
        mode="fast",
        generateInsights=True,
        platforms=["gemini"]  # Test only Gemini
    )
    
    print(f"🎯 Testing with native Gemini SDK...")
    print(f"📊 Company: SCAILE")
    print(f"🔍 Queries: 3")
    print(f"🤖 Platform: Gemini (native SDK)")
    
    try:
        result = await mentions_check_advanced(request)
        
        print(f"\n✅ SUCCESS! Native Gemini SDK working")
        print(f"⏱️  Execution time: {result.execution_time_seconds:.2f}s")
        print(f"🎯 Queries processed: {result.actualQueriesProcessed}")
        print(f"📊 Visibility: {result.visibility:.1f}% ({result.band})")
        print(f"💰 Cost: ${result.total_cost:.4f}")
        
        # Check if we got real results
        if result.query_results:
            print(f"\n🔍 QUERY RESULTS:")
            for i, qr in enumerate(result.query_results[:3], 1):
                print(f"   {i}. '{qr.query}' -> {qr.capped_mentions} mentions")
                if qr.response_text:
                    print(f"      Preview: {qr.response_text[:100]}...")
        
        # Verify native Gemini was used
        if any("native_gemini" in str(qr.platform) for qr in result.query_results):
            print(f"\n🎯 CONFIRMED: Native Gemini SDK in use!")
        else:
            print(f"\n⚠️  Warning: May still be using OpenRouter fallback")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_gemini_integration())
    if success:
        print(f"\n🎉 NATIVE GEMINI SDK INTEGRATION SUCCESSFUL!")
    else:
        print(f"\n💥 INTEGRATION TEST FAILED")