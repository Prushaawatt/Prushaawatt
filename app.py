from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Import models and initialize db
from models import db, User, Company, Employee, FinanceTransaction, Invoice, Product, Campaign, Lead, Task
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email already registered'})
        
        # Create new user
        user = User(
            full_name=data['full_name'],
            email=data['email'],
            phone=data['phone'],
            address=data['address'],
            password_hash=generate_password_hash(data['password'])
        )
        
        # Create company
        company = Company(
            name=data['company_name'],
            industry=data['industry'],
            location=data['location'],
            subscription=data['subscription'],
            user_id=user.id
        )
        
        db.session.add(user)
        db.session.add(company)
        db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'message': 'Registration successful'})
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        
        if user and check_password_hash(user.password_hash, data['password']):
            login_user(user)
            return jsonify({'success': True, 'message': 'Login successful'})
        else:
            return jsonify({'success': False, 'message': 'Invalid credentials'})
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get user's company
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    # Get dashboard stats
    stats = {
        'total_employees': Employee.query.filter_by(company_id=company.id).count(),
        'total_products': Product.query.filter_by(company_id=company.id).count(),
        'total_campaigns': Campaign.query.filter_by(company_id=company.id).count(),
        'total_leads': Lead.query.filter_by(company_id=company.id).count(),
        'monthly_revenue': db.session.query(db.func.sum(FinanceTransaction.amount)).filter(
            FinanceTransaction.company_id == company.id,
            FinanceTransaction.type == 'income',
            FinanceTransaction.date >= date.today().replace(day=1)
        ).scalar() or 0,
        'monthly_expenses': db.session.query(db.func.sum(FinanceTransaction.amount)).filter(
            FinanceTransaction.company_id == company.id,
            FinanceTransaction.type == 'expense',
            FinanceTransaction.date >= date.today().replace(day=1)
        ).scalar() or 0
    }
    
    return render_template('dashboard.html', company=company, stats=stats)

# Finance Module Routes
@app.route('/finance')
@login_required
def finance():
    company = Company.query.filter_by(user_id=current_user.id).first()
    transactions = FinanceTransaction.query.filter_by(company_id=company.id).order_by(FinanceTransaction.date.desc()).all()
    invoices = Invoice.query.filter_by(company_id=company.id).order_by(Invoice.date.desc()).all()
    return render_template('finance.html', transactions=transactions, invoices=invoices)

@app.route('/finance/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    data = request.get_json()
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    transaction = FinanceTransaction(
        description=data['description'],
        amount=float(data['amount']),
        type=data['type'],
        category=data['category'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        company_id=company.id
    )
    
    db.session.add(transaction)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Transaction added successfully'})

@app.route('/finance/create_invoice', methods=['POST'])
@login_required
def create_invoice():
    data = request.get_json()
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    invoice = Invoice(
        client_name=data['client_name'],
        amount=float(data['amount']),
        description=data['description'],
        status='pending',
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        company_id=company.id
    )
    
    db.session.add(invoice)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Invoice created successfully'})

# HR Module Routes
@app.route('/hr')
@login_required
def hr():
    company = Company.query.filter_by(user_id=current_user.id).first()
    employees = Employee.query.filter_by(company_id=company.id).all()
    tasks = Task.query.filter_by(company_id=company.id).all()
    return render_template('hr.html', employees=employees, tasks=tasks)

@app.route('/hr/add_employee', methods=['POST'])
@login_required
def add_employee():
    data = request.get_json()
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    employee = Employee(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        position=data['position'],
        salary=float(data['salary']),
        department=data['department'],
        hire_date=datetime.strptime(data['hire_date'], '%Y-%m-%d').date(),
        company_id=company.id
    )
    
    db.session.add(employee)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Employee added successfully'})

@app.route('/hr/add_task', methods=['POST'])
@login_required
def add_task():
    data = request.get_json()
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    task = Task(
        title=data['title'],
        description=data['description'],
        assigned_to=int(data['assigned_to']),
        priority=data['priority'],
        status='pending',
        due_date=datetime.strptime(data['due_date'], '%Y-%m-%d').date(),
        company_id=company.id
    )
    
    db.session.add(task)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Task added successfully'})

# Marketing Module Routes
@app.route('/marketing')
@login_required
def marketing():
    company = Company.query.filter_by(user_id=current_user.id).first()
    campaigns = Campaign.query.filter_by(company_id=company.id).all()
    leads = Lead.query.filter_by(company_id=company.id).all()
    return render_template('marketing.html', campaigns=campaigns, leads=leads)

@app.route('/marketing/add_campaign', methods=['POST'])
@login_required
def add_campaign():
    data = request.get_json()
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    campaign = Campaign(
        name=data['name'],
        description=data['description'],
        budget=float(data['budget']),
        start_date=datetime.strptime(data['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(data['end_date'], '%Y-%m-%d').date(),
        status='active',
        company_id=company.id
    )
    
    db.session.add(campaign)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Campaign added successfully'})

@app.route('/marketing/add_lead', methods=['POST'])
@login_required
def add_lead():
    data = request.get_json()
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    lead = Lead(
        name=data['name'],
        email=data['email'],
        phone=data['phone'],
        company_name=data['company_name'],
        status='new',
        source=data['source'],
        company_id=company.id
    )
    
    db.session.add(lead)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Lead added successfully'})

# Inventory Module Routes
@app.route('/inventory')
@login_required
def inventory():
    company = Company.query.filter_by(user_id=current_user.id).first()
    products = Product.query.filter_by(company_id=company.id).all()
    return render_template('inventory.html', products=products)

@app.route('/inventory/add_product', methods=['POST'])
@login_required
def add_product():
    data = request.get_json()
    company = Company.query.filter_by(user_id=current_user.id).first()
    
    product = Product(
        name=data['name'],
        description=data['description'],
        category=data['category'],
        quantity=int(data['quantity']),
        unit_price=float(data['unit_price']),
        company_id=company.id
    )
    
    db.session.add(product)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Product added successfully'})

@app.route('/inventory/update_quantity', methods=['POST'])
@login_required
def update_quantity():
    data = request.get_json()
    product = Product.query.get(data['product_id'])
    
    if product:
        product.quantity += int(data['quantity_change'])
        db.session.commit()
        return jsonify({'success': True, 'message': 'Quantity updated successfully'})
    
    return jsonify({'success': False, 'message': 'Product not found'})

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # Add demo data if database is empty
        if User.query.count() == 0:
            from demo_data import create_demo_data
            create_demo_data()
    
    app.run(debug=True, host='0.0.0.0', port=8000)