# Quick Start Guide - ERP System

## For Replit

### Method 1: Using the Run Button (Recommended)
1. Click the green **Run** button at the top
2. Wait for the application to start
3. Click the provided URL to access the ERP system
4. Login with demo credentials

### Method 2: Using the Shell
```bash
bash run.sh
```

## Demo Login Credentials

### Admin User (Full Access)
- **Email**: `admin@demo.com`
- **Password**: `admin123`
- **Company**: TechCorp Solutions (Premium Plan)

### Regular User
- **Email**: `user@demo.com`
- **Password**: `user123`
- **Company**: TechCorp Solutions

### Manager User
- **Email**: `manager@demo.com`
- **Password**: `manager123`
- **Company**: Green Manufacturing Inc (Basic Plan)

## What's Included

The demo database includes:
- ✅ 3 user accounts (see above)
- ✅ 2 demo companies
- ✅ 8 employees with various roles
- ✅ 10 financial transactions
- ✅ 5 company assets
- ✅ 5 invoices/quotations
- ✅ 8 products in inventory
- ✅ 5 marketing campaigns
- ✅ 8 leads in various stages
- ✅ Sample notifications

## Exploring the System

### After Login, Try:

1. **Dashboard** - Overview of all statistics
2. **Finance Module** - Add transactions, view profit/loss
3. **Invoices** - Create new invoices or quotations
4. **HR Management** - View employee database, add new employees
5. **Marketing** - Track campaigns and leads, update lead status
6. **Inventory** - Check stock levels, record stock movements
7. **Notifications** - View system alerts
8. **Profile** - See your account and company details

## Adding New Data

### Create New Invoice
1. Go to **Invoices** → Click **Create Invoice/Quotation**
2. Fill in client details and amounts
3. Click **Create Invoice**

### Add Employee
1. Go to **HR Management** → Click **Add Employee**
2. Fill in personal and employment details
3. Click **Add Employee**

### Record Transaction
1. Go to **Finance** → Click **Add Transaction**
2. Select type (Income/Expense)
3. Fill in details and amount
4. Click **Add Transaction**

### Add Product
1. Go to **Inventory** → Click **Add Product**
2. Fill in product details and SKU
3. Set initial quantity and reorder level
4. Click **Add Product**

### Track Lead
1. Go to **Marketing** → Click **Add Lead**
2. Enter lead information
3. Update status as lead progresses

## Resetting Demo Data

If you want to reset the database to its original demo state:

```bash
python3 init_db.py
```

This will:
- Delete the current database
- Create a fresh database
- Populate it with demo data

## Features Demonstration

### Finance Module
- Track all income and expenses
- Automatic profit calculation
- Asset management
- Transaction history

### Invoicing
- Professional invoice generation
- Quotation creation
- Payment status tracking
- Auto-generated invoice numbers

### HR Management
- Complete employee database
- Department and role assignment
- Salary information
- Contract details storage

### Marketing
- Campaign budget tracking
- Lead conversion funnel
- Source tracking
- Status workflow

### Inventory
- Real-time stock levels
- Low stock alerts (shown in yellow)
- Stock movement tracking
- Category-based organization

## Tips

- **Low Stock Alert**: Products at or below reorder level are highlighted in yellow in the inventory
- **Notifications**: Unread notifications show a badge in the top navigation
- **Role-Based Access**: Admin users have full access to all features
- **Multi-Company**: Each company has its own isolated data

## Technical Details

- **Framework**: Flask 3.0.0 (Python)
- **Database**: SQLite (file-based, no external server needed)
- **Frontend**: Bootstrap 5.3.0 + Font Awesome
- **Port**: 5000 (default)

## Need Help?

Refer to the main **README.md** file for:
- Detailed feature descriptions
- Installation instructions
- Troubleshooting guide
- Project structure
- Customization options

## Next Steps

1. **Explore all modules** to see the full functionality
2. **Add your own data** to test the system
3. **Customize** the code for your specific needs
4. **Extend** with additional features

---

**Enjoy exploring the ERP System!** 🚀
