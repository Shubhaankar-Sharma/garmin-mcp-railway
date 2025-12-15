# Garmin MCP Server - Complete Setup Guide

## Overview

This guide covers deploying your Garmin MCP server to Railway and connecting it to Poke (or any other MCP-compatible AI assistant).

## What's Changed

I've transformed your Garmin MCP server to support remote hosting:

1. ✅ Created `server_sse.py` - SSE-enabled server for remote access
2. ✅ Added Railway deployment files (`Procfile`, `railway.toml`, `runtime.txt`)
3. ✅ Updated dependencies to include web server components
4. ✅ Created comprehensive deployment documentation

## Garmin API Requirements

### Good News: No API Keys Needed! 🎉

Unlike many services, Garmin Connect does **NOT** require API keys. You only need:

- **Garmin Email:** Your Garmin Connect account email
- **Garmin Password:** Your Garmin Connect account password

That's it! The server uses the `garminconnect` Python library which interfaces directly with Garmin Connect's web API.

### Authentication Flow

1. **First login:** Server uses email + password to authenticate
2. **OAuth tokens generated:** Garmin returns OAuth tokens
3. **Tokens stored:** Tokens saved for future use (no re-login needed)
4. **Automatic refresh:** Library handles token refresh automatically

### Multi-Factor Authentication (MFA)

If you have MFA enabled (recommended for security):

1. You must generate OAuth tokens locally first
2. Then provide those tokens to the Railway deployment
3. See "MFA Setup" section in RAILWAY_DEPLOYMENT.md

## Quick Deployment Steps

### Step 1: Generate OAuth Tokens (MFA users only)

```bash
# Set credentials
export GARMIN_EMAIL="your_email@example.com"
export GARMIN_PASSWORD="your_password"

# Run local server to generate tokens
uv run garmin-mcp
# Enter MFA code when prompted

# Get the token for Railway
cat ~/.garminconnect_base64
# Copy this token!
```

### Step 2: Deploy to Railway

```bash
# Initialize Railway project (will open browser)
railway init

# Deploy the code
railway up

# Set environment variables
railway variables set GARMIN_EMAIL="your_email@example.com"
railway variables set GARMIN_PASSWORD="your_password"

# OR if you have MFA and generated tokens:
railway variables set GARMINTOKENS_BASE64="<paste_token_here>"

# Open dashboard to get your URL
railway open
```

### Step 3: Get Your Server URL

1. In Railway dashboard, go to **Settings**
2. Click **Generate Domain** under Domains
3. Copy the URL (e.g., `https://garmin-mcp-server-production.up.railway.app`)

### Step 4: Connect to Poke

In Poke's integration form:

- **Name:** `Garmin Connect`
- **Server URL:** `https://your-railway-url.railway.app/sse`
- **API Key:** Leave empty (not needed)

**Important:** Don't forget to add `/sse` at the end of your Railway URL!

## What Can Poke Access?

Once connected, Poke can access these tools from your Garmin account:

### Activity Management
- List recent activities
- Get detailed activity data
- View activity summaries
- Access exercise sets and workout steps

### Health & Wellness
- Daily step counts
- Heart rate data
- Sleep tracking
- Stress levels
- Body battery
- Respiration rate

### User Profile & Devices
- Personal profile information
- Connected devices
- Device settings

### Training & Workouts
- Training status
- Workout schedules
- Training plans
- VO2 Max data

### Body Composition
- Weight tracking
- Body composition metrics
- Hydration levels

### Other Features
- Gear management
- Active challenges
- Women's health tracking
- Data export capabilities

## Security Considerations

### Credentials
- Never commit credentials to git
- Use Railway's environment variables for all secrets
- Consider using Railway's secret files for OAuth tokens

### Token Storage
- OAuth tokens are sensitive - treat like passwords
- Tokens stored in Railway are encrypted at rest
- Railway has ephemeral filesystem, so tokens need to be in env vars

### Network Security
- Railway provides HTTPS by default
- Your credentials are never exposed in URLs
- MCP communication over SSE is secure

## Environment Variables Reference

### Required (choose one option):

**Option A - Email/Password (without MFA):**
```
GARMIN_EMAIL=your_email@example.com
GARMIN_PASSWORD=your_password
```

**Option B - Pre-generated OAuth Tokens (with MFA):**
```
GARMINTOKENS_BASE64=<base64_encoded_oauth_tokens>
```

### Optional:
```
PORT=8000  # Railway sets this automatically
GARMINTOKENS=~/.garminconnect  # Token directory path
```

## Troubleshooting

### "MFA not supported in SSE mode"
**Solution:** Pre-generate OAuth tokens locally and use `GARMINTOKENS_BASE64`.

### "Failed to initialize Garmin Connect client"
**Solutions:**
- Verify credentials are correct
- Check Railway logs: `railway logs`
- Ensure tokens are valid (may need to regenerate)

### "Connection timeout" in Poke
**Solutions:**
- Verify Railway service is running
- Check that you added `/sse` to the URL
- Test the health endpoint: `https://your-url/health` (should return "OK")

### Garmin rate limiting
Garmin may rate limit requests. If you see errors:
- Wait a few minutes before retrying
- Consider caching responses if making frequent requests

## Cost Information

### Railway Pricing
- **Hobby Plan:** $5/month (enough for personal use)
- **Pro Plan:** $20/month (for higher usage)
- First 500 hours of execution free each month

### Typical Usage
- Idle server: ~$0.50-1.00/month
- Light use (few requests/day): ~$1-2/month
- Should fit comfortably in Hobby plan

## Testing Your Deployment

### 1. Test Health Endpoint
```bash
curl https://your-railway-url.railway.app/health
# Should return: OK
```

### 2. Check Railway Logs
```bash
railway logs
# Look for: "Garmin Connect client initialized successfully"
```

### 3. Test in Poke
Ask Poke: "List my recent Garmin activities"

## Files Added/Modified

- `src/garmin_mcp/server_sse.py` - New SSE server
- `pyproject.toml` - Added web server dependencies
- `requirements.txt` - Dependency list for Railway
- `Procfile` - Railway process definition
- `railway.toml` - Railway configuration
- `runtime.txt` - Python version specification
- `.env.example` - Example environment variables
- `RAILWAY_DEPLOYMENT.md` - Detailed deployment guide
- `SETUP_GUIDE.md` - This file

## Next Steps

1. Follow deployment steps above
2. Test the health endpoint
3. Connect to Poke
4. Try asking Poke about your Garmin data!

## Support & Issues

- Railway Docs: https://docs.railway.app
- MCP Protocol: https://modelcontextprotocol.io
- Garmin MCP Issues: https://github.com/Taxuspt/garmin_mcp/issues

## Example Poke Queries

Once connected, try asking Poke:
- "Show me my recent workouts"
- "What was my sleep quality last night?"
- "How many steps did I take yesterday?"
- "What's my current training status?"
- "Show me my heart rate data from my last run"
- "List my connected Garmin devices"
