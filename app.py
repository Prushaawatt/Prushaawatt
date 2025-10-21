from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import os
import json

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp_system.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
CORS(app)

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.String(20), default='user')  # admin, user
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Company details
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', backref='users')

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50))
    location = db.Column(db.String(100))
    subscription = db.Column(db.String(20), default='free')  # free, basic, premium
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class FinanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # income, expense
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    category = db.Column(db.String(50))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    client_email = db.Column(db.String(120))
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, paid, overdue
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50))
    department = db.Column(db.String(50))
    salary = db.Column(db.Float)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='active')  # active, inactive

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    assigned_to = db.Column(db.Integer, db.ForeignKey('employee.id'))
    status = db.Column(db.String(20), default='pending')  # pending, in_progress, completed
    priority = db.Column(db.String(20), default='medium')  # low, medium, high
    due_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50))  # email, social, ads
    budget = db.Column(db.Float)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    status = db.Column(db.String(20), default='draft')  # draft, active, completed
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    source = db.Column(db.String(50))  # website, referral, campaign
    status = db.Column(db.String(20), default='new')  # new, contacted, qualified, converted
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    sku = db.Column(db.String(50), unique=True)
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    quantity = db.Column(db.Integer, default=0)
    min_stock = db.Column(db.Integer, default=10)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # in, out
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(100))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# API Routes
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create company first
    company = Company(
        name=data['company_name'],
        industry=data['industry'],
        location=data['location'],
        subscription=data.get('subscription', 'free')
    )
    db.session.add(company)
    db.session.flush()  # Get company ID
    
    # Create user
    user = User(
        email=data['email'],
        password_hash=generate_password_hash(data['password']),
        full_name=data['full_name'],
        phone=data.get('phone'),
        address=data.get('address'),
        role='admin',  # First user is admin
        company_id=company.id
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful', 'user_id': user.id})

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and check_password_hash(user.password_hash, data['password']):
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role,
                'company': {
                    'id': user.company.id,
                    'name': user.company.name,
                    'subscription': user.company.subscription
                } if user.company else None
            }
        })
    
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'})

@app.route('/api/dashboard', methods=['GET'])
@login_required
def dashboard():
    company_id = current_user.company_id
    
    # Get dashboard statistics
    total_income = db.session.query(db.func.sum(FinanceRecord.amount)).filter_by(
        company_id=company_id, type='income'
    ).scalar() or 0
    
    total_expenses = db.session.query(db.func.sum(FinanceRecord.amount)).filter_by(
        company_id=company_id, type='expense'
    ).scalar() or 0
    
    net_profit = total_income - total_expenses
    
    employee_count = Employee.query.filter_by(company_id=company_id, status='active').count()
    pending_invoices = Invoice.query.filter_by(company_id=company_id, status='pending').count()
    active_campaigns = Campaign.query.filter_by(company_id=company_id, status='active').count()
    total_products = Product.query.filter_by(company_id=company_id).count()
    
    return jsonify({
        'stats': {
            'total_income': total_income,
            'total_expenses': total_expenses,
            'net_profit': net_profit,
            'employee_count': employee_count,
            'pending_invoices': pending_invoices,
            'active_campaigns': active_campaigns,
            'total_products': total_products
        }
    })

# Finance Routes
@app.route('/api/finance/records', methods=['GET', 'POST'])
@login_required
def finance_records():
    if request.method == 'POST':
        data = request.get_json()
        record = FinanceRecord(
            company_id=current_user.company_id,
            type=data['type'],
            amount=data['amount'],
            description=data['description'],
            category=data['category'],
            created_by=current_user.id
        )
        db.session.add(record)
        db.session.commit()
        return jsonify({'message': 'Record added successfully'})
    
    records = FinanceRecord.query.filter_by(company_id=current_user.company_id).order_by(FinanceRecord.date.desc()).all()
    return jsonify([{
        'id': r.id,
        'type': r.type,
        'amount': r.amount,
        'description': r.description,
        'category': r.category,
        'date': r.date.isoformat()
    } for r in records])

@app.route('/api/finance/invoices', methods=['GET', 'POST'])
@login_required
def invoices():
    if request.method == 'POST':
        data = request.get_json()
        invoice = Invoice(
            company_id=current_user.company_id,
            invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{Invoice.query.count() + 1:03d}",
            client_name=data['client_name'],
            client_email=data['client_email'],
            amount=data['amount'],
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None,
            created_by=current_user.id
        )
        db.session.add(invoice)
        db.session.commit()
        return jsonify({'message': 'Invoice created successfully'})
    
    invoices = Invoice.query.filter_by(company_id=current_user.company_id).order_by(Invoice.created_at.desc()).all()
    return jsonify([{
        'id': i.id,
        'invoice_number': i.invoice_number,
        'client_name': i.client_name,
        'client_email': i.client_email,
        'amount': i.amount,
        'status': i.status,
        'due_date': i.due_date.isoformat() if i.due_date else None,
        'created_at': i.created_at.isoformat()
    } for i in invoices])

# HR Routes
@app.route('/api/hr/employees', methods=['GET', 'POST'])
@login_required
def employees():
    if request.method == 'POST':
        data = request.get_json()
        employee = Employee(
            company_id=current_user.company_id,
            full_name=data['full_name'],
            email=data['email'],
            phone=data['phone'],
            role=data['role'],
            department=data['department'],
            salary=data['salary']
        )
        db.session.add(employee)
        db.session.commit()
        return jsonify({'message': 'Employee added successfully'})
    
    employees = Employee.query.filter_by(company_id=current_user.company_id).all()
    return jsonify([{
        'id': e.id,
        'full_name': e.full_name,
        'email': e.email,
        'phone': e.phone,
        'role': e.role,
        'department': e.department,
        'salary': e.salary,
        'hire_date': e.hire_date.isoformat(),
        'status': e.status
    } for e in employees])

@app.route('/api/hr/tasks', methods=['GET', 'POST'])
@login_required
def tasks():
    if request.method == 'POST':
        data = request.get_json()
        task = Task(
            company_id=current_user.company_id,
            title=data['title'],
            description=data['description'],
            assigned_to=data.get('assigned_to'),
            priority=data.get('priority', 'medium'),
            due_date=datetime.fromisoformat(data['due_date']) if data.get('due_date') else None
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'})
    
    tasks = Task.query.filter_by(company_id=current_user.company_id).all()
    return jsonify([{
        'id': t.id,
        'title': t.title,
        'description': t.description,
        'assigned_to': t.assigned_to,
        'status': t.status,
        'priority': t.priority,
        'due_date': t.due_date.isoformat() if t.due_date else None,
        'created_at': t.created_at.isoformat()
    } for t in tasks])

# Marketing Routes
@app.route('/api/marketing/campaigns', methods=['GET', 'POST'])
@login_required
def campaigns():
    if request.method == 'POST':
        data = request.get_json()
        campaign = Campaign(
            company_id=current_user.company_id,
            name=data['name'],
            type=data['type'],
            budget=data['budget'],
            start_date=datetime.fromisoformat(data['start_date']) if data.get('start_date') else None,
            end_date=datetime.fromisoformat(data['end_date']) if data.get('end_date') else None
        )
        db.session.add(campaign)
        db.session.commit()
        return jsonify({'message': 'Campaign created successfully'})
    
    campaigns = Campaign.query.filter_by(company_id=current_user.company_id).all()
    return jsonify([{
        'id': c.id,
        'name': c.name,
        'type': c.type,
        'budget': c.budget,
        'start_date': c.start_date.isoformat() if c.start_date else None,
        'end_date': c.end_date.isoformat() if c.end_date else None,
        'status': c.status,
        'created_at': c.created_at.isoformat()
    } for c in campaigns])

@app.route('/api/marketing/leads', methods=['GET', 'POST'])
@login_required
def leads():
    if request.method == 'POST':
        data = request.get_json()
        lead = Lead(
            company_id=current_user.company_id,
            name=data['name'],
            email=data['email'],
            phone=data['phone'],
            source=data['source'],
            notes=data.get('notes')
        )
        db.session.add(lead)
        db.session.commit()
        return jsonify({'message': 'Lead added successfully'})
    
    leads = Lead.query.filter_by(company_id=current_user.company_id).all()
    return jsonify([{
        'id': l.id,
        'name': l.name,
        'email': l.email,
        'phone': l.phone,
        'source': l.source,
        'status': l.status,
        'notes': l.notes,
        'created_at': l.created_at.isoformat()
    } for l in leads])

# Inventory Routes
@app.route('/api/inventory/products', methods=['GET', 'POST'])
@login_required
def products():
    if request.method == 'POST':
        data = request.get_json()
        product = Product(
            company_id=current_user.company_id,
            name=data['name'],
            sku=data['sku'],
            category=data['category'],
            price=data['price'],
            quantity=data['quantity'],
            min_stock=data.get('min_stock', 10),
            description=data.get('description')
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product added successfully'})
    
    products = Product.query.filter_by(company_id=current_user.company_id).all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'sku': p.sku,
        'category': p.category,
        'price': p.price,
        'quantity': p.quantity,
        'min_stock': p.min_stock,
        'description': p.description,
        'created_at': p.created_at.isoformat()
    } for p in products])

@app.route('/api/inventory/stock-movement', methods=['POST'])
@login_required
def stock_movement():
    data = request.get_json()
    product = Product.query.get(data['product_id'])
    
    if not product or product.company_id != current_user.company_id:
        return jsonify({'error': 'Product not found'}), 404
    
    movement = StockMovement(
        product_id=data['product_id'],
        type=data['type'],
        quantity=data['quantity'],
        reason=data['reason'],
        created_by=current_user.id
    )
    
    # Update product quantity
    if data['type'] == 'in':
        product.quantity += data['quantity']
    else:
        product.quantity -= data['quantity']
    
    db.session.add(movement)
    db.session.commit()
    
    return jsonify({'message': 'Stock movement recorded successfully'})

# Serve React App
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

def init_demo_data():
    """Initialize demo data for testing"""
    if Company.query.first():
        return  # Demo data already exists
    
    # Create demo company
    demo_company = Company(
        name="Demo Corp",
        industry="Technology",
        location="San Francisco, CA",
        subscription="premium"
    )
    db.session.add(demo_company)
    db.session.flush()
    
    # Create demo admin user
    admin_user = User(
        email="admin@demo.com",
        password_hash=generate_password_hash("admin123"),
        full_name="Admin User",
        phone="+1-555-0123",
        address="123 Demo Street, San Francisco, CA",
        role="admin",
        company_id=demo_company.id
    )
    db.session.add(admin_user)
    db.session.flush()
    
    # Create demo employees
    employees = [
        Employee(company_id=demo_company.id, full_name="John Smith", email="john@demo.com", role="Developer", department="IT", salary=75000),
        Employee(company_id=demo_company.id, full_name="Jane Doe", email="jane@demo.com", role="Designer", department="Marketing", salary=65000),
        Employee(company_id=demo_company.id, full_name="Bob Johnson", email="bob@demo.com", role="Sales Rep", department="Sales", salary=55000)
    ]
    for emp in employees:
        db.session.add(emp)
    
    # Create demo finance records
    finance_records = [
        FinanceRecord(company_id=demo_company.id, type="income", amount=50000, description="Product Sales", category="Revenue", created_by=admin_user.id),
        FinanceRecord(company_id=demo_company.id, type="income", amount=25000, description="Consulting Services", category="Services", created_by=admin_user.id),
        FinanceRecord(company_id=demo_company.id, type="expense", amount=15000, description="Office Rent", category="Operations", created_by=admin_user.id),
        FinanceRecord(company_id=demo_company.id, type="expense", amount=8000, description="Marketing Campaign", category="Marketing", created_by=admin_user.id)
    ]
    for record in finance_records:
        db.session.add(record)
    
    # Create demo invoices
    invoices = [
        Invoice(company_id=demo_company.id, invoice_number="INV-001", client_name="ABC Corp", client_email="billing@abc.com", amount=15000, status="paid", created_by=admin_user.id),
        Invoice(company_id=demo_company.id, invoice_number="INV-002", client_name="XYZ Ltd", client_email="accounts@xyz.com", amount=22000, status="pending", created_by=admin_user.id)
    ]
    for invoice in invoices:
        db.session.add(invoice)
    
    # Create demo campaigns
    campaigns = [
        Campaign(company_id=demo_company.id, name="Summer Sale 2024", type="email", budget=5000, status="active"),
        Campaign(company_id=demo_company.id, name="Social Media Push", type="social", budget=3000, status="completed")
    ]
    for campaign in campaigns:
        db.session.add(campaign)
    
    # Create demo leads
    leads = [
        Lead(company_id=demo_company.id, name="Alice Cooper", email="alice@potential.com", phone="+1-555-0456", source="website", status="new"),
        Lead(company_id=demo_company.id, name="Charlie Brown", email="charlie@prospect.com", phone="+1-555-0789", source="referral", status="contacted")
    ]
    for lead in leads:
        db.session.add(lead)
    
    # Create demo products
    products = [
        Product(company_id=demo_company.id, name="Laptop Pro", sku="LAP-001", category="Electronics", price=1299.99, quantity=50, min_stock=10),
        Product(company_id=demo_company.id, name="Wireless Mouse", sku="MOU-001", category="Accessories", price=29.99, quantity=200, min_stock=25),
        Product(company_id=demo_company.id, name="Office Chair", sku="CHR-001", category="Furniture", price=299.99, quantity=25, min_stock=5)
    ]
    for product in products:
        db.session.add(product)
    
    db.session.commit()
    print("Demo data initialized successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_demo_data()
    
    app.run(host='0.0.0.0', port=5000, debug=True)