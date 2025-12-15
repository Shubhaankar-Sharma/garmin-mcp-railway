# Quick Deploy to Railway 🚀

Your code is ready and pushed to GitHub! Here's how to deploy in 2 minutes:

## GitHub Repository
**https://github.com/Shubhaankar-Sharma/garmin-mcp-railway**

## Deploy to Railway (Easy Method)

### Step 1: Go to Railway
Visit: https://railway.app/new

### Step 2: Deploy from GitHub
1. Click **"Deploy from GitHub repo"**
2. Select: **Shubhaankar-Sharma/garmin-mcp-railway**
3. Click **Deploy**

Railway will automatically:
- Detect the Python project
- Install dependencies
- Use the Dockerfile
- Start the server

### Step 3: Add Environment Variables

In Railway dashboard:
1. Click on your service
2. Go to **Variables** tab
3. Click **+ New Variable**
4. Add these:

```
GARMIN_EMAIL=your_garmin_email@example.com
GARMIN_PASSWORD=your_garmin_password
```

### Step 4: Generate Domain

1. Go to **Settings** tab
2. Scroll to **Networking** section
3. Click **Generate Domain**
4. Copy the URL (e.g., `https://garmin-mcp-railway-production.up.railway.app`)

### Step 5: Connect to Poke

In Poke's integration form:
- **Name:** `Garmin Connect`
- **Server URL:** `https://your-railway-domain.railway.app/sse`
- **API Key:** Leave empty

**⚠️ Don't forget `/sse` at the end!**

---

## Alternative: Deploy via Railway CLI

```bash
# 1. Clone your repo (or stay in current directory)
cd /Users/shubhaankar/github.com/Taxuspt/garmin_mcp

# 2. Initialize Railway
railway init

# 3. Deploy
railway up

# 4. Set variables
railway variables set GARMIN_EMAIL="your_email@example.com"
railway variables set GARMIN_PASSWORD="your_password"

# 5. Open dashboard
railway open
```

---

## Test Your Deployment

### Health Check
```bash
curl https://your-domain.railway.app/health
# Should return: OK
```

### View Logs
```bash
railway logs
# Should show: "Garmin Connect client initialized successfully"
```

### Test in Poke
Ask: **"List my recent Garmin activities"**

---

## Deployment Options Summary

You have **3 deployment methods**:

1. **Railway Dashboard** (Easiest) ✅ Recommended
   - Go to https://railway.app/new
   - Click "Deploy from GitHub repo"
   - Select your repo

2. **Railway CLI**
   - Run `railway init` → `railway up`

3. **Docker** (Advanced)
   - Build: `docker build -t garmin-mcp .`
   - Run: `docker run -p 8000:8000 -e GARMIN_EMAIL=... garmin-mcp`

---

## What's Included

- ✅ SSE Server for remote MCP access
- ✅ Dockerfile for containerized deployment
- ✅ Railway configuration files
- ✅ Automated deployment script
- ✅ Comprehensive documentation
- ✅ Health check endpoint
- ✅ All Garmin MCP tools

---

## Need Help?

- **Railway Dashboard:** https://railway.app
- **View Logs:** `railway logs`
- **Documentation:** See SETUP_GUIDE.md
- **Issues:** https://github.com/Shubhaankar-Sharma/garmin-mcp-railway/issues

---

## Next Steps

1. ✅ Code is on GitHub
2. 🚀 Deploy via Railway dashboard (https://railway.app/new)
3. 🔧 Add your Garmin credentials as environment variables
4. 🌐 Generate domain
5. 🤖 Connect to Poke with `/sse` endpoint
6. ✨ Ask Poke about your Garmin data!

**Ready? Go to https://railway.app/new and deploy now!**
