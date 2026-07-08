# Playwright — Browser Automation

## Overview

15 lessons covering Playwright for modern browser automation and testing.

| # | Lesson | Code | Topic |
|---|--------|------|-------|
| 01 | [Browser Basics](lessons/01-browser-basics.md) | [01-browser-basics.py](code/01-browser-basics.py) | Launch, navigate, screenshot, close |
| 02 | [Locators & Selectors](lessons/02-locators-selectors.md) | [02-locators-selectors.py](code/02-locators-selectors.py) | CSS, text, XPath selectors |
| 03 | [Interactions](lessons/03-interactions.md) | [03-interactions.py](code/03-interactions.py) | click, fill, select, check |
| 04 | [Waiting Strategies](lessons/04-waiting-strategies.md) | [04-waiting-strategies.py](code/04-waiting-strategies.py) | wait_for_selector, load_state |
| 05 | [Assertions](lessons/05-assertions.md) | [05-assertions.py](code/05-assertions.py) | expect() API matchers |
| 06 | [Frames & Windows](lessons/06-frames-windows.md) | [06-frames-windows.py](code/06-frames-windows.py) | frame locators, popups |
| 07 | [Network Interception](lessons/07-network-interception.md) | [07-network-interception.py](code/07-network-interception.py) | route(), abort, mock |
| 08 | [File Uploads & Downloads](lessons/08-file-uploads-downloads.md) | [08-file-uploads-downloads.py](code/08-file-uploads-downloads.py) | set_input_files, screenshots |
| 09 | [Authentication](lessons/09-authentication.md) | [09-authentication.py](code/09-authentication.py) | storageState, cookies |
| 10 | [Mobile Emulation](lessons/10-mobile-emulation.md) | [10-mobile-emulation.py](code/10-mobile-emulation.py) | Device presets, viewport |
| 11 | [Visual Testing](lessons/11-visual-testing.md) | [11-visual-testing.py](code/11-visual-testing.py) | Screenshots, comparison |
| 12 | [Performance Metrics](lessons/12-performance-metrics.md) | [12-performance-metrics.py](code/12-performance-metrics.py) | Timing, console, tracing |
| 13 | [API Testing](lessons/13-api-testing.md) | [13-api-testing.py](code/13-api-testing.py) | request context, REST |
| 14 | [Fixtures & Parallel](lessons/14-fixtures-parallel.md) | [14-fixtures-parallel.py](code/14-fixtures-parallel.py) | Isolation, parallel execution |
| 15 | [CI & Reports](lessons/15-ci-reports.md) | [15-ci-reports.py](code/15-ci-reports.py) | HTML/JUnit reports |

## Prerequisites

```bash
pip install playwright
playwright install chromium
```

## Notes

- All code uses `sync_api` (synchronous API) for simplicity
- Uses headless mode by default — no GUI needed
- Tests against `https://example.com`, `data:text/html`, and `https://httpbin.org` — no app server required
- Browser contexts provide full test isolation (cookies, localStorage, etc.)

## Practice

- [Phase 01 Exercises](practice/phase01-exercises.md)
