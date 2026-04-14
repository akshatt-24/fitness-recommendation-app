"# 🚀 Complete Deployment Guide

## Table of Contents
1. [Local Development](#local-development)
2. [Streamlit Cloud Deployment](#streamlit-cloud-deployment)
3. [Other Deployment Options](#other-deployment-options)
4. [Database Setup](#database-setup)
5. [Troubleshooting](#troubleshooting)

---

## 📍 Local Development

### Step 1: Install Python
Ensure Python 3.8 or higher is installed:
```bash
python --version
# or
python3 --version
```

### Step 2: Install Dependencies
```bash
cd streamlit_app
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
streamlit run app.py
```

The app will be available at: **http://localhost:8501**

### Step 4: Access Different Ports (Optional)
If port 8501 is in use:
```bash
streamlit run app.py --server.port 8502
```

---

## ☁️ Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free): [streamlit.io/cloud](https://streamlit.io/cloud)

### Step-by-Step Deployment

#### 1. Push Code to GitHub

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m \"Initial commit: Fitness categorization app\"

# Create repository on GitHub (via web interface)
# Then link and push:
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/fitness-app.git
git push -u origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **\"New app\"**
3. Connect your GitHub account (if not already connected)
4. Fill in the deployment form:
   - **Repository**: Select your repository
   - **Branch**: `main`
   - **Main file path**: `streamlit_app/app.py`
5. Click **\"Deploy!\"**

#### 3. Configure Secrets (Optional - for PostgreSQL)

In your Streamlit Cloud dashboard:
1. Click on your app
2. Go to **Settings** → **Secrets**
3. Add secrets in TOML format:

```toml
# Database Configuration
DB_TYPE = \"postgresql\"
POSTGRES_HOST = \"your-db-host.example.com\"
POSTGRES_PORT = \"5432\"
POSTGRES_DB = \"fitness_db\"
POSTGRES_USER = \"your_username\"
POSTGRES_PASSWORD = \"your_password\"
```

4. Save and the app will automatically reboot

#### 4. Update Application

To deploy updates:
```bash
git add .
git commit -m \"Update: your changes\"
git push
```

Streamlit Cloud will automatically redeploy!

---

## 🗄️ Database Setup

### Option 1: SQLite (Default - No Setup Required)

The app uses SQLite by default. No configuration needed! Database file will be created automatically at `data/fitness_app.db`.

**Pros:**
- Zero setup
- Perfect for development and small-scale use
- Portable

**Cons:**
- Not suitable for high traffic
- Limited for Streamlit Cloud (resets on redeploy)

### Option 2: PostgreSQL (Recommended for Production)

#### Local PostgreSQL Setup

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Windows:**
Download and install from: [postgresql.org/download/windows](https://www.postgresql.org/download/windows/)

#### Create Database

```bash
# Access PostgreSQL prompt
sudo -u postgres psql

# Create database and user
CREATE DATABASE fitness_db;
CREATE USER fitness_user WITH PASSWORD 'secure_password_here';
GRANT ALL PRIVILEGES ON DATABASE fitness_db TO fitness_user;

# Exit
\q
```

#### Configure Application

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env`:
```bash
DB_TYPE=postgresql
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=fitness_db
POSTGRES_USER=fitness_user
POSTGRES_PASSWORD=secure_password_here
```

#### Cloud PostgreSQL Options

For Streamlit Cloud deployment, use managed PostgreSQL:

**1. Supabase (Recommended - Free Tier Available)**
- Sign up at [supabase.com](https://supabase.com)
- Create new project
- Get connection details from Settings → Database
- Use the \"Connection string\" in your Streamlit secrets

**2. ElephantSQL (Free Tier)**
- Sign up at [elephantsql.com](https://www.elephantsql.com)
- Create new instance (free \"Tiny Turtle\" plan)
- Copy connection details

**3. Heroku Postgres**
- Create Heroku app
- Add \"Heroku Postgres\" add-on
- Get credentials from Heroku dashboard

**4. AWS RDS**
- Create PostgreSQL instance on AWS RDS
- Configure security groups
- Use endpoint details

**5. Google Cloud SQL**
- Create PostgreSQL instance on Google Cloud
- Set up connection

#### Connection String Format

Most cloud providers give you a connection string like:
```
postgresql://username:password@host:port/database
```

To use this in `.env`:
```bash
DB_TYPE=postgresql
POSTGRES_HOST=host-from-connection-string
POSTGRES_PORT=5432
POSTGRES_DB=database-name
POSTGRES_USER=username
POSTGRES_PASSWORD=password
```

---

## 🌐 Other Deployment Options

### Docker Deployment

Create `Dockerfile`:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD [\"streamlit\", \"run\", \"app.py\", \"--server.port=8501\", \"--server.address=0.0.0.0\"]
```

Build and run:
```bash
docker build -t fitness-app .
docker run -p 8501:8501 fitness-app
```

### Heroku Deployment

1. Create `setup.sh`:
```bash
mkdir -p ~/.streamlit/

echo \"\
[server]
\
headless = true
\
port = $PORT
\
enableCORS = false
\

\
\" > ~/.streamlit/config.toml
```

2. Create `Procfile`:
```
web: sh setup.sh && streamlit run app.py
```

3. Deploy:
```bash
heroku create your-app-name
git push heroku main
```

### AWS EC2 Deployment

1. Launch EC2 instance (Ubuntu)
2. SSH into instance
3. Install dependencies:
```bash
sudo apt update
sudo apt install python3-pip
pip3 install -r requirements.txt
```
4. Run with nohup:
```bash
nohup streamlit run app.py --server.port 8501 &
```

### Google Cloud Run

1. Create `Dockerfile` (as shown above)
2. Build and push to Google Container Registry
3. Deploy to Cloud Run:
```bash
gcloud run deploy fitness-app \
  --image gcr.io/PROJECT_ID/fitness-app \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

---

## 🐛 Troubleshooting

### Issue: Port Already in Use

**Solution:**
```bash
# Find process using port 8501
lsof -i :8501

# Kill the process
kill -9 <PID>

# Or use a different port
streamlit run app.py --server.port 8502
```

### Issue: Database Connection Failed

**Symptoms:** App shows \"Database connection failed\" or falls back to SQLite

**Solutions:**
1. Check PostgreSQL is running:
   ```bash
   sudo service postgresql status
   ```

2. Verify credentials in `.env`

3. Test connection manually:
   ```python
   import psycopg2
   conn = psycopg2.connect(
       host=\"localhost\",
       database=\"fitness_db\",
       user=\"fitness_user\",
       password=\"your_password\"
   )
   print(\"Connection successful!\")
   ```

4. Check firewall rules (for cloud databases)

5. Ensure database exists:
   ```bash
   psql -U fitness_user -d fitness_db -c \"SELECT 1\"
   ```

### Issue: Model Not Loading

**Symptoms:** \"Error loading model\" or predictions fail

**Solutions:**
1. Verify model file exists:
   ```bash
   ls -la fitness_model_bundle.pkl
   ```

2. Check file path in `utils/model_loader.py`

3. Ensure scikit-learn version compatibility

4. App includes fallback rule-based clustering

### Issue: Module Not Found

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: Streamlit Cloud Build Fails

**Common Causes:**
1. Wrong file path specified
2. Missing `requirements.txt`
3. Syntax errors in code

**Solutions:**
1. Check build logs in Streamlit Cloud dashboard
2. Verify `requirements.txt` is in correct location
3. Test locally first: `streamlit run app.py`

### Issue: App Resets on Streamlit Cloud

**Cause:** Streamlit Cloud's ephemeral storage

**Solution:**
- Use external database (PostgreSQL) for data persistence
- SQLite data will be lost on redeployment

### Issue: Slow Performance

**Solutions:**
1. Enable caching (already implemented in model loader)
2. Use PostgreSQL instead of SQLite for large datasets
3. Optimize database queries
4. Consider upgrading Streamlit Cloud tier

---

## 📊 Monitoring and Maintenance

### Check Database Size

**PostgreSQL:**
```sql
SELECT pg_size_pretty(pg_database_size('fitness_db'));
```

**SQLite:**
```bash
ls -lh data/fitness_app.db
```

### View Logs

**Local:**
```bash
# Streamlit logs are shown in terminal
```

**Streamlit Cloud:**
- View logs in dashboard → Your app → More actions → Logs

### Backup Database

**PostgreSQL:**
```bash
pg_dump -U fitness_user fitness_db > backup.sql
```

**SQLite:**
```bash
cp data/fitness_app.db data/fitness_app_backup.db
```

### Restore Database

**PostgreSQL:**
```bash
psql -U fitness_user fitness_db < backup.sql
```

**SQLite:**
```bash
cp data/fitness_app_backup.db data/fitness_app.db
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` file** - Use `.gitignore`
2. **Use strong passwords** for database
3. **Rotate credentials** regularly
4. **Use environment variables** for all secrets
5. **Enable SSL** for database connections in production
6. **Keep dependencies updated**: `pip list --outdated`
7. **Use HTTPS** in production

---

## 📈 Scaling Recommendations

### For Small Traffic (< 100 users/day)
- SQLite or free PostgreSQL tier
- Streamlit Cloud free tier

### For Medium Traffic (100-1000 users/day)
- Managed PostgreSQL (Supabase, ElephantSQL)
- Streamlit Cloud paid tier or dedicated hosting

### For High Traffic (> 1000 users/day)
- AWS RDS or Google Cloud SQL
- Deploy on AWS/GCP/Azure with load balancing
- Consider adding Redis for caching
- Optimize database with proper indexing

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review README.md
3. Check Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
4. Review PostgreSQL documentation: [postgresql.org/docs](https://www.postgresql.org/docs/)

---

## ✅ Pre-Deployment Checklist

- [ ] Code tested locally
- [ ] All dependencies in `requirements.txt`
- [ ] `.env` file not in repository
- [ ] `.gitignore` configured properly
- [ ] Database configured (if using PostgreSQL)
- [ ] Model file (`fitness_model_bundle.pkl`) included
- [ ] README.md updated
- [ ] Repository pushed to GitHub
- [ ] Streamlit Cloud secrets configured (if needed)
- [ ] Test deployment successful
- [ ] App accessible via public URL

---

**Happy Deploying! 🚀**

Developed by Akshat with ❤️
"