# Railway Deployment Summary

## What Was Done ✅

I've transformed your Garmin MCP server to support remote hosting on Railway:

### Files Created:
1. **`src/garmin_mcp/server_sse.py`** - SSE-enabled server for remote access
2. **`Procfile`** - Railway process configuration
3. **`railway.toml`** - Railway deployment settings
4. **`runtime.txt`** - Python version specification
5. **`requirements.txt`** - Python dependencies
6. **`.env.example`** - Example environment variables
7. **`deploy_to_railway.sh`** - Automated deployment script
8. **Documentation:**
   - `SETUP_GUIDE.md` - Quick start guide
   - `RAILWAY_DEPLOYMENT.md` - Detailed deployment instructions
   - `DEPLOYMENT_SUMMARY.md` - This file

### Files Modified:
1. **`pyproject.toml`** - Added web server dependencies (starlette, uvicorn, httpx)
2. **`README.md`** - Added Railway deployment section

## Garmin API Keys & Credentials 🔑

### No API Keys Required! 🎉

**You only need:**
- Your Garmin Connect email address
- Your Garmin Connect password

**How it works:**
1. Server logs in with your credentials
2. Garmin returns OAuth tokens
3. Tokens are stored and automatically refreshed
4. No manual API key registration needed

### If You Have MFA Enabled:

You'll need to generate OAuth tokens locally first:

```bash
export GARMIN_EMAIL="your_email@example.com"
export GARMIN_PASSWORD="your_password"
uv run garmin-mcp  # Enter MFA code when prompted
cat ~/.garminconnect_base64  # Copy this token for Railway
```

## Deployment Steps 🚀

### Option 1: Automated Script (Easiest)

```bash
./deploy_to_railway.sh
```

The script will:
- Check Railway CLI installation
- Verify authentication
- Guide you through MFA setup if needed
- Deploy the code
- Set environment variables
- Provide next steps

### Option 2: Manual Deployment

```bash
# 1. Initialize project
railway init

# 2. Deploy code
railway up

# 3. Set credentials (choose one):

# Without MFA:
railway variables set GARMIN_EMAIL="your_email@example.com"
railway variables set GARMIN_PASSWORD="your_password"

# With MFA (preferred):
railway variables set GARMINTOKENS_BASE64="<your_token>"

# 4. Get your URL
railway open
```

## Configuring Poke 🤖

Once deployed:

1. **Get your Railway URL** from the dashboard (Settings → Domains)
2. **Add to Poke:**
   - **Name:** `Garmin Connect`
   - **Server URL:** `https://your-railway-url.railway.app/sse`
   - **API Key:** Leave empty

**⚠️ Important:** Add `/sse` to the end of your Railway URL!

## Testing Your Deployment ✓

```bash
# 1. Test health endpoint
curl https://your-railway-url.railway.app/health
# Should return: OK

# 2. Check logs
railway logs
# Look for: "Garmin Connect client initialized successfully"

# 3. Test in Poke
# Ask: "List my recent Garmin activities"
```

## What Poke Can Access 📊

Once connected, Poke can access:

- **Activities:** List and view detailed activity data
- **Health Metrics:** Steps, heart rate, sleep, stress, body battery
- **Training:** Training status, plans, VO2 Max
- **Body Composition:** Weight, body fat, hydration
- **Devices:** Connected devices and settings
- **Gear:** Gear management
- **Challenges:** Active challenges
- **And more!**

## Environment Variables Reference 📝

### Required (choose one):

**Without MFA:**
```bash
GARMIN_EMAIL=your_email@example.com
GARMIN_PASSWORD=your_password
```

**With MFA (recommended):**
```bash
GARMINTOKENS_BASE64=<base64_oauth_tokens>
```

### Optional:
```bash
PORT=8000  # Railway sets automatically
```

## Troubleshooting 🔧

### "MFA not supported in SSE mode"
→ Pre-generate tokens locally with `uv run garmin-mcp`

### "Failed to initialize Garmin Connect client"
→ Check credentials and logs with `railway logs`

### "Connection timeout" in Poke
→ Verify URL ends with `/sse` and test `/health` endpoint

### View logs
```bash
railway logs  # View deployment logs
railway logs -f  # Follow logs in real-time
```

## Cost Estimate 💰

**Railway Hobby Plan:** $5/month
- Includes $5 of usage
- Enough for personal use
- Typical usage: $1-2/month

## Next Steps 📋

1. ✅ Run `./deploy_to_railway.sh` OR follow manual steps
2. ✅ Generate domain in Railway dashboard
3. ✅ Test health endpoint
4. ✅ Add to Poke with `/sse` URL
5. ✅ Ask Poke about your Garmin data!

## Quick Links 🔗

- **Railway Dashboard:** `railway open`
- **View Logs:** `railway logs`
- **Detailed Guide:** [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
- **Setup Guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)

## Support 🆘

- Railway Docs: https://docs.railway.app
- MCP Protocol: https://modelcontextprotocol.io
- Project Issues: https://github.com/Taxuspt/garmin_mcp/issues

---

**Ready to deploy?** Run `./deploy_to_railway.sh` to get started!
