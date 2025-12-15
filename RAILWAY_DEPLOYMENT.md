# Railway Deployment Guide for Garmin MCP Server

This guide will help you deploy the Garmin MCP server to Railway so it can be accessed remotely by AI assistants like Poke.

## Prerequisites

1. Railway account (sign up at https://railway.app)
2. Railway CLI installed (you have this ✅)
3. Garmin Connect account credentials

## Important: No Garmin API Keys Required!

**Good news:** This server does NOT require Garmin API keys. It uses your personal Garmin Connect credentials (email and password) to access your data directly through the Garmin Connect API.

## Step 1: Setup OAuth Tokens Locally (REQUIRED for MFA users)

If you have Multi-Factor Authentication (MFA) enabled on your Garmin account, you need to generate OAuth tokens locally first:

```bash
# Set your credentials as environment variables
export GARMIN_EMAIL="your_email@example.com"
export GARMIN_PASSWORD="your_password"

# Run the local server to generate tokens (it will prompt for MFA code)
uv run garmin-mcp
```

When prompted, enter your MFA code. This will generate OAuth tokens in `~/.garminconnect/` directory.

**Important:** You'll need to provide these tokens to Railway as an environment variable. Get the base64-encoded token:

```bash
cat ~/.garminconnect_base64
```

Copy this token - you'll need it in Step 3.

## Step 2: Deploy to Railway

### Option A: Using Railway CLI (Recommended)

1. **Initialize the project:**
   ```bash
   railway init
   ```
   - Select "Create a new project"
   - Name it "garmin-mcp-server" (or your preferred name)
   - Select your workspace

2. **Deploy:**
   ```bash
   railway up
   ```

### Option B: Using Railway Dashboard

1. Go to https://railway.app/new
2. Click "Deploy from GitHub repo"
3. Connect this repository
4. Railway will automatically detect the Python app

## Step 3: Configure Environment Variables

In the Railway dashboard for your project:

1. Go to **Variables** tab
2. Add the following variables:

### Required Variables:

```
GARMIN_EMAIL=your_email@example.com
GARMIN_PASSWORD=your_password
```

### For MFA Users (Highly Recommended):

Instead of email/password, use the pre-generated OAuth tokens:

```
GARMINTOKENS_BASE64=<paste the token from ~/.garminconnect_base64>
```

**Note:** If you use `GARMINTOKENS_BASE64`, you can omit `GARMIN_EMAIL` and `GARMIN_PASSWORD`.

### Optional Variables:

```
PORT=8000  # Railway sets this automatically, usually not needed
```

## Step 4: Get Your Server URL

After deployment:

1. Go to your Railway project dashboard
2. Click on **Settings** tab
3. Under **Domains**, click **Generate Domain**
4. Copy the generated URL (e.g., `https://garmin-mcp-server-production.up.railway.app`)

## Step 5: Configure Poke Integration

Now you can add this MCP server to Poke:

1. In Poke, go to **Integrations** → **New Integration**
2. Fill in the form:
   - **Name:** Garmin Connect
   - **Server URL:** `https://your-railway-domain.railway.app/sse`
   - **API Key:** Leave empty (not required)

**Important:** Make sure to add `/sse` to the end of your Railway URL!

## Manual Deployment Steps (Alternative)

If the CLI approach doesn't work, you can deploy manually:

```bash
# 1. Login to Railway
railway login

# 2. Create a new project (this will open a browser)
railway init --name garmin-mcp-server

# 3. Deploy the code
railway up

# 4. Set environment variables
railway variables set GARMIN_EMAIL="your_email@example.com"
railway variables set GARMIN_PASSWORD="your_password"

# Or if using OAuth tokens:
railway variables set GARMINTOKENS_BASE64="<your_token>"

# 5. Open the dashboard to get your URL
railway open
```

## Available Endpoints

Once deployed, your server will have:

- **Health Check:** `https://your-domain.railway.app/health` - Returns "OK" if server is running
- **SSE Endpoint:** `https://your-domain.railway.app/sse` - MCP Server-Sent Events endpoint

## Troubleshooting

### Issue: "MFA not supported in SSE mode"

**Solution:** Pre-generate OAuth tokens locally (see Step 1) and use `GARMINTOKENS_BASE64` environment variable.

### Issue: "Failed to initialize Garmin Connect client"

**Solutions:**
- Verify your credentials are correct
- Check if you need to set `GARMINTOKENS_BASE64`
- Check Railway logs: `railway logs`

### Issue: "Connection refused" or timeout

**Solutions:**
- Ensure the Railway service is running
- Check that the domain was generated in Railway settings
- Verify the PORT environment variable is set correctly

### Check Logs

View deployment logs:
```bash
railway logs
```

## Security Notes

⚠️ **Important Security Considerations:**

1. **Never commit credentials** to git - Railway will inject them as environment variables
2. **OAuth tokens are sensitive** - treat them like passwords
3. **Use Railway's environment variables** - don't hardcode credentials
4. **Consider using Railway's Volume feature** for persistent token storage across deploys

## What Can Poke Do With This Integration?

Once connected, Poke can:
- List your recent Garmin activities
- Get detailed activity information
- Access health metrics (steps, heart rate, sleep)
- View body composition data
- Check device information
- View training plans and scheduled workouts
- Access gear management data
- And much more!

## Cost Estimate

Railway offers:
- **Free tier:** $5 of usage per month (usually enough for hobby projects)
- **Pro plan:** $20/month with $5 included usage

This MCP server is lightweight and should run well within free tier limits for personal use.

## Need Help?

- Railway Documentation: https://docs.railway.app
- MCP Protocol: https://modelcontextprotocol.io
- This project's issues: https://github.com/Taxuspt/garmin_mcp/issues
