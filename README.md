# Mini ERP Demo (Flask)

A demo web-based ERP system built with Flask. It includes authentication, role-based access, and modules for Finance, HR, Marketing, and Inventory. The app seeds demo data on first run.

## Features
- User registration and login
- Company & subscription selection (Free/Basic/Premium) with dummy payment
- Role-based access (Admin/User)
- Dashboard with module shortcuts and notifications
- Finance: income/expenses, net profit, invoices/quotes, assets
- HR: employees (with document upload), department & tasks
- Marketing: campaigns, leads, simple analytics
- Inventory: products, categories, stock movements
- Demo data seeded automatically

## Quick Start (Local or Replit)

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the server:
```bash
python main.py
```

By default the server listens on `0.0.0.0:8080` (Replit-friendly). If `PORT` is set in the environment, it will use that.

3. Open the app in your browser and log in with the seeded admin user:
- Email: `admin@example.com`
- Password: `admin123`

## Notes
- This is a demo app, not production-ready. Authentication and authorization are basic.
- File uploads (employee contracts) are stored under `uploads/`.
- SQLite database file is `erp.db` in the project root.
