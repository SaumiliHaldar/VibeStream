#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate --no-input

# Create superuser only if it doesn't exist
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()

if not User.objects.filter(username="saumilihaldar").exists():
    User.objects.create_superuser(
        username="saumilihaldar",
        email="haldar.saumili843@gmail.com",
        password="1234"
    )
    print("Superuser created successfully!")
else:
    print("Superuser already exists. Skipping creation.")
EOF
