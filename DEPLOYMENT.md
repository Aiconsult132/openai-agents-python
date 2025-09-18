# 🚀 Deployment Guide

## Vercel Deployment

This project includes a Vercel-compatible version for easy deployment to the cloud.

### Files for Vercel:
- `app.py` - Vercel-compatible FastAPI app (simplified, no WebSockets)
- `vercel.json` - Vercel configuration
- `requirements.txt` - Python dependencies

### 🔧 Setup Instructions:

1. **Fork/Clone this repository** to your GitHub account

2. **Connect to Vercel:**
   - Go to [vercel.com](https://vercel.com)
   - Sign up/login with your GitHub account
   - Click "New Project"
   - Import your forked repository

3. **Set Environment Variables:**
   - In your Vercel project dashboard, go to Settings → Environment Variables
   - Add: `OPENAI_API_KEY` = `your-actual-api-key-here`

4. **Deploy:**
   - Vercel will automatically deploy when you push to main branch
   - Your app will be available at `https://your-project-name.vercel.app`

### 🌐 Vercel vs Local Differences:

| Feature | Local (web_ui_server.py) | Vercel (app.py) |
|---------|-------------------------|-----------------|
| **WebSockets** | ✅ Real-time chat | ❌ HTTP requests only |
| **UI Style** | Interactive chat | Form-based |
| **Agents** | All 6 agents | Simple + LinkedIn |
| **Deployment** | Manual | Automatic |

### 🎯 Available Endpoints:

- **`/`** - Web interface
- **`/chat`** - POST API endpoint
- **`/health`** - Health check

### 📱 API Usage:

```bash
curl -X POST "https://your-app.vercel.app/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Reformat this for LinkedIn: I completed a project today",
    "agent": "linkedin"
  }'
```

### 🔧 Local Development:

For full features (WebSockets, all agents), run locally:

```bash
# Set environment variable
export OPENAI_API_KEY=your-key-here

# Run full-featured local version
python web_ui_server.py

# Or run Vercel-compatible version locally
python app.py
```

### 🚨 Important Notes:

1. **Environment Variables:** Never commit API keys to git
2. **Rate Limits:** Be aware of OpenAI API usage limits
3. **Costs:** Monitor your OpenAI API usage
4. **Serverless Limitations:** Vercel functions have execution time limits

### 🆘 Troubleshooting:

- **Build fails:** Check `requirements.txt` has correct versions
- **API errors:** Verify `OPENAI_API_KEY` is set in Vercel environment
- **Slow responses:** Normal for cold starts on serverless functions

Happy deploying! 🎉
