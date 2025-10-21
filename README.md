# ERP Demo System

A comprehensive web-based ERP (Enterprise Resource Planning) system built with Python Flask and modern frontend technologies. This demo showcases all major business management modules with a clean, responsive interface.

## 🚀 Features

### 🔐 User Authentication & Accounts
- User registration and login system
- Personal details collection (name, email, phone, address)
- Company/brand details (company name, industry, location)
- Subscription selection (Free, Basic, Premium)
- Secure password hashing and session management

### 📊 Dashboard
- Comprehensive overview with key metrics
- Module navigation with clickable menu
- Real-time statistics and financial overview
- Company information display

### 💰 Finance Module
- Track income and expenses
- Calculate net profit automatically
- Generate invoices and quotations
- Transaction history with filtering
- Financial analytics and reporting

### 👥 HR Module
- Employee database with personal details
- Role and salary management
- Task assignment and tracking
- Department organization
- Employee contract management

### 📈 Marketing Module
- Marketing campaign management
- Lead tracking and pipeline
- Client relationship management
- Campaign analytics dashboard
- Lead source tracking

### 📦 Inventory/POM Module
- Product and asset management
- Quantity tracking (in/out)
- Category organization
- Low stock alerts
- Inventory valuation

### 🔔 Additional Features
- Multi-user support with role-based access
- Responsive design for all devices
- Modern UI with Bootstrap 5
- Real-time notifications
- Preloaded demo data for testing

## 🛠️ Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite (easily configurable for production)
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **UI Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Authentication**: Flask-Login
- **ORM**: SQLAlchemy

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd erp-demo-system

# Or download and extract the files
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application
```bash
python app.py
```

### 4. Access the System
Open your web browser and navigate to:
```
http://localhost:3000
```

**Alternative**: Use the startup script for easier setup:
```bash
python3 run.py
```

## 🔑 Demo Account

For immediate testing, use the pre-loaded demo account:
- **Email**: demo@erp.com
- **Password**: demo123

## 📱 Usage Guide

### Getting Started
1. **Register**: Create a new account or use the demo account
2. **Login**: Access your personalized dashboard
3. **Explore Modules**: Navigate through Finance, HR, Marketing, and Inventory modules
4. **Add Data**: Use the forms to add transactions, employees, campaigns, and products
5. **View Analytics**: Check the dashboard for real-time statistics

### Module Overview

#### Finance Module
- Add income and expense transactions
- Create invoices for clients
- View transaction history
- Monitor financial health

#### HR Module
- Add employees with complete details
- Assign tasks to team members
- Track employee information
- Manage departments

#### Marketing Module
- Create marketing campaigns
- Track leads and prospects
- Monitor campaign performance
- Manage client relationships

#### Inventory Module
- Add products and services
- Track stock quantities
- Monitor low stock alerts
- Calculate inventory value

## 🗄️ Database Schema

The system uses SQLite with the following main entities:
- **Users**: User accounts and authentication
- **Companies**: Business information
- **Employees**: Staff management
- **FinanceTransactions**: Income/expense tracking
- **Invoices**: Client billing
- **Products**: Inventory items
- **Campaigns**: Marketing activities
- **Leads**: Prospect management
- **Tasks**: Project assignments

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styling
- Bootstrap 5 classes are used throughout for consistency
- Responsive design ensures mobile compatibility

### Functionality
- Add new modules by creating routes in `app.py`
- Extend models in `models.py` for new data structures
- Modify templates in the `templates/` directory

## 🔧 Configuration

### Environment Variables
Create a `.env` file for production settings:
```
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///erp_demo.db
```

### Database
- Default: SQLite (development)
- Production: Configure PostgreSQL/MySQL in `app.py`

## 📊 Sample Data

The system comes pre-loaded with sample data including:
- Demo company and user account
- Sample employees and tasks
- Financial transactions and invoices
- Marketing campaigns and leads
- Product inventory

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. Set up a production database (PostgreSQL/MySQL)
2. Configure environment variables
3. Use a WSGI server like Gunicorn
4. Set up reverse proxy with Nginx

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is for demonstration purposes. Feel free to use and modify as needed.

## 🆘 Support

For issues or questions:
1. Check the demo account first
2. Review the code comments
3. Check the browser console for errors
4. Ensure all dependencies are installed

## 🔮 Future Enhancements

- Advanced reporting and analytics
- Email notifications
- File upload capabilities
- Advanced user roles and permissions
- API endpoints for mobile apps
- Integration with external services
- Advanced inventory management
- Time tracking and project management

---

**Note**: This is a demo system designed for showcasing ERP functionality. For production use, implement proper security measures, data validation, and error handling.