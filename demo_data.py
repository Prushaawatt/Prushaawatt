from app import db
from models import User, Company, Employee, FinanceTransaction, Invoice, Product, Campaign, Lead, Task
from werkzeug.security import generate_password_hash
from datetime import datetime, date, timedelta

def create_demo_data():
    # Create demo user
    demo_user = User(
        full_name="John Smith",
        email="demo@erp.com",
        phone="+1-555-0123",
        address="123 Business St, City, State 12345",
        password_hash=generate_password_hash("demo123")
    )
    db.session.add(demo_user)
    db.session.commit()
    
    # Create demo company
    demo_company = Company(
        name="Demo Tech Solutions",
        industry="Technology",
        location="San Francisco, CA",
        subscription="Premium",
        user_id=demo_user.id
    )
    db.session.add(demo_company)
    db.session.commit()
    
    # Create demo employees
    employees_data = [
        {
            "name": "Alice Johnson",
            "email": "alice@demotech.com",
            "phone": "+1-555-0124",
            "position": "Software Developer",
            "salary": 75000,
            "department": "Engineering",
            "hire_date": date(2023, 1, 15)
        },
        {
            "name": "Bob Wilson",
            "email": "bob@demotech.com",
            "phone": "+1-555-0125",
            "position": "Marketing Manager",
            "salary": 65000,
            "department": "Marketing",
            "hire_date": date(2023, 2, 1)
        },
        {
            "name": "Carol Davis",
            "email": "carol@demotech.com",
            "phone": "+1-555-0126",
            "position": "Sales Representative",
            "salary": 55000,
            "department": "Sales",
            "hire_date": date(2023, 3, 10)
        },
        {
            "name": "David Brown",
            "email": "david@demotech.com",
            "phone": "+1-555-0127",
            "position": "HR Manager",
            "salary": 60000,
            "department": "Human Resources",
            "hire_date": date(2023, 1, 20)
        }
    ]
    
    for emp_data in employees_data:
        employee = Employee(company_id=demo_company.id, **emp_data)
        db.session.add(employee)
    
    db.session.commit()
    
    # Get employee IDs for tasks
    employees = Employee.query.filter_by(company_id=demo_company.id).all()
    
    # Create demo finance transactions
    transactions_data = [
        {"description": "Client Payment - Project Alpha", "amount": 15000, "type": "income", "category": "Services", "date": date.today() - timedelta(days=5)},
        {"description": "Office Rent", "amount": 3000, "type": "expense", "category": "Rent", "date": date.today() - timedelta(days=3)},
        {"description": "Software Licenses", "amount": 500, "type": "expense", "category": "Software", "date": date.today() - timedelta(days=2)},
        {"description": "Client Payment - Project Beta", "amount": 12000, "type": "income", "category": "Services", "date": date.today() - timedelta(days=1)},
        {"description": "Employee Salaries", "amount": 25000, "type": "expense", "category": "Payroll", "date": date.today()},
    ]
    
    for trans_data in transactions_data:
        transaction = FinanceTransaction(company_id=demo_company.id, **trans_data)
        db.session.add(transaction)
    
    # Create demo invoices
    invoices_data = [
        {"client_name": "ABC Corporation", "amount": 8500, "description": "Web Development Services", "status": "paid", "date": date.today() - timedelta(days=10)},
        {"client_name": "XYZ Industries", "amount": 12000, "description": "Mobile App Development", "status": "pending", "date": date.today() - timedelta(days=5)},
        {"client_name": "Tech Startup Inc", "amount": 6500, "description": "Consulting Services", "status": "overdue", "date": date.today() - timedelta(days=15)},
    ]
    
    for inv_data in invoices_data:
        invoice = Invoice(company_id=demo_company.id, **inv_data)
        db.session.add(invoice)
    
    # Create demo products
    products_data = [
        {"name": "Web Development Package", "description": "Custom website development", "category": "Services", "quantity": 10, "unit_price": 5000},
        {"name": "Mobile App Development", "description": "iOS and Android app development", "category": "Services", "quantity": 5, "unit_price": 15000},
        {"name": "Consulting Hours", "description": "Technical consulting per hour", "category": "Services", "quantity": 100, "unit_price": 150},
        {"name": "Software License", "description": "Annual software license", "category": "Software", "quantity": 25, "unit_price": 200},
    ]
    
    for prod_data in products_data:
        product = Product(company_id=demo_company.id, **prod_data)
        db.session.add(product)
    
    # Create demo campaigns
    campaigns_data = [
        {
            "name": "Q4 Digital Marketing Campaign",
            "description": "Social media and Google Ads campaign",
            "budget": 10000,
            "start_date": date.today() - timedelta(days=30),
            "end_date": date.today() + timedelta(days=30),
            "status": "active"
        },
        {
            "name": "Product Launch Campaign",
            "description": "Launch campaign for new software product",
            "budget": 15000,
            "start_date": date.today() - timedelta(days=15),
            "end_date": date.today() + timedelta(days=45),
            "status": "active"
        }
    ]
    
    for camp_data in campaigns_data:
        campaign = Campaign(company_id=demo_company.id, **camp_data)
        db.session.add(campaign)
    
    # Create demo leads
    leads_data = [
        {"name": "Michael Johnson", "email": "michael@company1.com", "phone": "+1-555-1001", "company_name": "Company One", "status": "new", "source": "Website"},
        {"name": "Sarah Williams", "email": "sarah@company2.com", "phone": "+1-555-1002", "company_name": "Company Two", "status": "contacted", "source": "Referral"},
        {"name": "Robert Taylor", "email": "robert@company3.com", "phone": "+1-555-1003", "company_name": "Company Three", "status": "qualified", "source": "Cold Call"},
        {"name": "Lisa Anderson", "email": "lisa@company4.com", "phone": "+1-555-1004", "company_name": "Company Four", "status": "converted", "source": "Email Marketing"},
    ]
    
    for lead_data in leads_data:
        lead = Lead(company_id=demo_company.id, **lead_data)
        db.session.add(lead)
    
    # Create demo tasks
    tasks_data = [
        {
            "title": "Complete Project Alpha Documentation",
            "description": "Write comprehensive documentation for Project Alpha",
            "assigned_to": employees[0].id,
            "priority": "high",
            "status": "in_progress",
            "due_date": date.today() + timedelta(days=3)
        },
        {
            "title": "Prepare Q4 Marketing Report",
            "description": "Analyze Q4 marketing performance and prepare report",
            "assigned_to": employees[1].id,
            "priority": "medium",
            "status": "pending",
            "due_date": date.today() + timedelta(days=7)
        },
        {
            "title": "Follow up with XYZ Industries",
            "description": "Contact XYZ Industries about pending invoice",
            "assigned_to": employees[2].id,
            "priority": "high",
            "status": "pending",
            "due_date": date.today() + timedelta(days=1)
        },
        {
            "title": "Conduct Performance Reviews",
            "description": "Schedule and conduct quarterly performance reviews",
            "assigned_to": employees[3].id,
            "priority": "medium",
            "status": "pending",
            "due_date": date.today() + timedelta(days=14)
        }
    ]
    
    for task_data in tasks_data:
        task = Task(company_id=demo_company.id, **task_data)
        db.session.add(task)
    
    db.session.commit()
    print("Demo data created successfully!")