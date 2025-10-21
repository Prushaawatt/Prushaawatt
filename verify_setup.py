#!/usr/bin/env python3
"""
ERP System Demo - Setup Verification
This script verifies that the system is properly set up and ready to run.
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python():
    """Check Python version"""
    print("🐍 Checking Python...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need Python 3.7+")
        return False

def check_dependencies():
    """Check if Python dependencies are installed"""
    print("📦 Checking Python dependencies...")
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
        import flask_cors
        print("✅ All Python dependencies installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def check_node():
    """Check if Node.js is available"""
    print("📦 Checking Node.js...")
    try:
        result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()} - OK")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False

def check_npm():
    """Check if npm is available"""
    print("📦 Checking npm...")
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm {result.stdout.strip()} - OK")
            return True
        else:
            print("❌ npm not found")
            return False
    except FileNotFoundError:
        print("❌ npm not found")
        return False

def check_flask_app():
    """Check if Flask app can be imported"""
    print("🌐 Checking Flask application...")
    try:
        from app import app, db
        print("✅ Flask app imports successfully")
        
        # Test database initialization
        with app.app_context():
            db.create_all()
        print("✅ Database initialization successful")
        return True
    except Exception as e:
        print(f"❌ Flask app error: {e}")
        return False

def check_file_structure():
    """Check if all required files exist"""
    print("📁 Checking file structure...")
    required_files = [
        "app.py",
        "requirements.txt",
        "run.py",
        "README.md",
        "frontend/package.json",
        "frontend/src/App.js",
        "frontend/public/index.html"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ All required files present")
        return True

def main():
    """Main verification function"""
    print("🏢 ERP System Demo - Setup Verification")
    print("=" * 50)
    
    checks = [
        check_python(),
        check_dependencies(),
        check_file_structure(),
        check_flask_app(),
        check_node(),
        check_npm()
    ]
    
    print("\n" + "=" * 50)
    
    if all(checks[:4]):  # Core checks (Python, deps, files, Flask)
        print("✅ CORE SYSTEM READY!")
        print("🚀 You can run the system with: python3 run.py")
        
        if all(checks[4:]):  # Node.js checks
            print("✅ DEVELOPMENT MODE AVAILABLE!")
            print("🔧 You can run in dev mode with: python3 run.py --dev")
        else:
            print("⚠️  Development mode not available (Node.js/npm missing)")
            print("   Production mode will work fine.")
        
        print("\n🔑 Demo Login Credentials:")
        print("   Email: admin@demo.com")
        print("   Password: admin123")
        
        return True
    else:
        print("❌ SYSTEM NOT READY!")
        print("   Please fix the issues above before running.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)