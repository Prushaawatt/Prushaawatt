import json
from datetime import datetime, timedelta
from .app import db
from .models import (
    Company,
    User,
    FinanceTransaction,
    Asset,
    Invoice,
    Quote,
    Employee,
    EmployeeDocument,
    Campaign,
    Lead,
    Client,
    Product,
)


def seed_demo_data():
    if User.query.first():
        return

    # Company and Admin user
    acme = Company(name="ACME Corp", industry="Manufacturing", location="New York")
    db.session.add(acme)
    admin = User(
        email="admin@example.com",
        full_name="Admin User",
        role="admin",
        phone="+1-555-1000",
        address="123 Admin St, NY",
        company=acme,
        subscription_plan="Premium",
        subscription_status="active",
        payment_ref="DEMO123",
    )
    admin.set_password("admin123")
    db.session.add(admin)

    # Finance transactions
    db.session.add_all(
        [
            FinanceTransaction(company_id=1, type="income", amount=5000, description="Product sale"),
            FinanceTransaction(company_id=1, type="expense", amount=1200, description="Office rent"),
            FinanceTransaction(company_id=1, type="income", amount=2300, description="Service fee"),
            FinanceTransaction(company_id=1, type="expense", amount=300, description="Utilities"),
        ]
    )

    # Assets
    db.session.add_all(
        [
            Asset(company_id=1, name="Laptop", value=1200),
            Asset(company_id=1, name="3D Printer", value=2400),
        ]
    )

    # Invoices and Quotes
    invoice_items = json.dumps([
        {"item": "Widget A", "qty": 3, "price": 200},
        {"item": "Service Consulting", "qty": 5, "price": 100},
    ])
    quote_items = json.dumps([
        {"item": "Prototype B", "qty": 2, "price": 500},
    ])
    db.session.add(Invoice(company_id=1, client_name="Globex", items_json=invoice_items, total=1100, status="paid"))
    db.session.add(Quote(company_id=1, client_name="Soylent", items_json=quote_items, total=1000))

    # HR
    emp1 = Employee(company_id=1, full_name="Jane Doe", role="Engineer", salary=70000, department="R&D", email="jane@example.com", phone="+1-555-2001")
    emp2 = Employee(company_id=1, full_name="John Smith", role="Designer", salary=65000, department="Design", email="john@example.com", phone="+1-555-2002")
    db.session.add_all([emp1, emp2])
    db.session.add(EmployeeDocument(employee_id=1, title="Employment Contract", link="/docs/jane_contract.pdf"))

    # Marketing
    camp = Campaign(company_id=1, name="Spring Launch", channel="Email", budget=2000)
    db.session.add(camp)
    db.session.add_all([
        Lead(company_id=1, name="Alice Lead", email="alice@lead.com", status="contacted", source="web", campaign_id=1),
        Lead(company_id=1, name="Bob Lead", email="bob@lead.com", status="new", source="event", campaign_id=1),
    ])
    db.session.add(Client(company_id=1, name="Globex", email="sales@globex.com", phone="+1-555-4000", address="1 Global Way"))

    # Inventory
    prod1 = Product(company_id=1, name="Widget A", category="Widgets", sku="WID-A", quantity_on_hand=25, unit_price=200)
    prod2 = Product(company_id=1, name="Gadget B", category="Gadgets", sku="GAD-B", quantity_on_hand=5, unit_price=350)
    db.session.add_all([prod1, prod2])

    db.session.commit()
