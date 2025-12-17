"""
Modal Deployment Configuration for Master AEO Service
Combines health check and mentions functionality with advanced business intelligence.
"""

import modal
import os
from pathlib import Path

# Create Modal app
app = modal.App("master-aeo-service")

# Create image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .pip_install_from_requirements("master_requirements.txt")
    .apt_install("chromium", "chromium-driver")  # For Playwright
    .run_commands(
        "playwright install chromium",
        "playwright install-deps chromium"
    )
    .copy_local_file("master_aeo_service.py", "/app/master_aeo_service.py")
    .copy_local_file("fetcher.py", "/app/fetcher.py")
    .copy_local_file("ai_client.py", "/app/ai_client.py")
    .copy_local_dir("checks/", "/app/checks/")
    .copy_local_file("scoring.py", "/app/scoring.py")
    .workdir("/app")
)

# Mount secrets
secrets = [
    modal.Secret.from_name("openai-secret"),  # For logo detection
    modal.Secret.from_name("openrouter-secret"),  # For AI platform access
]

# Optional: Add Gemini native support if available
try:
    secrets.append(modal.Secret.from_name("gemini-secret"))
except:
    pass  # Gemini secret optional, will fallback to OpenRouter

@app.function(
    image=image,
    secrets=secrets,
    timeout=1800,  # 30 minutes for comprehensive analysis
    container_idle_timeout=300,  # 5 minutes idle timeout
    allow_concurrent_inputs=10,
)
@modal.asgi_app()
def fastapi_app():
    """Deploy Master AEO Service as Modal ASGI app."""
    from master_aeo_service import app
    return app

@app.function(
    image=image,
    secrets=secrets,
    timeout=600,  # 10 minutes for health check only
)
async def health_check_only(url: str, include_performance: bool = True, include_accessibility: bool = True):
    """Standalone health check function for direct invocation."""
    from master_aeo_service import health_check, HealthCheckRequest
    
    request = HealthCheckRequest(
        url=url,
        include_performance=include_performance,
        include_accessibility=include_accessibility
    )
    
    return await health_check(request)

@app.function(
    image=image,
    secrets=secrets,
    timeout=900,  # 15 minutes for mentions check
)
async def mentions_check_only(
    company_name: str,
    company_analysis: dict,
    language: str = "english",
    country: str = "US", 
    num_queries: int = 20,
    mode: str = "balanced"
):
    """Standalone mentions check function for direct invocation."""
    from master_aeo_service import mentions_check_advanced, MentionsCheckRequest, CompanyAnalysis
    
    # Convert dict to Pydantic model
    company_analysis_obj = CompanyAnalysis.parse_obj(company_analysis)
    
    request = MentionsCheckRequest(
        companyName=company_name,
        companyAnalysis=company_analysis_obj,
        language=language,
        country=country,
        numQueries=num_queries,
        mode=mode,
        generateInsights=True
    )
    
    return await mentions_check_advanced(request)

@app.function(
    image=image,
    secrets=secrets,
    timeout=1800,  # 30 minutes for complete analysis
)
async def master_analysis_only(
    url: str,
    company_name: str,
    company_analysis: dict,
    language: str = "english",
    country: str = "US",
    num_queries: int = 20,
    mode: str = "balanced"
):
    """Standalone master analysis function for direct invocation."""
    from master_aeo_service import master_analysis, MasterAnalysisRequest, CompanyAnalysis
    
    # Convert dict to Pydantic model  
    company_analysis_obj = CompanyAnalysis.parse_obj(company_analysis)
    
    request = MasterAnalysisRequest(
        url=url,
        companyName=company_name,
        companyAnalysis=company_analysis_obj,
        language=language,
        country=country,
        numQueries=num_queries,
        mode=mode,
        generateInsights=True
    )
    
    return await master_analysis(request)

@app.local_entrypoint()
def test_master_service():
    """Test the master service locally."""
    # Test health check
    print("Testing health check...")
    health_result = health_check_only.remote(
        url="https://scaile.tech",
        include_performance=True,
        include_accessibility=True
    )
    print(f"Health check result: {health_result['overall_score']}/100 ({health_result['grade']})")
    
    # Test mentions check (with minimal company analysis)
    print("Testing mentions check...")
    test_company_analysis = {
        "companyInfo": {
            "name": "SCAILE",
            "website": "https://scaile.tech",
            "description": "AEO consulting and optimization services",
            "industry": "SaaS",
            "products": ["AEO Consulting", "Answer Engine Optimization"],
            "services": ["AEO Strategy", "Content Optimization"],
            "target_audience": "B2B SaaS companies and marketing teams"
        },
        "competitors": [
            {"name": "BrightEdge", "website": "https://brightedge.com"},
            {"name": "Conductor", "website": "https://conductor.com"}
        ]
    }
    
    mentions_result = mentions_check_only.remote(
        company_name="SCAILE",
        company_analysis=test_company_analysis,
        language="english",
        country="US",
        num_queries=10,
        mode="fast"
    )
    print(f"Mentions check result: {mentions_result['visibility']:.1f}% ({mentions_result['band']})")
    
    print("Master service tests completed successfully!")

if __name__ == "__main__":
    # Deploy to Modal
    print("Deploying Master AEO Service to Modal...")
    with app.run():
        print("✅ Master AEO Service deployed successfully!")
        print("🔗 Endpoint: https://clients--master-aeo-service-fastapi-app.modal.run")
        print("📋 Available endpoints:")
        print("  - POST /health/check - Advanced health check")
        print("  - POST /mentions/check - Sophisticated mentions analysis") 
        print("  - POST /analyze/master - Complete combined analysis")
        print("  - GET /health - Service health status")
        print("  - GET /status - Detailed service status")