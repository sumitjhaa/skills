"""Selenium — dynamic web scraping with browser automation."""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

print("=== Selenium Demo ===")
print("""
This requires: pip install selenium webdriver-manager
And a Chrome/Chromium browser installed.

The full automation code is shown below for reference.
""")

DEMO_CODE = '''
from webdriver_manager.chrome import ChromeDriverManager

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options,
)

try:
    driver.get("https://example.com")
    heading = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "h1"))
    )
    print(f"Title: {driver.title}")
    print(f"Heading: {heading.text}")

    links = driver.find_elements(By.TAG_NAME, "a")
    for link in links[:5]:
        print(f"  {link.text}: {link.get_attribute('href')}")

    driver.save_screenshot("screenshot.png")

finally:
    driver.quit()
'''

print(DEMO_CODE)

print("\n=== Key Wait Strategies ===")
waits = [
    ("presence_of_element_located", "Element exists in DOM (may be hidden)"),
    ("visibility_of_element_located", "Element is visible"),
    ("element_to_be_clickable", "Element visible and enabled"),
    ("text_to_be_present_in_element", "Element contains specific text"),
    ("staleness_of", "Element removed from DOM"),
]
for name, desc in waits:
    print(f"  EC.{name} — {desc}")

print("\n=== Anti-Detection Tips ===")
tips = [
    "Set a realistic user-agent",
    "Add random delays between actions",
    "Use headless mode cautiously",
    "Rotate IPs via proxies for large-scale scraping",
    "Respect robots.txt and terms of service",
    "Consider Playwright as a modern alternative to Selenium",
]
for i, tip in enumerate(tips, 1):
    print(f"  {i}. {tip}")
