#!/usr/bin/env python3
"""
Setup script for website screenshot tool
Automatically installs dependencies and sets up Chrome driver
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Packages installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"✗ Error installing packages: {e}")
        return False
    return True

def install_chromedriver():
    """Install Chrome driver using webdriver-manager"""
    print("Setting up Chrome driver...")
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        
        # This will automatically download and setup Chrome driver
        driver_path = ChromeDriverManager().install()
        print(f"✓ Chrome driver installed at: {driver_path}")
        
        # Test the driver
        options = Options()
        options.add_argument("--headless")
        driver = webdriver.Chrome(options=options)
        driver.quit()
        print("✓ Chrome driver test successful!")
        
    except Exception as e:
        print(f"✗ Error setting up Chrome driver: {e}")
        return False
    return True

def main():
    print("Setting up website screenshot tool...")
    print("=" * 50)
    
    # Install requirements
    if not install_requirements():
        print("Failed to install requirements. Please check your Python/pip setup.")
        return
    
    # Install Chrome driver
    if not install_chromedriver():
        print("Failed to setup Chrome driver. Please make sure Chrome is installed.")
        return
    
    print("=" * 50)
    print("✓ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Start your local server (if not already running)")
    print("2. Update the base_url in screenshot_website.py if needed")
    print("3. Run: python screenshot_website.py")
    print("\nThe script will create screenshots of all pages in desktop and mobile views.")

if __name__ == "__main__":
    main()
