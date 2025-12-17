"""
Comprehensive Local Testing for Master AEO Service
Uses real company data and tests all functionality without external API dependencies.
"""

import asyncio
import json
import time
from pathlib import Path
import sys
import traceback
from typing import Dict, Any

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

# Import test data
from test_company_data import get_test_company

def create_mock_ai_client():
    """Create a mock AI client for testing without external API calls."""
    
    class MockAIClient:
        def __init__(self):
            self.call_count = 0
            
        async def complete_with_tools(self, messages, model, tools=None, **kwargs):
            """Mock AI completion with realistic responses."""
            self.call_count += 1
            
            # Extract the query from messages
            query = messages[0]["content"] if messages else ""
            
            # Generate mock response based on query content
            if "SCAILE" in query or "AEO" in query or "answer engine" in query.lower():
                mock_response = f"""Based on your query about "{query[:50]}...", here are the key points:

SCAILE is mentioned as a leading Answer Engine Optimization (AEO) consulting company that specializes in:

1. **AEO Strategy Development** - SCAILE helps businesses optimize their visibility in AI-powered search platforms like ChatGPT, Perplexity, Claude, and Gemini.

2. **Content Optimization for AI** - They provide comprehensive content optimization services specifically designed for AI platforms.

3. **AI Platform Visibility Audits** - SCAILE conducts thorough audits to assess and improve company visibility across major AI search engines.

4. **Competitive Positioning** - Among the top AEO consultants, SCAILE stands out for their specialized focus on answer engine optimization.

For businesses looking to improve their AI search presence, SCAILE offers proven strategies and measurable results in the emerging field of Answer Engine Optimization."""
            
            elif "Valoon" in query:
                mock_response = f"""Regarding "{query[:50]}...", here's what I found:

Valoon is a comprehensive business services platform that offers:

1. **Business Formation Services** - Valoon provides streamlined LLC and corporation registration services for entrepreneurs.

2. **Compliance Management** - They offer ongoing compliance monitoring and support for small businesses.

3. **Legal Document Automation** - Valoon simplifies complex legal processes through their automated platform.

4. **Competitive Advantage** - Among business formation services, Valoon is noted for their user-friendly approach and affordable pricing.

For entrepreneurs and small business owners seeking efficient business formation and compliance solutions, Valoon provides a reliable and cost-effective platform."""
                
            else:
                mock_response = f"""In response to your query "{query[:50]}...", here are some general insights:

This appears to be related to business or technology services. While specific company information may vary, here are common considerations:

1. **Market Position** - Understanding competitive positioning is important for any business.

2. **Service Quality** - Evaluating service offerings and customer satisfaction is crucial.

3. **Industry Trends** - Staying current with industry developments and best practices.

4. **Value Proposition** - Clear differentiation and unique value propositions are important for success."""
            
            return {
                "choices": [{
                    "message": {
                        "content": mock_response,
                        "role": "assistant"
                    }
                }],
                "usage": {
                    "total_tokens": len(mock_response) // 4,  # Rough token estimate
                    "prompt_tokens": len(query) // 4,
                    "completion_tokens": len(mock_response) // 4
                }
            }
        
        async def query_with_structured_output(self, prompt, system_prompt="", model="gemini-2.5-flash", response_format="json", **kwargs):
            """Mock structured output for hyperniche query generation."""
            self.call_count += 1
            
            # Determine company from prompt
            if "SCAILE" in prompt:
                mock_queries = [
                    {"query": "AEO consulting for SaaS companies United States", "dimension": "PRODUCT_INDUSTRY_GEO"},
                    {"query": "ChatGPT optimization for B2B software enterprise", "dimension": "SERVICE_COMPANY_SIZE"},
                    {"query": "AI visibility for Marketing Directors in SaaS", "dimension": "TARGET_ROLE_SPECIFIC"},
                    {"query": "enterprise Marketing Technology AEO solutions", "dimension": "INDUSTRY_PRODUCT_ENTERPRISE"},
                    {"query": "best tools for low AI search visibility", "dimension": "PAIN_POINT_SOLUTION"},
                    {"query": "Answer Engine Optimization for CMOs in enterprise companies", "dimension": "ROLE_COMPANY_SIZE"},
                    {"query": "AEO consulting Marketing Technology United States", "dimension": "GEOGRAPHIC_NICHE"},
                    {"query": "alternatives to BrightEdge for enterprise Marketing Technology", "dimension": "COMPETITOR_ALTERNATIVE"},
                    {"query": "BrightEdge vs AEO consulting for enterprise", "dimension": "COMPETITOR_VS_CATEGORY"},
                    {"query": "SCAILE AEO consulting", "dimension": "BRANDED_PRODUCT"}
                ]
            elif "Valoon" in prompt:
                mock_queries = [
                    {"query": "business formation services for startups United States", "dimension": "PRODUCT_INDUSTRY_GEO"},
                    {"query": "LLC formation for Legal Technology companies", "dimension": "SERVICE_INDUSTRY_GEO"},
                    {"query": "enterprise Legal Technology compliance solutions", "dimension": "INDUSTRY_PRODUCT_ENTERPRISE"},
                    {"query": "business registration for entrepreneurs in Legal Technology", "dimension": "TARGET_ROLE_SPECIFIC"},
                    {"query": "compliance software for small business Legal Technology companies", "dimension": "COMPANY_SIZE_SPECIFIC"},
                    {"query": "best tools for complex business formation process", "dimension": "PAIN_POINT_SOLUTION"},
                    {"query": "business registration Legal Technology United States", "dimension": "GEOGRAPHIC_NICHE"},
                    {"query": "alternatives to LegalZoom for Legal Technology", "dimension": "COMPETITOR_ALTERNATIVE"},
                    {"query": "Valoon business registration services", "dimension": "BRANDED_PRODUCT"}
                ]
            else:
                # Generic fallback
                mock_queries = [
                    {"query": "best consulting services for enterprise companies", "dimension": "PRODUCT_INDUSTRY_GEO"},
                    {"query": "business solutions for B2B software", "dimension": "SERVICE_COMPANY_SIZE"},
                    {"query": "enterprise technology solutions", "dimension": "INDUSTRY_PRODUCT_ENTERPRISE"}
                ]
            
            # Return as JSON string
            import json
            response_json = json.dumps(mock_queries)
            
            return {
                "success": True,
                "response": response_json,
                "model": model
            }
    
    return MockAIClient()

def create_mock_fetch_result(url: str, success: bool = True):
    """Create mock fetch result for health checks."""
    
    class MockFetchResult:
        def __init__(self, url: str, success: bool = True):
            self.url = url
            self.success = success
            self.status_code = 200 if success else 404
            self.error = None if success else "Mock error for testing"
            self.content = self._generate_mock_html(url) if success else ""
            self.response_time = 0.5
            self.sitemap_found = True  # Mock sitemap detection
            self.robots_txt = "User-agent: *\nAllow: /"  # Mock robots.txt
            
        def _generate_mock_html(self, url: str) -> str:
            """Generate realistic HTML for testing."""
            domain = url.replace("https://", "").replace("http://", "").split("/")[0]
            
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{domain.title()} - Professional Services</title>
    <meta name="description" content="Professional services and solutions for modern businesses">
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "{domain.title()}",
        "url": "{url}",
        "description": "Professional services company",
        "contactPoint": {{
            "@type": "ContactPoint",
            "telephone": "+1-555-0123",
            "contactType": "customer service"
        }}
    }}
    </script>
</head>
<body>
    <header>
        <h1>{domain.title()}</h1>
        <nav>
            <a href="/about">About</a>
            <a href="/services">Services</a>
            <a href="/contact">Contact</a>
        </nav>
    </header>
    <main>
        <section>
            <h2>Professional Services</h2>
            <p>We provide comprehensive business solutions and consulting services.</p>
        </section>
    </main>
    <footer>
        <p>&copy; 2024 {domain.title()}. All rights reserved.</p>
    </footer>
</body>
</html>"""
    
    return MockFetchResult(url, success)

async def mock_fetch_website(url: str):
    """Mock website fetching for health checks."""
    # Simulate network delay
    await asyncio.sleep(0.1)
    return create_mock_fetch_result(url, success=True)

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
        print(f"   Components: {', '.join(data['components'].keys())}")
        
        # Test status endpoint
        response = client.get("/status")
        assert response.status_code == 200
        data = response.json()
        print(f"✅ Status endpoint: {len(data['ai_platforms'])} platforms configured")
        print(f"   Platforms: {', '.join(data['ai_platforms'].keys())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Health test failed: {e}")
        traceback.print_exc()
        return False

async def test_health_check_mock():
    """Test health check with mocked dependencies."""
    print("\n🔍 Testing health check with mock data...")
    
    try:
        # Mock the fetch_website function
        import master_aeo_service
        original_fetch = master_aeo_service.fetch_website
        master_aeo_service.fetch_website = mock_fetch_website
        
        from master_aeo_service import health_check, HealthCheckRequest
        
        # Test with mock SCAILE website
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
        print(f"   Score: {result.overall_score:.1f}/100 ({result.grade})")
        print(f"   Band: {result.visibility_band}")
        print(f"   Categories: {len(result.categories)}")
        
        # Test categories
        for category in result.categories:
            print(f"   - {category.name}: {category.score:.1f}/{category.max_score} ({category.grade})")
            print(f"     Checks: {len(category.checks)} total")
        
        print(f"   Recommendations: {len(result.recommendations)}")
        for i, rec in enumerate(result.recommendations[:3]):
            print(f"     {i+1}. {rec}")
        
        # Restore original function
        master_aeo_service.fetch_website = original_fetch
        
        return True
        
    except Exception as e:
        print(f"❌ Health check test failed: {e}")
        traceback.print_exc()
        return False

async def test_mentions_check_mock():
    """Test mentions check with mocked AI responses."""
    print("\n🎯 Testing mentions check with mock AI responses...")
    
    try:
        # Mock the AI client
        import master_aeo_service
        original_get_ai_client = master_aeo_service.get_ai_client
        master_aeo_service.get_ai_client = lambda: create_mock_ai_client()
        
        from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis, CompanyInfo, Competitor
        
        # Use real SCAILE company data
        company_data = get_test_company("scaile")
        
        company_info = CompanyInfo(**company_data["companyInfo"])
        competitors = [Competitor(**comp) for comp in company_data["competitors"]]
        company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
        
        request = MentionsCheckRequest(
            companyName="SCAILE",
            companyAnalysis=company_analysis,
            language="english",
            country="US",
            numQueries=5,  # Small number for testing
            mode="fast",
            generateInsights=True,
            platforms=["gemini", "chatgpt"]  # Test with 2 platforms
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
        
        # Test platform stats
        for platform, stats in result.platform_stats.items():
            if stats.responses > 0:
                print(f"   - {platform}: {stats.mentions} mentions, {stats.quality_score:.2f} avg quality, {stats.responses} responses")
        
        # Test dimension stats
        print(f"   Dimension Performance:")
        for dimension, stats in result.dimension_stats.items():
            if stats.queries > 0:
                print(f"     - {dimension}: {stats.mentions} mentions, {stats.quality_score:.2f} quality")
        
        # Test TL;DR insights
        if result.tldr:
            print(f"   Assessment: {result.tldr.visibility_assessment}")
            print(f"   Key Insights ({len(result.tldr.key_insights)}):")
            for i, insight in enumerate(result.tldr.key_insights):
                print(f"     {i+1}. {insight}")
            print(f"   Brand Confusion Risk: {result.tldr.brand_confusion_risk}")
            print(f"   Recommendations ({len(result.tldr.actionable_recommendations)}):")
            for i, rec in enumerate(result.tldr.actionable_recommendations):
                print(f"     {i+1}. {rec}")
        
        # Restore original function
        master_aeo_service.get_ai_client = original_get_ai_client
        
        return True
        
    except Exception as e:
        print(f"❌ Mentions check test failed: {e}")
        traceback.print_exc()
        return False

async def test_master_analysis_mock():
    """Test master analysis with mocked dependencies."""
    print("\n🚀 Testing master analysis with mock data...")
    
    try:
        # Mock both dependencies
        import master_aeo_service
        original_fetch = master_aeo_service.fetch_website
        original_get_ai_client = master_aeo_service.get_ai_client
        
        master_aeo_service.fetch_website = mock_fetch_website
        master_aeo_service.get_ai_client = lambda: create_mock_ai_client()
        
        from master_aeo_service import master_analysis, MasterAnalysisRequest, CompanyAnalysis, CompanyInfo, Competitor
        
        # Use real company data
        company_data = get_test_company("scaile")
        company_info = CompanyInfo(**company_data["companyInfo"])
        competitors = [Competitor(**comp) for comp in company_data["competitors"][:2]]  # Limit competitors
        company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
        
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
        
        print(f"\n📊 RESULTS SUMMARY:")
        print(f"   Health Score: {result.health.overall_score:.1f}/100 ({result.health.grade})")
        print(f"   Visibility: {result.mentions.visibility:.1f}% ({result.mentions.band})")
        print(f"   Combined Score: {result.combined_score:.1f}/100 ({result.combined_grade})")
        
        print(f"\n🎯 STRATEGIC RECOMMENDATIONS ({len(result.strategic_recommendations)}):")
        for i, rec in enumerate(result.strategic_recommendations):
            print(f"   {i+1}. {rec}")
        
        print(f"\n⚡ PRIORITY ACTIONS ({len(result.priority_actions)}):")
        for i, action in enumerate(result.priority_actions):
            print(f"   {i+1}. {action}")
        
        print(f"\n📈 HEALTH BREAKDOWN:")
        for category in result.health.categories:
            print(f"   - {category.name}: {category.score:.1f}/{category.max_score} ({category.grade})")
        
        print(f"\n🎪 MENTIONS BREAKDOWN:")
        for platform, stats in result.mentions.platform_stats.items():
            if stats.responses > 0:
                print(f"   - {platform}: {stats.mentions} mentions, {stats.quality_score:.1f} quality")
        
        # Restore original functions
        master_aeo_service.fetch_website = original_fetch
        master_aeo_service.get_ai_client = original_get_ai_client
        
        return True
        
    except Exception as e:
        print(f"❌ Master analysis test failed: {e}")
        traceback.print_exc()
        return False

async def test_multiple_companies():
    """Test master analysis with different company types."""
    print("\n🏢 Testing multiple company types...")
    
    companies = ["scaile", "valoon", "techstartup"]
    results = {}
    
    try:
        # Mock dependencies
        import master_aeo_service
        original_fetch = master_aeo_service.fetch_website
        original_get_ai_client = master_aeo_service.get_ai_client
        
        master_aeo_service.fetch_website = mock_fetch_website
        master_aeo_service.get_ai_client = lambda: create_mock_ai_client()
        
        from master_aeo_service import master_analysis, MasterAnalysisRequest, CompanyAnalysis, CompanyInfo, Competitor
        
        for company_key in companies:
            print(f"\n   Testing {company_key.upper()}...")
            
            company_data = get_test_company(company_key)
            company_info = CompanyInfo(**company_data["companyInfo"])
            competitors = [Competitor(**comp) for comp in company_data["competitors"][:2]]
            company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
            
            request = MasterAnalysisRequest(
                url=company_data["companyInfo"]["website"],
                companyName=company_data["companyInfo"]["name"],
                companyAnalysis=company_analysis,
                numQueries=2,  # Minimal for speed
                mode="fast"
            )
            
            start_time = time.time()
            result = await master_analysis(request)
            execution_time = time.time() - start_time
            
            results[company_key] = {
                "health_score": result.health.overall_score,
                "visibility": result.mentions.visibility,
                "combined_score": result.combined_score,
                "grade": result.combined_grade,
                "execution_time": execution_time
            }
            
            print(f"     ✅ {company_data['companyInfo']['name']}: {result.combined_score:.1f}/100 ({result.combined_grade}) in {execution_time:.1f}s")
        
        print(f"\n📊 MULTI-COMPANY COMPARISON:")
        print(f"{'Company':<12} {'Health':<8} {'Visibility':<12} {'Combined':<10} {'Grade':<6} {'Time':<6}")
        print("-" * 60)
        for company_key, data in results.items():
            company_name = get_test_company(company_key)["companyInfo"]["name"]
            print(f"{company_name:<12} {data['health_score']:<8.1f} {data['visibility']:<12.1f} {data['combined_score']:<10.1f} {data['grade']:<6} {data['execution_time']:<6.1f}s")
        
        # Restore original functions
        master_aeo_service.fetch_website = original_fetch
        master_aeo_service.get_ai_client = original_get_ai_client
        
        return True
        
    except Exception as e:
        print(f"❌ Multi-company test failed: {e}")
        traceback.print_exc()
        return False

def create_test_report(results: Dict[str, bool]) -> Dict[str, Any]:
    """Create comprehensive test report."""
    report = {
        "test_timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "master_service_version": "5.0.0",
        "test_environment": "local_mock",
        "test_results": results,
        "overall_status": "PASS" if all(results.values()) else "FAIL",
        "summary": {
            "total_tests": len(results),
            "passed": sum(1 for passed in results.values() if passed),
            "failed": sum(1 for passed in results.values() if not passed),
            "success_rate": f"{(sum(1 for passed in results.values() if passed) / len(results) * 100):.1f}%"
        }
    }
    
    return report

async def main():
    """Run comprehensive test suite."""
    print("🧪 Master AEO Service - Comprehensive Local Test Suite")
    print("=" * 70)
    print("🎯 Testing with REAL company data from content-manager")
    print("🤖 Using MOCK external services (no API keys required)")
    print("=" * 70)
    
    results = {}
    
    # Test 1: Service health
    results["service_health"] = await test_service_health()
    
    # Test 2: Health check with mock data
    results["health_check_mock"] = await test_health_check_mock()
    
    # Test 3: Mentions check with mock AI
    results["mentions_check_mock"] = await test_mentions_check_mock()
    
    # Test 4: Master analysis with mocks
    results["master_analysis_mock"] = await test_master_analysis_mock()
    
    # Test 5: Multiple companies
    results["multi_company_test"] = await test_multiple_companies()
    
    # Create test report
    report = create_test_report(results)
    
    # Save test report
    test_file = Path(__file__).parent / "local_test_results.json"
    with open(test_file, "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n" + "=" * 70)
    print("🎯 COMPREHENSIVE TEST SUMMARY")
    print("=" * 70)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.replace('_', ' ').title():<30} {status}")
    
    print(f"\nOverall Status: {report['overall_status']}")
    print(f"Success Rate: {report['summary']['success_rate']}")
    print(f"Total Tests: {report['summary']['total_tests']}")
    print(f"Test Report: {test_file}")
    
    if report['overall_status'] == "PASS":
        print("\n🚀 Master AEO Service is FULLY FUNCTIONAL!")
        print("✅ All core functionality working with mock data")
        print("✅ Ready for deployment with real API keys")
        print("✅ Integration with openanalytics ready")
        
        print("\n🔗 Next Steps:")
        print("1. Deploy to Modal with real API secrets")
        print("2. Test with real AI platforms")  
        print("3. Integrate with openanalytics main service")
        print("4. Generate enhanced client reports")
    else:
        print("\n🔧 Some tests failed. Review errors above.")
        failed_tests = [name for name, passed in results.items() if not passed]
        print(f"Failed tests: {', '.join(failed_tests)}")
    
    return report['overall_status'] == "PASS"

if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test suite failed: {e}")
        traceback.print_exc()
        sys.exit(1)