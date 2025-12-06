"""
PDF Generation Service - Pixel-Perfect HTML to PDF Conversion.

Uses Playwright with Chromium for rendering, achieving exact visual match
between browser HTML and generated PDF.

Endpoints:
- POST /convert - Convert HTML string to PDF
- POST /convert/url - Convert URL to PDF
- POST /convert/debug - Convert + return screenshot for comparison
- GET /health - Health check
"""

import base64
import time
from io import BytesIO
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from playwright.async_api import async_playwright

app = FastAPI(
    title="PDF Generation Service",
    description="Pixel-perfect HTML to PDF conversion using Playwright/Chromium",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ConvertRequest(BaseModel):
    """Request model for HTML to PDF conversion."""
    html: str = Field(..., description="HTML content to convert")
    format: Optional[str] = Field(default="A4", description="Page format: A4, Letter, or None for auto")
    landscape: bool = Field(default=False, description="Landscape orientation")
    print_background: bool = Field(default=True, description="Include backgrounds/gradients")
    margin_top: str = Field(default="0mm", description="Top margin")
    margin_bottom: str = Field(default="0mm", description="Bottom margin")
    margin_left: str = Field(default="0mm", description="Left margin")
    margin_right: str = Field(default="0mm", description="Right margin")
    scale: float = Field(default=1.0, ge=0.1, le=2.0, description="Scale factor")
    prefer_css_page_size: bool = Field(default=True, description="Respect CSS @page rules")
    viewport_width: int = Field(default=900, description="Viewport width for rendering")
    width: Optional[str] = Field(default=None, description="Custom page width (e.g., '900px')")
    height: Optional[str] = Field(default=None, description="Custom page height (e.g., '1200px')")
    device_scale_factor: float = Field(default=2, ge=1, le=3, description="Device pixel ratio for rendering")
    color_scheme: Optional[str] = Field(default=None, description="Color scheme: 'light', 'dark', or None for auto")


class ConvertUrlRequest(BaseModel):
    """Request model for URL to PDF conversion."""
    url: str = Field(..., description="URL to convert")
    format: str = Field(default="A4")
    landscape: bool = Field(default=False)
    print_background: bool = Field(default=True)
    margin_top: str = Field(default="0mm")
    margin_bottom: str = Field(default="0mm")
    margin_left: str = Field(default="0mm")
    margin_right: str = Field(default="0mm")
    scale: float = Field(default=1.0, ge=0.1, le=2.0)
    prefer_css_page_size: bool = Field(default=True)
    viewport_width: int = Field(default=900)
    wait_for_selector: Optional[str] = Field(default=None, description="Wait for element")
    wait_timeout: int = Field(default=30000, description="Wait timeout in ms")


class ConvertResponse(BaseModel):
    """Response model for PDF conversion."""
    pdf_base64: str
    size_bytes: int
    render_time_ms: int


class DebugResponse(BaseModel):
    """Response model for debug endpoint with comparison data."""
    pdf_base64: str
    screenshot_base64: str
    size_bytes: int
    render_time_ms: int
    viewport: dict


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    service: str
    version: str


async def generate_pdf(
    html: str,
    format: Optional[str] = "A4",
    landscape: bool = False,
    print_background: bool = True,
    margin_top: str = "0mm",
    margin_bottom: str = "0mm",
    margin_left: str = "0mm",
    margin_right: str = "0mm",
    scale: float = 1.0,
    prefer_css_page_size: bool = True,
    viewport_width: int = 900,
    return_screenshot: bool = False,
    width: Optional[str] = None,
    height: Optional[str] = None,
    device_scale_factor: float = 2,
    color_scheme: Optional[str] = None,
) -> dict:
    """
    Generate PDF from HTML using Playwright.

    Key settings for pixel-perfect output:
    - Force light color scheme (no dark mode)
    - Set explicit viewport for consistent rendering
    - Enable print backgrounds for gradients/colors
    - Respect CSS @page rules
    """
    start_time = time.time()

    async with async_playwright() as p:
        # Launch Chromium
        browser = await p.chromium.launch()

        # Build context options
        context_options = {
            "viewport": {"width": viewport_width, "height": 1200},
            "device_scale_factor": device_scale_factor,  # Higher DPI for crisp rendering
        }

        # Set color scheme if specified (for @media prefers-color-scheme CSS)
        if color_scheme in ("light", "dark"):
            context_options["color_scheme"] = color_scheme

        context = await browser.new_context(**context_options)
        page = await context.new_page()

        # Load HTML content
        await page.set_content(html, wait_until="networkidle")

        # Wait a bit for fonts and images to load
        await page.wait_for_timeout(500)

        # Emulate print media FIRST - this affects layout/height
        # PDF generation uses print media, so we need measurements in print mode
        emulate_options = {"media": "print"}
        if color_scheme:
            emulate_options["color_scheme"] = color_scheme
        await page.emulate_media(**emulate_options)
        # Wait for print styles to apply
        await page.wait_for_timeout(100)

        # Get actual page height AFTER print media emulation
        # This ensures PDF height matches the print layout
        page_height = await page.evaluate("document.body.scrollHeight")

        result = {"viewport": {"width": viewport_width, "height": page_height}}

        # Take screenshot if requested (for comparison)
        if return_screenshot:
            screenshot_bytes = await page.screenshot(
                full_page=True,
                type="png",
            )
            result["screenshot_base64"] = base64.b64encode(screenshot_bytes).decode("utf-8")

        # Build PDF options
        pdf_options = {
            "landscape": landscape,
            "print_background": print_background,
            "margin": {
                "top": margin_top,
                "bottom": margin_bottom,
                "left": margin_left,
                "right": margin_right,
            },
            "scale": scale,
            "prefer_css_page_size": prefer_css_page_size,
        }

        # Use custom width/height if provided, otherwise use format
        # Note: width takes priority over format; height can be auto-calculated
        if width is not None:
            pdf_options["width"] = width
            if height is not None:
                pdf_options["height"] = height
            else:
                # Auto-calculate height from page content
                pdf_options["height"] = f"{page_height}px"
        elif format is not None:
            pdf_options["format"] = format

        # Generate PDF
        pdf_bytes = await page.pdf(**pdf_options)

        await browser.close()

        render_time_ms = int((time.time() - start_time) * 1000)

        result.update({
            "pdf_base64": base64.b64encode(pdf_bytes).decode("utf-8"),
            "size_bytes": len(pdf_bytes),
            "render_time_ms": render_time_ms,
        })

        return result


async def generate_pdf_from_url(
    url: str,
    format: str = "A4",
    landscape: bool = False,
    print_background: bool = True,
    margin_top: str = "0mm",
    margin_bottom: str = "0mm",
    margin_left: str = "0mm",
    margin_right: str = "0mm",
    scale: float = 1.0,
    prefer_css_page_size: bool = True,
    viewport_width: int = 900,
    wait_for_selector: Optional[str] = None,
    wait_timeout: int = 30000,
) -> dict:
    """Generate PDF from URL using Playwright."""
    start_time = time.time()

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={"width": viewport_width, "height": 1200},
            color_scheme="light",
            device_scale_factor=2,
        )
        page = await context.new_page()

        # Navigate to URL
        await page.goto(url, wait_until="networkidle", timeout=wait_timeout)

        # Wait for specific element if requested
        if wait_for_selector:
            await page.wait_for_selector(wait_for_selector, timeout=wait_timeout)

        # Wait for fonts/images
        await page.wait_for_timeout(500)

        # Generate PDF
        pdf_bytes = await page.pdf(
            format=format,
            landscape=landscape,
            print_background=print_background,
            margin={
                "top": margin_top,
                "bottom": margin_bottom,
                "left": margin_left,
                "right": margin_right,
            },
            scale=scale,
            prefer_css_page_size=prefer_css_page_size,
        )

        await browser.close()

        render_time_ms = int((time.time() - start_time) * 1000)

        return {
            "pdf_base64": base64.b64encode(pdf_bytes).decode("utf-8"),
            "size_bytes": len(pdf_bytes),
            "render_time_ms": render_time_ms,
        }


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        service="pdf-generation",
        version="1.0.0",
    )


@app.post("/convert", response_model=ConvertResponse)
async def convert_html_to_pdf(request: ConvertRequest):
    """
    Convert HTML string to PDF.

    Returns base64-encoded PDF.
    """
    try:
        result = await generate_pdf(
            html=request.html,
            format=request.format,
            landscape=request.landscape,
            print_background=request.print_background,
            margin_top=request.margin_top,
            margin_bottom=request.margin_bottom,
            margin_left=request.margin_left,
            margin_right=request.margin_right,
            scale=request.scale,
            prefer_css_page_size=request.prefer_css_page_size,
            viewport_width=request.viewport_width,
            return_screenshot=False,
            width=request.width,
            height=request.height,
            device_scale_factor=request.device_scale_factor,
            color_scheme=request.color_scheme,
        )
        return ConvertResponse(
            pdf_base64=result["pdf_base64"],
            size_bytes=result["size_bytes"],
            render_time_ms=result["render_time_ms"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert/url")
async def convert_url_to_pdf(request: ConvertUrlRequest):
    """
    Convert URL to PDF.

    Returns base64-encoded PDF.
    """
    try:
        result = await generate_pdf_from_url(
            url=request.url,
            format=request.format,
            landscape=request.landscape,
            print_background=request.print_background,
            margin_top=request.margin_top,
            margin_bottom=request.margin_bottom,
            margin_left=request.margin_left,
            margin_right=request.margin_right,
            scale=request.scale,
            prefer_css_page_size=request.prefer_css_page_size,
            viewport_width=request.viewport_width,
            wait_for_selector=request.wait_for_selector,
            wait_timeout=request.wait_timeout,
        )
        return ConvertResponse(
            pdf_base64=result["pdf_base64"],
            size_bytes=result["size_bytes"],
            render_time_ms=result["render_time_ms"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/convert/debug", response_model=DebugResponse)
async def convert_html_to_pdf_debug(request: ConvertRequest):
    """
    Convert HTML to PDF with debug info.

    Returns both PDF and screenshot for visual comparison.
    Use this endpoint during development to compare HTML rendering
    with PDF output and identify discrepancies.
    """
    try:
        result = await generate_pdf(
            html=request.html,
            format=request.format,
            landscape=request.landscape,
            print_background=request.print_background,
            margin_top=request.margin_top,
            margin_bottom=request.margin_bottom,
            margin_left=request.margin_left,
            margin_right=request.margin_right,
            scale=request.scale,
            prefer_css_page_size=request.prefer_css_page_size,
            viewport_width=request.viewport_width,
            return_screenshot=True,
            width=request.width,
            height=request.height,
            device_scale_factor=request.device_scale_factor,
            color_scheme=request.color_scheme,
        )
        return DebugResponse(
            pdf_base64=result["pdf_base64"],
            screenshot_base64=result["screenshot_base64"],
            size_bytes=result["size_bytes"],
            render_time_ms=result["render_time_ms"],
            viewport=result["viewport"],
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# For local development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
