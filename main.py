from flask import Flask, request, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

def search_google(query):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.google.com/")
        page.fill("input[name='q']", query)
        page.keyboard.press("Enter")
        page.wait_for_selector("h3", timeout=5000)
        results = page.query_selector_all("h3")
        output = []
        for r in results[:3]:  # top 3 results
            output.append(r.inner_text())
        browser.close()
        return output

@app.route("/browser-tool", methods=["POST"])
def browser_tool():
    data = request.json
    query = data.get("query", "")
    try:
        result = search_google(query)
        return jsonify({"status": "success", "results": result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    return "Browser Tool is Running"

