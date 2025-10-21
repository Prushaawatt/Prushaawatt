# ERP System Demo

A comprehensive web-based Enterprise Resource Planning (ERP) system built with Flask (Python) backend and React frontend. This demo showcases all major ERP modules including Finance, HR, Marketing, and Inventory management.

## 🌟 Features

### 🔐 User Authentication & Accounts
- User registration and login system
- Personal details management (name, email, phone, address)
- Company/brand details (company name, industry, location)
- Subscription plans (Free, Basic, Premium)
- Demo payment integration

### 📊 Dashboard
- Comprehensive overview of all business metrics
- Real-time statistics and KPIs
- Quick access to all modules
- Company information display

### 💰 Finance Module
- Income and expense tracking
- Net profit calculation
- Invoice generation and management
- Transaction history
- Financial reporting

### 👥 HR Module
- Employee database management
- Role and department assignment
- Salary tracking
- Task assignment and management
- Employee status monitoring

### 📢 Marketing Module
- Marketing campaign management
- Lead tracking and management
- Campaign performance analytics
- Lead source analysis
- Conversion tracking

### 📦 Inventory/POM Module
- Product catalog management
- Stock level monitoring
- Low stock alerts
- Stock movement tracking
- Category-based organization

### 🔒 Additional Features
- Role-based access control (Admin/User)
- Responsive, modern UI design
- Real-time notifications
- Demo data for testing
- Multi-user support

## 🚀 Quick Start

### Prerequisites
- Python 3.7+ 
- Node.js 14+ and npm
- Git

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd erp-system-demo
   ```

2. **Run the application:**
   
   **For Production (Recommended for Replit):**
   ```bash
   python run.py
   ```
   
   **For Development:**
   ```bash
   python run.py --dev
   ```

3. **Access the application:**
   - Open your browser and go to `http://localhost:5000`
   - Use the demo credentials to login

## 🔑 Demo Credentials

**Admin Account:**
- Email: `admin@demo.com`
- Password: `admin123`

This account has full access to all modules and demo data.

## 📁 Project Structure

```
erp-system-demo/
├── app.py                 # Flask backend application
├── requirements.txt       # Python dependencies
├── run.py                # Main runner script
├── README.md             # This file
├── frontend/             # React frontend
│   ├── public/          # Static files
│   ├── src/             # React source code
│   │   ├── components/  # Reusable components
│   │   ├── pages/       # Page components
│   │   ├── services/    # API services
│   │   └── App.js       # Main App component
│   └── package.json     # Node.js dependencies
└── erp_system.db        # SQLite database (created on first run)
```

## 🛠️ Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **Flask-Login** - User session management
- **SQLite** - Database (easily replaceable)

### Frontend
- **React** - UI framework
- **React Router** - Navigation
- **Axios** - HTTP client
- **CSS3** - Styling with modern design

## 📱 Responsive Design

The application is fully responsive and works seamlessly on:
- Desktop computers
- Tablets
- Mobile phones

## 🔧 Development

### Running in Development Mode

```bash
python run.py --dev
```

This will:
- Start Flask with debug mode and hot reloading
- Start React development server with hot reloading
- Enable CORS for cross-origin requests

### Project Architecture

- **Backend API**: RESTful API built with Flask
- **Frontend**: Single Page Application (SPA) with React
- **Database**: SQLite with SQLAlchemy ORM
- **Authentication**: Session-based with Flask-Login

## 🚀 Deployment

### Replit Deployment

1. **Import the project** into Replit
2. **Run the application:**
   ```bash
   python run.py
   ```
3. **Access via Replit's provided URL**

### Other Platforms

The application can be deployed on:
- Heroku
- DigitalOcean
- AWS
- Google Cloud Platform
- Any platform supporting Python and Node.js

## 📊 Demo Data

The system comes pre-loaded with demo data including:
- Sample company (Demo Corp)
- Demo employees and departments
- Financial records and invoices
- Marketing campaigns and leads
- Product inventory

## 🔒 Security Features

- Password hashing with Werkzeug
- Session management
- CSRF protection (can be enabled)
- Input validation
- SQL injection prevention through ORM

## 🎯 Use Cases

This ERP system is perfect for:
- Small to medium businesses
- Startups needing integrated business management
- Educational purposes and learning
- Proof of concept for larger ERP implementations
- Portfolio demonstrations

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source and available under the MIT License.

## 📞 Support

For questions, issues, or feature requests, please:
1. Check the existing documentation
2. Search through existing issues
3. Create a new issue with detailed information

## 🔮 Future Enhancements

Potential improvements for production use:
- Advanced reporting and analytics
- Email notifications
- File upload and document management
- Advanced user permissions
- API rate limiting
- Automated backups
- Integration with external services
- Mobile app development

---

**Built with ❤️ for modern businesses**