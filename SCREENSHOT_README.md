# Website Screenshot Tool

This tool automatically takes screenshots of all pages on Bianca's portfolio website for proofing and feedback.

## Quick Start

### 1. Setup (One-time)
```bash
python setup_screenshots.py
```

This will:
- Install required Python packages
- Download and setup Chrome driver automatically

### 2. Start Your Local Server
Make sure your website is running locally. If you're using the live server in VSCode, it should be running on `http://localhost:5500` or similar.

### 3. Update URL (if needed)
Edit `screenshot_website.py` and update the `base_url` variable to match your local server URL:
```python
base_url = "http://localhost:5500"  # or whatever port you're using
```

### 4. Run Screenshots
```bash
python screenshot_website.py
```

## What It Does

The script will create screenshots of:
- **Landing page** (desktop & mobile)
- **About page** (desktop & mobile)
- **Contact page** (desktop & mobile)
- **Portfolio page** (desktop & mobile)
- **Press page** (desktop & mobile)
- **Tearsheet page** (desktop & mobile)
- **Navigation page** (desktop & mobile)

## Output

Screenshots will be saved in a `screenshots/` folder:
- `01_landing_page.png` - Desktop landing page
- `mobile_01_landing_page.png` - Mobile landing page
- `02_about_page.png` - Desktop about page
- `mobile_02_about_page.png` - Mobile about page
- etc.

## Requirements

- Python 3.7+
- Google Chrome browser
- Local web server running

## Troubleshooting

### Chrome Driver Issues
If you get Chrome driver errors, try:
```bash
python setup_screenshots.py
```

### Port Issues
Make sure your local server is running and update the `base_url` in the script to match your server's port.

### Permission Issues
On Mac/Linux, you might need to make the script executable:
```bash
chmod +x screenshot_website.py
```

## Creating a PDF

After running the screenshots, you can:
1. Open the screenshots folder
2. Select all images
3. Right-click → "Print" or use a PDF tool to combine them
4. Save as a single PDF for easy sharing

## Notes

- The script runs Chrome in "headless" mode (no visible browser window)
- Desktop screenshots are 1920x1080
- Mobile screenshots are 375x812 (iPhone size)
- Each page waits 3 seconds to load completely
