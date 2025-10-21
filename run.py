#!/usr/bin/env python3
"""
ERP Demo System Startup Script
Run this script to start the ERP demo system
"""

import os
import sys
from app import app, db

def main():
    print("🚀 Starting ERP Demo System...")
    print("📊 Initializing database...")
    
    # Create database tables
    with app.app_context():
        db.create_all()
        print("✅ Database initialized successfully")
        
        # Check if demo data exists
        from models import User
        if User.query.count() == 0:
            print("📝 Creating demo data...")
            from demo_data import create_demo_data
            create_demo_data()
            print("✅ Demo data created successfully")
        else:
            print("ℹ️  Demo data already exists")
    
    print("\n🌐 Starting web server...")
    print("📍 Server will be available at: http://localhost:3000")
    print("🔑 Demo account: demo@erp.com / demo123")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        app.run(debug=True, host='0.0.0.0', port=3000)
    except KeyboardInterrupt:
        print("\n👋 Server stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()