#!/usr/bin/env python3
"""Test query generation to verify company context is properly used."""

import asyncio
from master_aeo_service import generate_advanced_queries, CompanyAnalysis, CompanyInfo, Competitor
from test_company_data import SCAILE_COMPANY_DATA

async def test_query_generation():
    """Test that queries are properly generated from SCAILE company context."""
    print("🧪 Testing Query Generation for SCAILE Company Context")
    print("=" * 60)
    
    # Create company analysis from SCAILE data
    company_info = CompanyInfo(**SCAILE_COMPANY_DATA["companyInfo"])
    competitors = [Competitor(**comp) for comp in SCAILE_COMPANY_DATA["competitors"]]
    company_analysis = CompanyAnalysis(companyInfo=company_info, competitors=competitors)
    
    print(f"📊 Company: {company_info.name}")
    print(f"📊 Industry: {company_info.industry}")
    print(f"📊 Products: {company_info.products}")
    print(f"📊 Services: {company_info.services}")
    print(f"📊 Competitors: {[c.name for c in competitors]}")
    print()
    
    # Generate queries
    queries = await generate_advanced_queries(
        company_name="SCAILE",
        company_analysis=company_analysis,
        num_queries=10,
        mode="fast",
        country="US",
        language="english"
    )
    
    print(f"🎯 Generated {len(queries)} Queries:")
    print("-" * 40)
    
    # Group by dimension
    dimensions = {}
    for query_data in queries:
        dimension = query_data["dimension"]
        query = query_data["query"]
        
        if dimension not in dimensions:
            dimensions[dimension] = []
        dimensions[dimension].append(query)
    
    for dimension, query_list in dimensions.items():
        print(f"\n📋 {dimension.upper()} ({len(query_list)} queries):")
        for i, query in enumerate(query_list, 1):
            print(f"   {i}. '{query}'")
    
    print("\n🔍 Context Usage Analysis:")
    print("-" * 30)
    
    # Check if company context is being used
    all_queries_text = " ".join([q["query"] for q in queries])
    
    context_usage = {
        "Company Name": "SCAILE" in all_queries_text,
        "Products Used": any(prod.lower() in all_queries_text.lower() for prod in (company_info.products or [])),
        "Services Used": any(svc.lower() in all_queries_text.lower() for svc in (company_info.services or [])),
        "Industry Used": company_info.industry.lower() in all_queries_text.lower() if company_info.industry else False,
        "Competitors Used": any(comp.name in all_queries_text for comp in competitors),
    }
    
    for check, result in context_usage.items():
        status = "✅" if result else "❌"
        print(f"{status} {check}: {result}")
    
    print(f"\n📈 Context Usage Score: {sum(context_usage.values())}/{len(context_usage)} ({sum(context_usage.values())/len(context_usage)*100:.0f}%)")
    
    return queries, context_usage

if __name__ == "__main__":
    asyncio.run(test_query_generation())