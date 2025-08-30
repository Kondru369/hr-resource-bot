# Deployment Guide

## Streamlit Cloud Deployment (Recommended)

### 1. Prepare Your Repository
- Ensure all code is committed to GitHub
- Make sure `requirements.txt` is up to date
- Create a `.streamlit/config.toml` file for configuration

### 2. Deploy to Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository: `hr-resource-bot`
5. Set main file path: `frontend/streamlit_app.py`
6. Click "Deploy!"

### 3. Environment Variables
In Streamlit Cloud, add your environment variables:
- `GROQ_API_KEY`: Your Groq API key

### 4. Update Frontend URL
After deployment, update the `BACKEND_URL` in `frontend/streamlit_app.py` to point to your deployed backend.

## Alternative Deployment Options

### Vercel (Frontend)
- Good for React/Vue apps
- Not ideal for Streamlit

### Railway/Heroku (Backend)
- Deploy FastAPI backend
- Set environment variables
- Update frontend to point to deployed backend

### Local Deployment
```bash
# Terminal 1: Backend
python run_backend.py

# Terminal 2: Frontend  
python run_frontend.py
```

## Environment Setup
1. Copy `env.example` to `.env`
2. Add your `GROQ_API_KEY`
3. Never commit `.env` files to Git
