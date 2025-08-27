#!/usr/bin/env python3

import uuid
from vajra import app, db, bcrypt
from vajra.models import Admin

def create_default_admin():
    with app.app_context():
        # Check if any admin users exist
        existing_admin = Admin.query.first()
        if existing_admin:
            print("✅ Admin user already exists!")
            print(f"Username: {existing_admin.username}")
            print(f"Email: {existing_admin.email}")
            return
        
        print("Creating default admin user...")
        
        # Create default admin credentials
        username = "admin"
        email = "admin@vajra.local"
        password = "admin123"
        
        # Hash the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new admin user
        user_id = str(uuid.uuid4())
        admin_user = Admin(
            id=user_id,
            username=username,
            email=email,
            password=hashed_password,
            enableIp="",
            ips="",
            theme="1",
            awsUsage=0,
            azureUsage=0
        )
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            print("\n✅ Default admin user created successfully!")
            print("=" * 50)
            print(f"Username: {username}")
            print(f"Email: {email}")
            print(f"Password: {password}")
            print("=" * 50)
            print("⚠️  Please change the password after first login!")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {str(e)}")

if __name__ == "__main__":
    create_default_admin()
