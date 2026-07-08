# Mobile Emulation

Emulate mobile devices, viewports, and geolocation to test responsive and location-aware behaviour without a physical device.

## Key Concepts
- `playwright.devices` — built-in device presets (iPhone, Pixel, Galaxy)
- `browser.new_context(**device_descriptor)` — apply a device preset
- `viewport={"width": W, "height": H}` — custom viewport dimensions
- `geolocation={"latitude": ..., "longitude": ...}` + `permissions` — location emulation
- Device descriptors include user agent, viewport, device scale factor, and touch support

## Code Example

```python
import asyncio
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)

        # Use a built-in device descriptor
        iphone = p.devices["iPhone 13"]
        context = await browser.new_context(**iphone)
        page = await context.new_page()
        await page.goto("https://example.com")
        print(f"iPhone 13 viewport: {await page.evaluate('window.innerWidth')}px")

        # Custom geolocation
        context2 = await browser.new_context(
            viewport={"width": 375, "height": 812},
            geolocation={"latitude": 48.8566, "longitude": 2.3522},
            permissions=["geolocation"],
        )
        page2 = await context2.new_page()
        await page2.goto("https://example.com")
        print("Geolocation set to Paris.")

        await browser.close()


asyncio.run(main())
```

Run with: `python ../code/10-mobile-emulation.py`

## Key Takeaways
- `playwright.devices` contains 50+ presets — use `list(devices.keys())` to explore.
- Device emulation is applied at the context level, not the page level.
- Combine geolocation with `permissions=[]` — location prompts require permission grants.
