from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .app import db, login_manager


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120))
    location = db.Column(db.String(120))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    users = db.relationship("User", backref="company", lazy=True)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))
    role = db.Column(db.String(20), default="admin")  # admin or user

    subscription_plan = db.Column(db.String(20), default="Free")
    subscription_status = db.Column(db.String(20), default="inactive")
    payment_ref = db.Column(db.String(64))

    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class FinanceTransaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    type = db.Column(db.String(20), nullable=False)  # income | expense
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    date = db.Column(db.DateTime, default=datetime.utcnow)


class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    value = db.Column(db.Float, default=0.0)
    acquired_date = db.Column(db.DateTime, default=datetime.utcnow)


class Invoice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    client_name = db.Column(db.String(120), nullable=False)
    items_json = db.Column(db.Text, nullable=False)  # simple JSON string of items
    total = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    client_name = db.Column(db.String(120), nullable=False)
    items_json = db.Column(db.Text, nullable=False)
    total = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120))
    salary = db.Column(db.Float, default=0.0)
    department = db.Column(db.String(120))
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class EmployeeDocument(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    link = db.Column(db.String(255))  # simple URL or text reference
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    channel = db.Column(db.String(120))
    budget = db.Column(db.Float, default=0.0)
    start_date = db.Column(db.DateTime, default=datetime.utcnow)
    end_date = db.Column(db.DateTime)
    notes = db.Column(db.Text)


class Lead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    status = db.Column(db.String(50), default="new")
    source = db.Column(db.String(120))
    campaign_id = db.Column(db.Integer, db.ForeignKey("campaign.id"))


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(50))
    address = db.Column(db.String(255))


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(120))
    sku = db.Column(db.String(120), unique=True)
    quantity_on_hand = db.Column(db.Integer, default=0)
    unit_price = db.Column(db.Float, default=0.0)


class InventoryMovement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # in | out
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    note = db.Column(db.String(255))
