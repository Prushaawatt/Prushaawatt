import os
from datetime import datetime, date
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///erp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(__file__), 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# -------------------- Models --------------------
class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120))
    location = db.Column(db.String(120))
    subscription = db.Column(db.String(20), default='Free')

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='User')  # Admin/User
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', backref='users')

class FinanceTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(10))  # income/expense
    description = db.Column(db.String(255))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    category = db.Column(db.String(120))
    value = db.Column(db.Float)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    number = db.Column(db.String(50))
    client = db.Column(db.String(120))
    kind = db.Column(db.String(20))  # Invoice / Quotation
    date = db.Column(db.Date)
    total = db.Column(db.Float)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    role = db.Column(db.String(120))
    salary = db.Column(db.Float)
    department = db.Column(db.String(120))
    document_path = db.Column(db.String(255))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    channel = db.Column(db.String(120))
    status = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    email = db.Column(db.String(120))
    status = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    category = db.Column(db.String(120))
    stock = db.Column(db.Integer, default=0)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

class StockMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
    product = db.relationship('Product')
    kind = db.Column(db.String(10))  # IN / OUT
    quantity = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

# -------------------- Auth --------------------
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def root():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('register'))
        # Create company first
        company = Company(
            name=request.form['company_name'],
            industry=request.form.get('industry'),
            location=request.form.get('location'),
            subscription=request.form.get('subscription', 'Free')
        )
        db.session.add(company)
        db.session.flush()
        # Create user
        user = User(
            email=email,
            password_hash=generate_password_hash(request.form['password']),
            full_name=request.form.get('full_name'),
            phone=request.form.get('phone'),
            address=request.form.get('address'),
            role='Admin',
            company_id=company.id
        )
        db.session.add(user)
        db.session.commit()
        # If subscription is not Free, redirect to dummy payment
        subscription = company.subscription
        if subscription != 'Free':
            return redirect(url_for('checkout', company_id=company.id))
        flash('Registration successful. Please login.', 'success')
        return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('auth/login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# -------------------- Payment (Dummy) --------------------
@app.route('/checkout/<int:company_id>', methods=['GET', 'POST'])
def checkout(company_id):
    company = Company.query.get_or_404(company_id)
    amount = {'Basic': '$19', 'Premium': '$49'}.get(company.subscription, '$0')
    if request.method == 'POST':
        flash(f"Payment for {company.subscription} successful.", 'success')
        return redirect(url_for('login'))
    return render_template('payment/checkout.html', subscription=company.subscription, amount=amount)

# -------------------- Dashboard --------------------
@app.route('/dashboard')
@login_required
def dashboard():
    notes = [
        f"Subscription: {current_user.company.subscription}",
        "Welcome to the ERP demo!",
    ]
    return render_template('dashboard.html', notifications=notes)

# -------------------- Finance --------------------
@app.route('/finance')
@login_required
def finance_index():
    company_id = current_user.company_id
    transactions = FinanceTransaction.query.filter_by(company_id=company_id).order_by(FinanceTransaction.date.desc()).all()
    total_income = sum(t.amount for t in transactions if t.type == 'income')
    total_expenses = sum(t.amount for t in transactions if t.type == 'expense')
    net_profit = total_income - total_expenses
    return render_template('finance/index.html', transactions=transactions, total_income=total_income, total_expenses=total_expenses, net_profit=net_profit)

@app.route('/finance/invoices')
@login_required
def finance_invoices():
    invoices = Invoice.query.filter_by(company_id=current_user.company_id).order_by(Invoice.date.desc()).all()
    return render_template('finance/invoices.html', invoices=invoices)

@app.route('/finance/invoices/new', methods=['GET', 'POST'])
@login_required
def finance_create_invoice():
    if request.method == 'POST':
        inv = Invoice(
            number=request.form['number'],
            client=request.form['client'],
            kind=request.form['kind'],
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            total=float(request.form['total']),
            company_id=current_user.company_id
        )
        db.session.add(inv)
        db.session.commit()
        flash('Invoice/Quotation saved', 'success')
        return redirect(url_for('finance_invoices'))
    return render_template('finance/invoice_form.html', today=date.today().isoformat())

@app.route('/finance/assets')
@login_required
def finance_assets():
    assets = Asset.query.filter_by(company_id=current_user.company_id).all()
    return render_template('finance/assets.html', assets=assets)

@app.route('/finance/assets/new', methods=['GET', 'POST'])
@login_required
def finance_add_asset():
    if request.method == 'POST':
        a = Asset(
            name=request.form['name'],
            category=request.form.get('category'),
            value=float(request.form['value']),
            company_id=current_user.company_id
        )
        db.session.add(a)
        db.session.commit()
        flash('Asset added', 'success')
        return redirect(url_for('finance_assets'))
    return render_template('finance/transaction_form.html', title='Add Asset', today=date.today().isoformat())

@app.route('/finance/income/new', methods=['GET', 'POST'])
@login_required
def finance_add_income():
    if request.method == 'POST':
        t = FinanceTransaction(
            type='income',
            description=request.form['description'],
            amount=float(request.form['amount']),
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            company_id=current_user.company_id
        )
        db.session.add(t)
        db.session.commit()
        flash('Income added', 'success')
        return redirect(url_for('finance_index'))
    return render_template('finance/transaction_form.html', title='Add Income', today=date.today().isoformat())

@app.route('/finance/expense/new', methods=['GET', 'POST'])
@login_required
def finance_add_expense():
    if request.method == 'POST':
        t = FinanceTransaction(
            type='expense',
            description=request.form['description'],
            amount=float(request.form['amount']),
            date=datetime.strptime(request.form['date'], '%Y-%m-%d').date(),
            company_id=current_user.company_id
        )
        db.session.add(t)
        db.session.commit()
        flash('Expense added', 'success')
        return redirect(url_for('finance_index'))
    return render_template('finance/transaction_form.html', title='Add Expense', today=date.today().isoformat())

# -------------------- HR --------------------
@app.route('/hr')
@login_required
def hr_index():
    employees = Employee.query.filter_by(company_id=current_user.company_id).all()
    # Aggregate documents list by reading filenames
    for e in employees:
        e.documents = [os.path.basename(e.document_path)] if e.document_path else []
    return render_template('hr/index.html', employees=employees)

@app.route('/hr/employees/new', methods=['GET', 'POST'])
@login_required
def hr_add_employee():
    if request.method == 'POST':
        document = request.files.get('document')
        saved_path = None
        if document and document.filename:
            filename = secure_filename(document.filename)
            saved_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            document.save(saved_path)
        emp = Employee(
            name=request.form['name'],
            role=request.form['role'],
            salary=float(request.form['salary']),
            department=request.form.get('department'),
            document_path=saved_path,
            company_id=current_user.company_id
        )
        db.session.add(emp)
        db.session.commit()
        flash('Employee added', 'success')
        return redirect(url_for('hr_index'))
    return render_template('hr/employee_form.html')

@app.route('/uploads/<path:filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/hr/departments', methods=['GET', 'POST'])
@login_required
def hr_departments():
    if request.method == 'POST':
        name = request.form['name']
        if name:
            d = Department(name=name, company_id=current_user.company_id)
            db.session.add(d)
            db.session.commit()
            flash('Department added', 'success')
            return redirect(url_for('hr_departments'))
    deps = Department.query.filter_by(company_id=current_user.company_id).all()
    # Build employees per department count
    for d in deps:
        d.employees = Employee.query.filter_by(company_id=current_user.company_id, department=d.name).all()
    return render_template('hr/departments.html', departments=deps)

# -------------------- Marketing --------------------
@app.route('/marketing')
@login_required
def marketing_index():
    company_id = current_user.company_id
    campaigns = Campaign.query.filter_by(company_id=company_id).all()
    leads = Lead.query.filter_by(company_id=company_id).all()
    metrics = {
        'leads': len(leads),
        'clients': len([l for l in leads if l.status == 'Client']),
        'campaigns': len(campaigns)
    }
    return render_template('marketing/index.html', campaigns=campaigns, leads=leads, metrics=metrics)

@app.route('/marketing/campaigns/new', methods=['GET', 'POST'])
@login_required
def marketing_add_campaign():
    if request.method == 'POST':
        c = Campaign(
            name=request.form['name'],
            channel=request.form['channel'],
            status=request.form['status'],
            company_id=current_user.company_id
        )
        db.session.add(c)
        db.session.commit()
        flash('Campaign added', 'success')
        return redirect(url_for('marketing_index'))
    return render_template('marketing/campaign_form.html')

@app.route('/marketing/leads/new', methods=['GET', 'POST'])
@login_required
def marketing_add_lead():
    if request.method == 'POST':
        l = Lead(
            name=request.form['name'],
            email=request.form['email'],
            status=request.form['status'],
            company_id=current_user.company_id
        )
        db.session.add(l)
        db.session.commit()
        flash('Lead added', 'success')
        return redirect(url_for('marketing_index'))
    return render_template('marketing/lead_form.html')

# -------------------- Inventory --------------------
@app.route('/inventory')
@login_required
def inventory_index():
    products = Product.query.filter_by(company_id=current_user.company_id).all()
    return render_template('inventory/index.html', products=products)

@app.route('/inventory/products/new', methods=['GET', 'POST'])
@login_required
def inventory_add_product():
    if request.method == 'POST':
        p = Product(
            name=request.form['name'],
            category=request.form.get('category'),
            stock=int(request.form.get('stock', 0)),
            company_id=current_user.company_id
        )
        db.session.add(p)
        db.session.commit()
        flash('Product added', 'success')
        return redirect(url_for('inventory_index'))
    return render_template('inventory/product_form.html')

@app.route('/inventory/categories', methods=['GET', 'POST'])
@login_required
def inventory_categories():
    # For simplicity categories are strings on Product; provide a simple list view
    if request.method == 'POST':
        name = request.form['name']
        if name:
            p = Product(name=f"Category placeholder: {name}", category=name, stock=0, company_id=current_user.company_id)
            db.session.add(p)
            db.session.commit()
            flash('Category added (as placeholder product)', 'info')
            return redirect(url_for('inventory_categories'))
    # Unique categories and product counts
    products = Product.query.filter_by(company_id=current_user.company_id).all()
    categories = {}
    for p in products:
        if p.category:
            categories.setdefault(p.category, []).append(p)
    class CatView:
        def __init__(self, name, products):
            self.name = name
            self.products = products
    cat_list = [CatView(name, items) for name, items in categories.items()]
    return render_template('inventory/categories.html', categories=cat_list)

@app.route('/inventory/movements', methods=['GET', 'POST'])
@login_required
def inventory_movements():
    if request.method == 'POST':
        product_id = int(request.form['product_id'])
        kind = request.form['kind']
        qty = int(request.form['quantity'])
        product = Product.query.filter_by(id=product_id, company_id=current_user.company_id).first_or_404()
        if kind == 'IN':
            product.stock += qty
        else:
            product.stock = max(0, product.stock - qty)
        m = StockMovement(product_id=product.id, kind=kind, quantity=qty, company_id=current_user.company_id)
        db.session.add(m)
        db.session.commit()
        flash('Movement recorded', 'success')
        return redirect(url_for('inventory_movements'))
    products = Product.query.filter_by(company_id=current_user.company_id).all()
    movements = StockMovement.query.filter_by(company_id=current_user.company_id).order_by(StockMovement.date.desc()).all()
    return render_template('inventory/movements.html', products=products, movements=movements)

# -------------------- Seed data --------------------
def seed_demo():
    if User.query.first():
        return
    company = Company(name='Acme Corp', industry='Manufacturing', location='NYC', subscription='Premium')
    db.session.add(company)
    db.session.flush()
    admin = User(email='admin@example.com', password_hash=generate_password_hash('admin123'), role='Admin', full_name='Admin User', company_id=company.id)
    db.session.add(admin)
    # Finance seed
    db.session.add_all([
        FinanceTransaction(type='income', description='Product Sale', amount=5000, date=date.today(), company_id=company.id),
        FinanceTransaction(type='expense', description='Office Rent', amount=1200, date=date.today(), company_id=company.id),
    ])
    db.session.add_all([
        Asset(name='Laptop', category='IT', value=1200, company_id=company.id),
    ])
    db.session.add_all([
        Invoice(number='INV-1001', client='Globex', kind='Invoice', date=date.today(), total=2300, company_id=company.id),
        Invoice(number='QUO-2001', client='Initech', kind='Quotation', date=date.today(), total=1500, company_id=company.id),
    ])
    # HR seed
    db.session.add_all([
        Employee(name='John Doe', role='Engineer', salary=70000, department='R&D', company_id=company.id),
        Employee(name='Jane Smith', role='HR Manager', salary=65000, department='HR', company_id=company.id),
    ])
    db.session.add_all([
        Department(name='R&D', company_id=company.id),
        Department(name='HR', company_id=company.id),
    ])
    # Marketing seed
    db.session.add_all([
        Campaign(name='Spring Promo', channel='Email', status='Running', company_id=company.id),
    ])
    db.session.add_all([
        Lead(name='Alice', email='alice@example.com', status='New', company_id=company.id),
        Lead(name='Bob', email='bob@example.com', status='Client', company_id=company.id),
    ])
    # Inventory seed
    p1 = Product(name='Widget', category='Hardware', stock=100, company_id=company.id)
    p2 = Product(name='Gadget', category='Electronics', stock=50, company_id=company.id)
    db.session.add_all([p1, p2])
    db.session.flush()
    db.session.add_all([
        StockMovement(product_id=p1.id, kind='IN', quantity=100, company_id=company.id),
        StockMovement(product_id=p2.id, kind='IN', quantity=50, company_id=company.id),
    ])
    db.session.commit()

# -------------------- App run --------------------
with app.app_context():
    db.create_all()
    seed_demo()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
