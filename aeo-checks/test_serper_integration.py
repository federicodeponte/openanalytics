#!/usr/bin/env python3
"""Test Serper API integration with Gemini client."""

import os
import asyncio
import sys
sys.path.append('/Users/federicodeponte/openanalytics/aeo-checks')

from gemini_client import get_gemini_client
from dotenv import load_dotenv

async def test_serper_integration():
    """Test that Serper API is working with Gemini client."""
    
    print("🔍 TESTING SERPER API INTEGRATION")
    print("=" * 50)
    
    # Load environment
    load_dotenv('.env.local')
    serper_key = os.getenv('SERPER_API_KEY')
    
    print(f"🔑 Serper API Key: {serper_key[:20]}..." if serper_key else "❌ No Serper key")
    
    # Test direct Serper search
    gemini_client = get_gemini_client()
    
    # Test search functionality
    test_query = "best AEO consulting for SaaS companies United States"
    
    print(f"\n🎯 Testing query: '{test_query}'")
    print(f"🔍 Should use Serper for web search enhancement...")
    
    try:
        # Test the search method directly
        print(f"\n1️⃣ Testing Serper search directly...")
        search_results = await gemini_client._serper_search(test_query)
        
        if search_results:
            print(f"✅ Serper search successful!")
            print(f"📄 Results length: {len(search_results)} chars")
            print(f"📖 Preview: {search_results[:200]}...")
        else:
            print(f"❌ No search results from Serper")
        
        # Test full completion with search
        print(f"\n2️⃣ Testing full completion with search...")
        response = await gemini_client._complete_with_search(test_query)
        
        if response and hasattr(response, 'text'):
            print(f"✅ Search-enhanced completion successful!")
            print(f"📄 Response length: {len(response.text)} chars")
            print(f"📖 Preview: {response.text[:200]}...")
            
            # Check if it contains web-sourced information
            web_indicators = ["according to", "based on", "sources", "research", "companies mentioned"]
            has_web_content = any(indicator in response.text.lower() for indicator in web_indicators)
            
            if has_web_content:
                print(f"🌐 Response contains web-sourced content!")
            else:
                print(f"⚠️  Response may not contain web search results")
        else:
            print(f"❌ Search-enhanced completion failed")
        
        # Test mentions query method
        print(f"\n3️⃣ Testing mentions query with search grounding...")
        result = await gemini_client.query_mentions_with_search_grounding(test_query, "SCAILE")
        
        if result.get("success"):
            print(f"✅ Mentions query with search successful!")
            print(f"📄 Response length: {len(result['response'])} chars")
            print(f"🔍 Search grounding: {result.get('search_grounding', False)}")
            
            # Check for company mentions
            response_text = result['response'].lower()
            scaile_mentioned = "scaile" in response_text
            competitors = ["brightedge", "conductor", "semrush", "moz"]
            competitors_mentioned = [comp for comp in competitors if comp in response_text]
            
            print(f"🎯 SCAILE mentioned: {'✅' if scaile_mentioned else '❌'}")
            print(f"🏢 Competitors found: {', '.join(competitors_mentioned) if competitors_mentioned else 'None'}")
            
        else:
            print(f"❌ Mentions query failed: {result.get('error', 'Unknown error')}")
        
        print(f"\n🎉 SERPER INTEGRATION TEST COMPLETE!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    success = asyncio.run(test_serper_integration())
    if success:
        print(f"\n🚀 SERPER + GEMINI INTEGRATION SUCCESS!")
    else:
        print(f"\n💥 INTEGRATION FAILED")