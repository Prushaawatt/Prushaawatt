from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Company, Employee, Transaction, Invoice, Asset, Product, StockMovement, Campaign, Lead, Notification
from config import Config
from datetime import datetime, timedelta
import json

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Authentication Routes
@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        full_name = request.form.get('full_name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        
        company_name = request.form.get('company_name')
        industry = request.form.get('industry')
        location = request.form.get('location')
        subscription = request.form.get('subscription', 'Free')
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered!', 'danger')
            return redirect(url_for('register'))
        
        # Create company
        company = Company(
            name=company_name,
            industry=industry,
            location=location,
            subscription_plan=subscription
        )
        db.session.add(company)
        db.session.flush()
        
        # Create user
        user = User(
            email=email,
            full_name=full_name,
            phone=phone,
            address=address,
            company_id=company.id,
            role='admin'  # First user is admin
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))


# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    # Get summary statistics
    company_id = current_user.company_id
    
    total_employees = Employee.query.filter_by(company_id=company_id, status='active').count()
    total_products = Product.query.filter_by(company_id=company_id).count()
    total_leads = Lead.query.filter_by(company_id=company_id).count()
    
    # Calculate total income and expenses
    income = db.session.query(db.func.sum(Transaction.amount)).filter_by(
        company_id=company_id, type='income'
    ).scalar() or 0
    
    expenses = db.session.query(db.func.sum(Transaction.amount)).filter_by(
        company_id=company_id, type='expense'
    ).scalar() or 0
    
    net_profit = income - expenses
    
    # Recent notifications
    notifications = Notification.query.filter_by(
        user_id=current_user.id, is_read=False
    ).order_by(Notification.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_employees=total_employees,
                         total_products=total_products,
                         total_leads=total_leads,
                         income=income,
                         expenses=expenses,
                         net_profit=net_profit,
                         notifications=notifications)


# Finance Module
@app.route('/finance')
@login_required
def finance():
    company_id = current_user.company_id
    
    transactions = Transaction.query.filter_by(company_id=company_id).order_by(
        Transaction.date.desc()
    ).all()
    
    income = db.session.query(db.func.sum(Transaction.amount)).filter_by(
        company_id=company_id, type='income'
    ).scalar() or 0
    
    expenses = db.session.query(db.func.sum(Transaction.amount)).filter_by(
        company_id=company_id, type='expense'
    ).scalar() or 0
    
    net_profit = income - expenses
    
    assets = Asset.query.filter_by(company_id=company_id).all()
    total_assets = sum(asset.value or 0 for asset in assets)
    
    return render_template('finance.html',
                         transactions=transactions,
                         income=income,
                         expenses=expenses,
                         net_profit=net_profit,
                         assets=assets,
                         total_assets=total_assets)


@app.route('/finance/transaction/add', methods=['POST'])
@login_required
def add_transaction():
    transaction = Transaction(
        company_id=current_user.company_id,
        type=request.form.get('type'),
        category=request.form.get('category'),
        description=request.form.get('description'),
        amount=float(request.form.get('amount')),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
    )
    db.session.add(transaction)
    db.session.commit()
    flash('Transaction added successfully!', 'success')
    return redirect(url_for('finance'))


@app.route('/finance/asset/add', methods=['POST'])
@login_required
def add_asset():
    asset = Asset(
        company_id=current_user.company_id,
        name=request.form.get('name'),
        category=request.form.get('category'),
        value=float(request.form.get('value')),
        purchase_date=datetime.strptime(request.form.get('purchase_date'), '%Y-%m-%d').date(),
        description=request.form.get('description')
    )
    db.session.add(asset)
    db.session.commit()
    flash('Asset added successfully!', 'success')
    return redirect(url_for('finance'))


@app.route('/invoices')
@login_required
def invoices():
    company_id = current_user.company_id
    invoices = Invoice.query.filter_by(company_id=company_id).order_by(
        Invoice.created_at.desc()
    ).all()
    return render_template('invoices.html', invoices=invoices)


@app.route('/invoice/add', methods=['GET', 'POST'])
@login_required
def add_invoice():
    if request.method == 'POST':
        invoice_type = request.form.get('type', 'invoice')
        subtotal = float(request.form.get('subtotal'))
        tax = float(request.form.get('tax', 0))
        total = subtotal + tax
        
        invoice = Invoice(
            company_id=current_user.company_id,
            invoice_number=f"INV-{datetime.now().strftime('%Y%m%d')}-{Invoice.query.count() + 1:04d}",
            client_name=request.form.get('client_name'),
            client_email=request.form.get('client_email'),
            type=invoice_type,
            items=request.form.get('items'),
            subtotal=subtotal,
            tax=tax,
            total=total,
            status='pending',
            issue_date=datetime.strptime(request.form.get('issue_date'), '%Y-%m-%d').date(),
            due_date=datetime.strptime(request.form.get('due_date'), '%Y-%m-%d').date() if request.form.get('due_date') else None
        )
        db.session.add(invoice)
        db.session.commit()
        flash(f'{invoice_type.capitalize()} created successfully!', 'success')
        return redirect(url_for('invoices'))
    
    return render_template('add_invoice.html')


# HR Module
@app.route('/hr')
@login_required
def hr():
    company_id = current_user.company_id
    employees = Employee.query.filter_by(company_id=company_id).all()
    return render_template('hr.html', employees=employees)


@app.route('/hr/employee/add', methods=['POST'])
@login_required
def add_employee():
    employee = Employee(
        company_id=current_user.company_id,
        full_name=request.form.get('full_name'),
        email=request.form.get('email'),
        phone=request.form.get('phone'),
        role=request.form.get('role'),
        department=request.form.get('department'),
        salary=float(request.form.get('salary')) if request.form.get('salary') else None,
        join_date=datetime.strptime(request.form.get('join_date'), '%Y-%m-%d').date(),
        contract_details=request.form.get('contract_details')
    )
    db.session.add(employee)
    db.session.commit()
    flash('Employee added successfully!', 'success')
    return redirect(url_for('hr'))


@app.route('/hr/employee/<int:id>/edit', methods=['POST'])
@login_required
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    
    if employee.company_id != current_user.company_id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('hr'))
    
    employee.full_name = request.form.get('full_name')
    employee.email = request.form.get('email')
    employee.phone = request.form.get('phone')
    employee.role = request.form.get('role')
    employee.department = request.form.get('department')
    employee.salary = float(request.form.get('salary')) if request.form.get('salary') else None
    employee.contract_details = request.form.get('contract_details')
    
    db.session.commit()
    flash('Employee updated successfully!', 'success')
    return redirect(url_for('hr'))


# Marketing Module
@app.route('/marketing')
@login_required
def marketing():
    company_id = current_user.company_id
    campaigns = Campaign.query.filter_by(company_id=company_id).all()
    leads = Lead.query.filter_by(company_id=company_id).order_by(Lead.created_at.desc()).all()
    
    total_leads = len(leads)
    converted_leads = len([l for l in leads if l.status == 'converted'])
    conversion_rate = (converted_leads / total_leads * 100) if total_leads > 0 else 0
    
    return render_template('marketing.html',
                         campaigns=campaigns,
                         leads=leads,
                         total_leads=total_leads,
                         converted_leads=converted_leads,
                         conversion_rate=conversion_rate)


@app.route('/marketing/campaign/add', methods=['POST'])
@login_required
def add_campaign():
    campaign = Campaign(
        company_id=current_user.company_id,
        name=request.form.get('name'),
        type=request.form.get('type'),
        description=request.form.get('description'),
        budget=float(request.form.get('budget')) if request.form.get('budget') else None,
        start_date=datetime.strptime(request.form.get('start_date'), '%Y-%m-%d').date(),
        end_date=datetime.strptime(request.form.get('end_date'), '%Y-%m-%d').date() if request.form.get('end_date') else None,
        status=request.form.get('status', 'active')
    )
    db.session.add(campaign)
    db.session.commit()
    flash('Campaign added successfully!', 'success')
    return redirect(url_for('marketing'))


@app.route('/marketing/lead/add', methods=['POST'])
@login_required
def add_lead():
    lead = Lead(
        company_id=current_user.company_id,
        name=request.form.get('name'),
        email=request.form.get('email'),
        phone=request.form.get('phone'),
        company_name=request.form.get('company_name'),
        source=request.form.get('source'),
        status=request.form.get('status', 'new'),
        notes=request.form.get('notes')
    )
    db.session.add(lead)
    db.session.commit()
    flash('Lead added successfully!', 'success')
    return redirect(url_for('marketing'))


@app.route('/marketing/lead/<int:id>/update', methods=['POST'])
@login_required
def update_lead_status(id):
    lead = Lead.query.get_or_404(id)
    
    if lead.company_id != current_user.company_id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('marketing'))
    
    lead.status = request.form.get('status')
    db.session.commit()
    flash('Lead status updated!', 'success')
    return redirect(url_for('marketing'))


# Inventory Module
@app.route('/inventory')
@login_required
def inventory():
    company_id = current_user.company_id
    products = Product.query.filter_by(company_id=company_id).all()
    
    low_stock_products = [p for p in products if p.quantity <= p.reorder_level]
    
    return render_template('inventory.html',
                         products=products,
                         low_stock_products=low_stock_products)


@app.route('/inventory/product/add', methods=['POST'])
@login_required
def add_product():
    product = Product(
        company_id=current_user.company_id,
        name=request.form.get('name'),
        sku=request.form.get('sku'),
        category=request.form.get('category'),
        description=request.form.get('description'),
        quantity=int(request.form.get('quantity', 0)),
        unit_price=float(request.form.get('unit_price')) if request.form.get('unit_price') else None,
        reorder_level=int(request.form.get('reorder_level', 10))
    )
    db.session.add(product)
    db.session.commit()
    flash('Product added successfully!', 'success')
    return redirect(url_for('inventory'))


@app.route('/inventory/stock/add', methods=['POST'])
@login_required
def add_stock_movement():
    product_id = int(request.form.get('product_id'))
    movement_type = request.form.get('type')
    quantity = int(request.form.get('quantity'))
    
    product = Product.query.get_or_404(product_id)
    
    if product.company_id != current_user.company_id:
        flash('Unauthorized access!', 'danger')
        return redirect(url_for('inventory'))
    
    # Update product quantity
    if movement_type == 'in':
        product.quantity += quantity
    else:
        product.quantity -= quantity
    
    # Record movement
    movement = StockMovement(
        product_id=product_id,
        type=movement_type,
        quantity=quantity,
        reference=request.form.get('reference'),
        date=datetime.strptime(request.form.get('date'), '%Y-%m-%d').date()
    )
    db.session.add(movement)
    db.session.commit()
    
    flash('Stock movement recorded!', 'success')
    return redirect(url_for('inventory'))


# Notifications
@app.route('/notifications')
@login_required
def notifications():
    user_notifications = Notification.query.filter_by(
        user_id=current_user.id
    ).order_by(Notification.created_at.desc()).all()
    return render_template('notifications.html', notifications=user_notifications)


@app.route('/notifications/<int:id>/read', methods=['POST'])
@login_required
def mark_notification_read(id):
    notification = Notification.query.get_or_404(id)
    
    if notification.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    notification.is_read = True
    db.session.commit()
    return jsonify({'success': True})


# Profile
@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
