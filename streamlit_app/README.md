# Fitness Categorization - Diet and Workout Recommendation System

💪 A production-ready Streamlit web application that uses Machine Learning (Agglomerative Hierarchical Clustering) to categorize users' fitness levels and provide personalized diet and workout recommendations.

## 🌟 Features

- **Clean, Modern UI**: Dark-themed, responsive design with smooth animations
- **Comprehensive Assessment**: 22+ lifestyle and fitness parameters
- **ML-Powered Analysis**: Agglomerative Hierarchical Clustering algorithm
- **Personalized Recommendations**: Custom diet plans and workout routines
- **Feedback Collection**: User satisfaction tracking for continuous improvement
- **Database Integration**: PostgreSQL with SQLite fallback
- **Future-Ready**: Data storage for model retraining and analytics

## 💻 Tech Stack

- **Framework**: Streamlit 1.30+
- **ML**: scikit-learn (Agglomerative Clustering)
- **Database**: PostgreSQL / SQLite
- **Language**: Python 3.8+

## 🚀 Quick Start

### Local Development

1. **Clone and Navigate**
   ```bash
   cd streamlit_app
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup Environment Variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials (optional - uses SQLite by default)
   ```

4. **Run the Application**
   ```bash
   streamlit run app.py
   ```

5. **Access the App**
   - Open your browser and navigate to: `http://localhost:8501`

## 💾 Database Setup

### Option 1: SQLite (Default)

No setup required! The app will automatically create a SQLite database at `data/fitness_app.db`.

### Option 2: PostgreSQL

1. **Install PostgreSQL** (if not already installed)
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql postgresql-contrib
   
   # macOS
   brew install postgresql
   ```

2. **Create Database**
   ```bash
   # Start PostgreSQL service
   sudo service postgresql start  # Linux
   brew services start postgresql # macOS
   
   # Create database
   sudo -u postgres psql
   CREATE DATABASE fitness_db;
   CREATE USER your_username WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE fitness_db TO your_username;
   \q
   ```

3. **Configure .env**
   ```bash
   DB_TYPE=postgresql
   POSTGRES_HOST=localhost
   POSTGRES_PORT=5432
   POSTGRES_DB=fitness_db
   POSTGRES_USER=your_username
   POSTGRES_PASSWORD=your_password
   ```

## ☁️ Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [streamlit.io/cloud](https://streamlit.io/cloud))

### Deployment Steps

1. **Prepare Your Repository**
   ```bash
   # Create a new GitHub repository
   git init
   git add .
   git commit -m "Initial commit: Fitness categorization app"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set the main file path: `streamlit_app/app.py`
   - Click "Deploy"

3. **Configure Environment Variables** (if using PostgreSQL)
   - In Streamlit Cloud dashboard, go to your app settings
   - Navigate to "Secrets" section
   - Add your environment variables:
     ```toml
     DB_TYPE = "postgresql"
     POSTGRES_HOST = "your-db-host"
     POSTGRES_PORT = "5432"
     POSTGRES_DB = "fitness_db"
     POSTGRES_USER = "your-username"
     POSTGRES_PASSWORD = "your-password"
     ```

### Using Cloud Database Services

For production, consider using managed PostgreSQL:

- **Heroku Postgres**: [heroku.com/postgres](https://www.heroku.com/postgres)
- **AWS RDS**: [aws.amazon.com/rds/postgresql](https://aws.amazon.com/rds/postgresql/)
- **Google Cloud SQL**: [cloud.google.com/sql](https://cloud.google.com/sql)
- **Supabase**: [supabase.com](https://supabase.com) (Free tier available)
- **ElephantSQL**: [elephantsql.com](https://www.elephantsql.com) (Free tier available)

## 📁 Project Structure

```
streamlit_app/
├── app.py                 # Main application entry point
├── pages/                 # Page modules
│   ├── home.py            # Landing page
│   ├── input_form.py      # User input form
│   └── results.py         # Results and feedback
├── utils/                 # Utility modules
│   └── model_loader.py    # ML model loading and prediction
├── database/              # Database modules
│   └── db_handler.py      # Database operations
├── .streamlit/            # Streamlit configuration
│   └── config.toml        # Theme and server settings
├── data/                  # SQLite database directory
├── fitness_model_bundle.pkl  # Trained ML model
├── requirements.txt       # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 📊 Database Schema

### predictions table
```sql
id                  INT/SERIAL PRIMARY KEY
user_inputs         JSONB/TEXT (all user form inputs)
predicted_cluster   INTEGER (0-4, fitness category)
timestamp          TIMESTAMP
```

### feedback table
```sql
id              INT/SERIAL PRIMARY KEY
prediction_id   INTEGER (foreign key to predictions)
satisfaction    VARCHAR(50) (user satisfaction level)
comments        TEXT (optional user comments)
timestamp      TIMESTAMP
```

## 🤖 ML Model Information

- **Algorithm**: Agglomerative Hierarchical Clustering
- **Model File**: `fitness_model_bundle.pkl`
- **Features**: 22 lifestyle and fitness parameters
- **Clusters**: 5 fitness categories (Elite, High, Moderate, Low, Very Low)

### Model Features
1. Gender, Height, Weight, BMI
2. Daily step count
3. Exercise frequency and duration
4. Workout type
5. Sleep hours
6. Screen time and sitting time
7. Alcohol and smoking habits
8. Stress level
9. Nutrition metrics (junk food, water, fruits/vegetables, calories, protein)
10. Food delivery frequency
11. Energy levels and fatigue
12. Self-assessed fitness rating

## 🔧 Customization

### Update ML Model
Replace `fitness_model_bundle.pkl` with your trained model. Ensure it follows the same input feature structure.

### Modify Questions
Edit `pages/input_form.py` to add/remove/modify questions.

### Change Interpretations
Update cluster interpretations in `utils/model_loader.py` > `interpret_cluster()` function.

### Adjust Theme
Modify `.streamlit/config.toml` and CSS in `app.py` to change colors and styling.

## 🛠️ Data Export for Model Retraining

```python
from database.db_handler import get_all_predictions, get_predictions_with_feedback

# Get all predictions
predictions = get_all_predictions()

# Get predictions with user feedback
feedback_data = get_predictions_with_feedback()

# Convert to pandas DataFrame for analysis
import pandas as pd
df = pd.DataFrame(predictions)
```

## 🐛 Troubleshooting

### Port Already in Use
```bash
streamlit run app.py --server.port 8502
```

### Database Connection Issues
- Verify PostgreSQL service is running
- Check credentials in `.env`
- Ensure database exists
- App will automatically fall back to SQLite if PostgreSQL fails

### Model Loading Errors
- Ensure `fitness_model_bundle.pkl` is in the correct location
- Check scikit-learn version compatibility
- App includes fallback rule-based clustering if model fails

## 📝 Environment Variables Reference

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DB_TYPE` | Database type | `sqlite` | No |
| `POSTGRES_HOST` | PostgreSQL host | `localhost` | If using PostgreSQL |
| `POSTGRES_PORT` | PostgreSQL port | `5432` | If using PostgreSQL |
| `POSTGRES_DB` | Database name | `fitness_db` | If using PostgreSQL |
| `POSTGRES_USER` | Database user | `postgres` | If using PostgreSQL |
| `POSTGRES_PASSWORD` | Database password | - | If using PostgreSQL |

## 🚀 Performance Tips

1. **Use PostgreSQL for production** - Better performance with large datasets
2. **Enable caching** - Model is cached after first load
3. **Database indexes** - Already created for timestamp and cluster columns
4. **Regular maintenance** - Archive old predictions periodically

## 📌 Future Enhancements

- Export reports as PDF
- Progress tracking over time
- Social sharing features
- Email notifications with recommendations
- Integration with fitness trackers
- Multi-language support
- Admin dashboard for analytics

## 📄 License

This project is open source and available for personal and commercial use.

## 👤 Developer

Developed by **Akshat** with ❤️

---

**Note**: This application is for educational and informational purposes. Always consult healthcare professionals for medical advice.
