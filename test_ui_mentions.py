#!/usr/bin/env python3
"""
UI Test Helper for Mentions Check with Live Logging
Provides easy testing interface with detailed output
"""

import json
import asyncio
import httpx
from datetime import datetime

def print_header():
    print("🎯 AEO MENTIONS UI TEST HELPER")
    print("=" * 50)
    print(f"⏰ Started: {datetime.now().strftime('%H:%M:%S')}")
    print()

async def test_mentions_endpoint():
    """Test the mentions endpoint with live feedback"""
    
    # Test payload with all 10-query generation data
    payload = {
        "companyName": "SCAILE",
        "companyAnalysis": {
            "companyInfo": {
                "products": [
                    "AI content generation platform",
                    "Marketing automation tools",
                    "SEO optimization software"
                ],
                "services": [
                    "Content creation services",
                    "Marketing strategy consulting",
                    "SEO optimization"
                ],
                "industry": "AI/Marketing Technology",
                "productCategory": "AI Marketing Tools",
                "description": "SCAILE is an advanced AI-powered marketing automation platform.",
                "pain_points": [
                    "content creation efficiency",
                    "marketing automation complexity"
                ],
                "geographic_modifiers": [
                    "German",
                    "European",
                    "DACH region"
                ],
                "use_cases": [
                    "automated blog generation",
                    "social media content automation"
                ]
            },
            "competitors": [
                {"name": "Jasper", "description": "AI writing assistant"},
                {"name": "Copy.ai", "description": "AI copywriting tool"}
            ]
        },
        "mode": "fast",
        "numQueries": 10,
        "language": "english",
        "country": "DE"
    }
    
    print("📋 Test Configuration:")
    print(f"   🏢 Company: {payload['companyName']}")
    print(f"   🎯 Mode: {payload['mode']}")
    print(f"   🔢 Expected Queries: 10")
    print(f"   🌍 Country: {payload['country']}")
    print()
    
    try:
        print("📡 Sending request to mentions endpoint...")
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "http://localhost:8000/mentions/check",
                json=payload
            )
            
        print(f"📊 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            
            print("✅ SUCCESS - Mentions check completed!")
            print("=" * 50)
            print(f"🏢 Company: {result.get('companyName')}")
            print(f"👁️  Visibility: {result.get('visibility', 0):.1f}%")
            print(f"🏆 Band: {result.get('band', 'Unknown')}")
            print(f"📈 Total Mentions: {result.get('mentions', 0)}")
            print(f"📊 Presence Rate: {result.get('presence_rate', 0):.1f}%")
            
            # Show query results if available
            if 'query_results' in result:
                queries = result['query_results']
                print(f"\n🔍 QUERY RESULTS ({len(queries)} queries):")
                print("-" * 50)
                
                for i, q in enumerate(queries, 1):
                    query_text = q.get('query', 'Unknown')
                    dimension = q.get('dimension', 'Unknown')
                    platform = q.get('platform', 'Unknown')
                    mentions = q.get('capped_mentions', 0)
                    
                    print(f"{i:2d}. {query_text}")
                    print(f"    📋 {dimension} | 🤖 {platform} | 📊 {mentions} mentions")
                
                # Verify 10 queries generated
                if len(queries) == 10:
                    print(f"\n✅ VERIFIED: All 10 queries generated and processed!")
                else:
                    print(f"\n⚠️  NOTICE: {len(queries)} queries processed (expected 10)")
            
            return True
            
        else:
            print(f"❌ Request failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except httpx.ConnectError:
        print("❌ Cannot connect to service. Is it running on localhost:8000?")
        print("💡 Start service with: ./start_ui_test.sh")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

async def check_service_health():
    """Check if the service is running and healthy"""
    print("🔍 Checking service health...")
    
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            # Check main service
            response = await client.get("http://localhost:8000/")
            if response.status_code == 200:
                print("✅ AEO Service: Running")
                return True
            else:
                print(f"⚠️  AEO Service: {response.status_code}")
                return False
    except:
        print("❌ AEO Service: Not running")
        return False

async def main():
    print_header()
    
    # Check service health first
    if not await check_service_health():
        print("\n💡 To start the service with full logging:")
        print("   ./start_ui_test.sh")
        return
    
    print("\n🎯 Running mentions endpoint test...")
    print("=" * 50)
    
    success = await test_mentions_endpoint()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 UI TEST COMPLETED SUCCESSFULLY!")
        print("📊 All 10 queries were generated and processed")
    else:
        print("💥 UI TEST FAILED")
        print("🔧 Check service logs for details")
    
    print(f"⏰ Finished: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    asyncio.run(main())
