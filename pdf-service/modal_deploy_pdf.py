"""
Modal deployment for SCAILE Services - Unified API Gateway

Core utility services:
- /ai/* - Unified AI service (OpenRouter gateway)
- /pdf/* - PDF generation (Playwright/Chromium)
- /serp/* - Search engine results (SearXNG free, DataForSEO paid)
- /url/* - URL content extraction (OpenPull/Gemini)

NOTE: Company analysis is in aeo-checks service (https://clients--aeo-checks-fastapi-app.modal.run/company/*)
"""

import modal
from pathlib import Path

app = modal.App("scaile-services")
local_dir = Path(__file__).parent

# Combined image with all dependencies
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        # Playwright Chromium dependencies (for PDF)
        "libnss3",
        "libnspr4",
        "libatk1.0-0",
        "libatk-bridge2.0-0",
        "libcups2",
        "libdrm2",
        "libxkbcommon0",
        "libxcomposite1",
        "libxdamage1",
        "libxfixes3",
        "libxrandr2",
        "libgbm1",
        "libasound2",
        "libpango-1.0-0",
        "libcairo2",
        # Fonts for better rendering
        "fonts-liberation",
        "fonts-noto-core",
        # Cairo for SVG (PDF service)
        "libcairo2-dev",
        # Git for installing packages from GitHub
        "git",
    )
    .pip_install(
        # SERP service (GCP auth for Cloud Run) - MUST be first
        "requests>=2.31.0",
        "google-auth>=2.23.0",
        # Core
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "httpx>=0.25.0",
        "brotli>=1.1.0",
        # AI service dependencies
        "aiohttp>=3.9.0",
        "openai>=1.50.0",  # For OpenRouter client (async SDK)
        # PDF service
        "playwright>=1.40.0",
        # URL service (BeautifulSoup for HTML parsing)
        "beautifulsoup4>=4.12.0",
    )
    .run_commands(
        "playwright install chromium",
        # Force fresh install of OpenPull with OpenRouter support (v2.0.0)
        "pip install --force-reinstall --no-cache-dir git+https://github.com/federicodeponte/openpull.git@master",
    )
    .add_local_python_source("main")
    # Simplified AI service
    .add_local_python_source("simple_ai_service")
    .add_local_python_source("openrouter_client")
    # PDF service
    .add_local_python_source("pdf_service")
    # SERP service
    .add_local_python_source("serp_service")
    .add_local_python_source("serp_types")
    .add_local_python_source("serp_searxng")
    .add_local_python_source("serp_dataforseo")
    # URL service
    .add_local_python_source("url_service")
)


@app.function(
    image=image,
    secrets=[
        modal.Secret.from_name("openrouter-api-key"),  # Single API key for all AI models
        modal.Secret.from_name("serp-credentials"),  # SEARXNG_URL, DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD
    ],
    timeout=600,  # 10 min timeout - updated Dec 4
    max_containers=20,
    memory=2048,  # Chromium needs decent memory
    min_containers=1,  # Keep 1 container warm to avoid cold starts (Chromium takes ~60s)
)
@modal.asgi_app()
def fastapi_app():
    from main import app
    return app
