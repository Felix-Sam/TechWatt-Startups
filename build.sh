#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install the dependencies
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Define superuser details
SUPERUSER_EMAIL=felixsam922@gmail.com
SUPERUSER_USERNAME=Felix 
SUPERUSER_PASSWORD=Fe0546637494

# Create a superuser account if it doesn't exist
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(email='$SUPERUSER_EMAIL').exists():
    User.objects.create_superuser(username='$SUPERUSER_USERNAME', email='$SUPERUSER_EMAIL', password='$SUPERUSER_PASSWORD')
    print('Superuser created.')
else:
    print('Superuser with this email already exists.')
EOF
