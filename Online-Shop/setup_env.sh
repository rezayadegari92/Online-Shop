#!/bin/bash

# =============================================================================
# Online Shop - Environment Setup Script
# =============================================================================
# This script helps you set up your .env file
# =============================================================================

echo "====================================="
echo "Online Shop - Environment Setup"
echo "====================================="
echo ""

# Check if .env already exists
if [ -f ".env" ]; then
    echo "⚠️  Warning: .env file already exists!"
    read -p "Do you want to overwrite it? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Setup cancelled."
        exit 1
    fi
fi

# Copy from ENV_TEMPLATE.txt
if [ -f "ENV_TEMPLATE.txt" ]; then
    echo "📄 Creating .env file from template..."
    cp ENV_TEMPLATE.txt .env
    echo "✅ .env file created successfully!"
else
    echo "❌ Error: ENV_TEMPLATE.txt not found!"
    exit 1
fi

echo ""
echo "====================================="
echo "⚡ Important Security Notes:"
echo "====================================="
echo ""
echo "1. 🔐 Change the SECRET_KEY in production!"
echo "   Generate a new one with:"
echo "   python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'"
echo ""
echo "2. 📧 Update EMAIL_HOST_PASSWORD with your Gmail App Password"
echo "   Visit: https://myaccount.google.com/apppasswords"
echo ""
echo "3. 🔒 Never commit the .env file to version control"
echo "   (It should already be in .gitignore)"
echo ""
echo "4. 🚀 For production, set DEBUG=False and update ALLOWED_HOSTS"
echo ""
echo "====================================="
echo "✅ Setup Complete!"
echo "====================================="
echo ""
echo "Next steps:"
echo "1. Edit .env file and update your configuration"
echo "2. Run: docker-compose up -d"
echo "3. Run migrations: docker-compose exec web python manage.py migrate"
echo ""

