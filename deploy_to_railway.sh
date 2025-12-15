#!/bin/bash

# Garmin MCP Server - Railway Deployment Helper Script
# This script helps deploy the Garmin MCP server to Railway

set -e  # Exit on error

echo "🚀 Garmin MCP Server - Railway Deployment Helper"
echo "================================================"
echo ""

# Check if railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found!"
    echo "Please install it: curl -fsSL https://railway.app/install.sh | sh"
    exit 1
fi

# Check if logged in
echo "Checking Railway authentication..."
if ! railway whoami &> /dev/null; then
    echo "❌ Not logged in to Railway"
    echo "Please run: railway login"
    exit 1
fi

echo "✅ Railway CLI authenticated"
echo ""

# Check for MFA
echo "Does your Garmin account have Multi-Factor Authentication (MFA) enabled?"
echo "1) Yes - I need to generate OAuth tokens first"
echo "2) No - I can use email/password directly"
read -p "Choose (1 or 2): " mfa_choice

if [ "$mfa_choice" == "1" ]; then
    echo ""
    echo "📝 MFA Setup Required"
    echo "===================="
    echo "You need to generate OAuth tokens locally first."
    echo ""
    echo "Steps:"
    echo "1. Set your credentials:"
    echo "   export GARMIN_EMAIL=\"your_email@example.com\""
    echo "   export GARMIN_PASSWORD=\"your_password\""
    echo ""
    echo "2. Run the local server:"
    echo "   uv run garmin-mcp"
    echo ""
    echo "3. Enter your MFA code when prompted"
    echo ""
    echo "4. Get the token:"
    echo "   cat ~/.garminconnect_base64"
    echo ""
    echo "5. Re-run this script when you have the token"
    echo ""
    read -p "Press Enter if you have completed these steps, or Ctrl+C to exit..."
    echo ""
    read -p "Paste your GARMINTOKENS_BASE64 token: " garmin_token

    if [ -z "$garmin_token" ]; then
        echo "❌ Token cannot be empty"
        exit 1
    fi
elif [ "$mfa_choice" == "2" ]; then
    echo ""
    read -p "Enter your Garmin email: " garmin_email
    read -s -p "Enter your Garmin password: " garmin_password
    echo ""

    if [ -z "$garmin_email" ] || [ -z "$garmin_password" ]; then
        echo "❌ Email and password cannot be empty"
        exit 1
    fi
else
    echo "❌ Invalid choice"
    exit 1
fi

echo ""
echo "🚂 Deploying to Railway..."
echo "=========================="
echo ""

# Initialize Railway project (this may prompt for project creation)
echo "Initializing Railway project..."
echo "If prompted, choose 'Create a new project' and name it 'garmin-mcp-server'"
echo ""

# Try to link/init Railway project
if [ ! -f ".railway" ]; then
    railway init
fi

echo ""
echo "📦 Deploying code to Railway..."
railway up

echo ""
echo "🔐 Setting environment variables..."
if [ "$mfa_choice" == "1" ]; then
    railway variables set GARMINTOKENS_BASE64="$garmin_token"
    echo "✅ Set GARMINTOKENS_BASE64"
else
    railway variables set GARMIN_EMAIL="$garmin_email"
    railway variables set GARMIN_PASSWORD="$garmin_password"
    echo "✅ Set GARMIN_EMAIL and GARMIN_PASSWORD"
fi

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📋 Next Steps:"
echo "=============="
echo "1. Open Railway dashboard:"
echo "   railway open"
echo ""
echo "2. Generate a domain in Settings → Domains"
echo ""
echo "3. Your SSE endpoint will be:"
echo "   https://your-domain.railway.app/sse"
echo ""
echo "4. Test the health endpoint:"
echo "   curl https://your-domain.railway.app/health"
echo ""
echo "5. Add to Poke with the /sse URL"
echo ""
echo "View logs: railway logs"
echo ""
echo "For detailed documentation, see SETUP_GUIDE.md"
