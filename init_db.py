"""
Database initialization script with demo data
Run this script to set up the database with sample data for testing
"""

from app import app
from models import db, User, Company, Employee, Transaction, Invoice, Asset, Product, Campaign, Lead, Notification
from datetime import datetime, timedelta
import random

def init_db_with_demo_data():
    with app.app_context():
        # Drop all tables and recreate
        print("Creating database tables...")
        db.drop_all()
        db.create_all()
        
        # Create Demo Company 1
        print("Creating demo companies...")
        company1 = Company(
            name="TechCorp Solutions",
            industry="Technology",
            location="San Francisco, CA",
            subscription_plan="Premium"
        )
        db.session.add(company1)
        db.session.flush()
        
        # Create Demo Company 2
        company2 = Company(
            name="Green Manufacturing Inc",
            industry="Manufacturing",
            location="Austin, TX",
            subscription_plan="Basic"
        )
        db.session.add(company2)
        db.session.flush()
        
        # Create Admin User for Company 1
        print("Creating demo users...")
        admin_user = User(
            email="admin@demo.com",
            full_name="John Admin",
            phone="+1-555-0100",
            address="123 Main St, San Francisco, CA 94102",
            role="admin",
            company_id=company1.id
        )
        admin_user.set_password("admin123")
        db.session.add(admin_user)
        
        # Create Regular User for Company 1
        regular_user = User(
            email="user@demo.com",
            full_name="Jane User",
            phone="+1-555-0101",
            address="456 Oak Ave, San Francisco, CA 94103",
            role="user",
            company_id=company1.id
        )
        regular_user.set_password("user123")
        db.session.add(regular_user)
        
        # Create User for Company 2
        user2 = User(
            email="manager@demo.com",
            full_name="Bob Manager",
            phone="+1-555-0200",
            address="789 Pine Rd, Austin, TX 78701",
            role="admin",
            company_id=company2.id
        )
        user2.set_password("manager123")
        db.session.add(user2)
        
        db.session.flush()
        
        # Create Employees for Company 1
        print("Creating demo employees...")
        employees_data = [
            {"name": "Alice Johnson", "role": "Software Engineer", "department": "Engineering", "salary": 85000},
            {"name": "Bob Smith", "role": "Product Manager", "department": "Engineering", "salary": 95000},
            {"name": "Carol White", "role": "Marketing Manager", "department": "Marketing", "salary": 75000},
            {"name": "David Brown", "role": "Sales Representative", "department": "Sales", "salary": 65000},
            {"name": "Eve Davis", "role": "HR Manager", "department": "HR", "salary": 70000},
            {"name": "Frank Wilson", "role": "Senior Developer", "department": "Engineering", "salary": 90000},
            {"name": "Grace Lee", "role": "Designer", "department": "Marketing", "salary": 68000},
            {"name": "Henry Martinez", "role": "Accountant", "department": "Finance", "salary": 72000},
        ]
        
        for emp_data in employees_data:
            employee = Employee(
                company_id=company1.id,
                full_name=emp_data["name"],
                email=emp_data["name"].lower().replace(" ", ".") + "@techcorp.com",
                phone=f"+1-555-{random.randint(1000, 9999)}",
                role=emp_data["role"],
                department=emp_data["department"],
                salary=emp_data["salary"],
                join_date=datetime.now().date() - timedelta(days=random.randint(30, 730)),
                contract_details="Full-time employment contract with standard benefits package.",
                status="active"
            )
            db.session.add(employee)
        
        # Create Transactions for Company 1
        print("Creating demo transactions...")
        transactions_data = [
            {"type": "income", "category": "Sales", "description": "Product sales - Q1", "amount": 50000},
            {"type": "income", "category": "Services", "description": "Consulting services", "amount": 25000},
            {"type": "income", "category": "Sales", "description": "Product sales - Q2", "amount": 65000},
            {"type": "expense", "category": "Salaries", "description": "Monthly payroll", "amount": 45000},
            {"type": "expense", "category": "Office", "description": "Office rent - Monthly", "amount": 5000},
            {"type": "expense", "category": "Marketing", "description": "Ad campaign expenses", "amount": 8000},
            {"type": "expense", "category": "Utilities", "description": "Internet and electricity", "amount": 1200},
            {"type": "income", "category": "Sales", "description": "Enterprise license sale", "amount": 100000},
            {"type": "expense", "category": "Equipment", "description": "New laptops for team", "amount": 15000},
            {"type": "expense", "category": "Travel", "description": "Business trip expenses", "amount": 3500},
        ]
        
        for i, trans_data in enumerate(transactions_data):
            transaction = Transaction(
                company_id=company1.id,
                type=trans_data["type"],
                category=trans_data["category"],
                description=trans_data["description"],
                amount=trans_data["amount"],
                date=datetime.now().date() - timedelta(days=random.randint(1, 90))
            )
            db.session.add(transaction)
        
        # Create Assets for Company 1
        print("Creating demo assets...")
        assets_data = [
            {"name": "Office Building", "category": "Property", "value": 500000},
            {"name": "Company Vehicles (3)", "category": "Vehicle", "value": 90000},
            {"name": "Computer Equipment", "category": "Technology", "value": 50000},
            {"name": "Office Furniture", "category": "Equipment", "value": 25000},
            {"name": "Server Infrastructure", "category": "Technology", "value": 75000},
        ]
        
        for asset_data in assets_data:
            asset = Asset(
                company_id=company1.id,
                name=asset_data["name"],
                category=asset_data["category"],
                value=asset_data["value"],
                purchase_date=datetime.now().date() - timedelta(days=random.randint(365, 1825)),
                description=f"{asset_data['name']} - Company asset"
            )
            db.session.add(asset)
        
        # Create Invoices for Company 1
        print("Creating demo invoices...")
        invoices_data = [
            {"client": "Acme Corp", "email": "billing@acme.com", "type": "invoice", "amount": 15000, "status": "paid"},
            {"client": "Global Tech", "email": "finance@globaltech.com", "type": "invoice", "amount": 25000, "status": "pending"},
            {"client": "StartUp Inc", "email": "accounts@startup.com", "type": "quotation", "amount": 12000, "status": "pending"},
            {"client": "Enterprise Solutions", "email": "pay@enterprise.com", "type": "invoice", "amount": 50000, "status": "paid"},
            {"client": "Small Business LLC", "email": "owner@smallbiz.com", "type": "quotation", "amount": 8000, "status": "pending"},
        ]
        
        for i, inv_data in enumerate(invoices_data):
            invoice = Invoice(
                company_id=company1.id,
                invoice_number=f"INV-{datetime.now().strftime('%Y%m')}-{1000 + i}",
                client_name=inv_data["client"],
                client_email=inv_data["email"],
                type=inv_data["type"],
                items=f"Professional services\nConsulting hours\nSoftware license",
                subtotal=inv_data["amount"],
                tax=inv_data["amount"] * 0.08,
                total=inv_data["amount"] * 1.08,
                status=inv_data["status"],
                issue_date=datetime.now().date() - timedelta(days=random.randint(5, 60)),
                due_date=datetime.now().date() + timedelta(days=30)
            )
            db.session.add(invoice)
        
        # Create Products for Company 1
        print("Creating demo products...")
        products_data = [
            {"name": "Laptop Computer", "sku": "TECH-001", "category": "Electronics", "qty": 25, "price": 1200},
            {"name": "Office Chair", "sku": "FURN-001", "category": "Furniture", "qty": 50, "price": 250},
            {"name": "Desk", "sku": "FURN-002", "category": "Furniture", "qty": 30, "price": 400},
            {"name": "Monitor 27\"", "sku": "TECH-002", "category": "Electronics", "qty": 45, "price": 350},
            {"name": "Wireless Mouse", "sku": "TECH-003", "category": "Electronics", "qty": 100, "price": 25},
            {"name": "Keyboard", "sku": "TECH-004", "category": "Electronics", "qty": 8, "price": 75},
            {"name": "Printer Paper (Ream)", "sku": "SUPP-001", "category": "Office Supplies", "qty": 200, "price": 5},
            {"name": "Whiteboard", "sku": "SUPP-002", "category": "Office Supplies", "qty": 5, "price": 150},
        ]
        
        for prod_data in products_data:
            product = Product(
                company_id=company1.id,
                name=prod_data["name"],
                sku=prod_data["sku"],
                category=prod_data["category"],
                description=f"High quality {prod_data['name']} for office use",
                quantity=prod_data["qty"],
                unit_price=prod_data["price"],
                reorder_level=10
            )
            db.session.add(product)
        
        # Create Marketing Campaigns for Company 1
        print("Creating demo campaigns...")
        campaigns_data = [
            {"name": "Q1 Email Campaign", "type": "Email", "budget": 5000, "status": "completed"},
            {"name": "Social Media Ads - Spring", "type": "Social Media", "budget": 8000, "status": "active"},
            {"name": "Google Ads - Product Launch", "type": "PPC", "budget": 12000, "status": "active"},
            {"name": "Content Marketing Series", "type": "Content", "budget": 3000, "status": "active"},
            {"name": "Trade Show Exhibition", "type": "Event", "budget": 15000, "status": "completed"},
        ]
        
        for camp_data in campaigns_data:
            campaign = Campaign(
                company_id=company1.id,
                name=camp_data["name"],
                type=camp_data["type"],
                description=f"Marketing campaign focused on brand awareness and lead generation",
                budget=camp_data["budget"],
                start_date=datetime.now().date() - timedelta(days=random.randint(30, 90)),
                end_date=datetime.now().date() + timedelta(days=random.randint(30, 90)),
                status=camp_data["status"]
            )
            db.session.add(campaign)
        
        # Create Leads for Company 1
        print("Creating demo leads...")
        leads_data = [
            {"name": "Sarah Johnson", "company": "Tech Startup", "email": "sarah@techstartup.com", "source": "Website", "status": "new"},
            {"name": "Mike Chen", "company": "Digital Agency", "email": "mike@digitalagency.com", "source": "Referral", "status": "contacted"},
            {"name": "Emily Rodriguez", "company": "E-commerce Store", "email": "emily@ecommerce.com", "source": "Campaign", "status": "qualified"},
            {"name": "James Wilson", "company": "Consulting Firm", "email": "james@consulting.com", "source": "Website", "status": "converted"},
            {"name": "Lisa Anderson", "company": "Manufacturing Co", "email": "lisa@mfg.com", "source": "Cold Call", "status": "contacted"},
            {"name": "Tom Baker", "company": "Retail Chain", "email": "tom@retail.com", "source": "Social Media", "status": "new"},
            {"name": "Nina Patel", "company": "Healthcare Provider", "email": "nina@healthcare.com", "source": "Website", "status": "qualified"},
            {"name": "Chris Taylor", "company": "Financial Services", "email": "chris@finserv.com", "source": "Referral", "status": "lost"},
        ]
        
        for lead_data in leads_data:
            lead = Lead(
                company_id=company1.id,
                name=lead_data["name"],
                email=lead_data["email"],
                phone=f"+1-555-{random.randint(1000, 9999)}",
                company_name=lead_data["company"],
                source=lead_data["source"],
                status=lead_data["status"],
                notes=f"Interested in our enterprise solutions. Follow up scheduled."
            )
            db.session.add(lead)
        
        # Create Notifications for admin user
        print("Creating demo notifications...")
        notifications_data = [
            {"message": "Welcome to the ERP System! Your account has been created successfully.", "type": "success"},
            {"message": "Low stock alert: Keyboard (TECH-004) is below reorder level.", "type": "warning"},
            {"message": "New lead added: Sarah Johnson from Tech Startup", "type": "info"},
            {"message": "Invoice INV-202501-1001 has been paid by Acme Corp", "type": "success"},
            {"message": "Monthly payroll transaction recorded: $45,000", "type": "info"},
        ]
        
        for notif_data in notifications_data:
            notification = Notification(
                user_id=admin_user.id,
                message=notif_data["message"],
                type=notif_data["type"],
                is_read=False
            )
            db.session.add(notification)
        
        # Commit all changes
        db.session.commit()
        print("\n" + "="*60)
        print("Database initialized successfully with demo data!")
        print("="*60)
        print("\nDemo Login Credentials:")
        print("-" * 60)
        print("Admin User (TechCorp Solutions):")
        print("  Email: admin@demo.com")
        print("  Password: admin123")
        print("\nRegular User (TechCorp Solutions):")
        print("  Email: user@demo.com")
        print("  Password: user123")
        print("\nManager User (Green Manufacturing Inc):")
        print("  Email: manager@demo.com")
        print("  Password: manager123")
        print("="*60)

if __name__ == '__main__':
    init_db_with_demo_data()
