"""
Test HTML Report Generation - Standalone (No API Keys Required)

Generates an HTML report using sample data - no external API calls.
"""

import sys
from pathlib import Path
from datetime import datetime

# Add reports to path
sys.path.insert(0, str(Path(__file__).parent))

from reports.html_generator import build_aeo_report_html


def get_sample_data(company_name: str = "Telli"):
    """Get sample AEO analysis data."""
    return {
        'clientName': company_name,
        'websiteUrl': 'https://telli.com',
        'generatedAt': datetime.now(),
        'theme': 'dark',
        'canvasData': {
            'clientInfo': {
                'name': company_name,
                'website': 'https://telli.com',
                'industry': 'SaaS',
                'products': ['Scheduling Software', 'Team Calendar'],
                'services': ['Meeting Scheduling', 'Calendar Integration'],
            },
            'healthCheck': {
                'score': 68,
                'grade': 'B',
                'checks': {}
            },
            'mentionsCheck': {
                'visibility': 42,
                'band': 'Moderate',
                'qualityScore': 6.2,
                'totalMentions': 18,
                'totalQueries': 50,
                'platformStats': {
                    'chatgpt': {'mentions': 18, 'responses': 50},
                    'perplexity': {'mentions': 15, 'responses': 50},
                    'claude': {'mentions': 16, 'responses': 50},
                    'gemini': {'mentions': 12, 'responses': 50},
                    'mistral': {'mentions': 14, 'responses': 50},
                }
            }
        }
    }


def main():
    """Generate HTML report from sample data."""
    
    company_name = sys.argv[1] if len(sys.argv) > 1 else "Telli"
    
    print(f"\n🧪 Generating HTML Report (Standalone Test)")
    print(f"📊 Company: {company_name}")
    print()
    
    # Get sample data
    data = get_sample_data(company_name)
    
    # Generate HTML report
    print("⏳ Generating HTML report...")
    html = build_aeo_report_html(data)
    
    # Save to file
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = f"test-report-{company_name.lower().replace(' ', '-')}-{timestamp}.html"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(html)
    
    size_kb = len(html) / 1024
    print(f"✅ HTML Report generated")
    print(f"   → Saved: {filename}")
    print(f"   → Size: {size_kb:.1f} KB")
    print()
    print(f"🌐 Open in browser:")
    print(f"   open {filename}")
    print()


if __name__ == '__main__':
    main()

