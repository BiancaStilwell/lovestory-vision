#!/usr/bin/env python3
"""
Website Screenshot Tool for Bianca's Portfolio
Takes screenshots of all pages for proofing and feedback
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in background
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")  # Desktop size
    chrome_options.add_argument("--disable-gpu")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def take_screenshot(driver, url, filename, wait_time=3):
    """Take screenshot of a page"""
    try:
        print(f"Taking screenshot of: {url}")
        driver.get(url)
        time.sleep(wait_time)  # Wait for page to load
        
        # Take screenshot
        driver.save_screenshot(f"screenshots/{filename}")
        print(f"✓ Saved: {filename}")
        
    except Exception as e:
        print(f"✗ Error with {url}: {e}")

def take_mobile_screenshot(driver, url, filename, wait_time=3):
    """Take mobile-sized screenshot"""
    try:
        print(f"Taking mobile screenshot of: {url}")
        driver.set_window_size(375, 812)  # iPhone size
        driver.get(url)
        time.sleep(wait_time)
        
        driver.save_screenshot(f"screenshots/mobile_{filename}")
        print(f"✓ Saved: mobile_{filename}")
        
    except Exception as e:
        print(f"✗ Error with mobile {url}: {e}")

def main():
    # Create screenshots directory
    if not os.path.exists("screenshots"):
        os.makedirs("screenshots")
    
    # Base URL (you'll need to update this to your actual URL)
    base_url = "http://localhost:5500"  # Update this to your actual URL
    
    # List of pages to screenshot
    pages = [
        ("/", "01_landing_page.png"),
        ("/pages/about.html", "02_about_page.png"),
        ("/pages/contact.html", "03_contact_page.png"),
        ("/pages/portfolio.html", "04_portfolio_page.png"),
        ("/pages/press.html", "05_press_page.png"),
        ("/pages/tearsheet.html", "06_tearsheet_page.png"),
        ("/pages/navigation.html", "07_navigation_page.png"),
    ]
    
    driver = setup_driver()
    
    try:
        print("Starting website screenshots...")
        print("=" * 50)
        
        for path, filename in pages:
            url = base_url + path
            take_screenshot(driver, url, filename)
            take_mobile_screenshot(driver, url, filename)
            print("-" * 30)
        
        print("=" * 50)
        print("✓ All screenshots completed!")
        print(f"Screenshots saved in: {os.path.abspath('screenshots')}")
        
    except Exception as e:
        print(f"Error: {e}")
    
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
