#!/usr/bin/env python3

from vajra import app, db
from vajra.models import Admin

with app.app_context():
    admin_count = Admin.query.count()
    print(f'Number of admin users: {admin_count}')
    if admin_count > 0:
        admins = Admin.query.all()
        for admin in admins:
            print(f'Username: {admin.username}, Email: {admin.email}')
    else:
        print("No admin users found.")
