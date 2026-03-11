"""
Silver Tier Dashboard Launcher
Start the dashboard server and open in browser automatically.
"""

import webbrowser
import sys
import time
import subprocess
from pathlib import Path

# Configuration
HOST = "0.0.0.0"
PORT = 8001
URL = f"http://localhost:{PORT}"

def check_dependencies():
    """Check if required dependencies are installed."""
    print("🔍 Checking dependencies...")
    
    required = ['fastapi', 'uvicorn', 'playwright']
    missing = []
    
    for package in required:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            print(f"  ❌ {package}")
            missing.append(package)
    
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print("\nInstall with:")
        print(f"  pip install {' '.join(missing)}")
        
        if 'playwright' in missing:
            print("\nAfter installing playwright, run:")
            print("  playwright install chromium")
        
        return False
    
    print("\n✅ All dependencies installed!\n")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("📦 Installing dependencies...")
    
    packages = ['fastapi', 'uvicorn', 'playwright', 'pydantic']
    
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + packages)
        print("\n✅ Dependencies installed!")
        
        # Install Playwright browsers
        print("\n🌐 Installing Playwright browsers...")
        subprocess.check_call([sys.executable, '-m', 'playwright', 'install', 'chromium'])
        print("✅ Browsers installed!")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Installation failed: {e}")
        return False

def start_server():
    """Start the dashboard server."""
    print(f"🚀 Starting Silver Tier Dashboard...")
    print(f"📍 Server: http://{HOST}:{PORT}")
    print(f"🌐 Dashboard: {URL}")
    print()
    print("="*60)
    print("Dashboard is starting...")
    print("Press Ctrl+C to stop the server")
    print("="*60)
    print()
    
    # Import and run uvicorn
    import uvicorn
    from dashboard_api import app
    
    uvicorn.run(app, host=HOST, port=PORT)

def open_browser():
    """Open dashboard in browser after a short delay."""
    time.sleep(2)
    webbrowser.open(URL)
    print(f"🌐 Opening dashboard in browser...")

def main():
    """Main entry point."""
    print()
    print("="*60)
    print("  🥈 Silver Tier Dashboard Launcher")
    print("  AI Employee v0.2 - Autonomous Automation")
    print("="*60)
    print()
    
    # Check dependencies
    if not check_dependencies():
        response = input("\nWould you like to install missing dependencies? (y/n): ")
        if response.lower() == 'y':
            if install_dependencies():
                print("\n✅ Installation complete! Please run the launcher again.")
            else:
                print("\n❌ Installation failed. Please install manually.")
        else:
            print("\n❌ Cannot start without required dependencies.")
        return
    
    # Check if dashboard files exist
    dashboard_file = Path(__file__).parent / "dashboard" / "index.html"
    if not dashboard_file.exists():
        print("❌ Dashboard files not found!")
        print(f"   Expected at: {dashboard_file}")
        return
    
    print("✅ Dashboard files found")
    print(f"📁 Location: {Path(__file__).parent.absolute()}")
    print()
    
    # Start browser opener in background
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start server
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
