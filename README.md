# Demo Web-Based ERP System

A comprehensive Enterprise Resource Planning (ERP) system built with Flask (Python) featuring multiple business modules for managing finance, human resources, marketing, and inventory.

## Features

### 1. User Authentication & Account Management
- User registration with personal and company details
- Secure login/logout system
- Multi-company support
- Subscription plan selection (Free, Basic, Premium)
- Role-based access control (Admin/User)

### 2. Dashboard
- Real-time statistics and KPIs
- Quick access to all modules
- Recent notifications
- Company information summary

### 3. Finance Module
- Track income and expenses
- Calculate net profit automatically
- Manage company assets
- Transaction history
- Financial reporting

### 4. Invoicing System
- Create invoices and quotations
- Client management
- Track payment status
- Auto-generate invoice numbers

### 5. HR Management
- Employee database with personal details
- Role and department assignment
- Salary information
- Contract document storage
- Employee status tracking

### 6. Marketing Module
- Marketing campaign management
- Lead tracking and conversion
- Lead status workflow (New → Contacted → Qualified → Converted/Lost)
- Campaign budget and timeline tracking
- Analytics dashboard

### 7. Inventory/POM Module
- Product catalog management
- Stock tracking (in/out movements)
- Low stock alerts
- Category-based organization
- Reorder level management
- SKU tracking

### 8. Additional Features
- Notification system
- User profile management
- Responsive design with Bootstrap 5
- Modern, clean UI with Font Awesome icons
- Demo data preloaded for testing

## Technology Stack

- **Backend**: Flask 3.0.0 (Python)
- **Database**: SQLite (included, no setup required)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login
- **Frontend**: HTML5, CSS3, JavaScript
- **UI Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0

## Installation & Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Quick Start

1. **Clone or download this repository**

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize the database with demo data**
```bash
python init_db.py
```

This will create the database and populate it with sample data including:
- 3 demo user accounts
- 2 demo companies
- Sample employees, transactions, products, leads, and more

4. **Run the application**
```bash
python app.py
```

5. **Access the application**

Open your web browser and navigate to:
```
http://localhost:5000
```

## Demo Login Credentials

### Admin User (TechCorp Solutions)
- **Email**: admin@demo.com
- **Password**: admin123
- **Role**: Administrator
- **Access**: Full access to all features

### Regular User (TechCorp Solutions)
- **Email**: user@demo.com
- **Password**: user123
- **Role**: User
- **Access**: Standard user permissions

### Manager User (Green Manufacturing Inc)
- **Email**: manager@demo.com
- **Password**: manager123
- **Role**: Administrator
- **Access**: Full access to own company data

## Running on Replit

1. **Create a new Repl** and upload all files

2. **Install dependencies** (automatically or manually)
```bash
pip install -r requirements.txt
```

3. **Initialize database**
```bash
python init_db.py
```

4. **Run the application**
```bash
python app.py
```

5. **Configure Replit**
   - The app will run on `0.0.0.0:5000`
   - Replit will provide a URL to access your application
   - Use the provided demo credentials to login

## Project Structure

```
.
├── app.py                 # Main Flask application
├── models.py             # Database models
├── config.py             # Application configuration
├── init_db.py            # Database initialization script
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── templates/           # HTML templates
│   ├── base.html        # Base template with navigation
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── dashboard.html   # Main dashboard
│   ├── finance.html     # Finance module
│   ├── invoices.html    # Invoice list
│   ├── add_invoice.html # Create invoice
│   ├── hr.html          # HR management
│   ├── marketing.html   # Marketing module
│   ├── inventory.html   # Inventory management
│   ├── notifications.html # Notifications
│   └── profile.html     # User profile
└── erp_demo.db          # SQLite database (created after init_db.py)
```

## Module Descriptions

### Finance Module (`/finance`)
- Add income and expense transactions
- Track company assets
- View transaction history
- Real-time profit/loss calculation
- Asset valuation

### Invoicing (`/invoices`)
- Create professional invoices
- Generate quotations
- Track payment status
- Client information management
- Auto-calculated totals with tax

### HR Management (`/hr`)
- Comprehensive employee database
- Department organization
- Salary tracking
- Contract management
- Employee status monitoring

### Marketing (`/marketing`)
- Campaign creation and tracking
- Lead management system
- Conversion rate analytics
- Lead source tracking
- Status workflow management

### Inventory (`/inventory`)
- Product catalog with SKU
- Stock movement tracking
- Low stock alerts
- Category management
- Reorder level monitoring

## Security Notes

⚠️ **This is a DEMO application** - Not production-ready!

- Uses demo/development secret key
- Basic password hashing (suitable for demo)
- No email verification
- No advanced security features
- SQLite database (single-file, suitable for demo)

For production use, you should:
- Change the SECRET_KEY in config.py
- Use a production database (PostgreSQL, MySQL)
- Add email verification
- Implement rate limiting
- Add CSRF protection
- Use HTTPS
- Add more robust authentication

## Customization

### Adding New Features
1. Add database models in `models.py`
2. Create routes in `app.py`
3. Design templates in `templates/`
4. Update navigation in `base.html`

### Changing Subscription Plans
Edit the subscription plans in:
- `templates/register.html`
- `templates/profile.html`

### Modifying Demo Data
Edit `init_db.py` to customize:
- Demo companies
- Sample users
- Test data for each module

## Troubleshooting

### Database Issues
If you encounter database errors:
```bash
rm erp_demo.db
python init_db.py
```

### Port Already in Use
Change the port in `app.py`:
```python
app.run(host='0.0.0.0', port=5001, debug=True)
```

### Missing Dependencies
Reinstall all requirements:
```bash
pip install -r requirements.txt --force-reinstall
```

## Future Enhancements

Potential features for expansion:
- Report generation (PDF exports)
- Email notifications
- Calendar/scheduling system
- Document management
- Advanced analytics and charts
- API endpoints for integrations
- Mobile-responsive improvements
- Multi-language support

## License

This is a demo project for educational purposes. Feel free to use and modify as needed.

## Support

For issues or questions about this demo:
1. Check the troubleshooting section
2. Review the demo login credentials
3. Ensure all dependencies are installed
4. Verify Python version compatibility

---

**Note**: This ERP system is designed as a working demo to showcase various business management features. While functional, it should be enhanced with proper security, scalability, and error handling before production use.
