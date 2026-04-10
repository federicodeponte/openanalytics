"""
Floom wrapper for OpenAnalytics.

Exposes AEO health check and AI visibility analysis as Floom actions.
"""

import asyncio
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import List, Optional

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def health_check(url: str, _knowledge: dict = None) -> dict:
    """Run comprehensive AEO health check on a website (29 checks)."""
    print(f"Running AEO health check on: {url}")
    if _knowledge:
        logger.info("health_check() received %d knowledge docs", len(_knowledge))

    result = asyncio.run(_run_health_check(url))

    score = result.get("score", 0)
    grade = result.get("grade", "N/A")
    print(f"Health check complete: score={score}, grade={grade}")

    report = _build_health_report(result)

    return {
        "report": report,
        "score": score,
        "details": result,
    }


async def _run_health_check(url: str) -> dict:
    """Run health check using the fetcher and check modules."""
    start_time = time.time()

    from fetcher import fetch_website
    from scoring import calculate_tiered_score, calculate_grade, calculate_visibility_band
    from checks.technical import run_technical_checks
    from checks.structured_data import run_structured_data_checks
    from checks.aeo_crawler import run_aeo_crawler_checks
    from checks.authority import run_authority_checks

    fetch_result = await fetch_website(url)

    if fetch_result.error:
        return {
            "url": url,
            "score": 0,
            "grade": "F",
            "band": "Critical",
            "error": fetch_result.error,
            "checks_passed": 0,
            "checks_failed": 0,
            "issues": [],
            "execution_time": time.time() - start_time,
        }

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(fetch_result.html, 'html.parser')

    technical_results = run_technical_checks(
        soup, fetch_result.final_url, fetch_result.sitemap_found, fetch_result.html_response_time_ms
    )
    structured_results = run_structured_data_checks(soup)
    crawler_results = run_aeo_crawler_checks(fetch_result.robots_txt or "")
    authority_results = run_authority_checks(soup)

    all_results = technical_results + structured_results + crawler_results + authority_results

    final_score, tier_details = calculate_tiered_score(all_results)
    grade = calculate_grade(final_score)
    band, band_color = calculate_visibility_band(final_score)

    passed = sum(1 for r in all_results if r.get("passed") is True)
    failed = len(all_results) - passed

    return {
        "url": fetch_result.final_url,
        "score": final_score,
        "max_score": 100.0,
        "grade": grade,
        "band": band,
        "band_color": band_color,
        "checks_passed": passed,
        "checks_failed": failed,
        "issues": [r for r in all_results if r.get("passed") is not True],
        "tier_details": tier_details,
        "execution_time": round(time.time() - start_time, 2),
        "fetch_time_ms": fetch_result.html_response_time_ms,
    }


def _build_health_report(result: dict) -> str:
    """Build markdown health check report."""
    lines = []
    url = result.get("url", "Unknown")
    score = result.get("score", 0)
    grade = result.get("grade", "N/A")
    band = result.get("band", "Unknown")

    if result.get("error"):
        lines.append(f"# AEO Health Check: Failed")
        lines.append(f"**URL:** {url}")
        lines.append(f"**Error:** {result['error']}")
        return "\n".join(lines)

    lines.append(f"# AEO Health Check: {url}")
    lines.append("")
    lines.append(f"**Score:** {score}/100 | **Grade:** {grade} | **Band:** {band}")
    lines.append(f"**Checks Passed:** {result.get('checks_passed', 0)} | **Failed:** {result.get('checks_failed', 0)}")
    lines.append("")

    # Tier details
    tier_details = result.get("tier_details", {})
    if tier_details:
        lines.append("## Category Breakdown")
        for tier_name, tier_data in tier_details.items():
            if isinstance(tier_data, dict):
                earned = tier_data.get("earned", 0)
                maximum = tier_data.get("max", 0)
                lines.append(f"- **{tier_name}:** {earned}/{maximum}")
        lines.append("")

    # Issues
    issues = result.get("issues", [])
    if issues:
        lines.append("## Issues Found")
        for issue in issues:
            name = issue.get("check", issue.get("name", "Unknown"))
            detail = issue.get("detail", issue.get("message", ""))
            lines.append(f"- **{name}**: {detail}")
        lines.append("")

    lines.append(f"---\n*Execution time: {result.get('execution_time', 0)}s*")
    return "\n".join(lines)


def mentions_check(
    company_name: str,
    industry: str = "",
    products: str = "",
    target_audience: str = "",
    num_queries: int = 10,
    _knowledge: dict = None,
) -> dict:
    """Run AI visibility check with hyperniche query generation."""
    print(f"Running AI visibility check for: {company_name}")

    # Enrich inputs from knowledge docs if available
    if _knowledge:
        logger.info("mentions_check() received %d knowledge docs", len(_knowledge))
        for doc_name, doc_text in _knowledge.items():
            # Auto-fill industry/products from knowledge if not provided
            if not industry and "industry" in doc_text.lower()[:200]:
                logger.info("mentions_check() has knowledge context available for enrichment")

    # Parse products from textarea (one per line)
    products_list = [p.strip() for p in products.split("\n") if p.strip()] if products else None

    result = asyncio.run(_run_mentions_check(
        company_name=company_name,
        industry=industry if industry else None,
        products=products_list,
        target_audience=target_audience if target_audience else None,
        num_queries=int(num_queries),
    ))

    visibility = result.get("visibility", 0)
    print(f"Visibility check complete: {visibility}% visibility")

    report = _build_mentions_report(result)

    return {
        "report": report,
        "visibility_score": visibility,
        "details": result,
    }


async def _run_mentions_check(
    company_name: str,
    industry: Optional[str],
    products: Optional[List[str]],
    target_audience: Optional[str],
    num_queries: int,
) -> dict:
    """Run mentions check using Gemini with search grounding."""
    start_time = time.time()

    from gemini_client import get_gemini_client

    # Generate hyperniche queries
    products_str = ", ".join(products) if products else "N/A"
    prompt = f"""Generate {num_queries} hyperniche AEO visibility queries for {company_name}.

Company Data:
- Industry: {industry or 'N/A'}
- Products: {products_str}
- Target Audience: {target_audience or 'N/A'}

Query Distribution:
- 70% UNBRANDED (no mention of {company_name})
- 20% COMPETITIVE (alternatives, comparisons)
- 10% BRANDED ({company_name} + product)

Return as JSON array:
[{{"query": "actual query", "dimension": "UNBRANDED_HYPERNICHE"}}]"""

    client = get_gemini_client()

    try:
        response = await client.query_with_structured_output(
            prompt=prompt,
            system_prompt="You are a B2B hyperniche query generation expert.",
            model="gemini-3-flash-preview",
            response_format="json"
        )
        text = response.get("response", "[]").strip()
        if text.startswith("```json"):
            text = text[7:]
        if text.startswith("```"):
            text = text[3:]
        if text.endswith("```"):
            text = text[:-3]
        queries = json.loads(text.strip())[:num_queries]
    except Exception as e:
        print(f"AI query generation failed: {e}, using fallback")
        queries = [
            {"query": f"best {products[0] if products else 'solution'} for {industry or 'companies'}", "dimension": "Product-Industry"},
            {"query": f"{company_name} alternatives", "dimension": "Competitive"},
            {"query": f"{company_name}", "dimension": "Branded"},
        ][:num_queries]

    # Test queries with search grounding
    async def test_query(q):
        try:
            resp = await client.query_with_search_grounding(q["query"])
            if resp.get("success") and resp.get("response"):
                text = resp["response"]
                mentioned = company_name.lower() in text.lower()
                return {"query": q["query"], "dimension": q.get("dimension", ""), "mentioned": mentioned, "response_preview": text[:200]}
            return {"query": q["query"], "dimension": q.get("dimension", ""), "mentioned": False}
        except Exception:
            return {"query": q["query"], "dimension": q.get("dimension", ""), "mentioned": False}

    results = await asyncio.gather(*[test_query(q) for q in queries])

    total_mentions = sum(1 for r in results if r.get("mentioned"))
    visibility = round((total_mentions / len(results) * 100) if results else 0, 1)

    return {
        "company_name": company_name,
        "queries_tested": len(results),
        "mentions": total_mentions,
        "visibility": visibility,
        "query_results": results,
        "execution_time": round(time.time() - start_time, 2),
    }


def _build_mentions_report(result: dict) -> str:
    """Build markdown visibility report."""
    lines = []
    company = result.get("company_name", "Unknown")
    visibility = result.get("visibility", 0)
    mentions = result.get("mentions", 0)
    total = result.get("queries_tested", 0)

    lines.append(f"# AI Visibility Report: {company}")
    lines.append("")
    lines.append(f"**Visibility Score:** {visibility}%")
    lines.append(f"**Mentions:** {mentions}/{total} queries")
    lines.append("")

    query_results = result.get("query_results", [])
    if query_results:
        lines.append("## Query Results")
        lines.append("")
        for qr in query_results:
            icon = "mentioned" if qr.get("mentioned") else "not found"
            dim = qr.get("dimension", "")
            lines.append(f"- **{qr.get('query', '')}** [{dim}] -- {icon}")
        lines.append("")

    lines.append(f"---\n*Execution time: {result.get('execution_time', 0)}s*")
    return "\n".join(lines)
