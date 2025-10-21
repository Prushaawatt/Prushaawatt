# ERP Demo System

A comprehensive web-based Enterprise Resource Planning (ERP) system built with Python Flask and modern frontend technologies. This demo system includes all major business modules with a responsive, user-friendly interface.

## 🚀 Features

### Core Modules
- **User Authentication & Management** - Registration, login, role-based access control
- **Dashboard** - Real-time overview with key metrics and charts
- **Finance Management** - Income/expense tracking, invoice generation, profit calculation
- **Human Resources** - Employee database, task assignment, contract management
- **Marketing Tools** - Campaign management, lead tracking, client database
- **Inventory Control** - Product management, stock tracking, transaction history

### Technical Features
- **Responsive Design** - Works on desktop, tablet, and mobile devices
- **Modern UI/UX** - Bootstrap 5 with custom styling and animations
- **Real-time Updates** - Live dashboard statistics and notifications
- **Role-based Access** - Admin and User roles with appropriate permissions
- **Demo Data** - Preloaded sample data for immediate testing
- **Export Functionality** - Export data in various formats (PDF, Excel, CSV)

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, Flask, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (for demo purposes)
- **Charts**: Chart.js for data visualization
- **Icons**: Font Awesome 6

## 📋 Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## 🚀 Quick Start

### 1. Clone or Download
```bash
# If using git
git clone <repository-url>
cd erp-demo-system

# Or download and extract the ZIP file
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
http://localhost:5000
```

## 👤 Demo Account

The system comes with a pre-configured demo account:

- **Username**: `admin`
- **Password**: `admin123`
- **Role**: Administrator

## 📊 Sample Data

The system includes preloaded demo data:
- Sample financial transactions
- Employee records
- Marketing campaigns and leads
- Inventory products and transactions
- Company information

## 🎯 Usage Guide

### 1. Login
- Use the demo account or create a new account
- The system will redirect you to the dashboard after successful login

### 2. Dashboard
- View key business metrics
- Access all modules from the navigation menu
- Monitor recent activities and transactions

### 3. Finance Module
- Add income and expense transactions
- Create and manage invoices
- View financial reports and profit calculations

### 4. HR Module
- Add and manage employee records
- Assign tasks to employees
- Track employee performance and contracts

### 5. Marketing Module
- Create marketing campaigns
- Track leads and convert them to clients
- Monitor campaign performance

### 6. Inventory Module
- Add products and manage stock levels
- Record stock in/out transactions
- Set reorder levels and alerts

## 🔧 Configuration

### Database
The system uses SQLite by default. To use a different database:

1. Update the `SQLALCHEMY_DATABASE_URI` in `app.py`
2. Example for PostgreSQL:
   ```python
   app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/erp_db'
   ```

### Security
For production use:
1. Change the `SECRET_KEY` in `app.py`
2. Use environment variables for sensitive data
3. Implement proper password hashing and validation
4. Add CSRF protection

## 📁 Project Structure

```
erp-demo-system/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # HTML templates
│   ├── base.html        # Base template
│   ├── index.html       # Landing page
│   ├── login.html       # Login page
│   ├── register.html    # Registration page
│   ├── dashboard.html   # Main dashboard
│   ├── finance.html     # Finance module
│   ├── hr.html          # HR module
│   ├── marketing.html   # Marketing module
│   └── inventory.html   # Inventory module
└── static/              # Static assets
    ├── css/
    │   └── style.css    # Custom styles
    └── js/
        └── main.js      # JavaScript functions
```

## 🎨 Customization

### Styling
- Modify `static/css/style.css` for custom styling
- Update color scheme by changing CSS variables
- Add custom animations and effects

### Functionality
- Add new modules by creating new routes in `app.py`
- Extend database models in the models section
- Add new API endpoints for AJAX functionality

## 🐛 Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Change port in app.py
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **Database errors**
   ```bash
   # Delete the database file and restart
   rm erp_demo.db
   python app.py
   ```

3. **Module not found**
   ```bash
   # Install missing dependencies
   pip install -r requirements.txt
   ```

## 📈 Future Enhancements

- [ ] Advanced reporting and analytics
- [ ] Email notifications
- [ ] File upload functionality
- [ ] Advanced user roles and permissions
- [ ] API endpoints for mobile apps
- [ ] Integration with external services
- [ ] Advanced search and filtering
- [ ] Data backup and restore

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for demonstration purposes. Feel free to use and modify as needed.

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review the code comments
3. Create an issue in the repository

## 🎉 Demo Features

### Interactive Elements
- Responsive navigation with hover effects
- Modal forms for data entry
- Real-time dashboard updates
- Tabbed interfaces for better organization
- Status badges and progress indicators

### Data Visualization
- Revenue vs expenses charts
- Module usage statistics
- Financial overview cards
- Inventory status indicators

### User Experience
- Intuitive navigation
- Form validation
- Success/error notifications
- Loading states and animations
- Mobile-responsive design

---

**Note**: This is a demo system designed for educational and demonstration purposes. For production use, additional security measures, error handling, and performance optimizations should be implemented.