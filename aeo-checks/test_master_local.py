"""
Local Test Script for Master AEO Service
Tests all endpoints before deployment to ensure functionality.
"""

import asyncio
import json
import time
from pathlib import Path
import sys
import os

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

async def test_service_health():
    """Test basic service health endpoints."""
    print("🏥 Testing service health endpoints...")
    
    try:
        from master_aeo_service import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test root endpoint
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        print(f"✅ Root endpoint: {data['service']} v{data['version']}")
        
        # Test health endpoint
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        print(f"✅ Health endpoint: {data['status']}")
        
        # Test status endpoint
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        print(f"✅ Status endpoint: {len(data['ai_platforms'])} platforms available")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        return False

async def test_health_check():
    """Test health check endpoint with a real website."""
    print("\n🔍 Testing health check functionality...")
    
    try:
        from master_aeo_service import health_check, HealthCheckRequest
        
        # Test with SCAILE website
        request = HealthCheckRequest(
            url="https://scaile.tech",
            include_performance=True,
            include_accessibility=True
        )
        
        start_time = time.time()
        result = await health_check(request)
        execution_time = time.time() - start_time
        
        print(f"✅ Health check completed in {execution_time:.2f}s")
        print(f"   URL: {result.url}")
        print(f"   Score: {result.overall_score}/100 ({result.grade})")
        print(f"   Band: {result.visibility_band}")
        print(f"   Categories: {len(result.categories)}")
        print(f"   Recommendations: {len(result.recommendations)}")
        
        # Test categories
        for category in result.categories:
            print(f"   - {category.name}: {category.score:.1f}/{category.max_score} ({category.grade})")
        
        return True
        
    except Exception as e:
        print(f"❌ Health check test failed: {e}")
        return False

async def test_mentions_check():
    """Test mentions check with sample company data."""
    print("\n🎯 Testing mentions check functionality...")
    
    try:
        from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis, CompanyInfo, Competitor
        
        # Create test company analysis
        company_info = CompanyInfo(
            name="SCAILE",
            website="https://scaile.tech",
            description="Answer Engine Optimization consulting and services",
            industry="Marketing Technology",
            productCategory="AEO Software",
            products=["AEO Consulting", "Answer Engine Optimization", "AI Search Optimization"],
            services=["AEO Strategy", "Content Optimization", "AI Visibility Consulting"],
            pain_points=["Low AI search visibility", "Poor AI platform mentions"],
            target_audience="B2B SaaS companies and marketing teams",
            country="US"
        )
        
        competitors = [
            Competitor(name="BrightEdge", website="https://brightedge.com"),
            Competitor(name="Conductor", website="https://conductor.com"),
            Competitor(name="Searchmetrics", website="https://searchmetrics.com")
        ]
        
        company_analysis = CompanyAnalysis(
            companyInfo=company_info,
            competitors=competitors
        )
        
        request = MentionsCheckRequest(
            companyName="SCAILE",
            companyAnalysis=company_analysis,
            language="english",
            country="US",
            numQueries=5,  # Small number for testing
            mode="fast",
            generateInsights=True,
            platforms=["gemini"]  # Test with just one platform for speed
        )
        
        start_time = time.time()
        result = await mentions_check_advanced(request)
        execution_time = time.time() - start_time
        
        print(f"✅ Mentions check completed in {execution_time:.2f}s")
        print(f"   Company: {result.companyName}")
        print(f"   Visibility: {result.visibility:.1f}% ({result.band})")
        print(f"   Mentions: {result.mentions}")
        print(f"   Presence Rate: {result.presence_rate:.1f}%")
        print(f"   Quality Score: {result.quality_score:.2f}/10")
        print(f"   Queries Processed: {result.actualQueriesProcessed}")
        print(f"   Total Cost: ${result.total_cost:.4f}")
        
        # Test TL;DR
        if result.tldr:
            print(f"   Assessment: {result.tldr.visibility_assessment}")
            print(f"   Key Insights: {len(result.tldr.key_insights)}")
            print(f"   Recommendations: {len(result.tldr.actionable_recommendations)}")
        
        # Test platform stats
        for platform, stats in result.platform_stats.items():
            if stats.responses > 0:
                print(f"   - {platform}: {stats.mentions} mentions, {stats.quality_score:.2f} avg quality")
        
        return True
        
    except Exception as e:
        print(f"❌ Mentions check test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_master_analysis():
    """Test master analysis combining health + mentions."""
    print("\n🚀 Testing master analysis functionality...")
    
    try:
        from master_aeo_service import master_analysis, MasterAnalysisRequest, CompanyAnalysis, CompanyInfo, Competitor
        
        # Create test company analysis
        company_info = CompanyInfo(
            name="SCAILE",
            website="https://scaile.tech",
            description="Answer Engine Optimization consulting and services",
            industry="Marketing Technology",
            products=["AEO Consulting", "AI Search Optimization"],
            services=["AEO Strategy", "Content Optimization"],
            target_audience="B2B SaaS companies"
        )
        
        company_analysis = CompanyAnalysis(
            companyInfo=company_info,
            competitors=[Competitor(name="BrightEdge")]
        )
        
        request = MasterAnalysisRequest(
            url="https://scaile.tech",
            companyName="SCAILE",
            companyAnalysis=company_analysis,
            language="english",
            country="US",
            numQueries=3,  # Very small for testing
            mode="fast",
            generateInsights=True
        )
        
        start_time = time.time()
        result = await master_analysis(request)
        execution_time = time.time() - start_time
        
        print(f"✅ Master analysis completed in {execution_time:.2f}s")
        print(f"   URL: {result.url}")
        print(f"   Company: {result.companyName}")
        print(f"   Health Score: {result.health.overall_score:.1f}/100 ({result.health.grade})")
        print(f"   Visibility: {result.mentions.visibility:.1f}% ({result.mentions.band})")
        print(f"   Combined Score: {result.combined_score:.1f}/100 ({result.combined_grade})")
        print(f"   Strategic Recommendations: {len(result.strategic_recommendations)}")
        print(f"   Priority Actions: {len(result.priority_actions)}")
        
        # Print recommendations
        for i, rec in enumerate(result.strategic_recommendations[:3]):
            print(f"   Strategy {i+1}: {rec}")
        
        for i, action in enumerate(result.priority_actions[:3]):
            print(f"   Action {i+1}: {action}")
        
        return True
        
    except Exception as e:
        print(f"❌ Master analysis test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def create_test_report(results):
    """Create a test report and save to file."""
    report = {
        "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "test_results": {
            "service_health": results.get("health", False),
            "health_check": results.get("health_check", False), 
            "mentions_check": results.get("mentions_check", False),
            "master_analysis": results.get("master_analysis", False)
        },
        "overall_status": "PASS" if all(results.values()) else "FAIL"
    }
    
    # Save test report
    test_file = Path(__file__).parent / "test_master_results.json"
    with open(test_file, "w") as f:
        json.dump(report, f, indent=2)
    
    return report

async def main():
    """Run all tests in sequence."""
    print("🧪 Master AEO Service - Local Testing Suite")
    print("=" * 50)
    
    results = {}
    
    # Test service health
    results["health"] = await test_service_health()
    
    # Test health check
    results["health_check"] = await test_health_check()
    
    # Test mentions check
    results["mentions_check"] = await test_mentions_check()
    
    # Test master analysis
    results["master_analysis"] = await test_master_analysis()
    
    # Create test report
    report = create_test_report(results)
    
    print("\n" + "=" * 50)
    print("🎯 TEST SUMMARY")
    print("=" * 50)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title()}: {status}")
    
    print(f"\nOverall Status: {report['overall_status']}")
    print(f"Test Report: {Path(__file__).parent / 'test_master_results.json'}")
    
    if report['overall_status'] == "PASS":
        print("\n🚀 Master service is ready for deployment!")
        print("Next steps:")
        print("1. Run: modal deploy master_deploy.py") 
        print("2. Test deployed service")
        print("3. Integration with openanalytics")
    else:
        print("\n🔧 Some tests failed. Fix issues before deployment.")
    
    return report['overall_status'] == "PASS"

if __name__ == "__main__":
    # Set environment variables for testing
    os.environ.setdefault("OPENAI_API_KEY", "test-key")
    os.environ.setdefault("OPENROUTER_API_KEY", "test-key")
    
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)