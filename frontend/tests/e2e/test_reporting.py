import pytest
from playwright.sync_api import sync_playwright

def test_pothole_reporting_workflow():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Navigate to home page
        page.goto("http://127.0.0.1:5173") # Assuming Vite dev server
        
        # Confirm home page is reachable and primary CTA is visible.
        assert "127.0.0.1:5173" in page.url
        assert page.locator("text=Report Pothole").is_visible()
        
        # Click Report Pothole
        page.click("text=Report Pothole")
        
        # Should be redirected to login (if required) or reporting page
        # In current setup, it goes to /citizen-login
        assert "/citizen-login" in page.url
        
        browser.close()
