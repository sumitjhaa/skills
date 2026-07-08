"""API testing — request context, REST methods."""
from playwright.sync_api import sync_playwright

print("=== API Testing ===\n")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context()
    request = context.request

    get_resp = request.get("https://httpbin.org/get")
    print(f"GET status: {get_resp.status}")
    print(f"GET body keys: {list(get_resp.json().keys())}")

    post_resp = request.post("https://httpbin.org/post", data={"name": "Alice"})
    print(f"POST status: {post_resp.status}")
    print(f"POST form: {post_resp.json().get('form')}")

    put_resp = request.put("https://httpbin.org/put", data="updated")
    print(f"PUT status: {put_resp.status}")

    delete_resp = request.delete("https://httpbin.org/delete")
    print(f"DELETE status: {delete_resp.status}")

    assert get_resp.ok
    assert post_resp.status == 200
    print("✅ All API assertions passed")

    context.close()
    browser.close()

print("\n✅ API testing works.")
