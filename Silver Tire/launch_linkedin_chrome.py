"""
LinkedIn Chrome Launcher - Opens LinkedIn in Chrome directly
"""
import subprocess
import os
import sys

print("="*60)
print("  LINKEDIN CHROME LAUNCHER")
print("="*60)
print()

# Find Chrome
chrome_paths = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]

chrome_path = None
for path in chrome_paths:
    if os.path.exists(path):
        chrome_path = path
        break

if not chrome_path:
    print("❌ ERROR: Google Chrome not found!")
    print()
    print("Please install Chrome from:")
    print("https://www.google.com/chrome/")
    print()
    input("Press Enter to exit...")
    sys.exit(1)

print(f"✅ Found Chrome: {chrome_path}")
print()

# Open LinkedIn in Chrome
linkedin_url = "https://www.linkedin.com/login"
print(f"🚀 Opening LinkedIn in Chrome...")
print(f"📍 URL: {linkedin_url}")
print()

try:
    subprocess.Popen([chrome_path, linkedin_url])
    print("✅ Chrome is opening!")
    print()
    print("="*60)
    print("  NEXT STEPS:")
    print("="*60)
    print("1. Login to LinkedIn IN CHROME")
    print("2. Navigate to your feed")
    print("3. Wait 10 seconds (saves session)")
    print("4. KEEP CHROME OPEN (don't close it!)")
    print("5. Go to dashboard: http://localhost:8001/working.html")
    print("6. Click 'Post to LinkedIn'")
    print("="*60)
    print()
    input("Press Enter after you've logged in...")
except Exception as e:
    print(f"❌ ERROR: {e}")
    input("Press Enter to exit...")
    sys.exit(1)
