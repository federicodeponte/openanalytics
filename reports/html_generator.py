"""
HTML Report Generator for AEO Analysis

Generates professional HTML reports from AEO analysis data.
Works with API responses from the aeo-checks service.
"""

from datetime import datetime
from typing import Dict, Any, Optional
import json


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    if not text:
        return ""
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#x27;")
    )


def format_number(value: Optional[float]) -> str:
    """Format number with appropriate precision."""
    if value is None:
        return "N/A"
    if isinstance(value, float):
        return f"{value:.1f}"
    return str(value)


def build_score_card(title: str, score: float, grade: str, max_score: int = 100) -> str:
    """Build a score card component."""
    percentage = (score / max_score) * 100
    color_class = (
        "excellent" if percentage >= 90
        else "good" if percentage >= 70
        else "fair" if percentage >= 50
        else "poor"
    )
    
    return f"""
    <div class="score-card {color_class}">
        <div class="score-header">
            <h3>{escape_html(title)}</h3>
            <span class="grade">{escape_html(grade)}</span>
        </div>
        <div class="score-value">
            <span class="score">{format_number(score)}</span>
            <span class="max-score">/{max_score}</span>
        </div>
        <div class="score-bar">
            <div class="score-fill" style="width: {percentage}%"></div>
        </div>
    </div>
    """


def build_metrics_section(health_data: Dict[str, Any]) -> str:
    """Build metrics section from health check data."""
    if not health_data:
        return "<p>Health check data not available.</p>"
    
    score = health_data.get("score", 0)
    grade = health_data.get("grade", "N/A")
    
    categories = health_data.get("categories", {})
    technical = categories.get("technical", {})
    structured_data = categories.get("structured_data", {})
    aeo_crawler = categories.get("aeo_crawler", {})
    authority = categories.get("authority", {})
    
    return f"""
    <div class="metrics-section">
        {build_score_card("Overall Health Score", score, grade)}
        <div class="category-scores">
            <div class="category-card">
                <h4>Technical SEO</h4>
                <p>Score: {format_number(technical.get("score", 0))}</p>
                <p>Issues: {technical.get("issues_count", 0)}</p>
            </div>
            <div class="category-card">
                <h4>Structured Data</h4>
                <p>Score: {format_number(structured_data.get("score", 0))}</p>
                <p>Issues: {structured_data.get("issues_count", 0)}</p>
            </div>
            <div class="category-card">
                <h4>AI Crawler Access</h4>
                <p>Score: {format_number(aeo_crawler.get("score", 0))}</p>
                <p>Issues: {aeo_crawler.get("issues_count", 0)}</p>
            </div>
            <div class="category-card">
                <h4>Authority Signals</h4>
                <p>Score: {format_number(authority.get("score", 0))}</p>
                <p>Issues: {authority.get("issues_count", 0)}</p>
            </div>
        </div>
    </div>
    """


def build_mentions_section(mentions_data: Dict[str, Any]) -> str:
    """Build mentions section from mentions check data."""
    if not mentions_data:
        return "<p>Mentions check data not available.</p>"
    
    visibility = mentions_data.get("visibility", 0)
    mentions = mentions_data.get("mentions", {})
    
    platforms = mentions_data.get("platform_stats", {})
    
    platform_html = ""
    for platform, stats in platforms.items():
        platform_html += f"""
        <div class="platform-card">
            <h4>{escape_html(platform.title())}</h4>
            <p>Mentions: {stats.get("mentions", 0)}</p>
            <p>Quality Score: {format_number(stats.get("quality_score", 0))}</p>
        </div>
        """
    
    return f"""
    <div class="mentions-section">
        {build_score_card("AI Visibility", visibility, mentions_data.get("band", "N/A"), 100)}
        <div class="platform-breakdown">
            <h3>Platform Breakdown</h3>
            {platform_html}
        </div>
    </div>
    """


def build_company_info_section(company_data: Dict[str, Any]) -> str:
    """Build company information section."""
    if not company_data:
        return "<p>Company analysis data not available.</p>"
    
    company_info = company_data.get("companyInfo", {})
    brand_assets = company_data.get("brandAssets", {})
    
    return f"""
    <div class="company-section">
        <h2>Company Information</h2>
        <div class="info-grid">
            <div class="info-item">
                <strong>Industry:</strong> {escape_html(company_info.get("industry", "N/A"))}
            </div>
            <div class="info-item">
                <strong>Description:</strong> {escape_html(company_info.get("description", "N/A"))}
            </div>
            <div class="info-item">
                <strong>Products:</strong> {", ".join([escape_html(p) for p in company_info.get("products", [])])}
            </div>
            <div class="info-item">
                <strong>Services:</strong> {", ".join([escape_html(s) for s in company_info.get("services", [])])}
            </div>
        </div>
        {f'<div class="logo-section"><img src="{escape_html(brand_assets.get("logo", {}).get("url", ""))}" alt="Company Logo" class="company-logo"></div>' if brand_assets.get("logo", {}).get("url") else ""}
    </div>
    """


def get_styles(theme: str = "dark") -> str:
    """Get CSS styles for the report."""
    bg_color = "#18181b" if theme == "dark" else "#ffffff"
    text_color = "#e0e0e0" if theme == "dark" else "#1a1a1a"
    card_bg = "#262626" if theme == "dark" else "#f5f5f5"
    border_color = "#333" if theme == "dark" else "#ddd"
    
    return f"""
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: {bg_color};
            color: {text_color};
            line-height: 1.6;
            padding: 20px;
        }}
        .report-container {{
            max-width: 1200px;
            margin: 0 auto;
            background: {card_bg};
            border-radius: 12px;
            padding: 40px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }}
        .report-header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 20px;
            border-bottom: 2px solid {border_color};
        }}
        .report-header h1 {{
            font-size: 2.5em;
            margin-bottom: 10px;
            color: {text_color};
        }}
        .report-header .date {{
            color: {text_color};
            opacity: 0.7;
            font-size: 0.9em;
        }}
        .score-card {{
            background: {card_bg};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 20px;
            margin-bottom: 20px;
        }}
        .score-card.excellent {{ border-color: #10b981; }}
        .score-card.good {{ border-color: #3b82f6; }}
        .score-card.fair {{ border-color: #f59e0b; }}
        .score-card.poor {{ border-color: #ef4444; }}
        .score-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}
        .score-header h3 {{
            font-size: 1.2em;
            color: {text_color};
        }}
        .grade {{
            font-size: 1.5em;
            font-weight: bold;
            padding: 5px 15px;
            border-radius: 5px;
            background: {bg_color};
        }}
        .score-value {{
            font-size: 3em;
            font-weight: bold;
            margin: 20px 0;
            color: {text_color};
        }}
        .score-bar {{
            height: 8px;
            background: {bg_color};
            border-radius: 4px;
            overflow: hidden;
        }}
        .score-fill {{
            height: 100%;
            background: linear-gradient(90deg, #3b82f6, #10b981);
            transition: width 0.3s ease;
        }}
        .category-scores {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .category-card {{
            background: {bg_color};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 15px;
        }}
        .category-card h4 {{
            margin-bottom: 10px;
            color: {text_color};
        }}
        .category-card p {{
            margin: 5px 0;
            color: {text_color};
            opacity: 0.8;
        }}
        .platform-breakdown {{
            margin-top: 30px;
        }}
        .platform-breakdown h3 {{
            margin-bottom: 20px;
            color: {text_color};
        }}
        .platform-card {{
            background: {bg_color};
            border: 1px solid {border_color};
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
        }}
        .platform-card h4 {{
            margin-bottom: 10px;
            color: {text_color};
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .info-item {{
            padding: 10px;
            background: {bg_color};
            border-radius: 5px;
        }}
        .company-logo {{
            max-width: 200px;
            margin-top: 20px;
        }}
        @media print {{
            body {{
                background: white;
                color: black;
            }}
            .report-container {{
                box-shadow: none;
            }}
        }}
    </style>
    """


def generate_report_html(
    company_data: Optional[Dict[str, Any]] = None,
    health_data: Optional[Dict[str, Any]] = None,
    mentions_data: Optional[Dict[str, Any]] = None,
    client_name: str = "Client",
    website_url: Optional[str] = None,
    logo_url: Optional[str] = None,
    theme: str = "dark",
) -> str:
    """
    Generate HTML report from AEO analysis data.
    
    Args:
        company_data: Company analysis response from /company/analyze
        health_data: Health check response from /health/check
        mentions_data: Mentions check response from /mentions/check
        client_name: Client company name
        website_url: Client website URL
        logo_url: Logo URL (optional)
        theme: Theme ('dark' or 'light')
    
    Returns:
        HTML string of the report
    """
    date_str = datetime.now().strftime("%B %d, %Y")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AEO Analysis Report - {escape_html(client_name)}</title>
    {get_styles(theme)}
</head>
<body>
    <div class="report-container">
        <header class="report-header">
            <h1>AEO Visibility Report</h1>
            <div class="date">{date_str}</div>
            {f'<p>{escape_html(client_name)}</p>' if client_name else ''}
            {f'<p><a href="{escape_html(website_url)}" style="color: inherit;">{escape_html(website_url)}</a></p>' if website_url else ''}
        </header>
        
        <main>
            {build_company_info_section(company_data) if company_data else ''}
            {build_metrics_section(health_data) if health_data else ''}
            {build_mentions_section(mentions_data) if mentions_data else ''}
        </main>
    </div>
</body>
</html>
"""
    
    return html


if __name__ == "__main__":
    # Example usage
    sample_data = {
        "company_data": {
            "companyInfo": {
                "industry": "Technology",
                "description": "A leading technology company",
                "products": ["Product A", "Product B"],
                "services": ["Service 1", "Service 2"]
            },
            "brandAssets": {
                "logo": {
                    "url": "https://example.com/logo.png"
                }
            }
        },
        "health_data": {
            "score": 75,
            "grade": "B",
            "categories": {
                "technical": {"score": 80, "issues_count": 2},
                "structured_data": {"score": 70, "issues_count": 3},
                "aeo_crawler": {"score": 90, "issues_count": 0},
                "authority": {"score": 60, "issues_count": 5}
            }
        },
        "mentions_data": {
            "visibility": 65,
            "band": "Moderate",
            "platform_stats": {
                "perplexity": {"mentions": 12, "quality_score": 7.5},
                "claude": {"mentions": 8, "quality_score": 6.8},
                "chatgpt": {"mentions": 15, "quality_score": 8.2},
                "gemini": {"mentions": 10, "quality_score": 7.0}
            }
        }
    }
    
    html = generate_report_html(
        company_data=sample_data["company_data"],
        health_data=sample_data["health_data"],
        mentions_data=sample_data["mentions_data"],
        client_name="Example Inc",
        website_url="https://example.com",
        theme="dark"
    )
    
    with open("sample_report.html", "w") as f:
        f.write(html)
    
    print("Sample report generated: sample_report.html")

