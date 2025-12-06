# PDF Generation Service

Pixel-perfect HTML to PDF conversion using Playwright/Chromium.

## Features

- **Pixel-perfect rendering** - Exact visual match between HTML and PDF
- **Dark mode support** - Respects CSS color schemes
- **Custom page sizes** - A4, Letter, or custom dimensions
- **High-quality output** - 2x device scale factor for crisp rendering

## Deployment

```bash
cd pdf-service
modal profile activate YOUR_WORKSPACE
modal deploy modal_deploy.py
```

## Endpoints

**Base URL:** `https://YOUR_WORKSPACE--pdf-service-fastapi-app.modal.run`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/convert` | POST | Convert HTML string to PDF |
| `/convert/url` | POST | Convert URL to PDF |
| `/convert/debug` | POST | Convert HTML + return screenshot for comparison |

## Usage Examples

### Convert HTML to PDF

```bash
curl -X POST https://YOUR_WORKSPACE--pdf-service-fastapi-app.modal.run/convert \
  -H "Content-Type: application/json" \
  -d '{
    "html": "<html><body><h1>Hello World</h1></body></html>",
    "format": "A4",
    "print_background": true,
    "theme": "dark"
  }'
```

### Convert URL to PDF

```bash
curl -X POST https://YOUR_WORKSPACE--pdf-service-fastapi-app.modal.run/convert/url \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "format": "A4",
    "print_background": true
  }'
```

## Request Parameters

- `html` (string, required) - HTML content to convert
- `format` (string, optional) - Page format: "A4", "Letter", or None for auto
- `landscape` (boolean, default: false) - Landscape orientation
- `print_background` (boolean, default: true) - Include backgrounds/gradients
- `margin_top/bottom/left/right` (string, default: "0mm") - Page margins
- `scale` (float, default: 1.0) - Scale factor (0.1-2.0)
- `viewport_width` (int, default: 900) - Viewport width for rendering
- `device_scale_factor` (float, default: 2) - Device pixel ratio
- `color_scheme` (string, optional) - "light", "dark", or None for auto

## Response

```json
{
  "pdf_base64": "base64-encoded-pdf-content",
  "size_bytes": 12345,
  "render_time_ms": 1234
}
```

