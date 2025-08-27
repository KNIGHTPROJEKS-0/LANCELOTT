#!/usr/bin/env python3

# Quick setup script for Vajra admin account
# This script creates the initial admin user for Vajra

import uuid
from vajra import app, db, bcrypt
from vajra.models import Admin

def create_admin_user():
    with app.app_context():
        # Check if any admin users exist
        existing_admin = Admin.query.first()
        if existing_admin:
            print("Admin user already exists!")
            print(f"Username: {existing_admin.username}")
            print(f"Email: {existing_admin.email}")
            response = input("Do you want to create another admin user? (y/n): ")
            if response.lower() != 'y':
                return
        
        print("Creating new admin user for Vajra...")
        print("=" * 50)
        
        # Get user input
        username = input("Enter username: ")
        email = input("Enter email: ")
        password = input("Enter password: ")
        
        # Validate input
        if not username or not email or not password:
            print("Error: All fields are required!")
            return
        
        # Check if username or email already exists
        existing_user = Admin.query.filter((Admin.username == username) | (Admin.email == email)).first()
        if existing_user:
            print("Error: Username or email already exists!")
            return
        
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
            theme="1",  # Default theme
            awsUsage=0,
            azureUsage=0
        )
        
        try:
            db.session.add(admin_user)
            db.session.commit()
            print("\n✅ Admin user created successfully!")
            print("=" * 50)
            print(f"Username: {username}")
            print(f"Email: {email}")
            print("You can now log in to Vajra with these credentials.")
        except Exception as e:
            db.session.rollback()
            print(f"❌ Error creating admin user: {str(e)}")

if __name__ == "__main__":
    create_admin_user()
