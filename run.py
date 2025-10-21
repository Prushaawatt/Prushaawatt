#!/usr/bin/env python3
"""
ERP System Demo - Main Runner Script
This script handles both development and production modes.
"""

import os
import sys
import subprocess
import threading
import time
from pathlib import Path

def install_python_dependencies():
    """Install Python dependencies"""
    print("📦 Installing Python dependencies...")
    try:
        subprocess.check_call(["python3", "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Python dependencies: {e}")
        return False

def install_node_dependencies():
    """Install Node.js dependencies for React frontend"""
    print("📦 Installing Node.js dependencies...")
    frontend_dir = Path("frontend")
    
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return False
    
    try:
        # Check if npm is available
        subprocess.check_call(["npm", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ npm not found! Please install Node.js and npm first.")
        return False
    
    try:
        subprocess.check_call(["npm", "install"], cwd=frontend_dir)
        print("✅ Node.js dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install Node.js dependencies: {e}")
        return False

def build_frontend():
    """Build the React frontend for production"""
    print("🏗️  Building React frontend...")
    frontend_dir = Path("frontend")
    
    try:
        subprocess.check_call(["npm", "run", "build"], cwd=frontend_dir)
        print("✅ Frontend built successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to build frontend: {e}")
        return False

def run_flask_app():
    """Run the Flask application"""
    print("🚀 Starting Flask server...")
    try:
        # Import and run the Flask app
        from app import app
        app.run(host='0.0.0.0', port=5000, debug=False)
    except Exception as e:
        print(f"❌ Failed to start Flask server: {e}")
        sys.exit(1)

def run_development_mode():
    """Run in development mode with hot reloading"""
    print("🔧 Starting development mode...")
    
    def run_flask():
        print("🚀 Starting Flask development server...")
        try:
            from app import app
            app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
        except Exception as e:
            print(f"❌ Failed to start Flask server: {e}")
    
    def run_react():
        print("🚀 Starting React development server...")
        frontend_dir = Path("frontend")
        try:
            subprocess.check_call(["npm", "start"], cwd=frontend_dir)
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to start React server: {e}")
    
    # Start Flask in a separate thread
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Give Flask a moment to start
    time.sleep(2)
    
    # Start React (this will block)
    run_react()

def main():
    """Main entry point"""
    print("🏢 ERP System Demo")
    print("=" * 50)
    
    # Check if we're in development mode
    dev_mode = "--dev" in sys.argv or os.getenv("FLASK_ENV") == "development"
    
    # Install Python dependencies
    if not install_python_dependencies():
        sys.exit(1)
    
    if dev_mode:
        print("🔧 Running in DEVELOPMENT mode")
        # Install Node dependencies for development
        if not install_node_dependencies():
            sys.exit(1)
        run_development_mode()
    else:
        print("🚀 Running in PRODUCTION mode")
        # Install Node dependencies and build frontend
        if not install_node_dependencies():
            sys.exit(1)
        if not build_frontend():
            sys.exit(1)
        run_flask_app()

if __name__ == "__main__":
    main()