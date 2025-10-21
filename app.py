from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp_demo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Database Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    role = db.Column(db.String(20), default='User')  # Admin or User
    subscription = db.Column(db.String(20), default='Free')  # Free, Basic, Premium
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Company details
    company_name = db.Column(db.String(100))
    industry = db.Column(db.String(50))
    company_location = db.Column(db.String(100))

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    industry = db.Column(db.String(50))
    location = db.Column(db.String(100))
    assets = db.Column(db.Float, default=0.0)

class FinanceTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # income or expense
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(200))
    category = db.Column(db.String(50))
    date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    client_name = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')  # Pending, Paid, Overdue
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    position = db.Column(db.String(50))
    department = db.Column(db.String(50))
    salary = db.Column(db.Float)
    hire_date = db.Column(db.Date, default=date.today)
    status = db.Column(db.String(20), default='Active')  # Active, Inactive

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.String(20), default='Pending')  # Pending, In Progress, Completed
    due_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class MarketingCampaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    budget = db.Column(db.Float)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    status = db.Column(db.String(20), default='Planning')  # Planning, Active, Completed, Paused

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))
    company = db.Column(db.String(100))
    source = db.Column(db.String(50))
    status = db.Column(db.String(20), default='New')  # New, Contacted, Qualified, Converted, Lost
    value = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    quantity = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, default=0.0)
    reorder_level = db.Column(db.Integer, default=10)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class InventoryTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # in or out
    quantity = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(100))
    date = db.Column(db.Date, default=date.today)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

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
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        full_name = request.form['full_name']
        phone = request.form['phone']
        address = request.form['address']
        company_name = request.form['company_name']
        industry = request.form['industry']
        company_location = request.form['company_location']
        subscription = request.form['subscription']
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists')
            return render_template('register.html')
        
        # Create new user
        user = User(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            full_name=full_name,
            phone=phone,
            address=address,
            company_name=company_name,
            industry=industry,
            company_location=company_location,
            subscription=subscription
        )
        
        db.session.add(user)
        db.session.commit()
        
        # Create company record
        company = Company(
            user_id=user.id,
            name=company_name,
            industry=industry,
            location=company_location
        )
        db.session.add(company)
        db.session.commit()
        
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password')
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    # Get dashboard statistics
    total_income = db.session.query(db.func.sum(FinanceTransaction.amount)).filter_by(
        user_id=current_user.id, type='income'
    ).scalar() or 0
    
    total_expenses = db.session.query(db.func.sum(FinanceTransaction.amount)).filter_by(
        user_id=current_user.id, type='expense'
    ).scalar() or 0
    
    net_profit = total_income - total_expenses
    
    total_employees = Employee.query.filter_by(user_id=current_user.id).count()
    total_products = Product.query.filter_by(user_id=current_user.id).count()
    total_leads = Lead.query.filter_by(user_id=current_user.id).count()
    active_campaigns = MarketingCampaign.query.filter_by(
        user_id=current_user.id, status='Active'
    ).count()
    
    # Recent transactions
    recent_transactions = FinanceTransaction.query.filter_by(
        user_id=current_user.id
    ).order_by(FinanceTransaction.created_at.desc()).limit(5).all()
    
    # Recent leads
    recent_leads = Lead.query.filter_by(
        user_id=current_user.id
    ).order_by(Lead.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_income=total_income,
                         total_expenses=total_expenses,
                         net_profit=net_profit,
                         total_employees=total_employees,
                         total_products=total_products,
                         total_leads=total_leads,
                         active_campaigns=active_campaigns,
                         recent_transactions=recent_transactions,
                         recent_leads=recent_leads)

# Finance Module Routes
@app.route('/finance')
@login_required
def finance():
    transactions = FinanceTransaction.query.filter_by(user_id=current_user.id).order_by(
        FinanceTransaction.date.desc()
    ).all()
    
    total_income = db.session.query(db.func.sum(FinanceTransaction.amount)).filter_by(
        user_id=current_user.id, type='income'
    ).scalar() or 0
    
    total_expenses = db.session.query(db.func.sum(FinanceTransaction.amount)).filter_by(
        user_id=current_user.id, type='expense'
    ).scalar() or 0
    
    invoices = Invoice.query.filter_by(user_id=current_user.id).order_by(
        Invoice.created_at.desc()
    ).all()
    
    return render_template('finance.html',
                         transactions=transactions,
                         total_income=total_income,
                         total_expenses=total_expenses,
                         invoices=invoices)

@app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    transaction = FinanceTransaction(
        user_id=current_user.id,
        type=request.form['type'],
        amount=float(request.form['amount']),
        description=request.form['description'],
        category=request.form['category'],
        date=datetime.strptime(request.form['date'], '%Y-%m-%d').date()
    )
    db.session.add(transaction)
    db.session.commit()
    flash('Transaction added successfully!')
    return redirect(url_for('finance'))

@app.route('/add_invoice', methods=['POST'])
@login_required
def add_invoice():
    invoice = Invoice(
        user_id=current_user.id,
        client_name=request.form['client_name'],
        amount=float(request.form['amount']),
        description=request.form['description'],
        due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
    )
    db.session.add(invoice)
    db.session.commit()
    flash('Invoice created successfully!')
    return redirect(url_for('finance'))

# HR Module Routes
@app.route('/hr')
@login_required
def hr():
    employees = Employee.query.filter_by(user_id=current_user.id).all()
    tasks = Task.query.filter_by(user_id=current_user.id).order_by(
        Task.created_at.desc()
    ).all()
    return render_template('hr.html', employees=employees, tasks=tasks)

@app.route('/add_employee', methods=['POST'])
@login_required
def add_employee():
    employee = Employee(
        user_id=current_user.id,
        full_name=request.form['full_name'],
        email=request.form['email'],
        phone=request.form['phone'],
        position=request.form['position'],
        department=request.form['department'],
        salary=float(request.form['salary']) if request.form['salary'] else 0,
        hire_date=datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
    )
    db.session.add(employee)
    db.session.commit()
    flash('Employee added successfully!')
    return redirect(url_for('hr'))

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    task = Task(
        user_id=current_user.id,
        employee_id=int(request.form['employee_id']),
        title=request.form['title'],
        description=request.form['description'],
        due_date=datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
    )
    db.session.add(task)
    db.session.commit()
    flash('Task assigned successfully!')
    return redirect(url_for('hr'))

# Marketing Module Routes
@app.route('/marketing')
@login_required
def marketing():
    campaigns = MarketingCampaign.query.filter_by(user_id=current_user.id).order_by(
        MarketingCampaign.created_at.desc()
    ).all()
    leads = Lead.query.filter_by(user_id=current_user.id).order_by(
        Lead.created_at.desc()
    ).all()
    return render_template('marketing.html', campaigns=campaigns, leads=leads)

@app.route('/add_campaign', methods=['POST'])
@login_required
def add_campaign():
    campaign = MarketingCampaign(
        user_id=current_user.id,
        name=request.form['name'],
        description=request.form['description'],
        budget=float(request.form['budget']) if request.form['budget'] else 0,
        start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
        end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
    )
    db.session.add(campaign)
    db.session.commit()
    flash('Campaign created successfully!')
    return redirect(url_for('marketing'))

@app.route('/add_lead', methods=['POST'])
@login_required
def add_lead():
    lead = Lead(
        user_id=current_user.id,
        name=request.form['name'],
        email=request.form['email'],
        phone=request.form['phone'],
        company=request.form['company'],
        source=request.form['source'],
        value=float(request.form['value']) if request.form['value'] else 0
    )
    db.session.add(lead)
    db.session.commit()
    flash('Lead added successfully!')
    return redirect(url_for('marketing'))

# Inventory Module Routes
@app.route('/inventory')
@login_required
def inventory():
    products = Product.query.filter_by(user_id=current_user.id).all()
    transactions = InventoryTransaction.query.filter_by(user_id=current_user.id).order_by(
        InventoryTransaction.created_at.desc()
    ).all()
    return render_template('inventory.html', products=products, transactions=transactions)

@app.route('/add_product', methods=['POST'])
@login_required
def add_product():
    product = Product(
        user_id=current_user.id,
        name=request.form['name'],
        description=request.form['description'],
        category=request.form['category'],
        quantity=int(request.form['quantity']),
        unit_price=float(request.form['unit_price']),
        reorder_level=int(request.form['reorder_level'])
    )
    db.session.add(product)
    db.session.commit()
    flash('Product added successfully!')
    return redirect(url_for('inventory'))

@app.route('/inventory_transaction', methods=['POST'])
@login_required
def inventory_transaction():
    product_id = int(request.form['product_id'])
    transaction_type = request.form['type']
    quantity = int(request.form['quantity'])
    reason = request.form['reason']
    
    product = Product.query.get(product_id)
    if not product or product.user_id != current_user.id:
        flash('Product not found!')
        return redirect(url_for('inventory'))
    
    if transaction_type == 'out' and product.quantity < quantity:
        flash('Insufficient quantity!')
        return redirect(url_for('inventory'))
    
    # Update product quantity
    if transaction_type == 'in':
        product.quantity += quantity
    else:
        product.quantity -= quantity
    
    # Create transaction record
    transaction = InventoryTransaction(
        user_id=current_user.id,
        product_id=product_id,
        type=transaction_type,
        quantity=quantity,
        reason=reason
    )
    db.session.add(transaction)
    db.session.commit()
    flash('Inventory transaction recorded!')
    return redirect(url_for('inventory'))

# API Routes for AJAX
@app.route('/api/dashboard_stats')
@login_required
def dashboard_stats():
    stats = {
        'total_income': db.session.query(db.func.sum(FinanceTransaction.amount)).filter_by(
            user_id=current_user.id, type='income'
        ).scalar() or 0,
        'total_expenses': db.session.query(db.func.sum(FinanceTransaction.amount)).filter_by(
            user_id=current_user.id, type='expense'
        ).scalar() or 0,
        'total_employees': Employee.query.filter_by(user_id=current_user.id).count(),
        'total_products': Product.query.filter_by(user_id=current_user.id).count(),
        'total_leads': Lead.query.filter_by(user_id=current_user.id).count(),
        'active_campaigns': MarketingCampaign.query.filter_by(
            user_id=current_user.id, status='Active'
        ).count()
    }
    stats['net_profit'] = stats['total_income'] - stats['total_expenses']
    return jsonify(stats)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Create demo data if no users exist
        if User.query.count() == 0:
            # Create demo admin user
            admin = User(
                username='admin',
                email='admin@demo.com',
                password_hash=generate_password_hash('admin123'),
                full_name='Demo Admin',
                phone='+1234567890',
                address='123 Demo Street, Demo City',
                role='Admin',
                subscription='Premium',
                company_name='Demo Company',
                industry='Technology',
                company_location='Demo City, DC'
            )
            db.session.add(admin)
            db.session.commit()
            
            # Create demo company
            company = Company(
                user_id=admin.id,
                name='Demo Company',
                industry='Technology',
                location='Demo City, DC',
                assets=50000.0
            )
            db.session.add(company)
            
            # Add demo transactions
            transactions = [
                FinanceTransaction(user_id=admin.id, type='income', amount=5000, description='Client Payment', category='Services'),
                FinanceTransaction(user_id=admin.id, type='income', amount=3000, description='Product Sales', category='Sales'),
                FinanceTransaction(user_id=admin.id, type='expense', amount=1500, description='Office Rent', category='Rent'),
                FinanceTransaction(user_id=admin.id, type='expense', amount=800, description='Utilities', category='Utilities'),
            ]
            for t in transactions:
                db.session.add(t)
            
            # Add demo employees
            employees = [
                Employee(user_id=admin.id, full_name='John Doe', email='john@demo.com', phone='+1234567891', position='Developer', department='IT', salary=60000),
                Employee(user_id=admin.id, full_name='Jane Smith', email='jane@demo.com', phone='+1234567892', position='Manager', department='Sales', salary=70000),
                Employee(user_id=admin.id, full_name='Bob Johnson', email='bob@demo.com', phone='+1234567893', position='Designer', department='Marketing', salary=55000),
            ]
            for e in employees:
                db.session.add(e)
            
            # Add demo products
            products = [
                Product(user_id=admin.id, name='Laptop', description='High-performance laptop', category='Electronics', quantity=50, unit_price=1200, reorder_level=10),
                Product(user_id=admin.id, name='Office Chair', description='Ergonomic office chair', category='Furniture', quantity=25, unit_price=300, reorder_level=5),
                Product(user_id=admin.id, name='Software License', description='Annual software license', category='Software', quantity=100, unit_price=500, reorder_level=20),
            ]
            for p in products:
                db.session.add(p)
            
            # Add demo leads
            leads = [
                Lead(user_id=admin.id, name='Alice Brown', email='alice@client.com', phone='+1234567894', company='Client Corp', source='Website', value=5000),
                Lead(user_id=admin.id, name='Charlie Wilson', email='charlie@client.com', phone='+1234567895', company='Client Inc', source='Referral', value=7500),
            ]
            for l in leads:
                db.session.add(l)
            
            # Add demo campaigns
            campaigns = [
                MarketingCampaign(user_id=admin.id, name='Q4 Campaign', description='End of year promotion', budget=10000, start_date=date.today(), end_date=date(2024, 12, 31), status='Active'),
                MarketingCampaign(user_id=admin.id, name='Social Media Push', description='Social media advertising', budget=5000, start_date=date.today(), end_date=date(2024, 11, 30), status='Planning'),
            ]
            for c in campaigns:
                db.session.add(c)
            
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000)