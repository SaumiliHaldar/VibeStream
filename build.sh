#!/usr/bin/env bash
# exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --no-input

# Check if superuser exists, and create if not
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

# Check if superuser already exists
if not User.objects.filter(username="admin").exists():
    User.objects.create_superuser(
        username="admin",
        email="admin@example.com",
        password="admin123"
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists.")
EOF
