"""
Modal deployment for PDF Generation Service

Converts HTML to PDF using Playwright/Chromium for pixel-perfect rendering.

Usage:
    modal deploy modal_deploy.py
    
Test:
    curl https://YOUR_WORKSPACE--pdf-service-fastapi-app.modal.run/health
"""

import modal
from pathlib import Path

app = modal.App("pdf-service")
local_dir = Path(__file__).parent

# Build image with Playwright and Chromium
image = (
    modal.Image.debian_slim(python_version="3.11")
    .apt_install(
        # Playwright Chromium dependencies
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
    )
    .pip_install(
        "fastapi>=0.104.0",
        "uvicorn>=0.24.0",
        "pydantic>=2.5.0",
        "playwright>=1.40.0",
    )
    .run_commands(
        "playwright install chromium",
    )
    .add_local_python_source("pdf_service")
)


@app.function(
    image=image,
    timeout=300,  # 5 min timeout
    max_containers=10,
    memory=2048,  # Chromium needs decent memory
    min_containers=1,  # Keep 1 container warm to avoid cold starts
)
@modal.asgi_app()
def fastapi_app():
    """Serve the PDF generation FastAPI application."""
    from pdf_service import app
    return app


# Local entrypoint for testing
@app.local_entrypoint()
def main():
    """Test the deployment locally."""
    print("\n🚀 PDF Generation Service")
    print("=" * 60)
    print("\nEndpoint: https://YOUR_WORKSPACE--pdf-service-fastapi-app.modal.run")
    print("\nTest with:")
    print('  curl https://YOUR_WORKSPACE--pdf-service-fastapi-app.modal.run/health')
    print("\n" + "=" * 60)

