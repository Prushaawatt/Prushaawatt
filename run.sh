#!/bin/bash

echo "================================================"
echo "  ERP System - Starting Application"
echo "================================================"
echo ""

# Check if database exists
if [ ! -f "erp_demo.db" ]; then
    echo "Database not found. Initializing with demo data..."
    python3 init_db.py
    echo ""
fi

echo "Starting Flask application..."
echo ""
echo "Login Credentials:"
echo "  Admin: admin@demo.com / admin123"
echo "  User: user@demo.com / user123"
echo ""
echo "================================================"
echo ""

python3 app.py
