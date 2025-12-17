"""
Real Company Test Data for Master AEO Service
Based on actual company information from content-manager context.
"""

# SCAILE - Real company data from content-manager
SCAILE_COMPANY_DATA = {
    "companyInfo": {
        "name": "SCAILE",
        "website": "https://scaile.tech",
        "description": "Answer Engine Optimization (AEO) consulting and services company helping businesses optimize their visibility in AI-powered search platforms like ChatGPT, Perplexity, Claude, and Gemini.",
        "industry": "Marketing Technology",
        "productCategory": "AEO Software & Consulting",
        "products": [
            "AEO Consulting",
            "Answer Engine Optimization",
            "AI Search Optimization",
            "ChatGPT Visibility Optimization",
            "Perplexity SEO Services"
        ],
        "services": [
            "AEO Strategy Development",
            "Content Optimization for AI",
            "AI Platform Visibility Audits",
            "Answer Engine Analytics",
            "AI Search Training & Workshops"
        ],
        "pain_points": [
            "Low AI search visibility",
            "Poor mentions in AI platform responses",
            "Lack of AEO strategy",
            "Invisible to ChatGPT and Perplexity",
            "Missing from AI-generated recommendations"
        ],
        "target_audience": "B2B SaaS companies, marketing teams, CMOs, digital marketing managers, and enterprise companies looking to optimize their presence in AI-powered search platforms",
        "icp": "Marketing directors and CMOs at B2B SaaS companies with 50-500 employees who are struggling with AI search visibility",
        "country": "US",
        "founded": "2023",
        "employees": "10-25",
        "funding_stage": "Bootstrap"
    },
    "competitors": [
        {
            "name": "BrightEdge",
            "website": "https://brightedge.com",
            "description": "Enterprise SEO and content performance marketing platform"
        },
        {
            "name": "Conductor",
            "website": "https://conductor.com", 
            "description": "Organic marketing platform for content and SEO optimization"
        },
        {
            "name": "Searchmetrics",
            "website": "https://searchmetrics.com",
            "description": "Enterprise SEO platform and digital marketing insights"
        },
        {
            "name": "seoClarity",
            "website": "https://seoclarity.net",
            "description": "AI-powered SEO platform for enterprise businesses"
        },
        {
            "name": "Semrush",
            "website": "https://semrush.com",
            "description": "All-in-one digital marketing toolkit for SEO, PPC, and content marketing"
        }
    ]
}

# Valoon - E-commerce/Legal tech company data  
VALOON_COMPANY_DATA = {
    "companyInfo": {
        "name": "Valoon",
        "website": "https://valoon.com",
        "description": "E-commerce and legal technology platform providing business registration, compliance, and corporate services for entrepreneurs and small businesses.",
        "industry": "Legal Technology",
        "productCategory": "Business Services Platform",
        "products": [
            "Business Registration Services",
            "Corporate Compliance Software",
            "Legal Document Automation",
            "Business Formation Platform",
            "Compliance Management Tools"
        ],
        "services": [
            "LLC Formation",
            "Corporation Registration", 
            "Compliance Monitoring",
            "Legal Document Preparation",
            "Business Licensing Support"
        ],
        "pain_points": [
            "Complex business formation process",
            "Compliance tracking difficulties", 
            "Legal document complexity",
            "Small business legal costs",
            "Regulatory confusion"
        ],
        "target_audience": "Entrepreneurs, small business owners, startups, and freelancers looking for affordable and streamlined business formation and compliance services",
        "icp": "First-time entrepreneurs and small business owners who need simple, affordable business formation and ongoing compliance support",
        "country": "US",
        "founded": "2020",
        "employees": "25-50", 
        "funding_stage": "Seed"
    },
    "competitors": [
        {
            "name": "LegalZoom",
            "website": "https://legalzoom.com",
            "description": "Online legal services for business formation and legal documents"
        },
        {
            "name": "Incfile",
            "website": "https://incfile.com",
            "description": "Business formation and corporate services platform"
        },
        {
            "name": "ZenBusiness", 
            "website": "https://zenbusiness.com",
            "description": "Small business formation and growth platform"
        },
        {
            "name": "Northwest Registered Agent",
            "website": "https://northwestregisteredagent.com",
            "description": "Business formation and registered agent services"
        }
    ]
}

# TechStartup - Generic SaaS company for testing
TECHSTARTUP_COMPANY_DATA = {
    "companyInfo": {
        "name": "TechStartup",
        "website": "https://techstartup.com",
        "description": "Cloud-based project management and collaboration platform for remote teams and distributed organizations.",
        "industry": "SaaS",
        "productCategory": "Project Management Software",
        "products": [
            "Project Management Platform",
            "Team Collaboration Tools",
            "Remote Work Software",
            "Task Management System",
            "Time Tracking Solution"
        ],
        "services": [
            "Project Setup & Onboarding",
            "Team Collaboration Consulting", 
            "Remote Work Training",
            "Custom Workflow Design",
            "Integration Support"
        ],
        "pain_points": [
            "Remote team coordination challenges",
            "Project visibility issues",
            "Inefficient communication",
            "Time tracking difficulties",
            "Resource allocation problems"
        ],
        "target_audience": "Remote teams, distributed companies, project managers, and technology teams looking for better collaboration and project management tools",
        "icp": "Project managers and team leads at remote-first companies with 25-250 employees",
        "country": "US",
        "founded": "2022",
        "employees": "15-30",
        "funding_stage": "Series A"
    },
    "competitors": [
        {
            "name": "Asana",
            "website": "https://asana.com",
            "description": "Work management platform for teams"
        },
        {
            "name": "Monday.com",
            "website": "https://monday.com",
            "description": "Work operating system for teams and organizations"
        },
        {
            "name": "Trello",
            "website": "https://trello.com",
            "description": "Visual collaboration tool for organizing projects"
        },
        {
            "name": "Notion",
            "website": "https://notion.so",
            "description": "All-in-one workspace for notes, tasks, and collaboration"
        }
    ]
}

# Test scenarios with different company sizes and industries
TEST_COMPANIES = {
    "scaile": SCAILE_COMPANY_DATA,
    "valoon": VALOON_COMPANY_DATA, 
    "techstartup": TECHSTARTUP_COMPANY_DATA
}

def get_test_company(company_name: str = "scaile"):
    """Get test company data by name."""
    return TEST_COMPANIES.get(company_name.lower(), SCAILE_COMPANY_DATA)