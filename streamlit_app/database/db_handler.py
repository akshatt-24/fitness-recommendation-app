import os
import psycopg2
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Database configuration
DB_TYPE = os.getenv('DB_TYPE', 'sqlite')  # 'postgresql' or 'sqlite'
POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5432')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'fitness_db')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'password')

# SQLite fallback
SQLITE_DB_PATH = Path(__file__).parent.parent / 'data' / 'fitness_app.db'

def get_connection():
    """
    Get database connection based on configuration
    """
    if DB_TYPE == 'postgresql':
        try:
            conn = psycopg2.connect(
                host=POSTGRES_HOST,
                port=POSTGRES_PORT,
                database=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD
            )
            return conn, 'postgresql'
        except Exception as e:
            print(f"PostgreSQL connection failed: {str(e)}")
            print("Falling back to SQLite...")
    
    # Fallback to SQLite
    SQLITE_DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(SQLITE_DB_PATH))
    return conn, 'sqlite'

def init_database():
    """
    Initialize database tables
    """
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    try:
        if db_type == 'postgresql':
            # PostgreSQL schema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id SERIAL PRIMARY KEY,
                    user_inputs JSONB NOT NULL,
                    predicted_cluster INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id SERIAL PRIMARY KEY,
                    prediction_id INTEGER REFERENCES predictions(id),
                    satisfaction VARCHAR(50) NOT NULL,
                    comments TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_predictions_timestamp 
                ON predictions(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_predictions_cluster 
                ON predictions(predicted_cluster)
            """)
            
        else:
            # SQLite schema
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS predictions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_inputs TEXT NOT NULL,
                    predicted_cluster INTEGER NOT NULL,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS feedback (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    prediction_id INTEGER,
                    satisfaction TEXT NOT NULL,
                    comments TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (prediction_id) REFERENCES predictions(id)
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_predictions_timestamp 
                ON predictions(timestamp)
            """)
            
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_predictions_cluster 
                ON predictions(predicted_cluster)
            """)
        
        conn.commit()
        print(f"Database initialized successfully using {db_type}")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()

def save_prediction(user_inputs, predicted_cluster):
    """
    Save prediction to database
    """
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    try:
        if db_type == 'postgresql':
            cursor.execute("""
                INSERT INTO predictions (user_inputs, predicted_cluster, timestamp)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (json.dumps(user_inputs), predicted_cluster, datetime.now()))
            prediction_id = cursor.fetchone()[0]
        else:
            cursor.execute("""
                INSERT INTO predictions (user_inputs, predicted_cluster, timestamp)
                VALUES (?, ?, ?)
            """, (json.dumps(user_inputs), predicted_cluster, datetime.now().isoformat()))
            prediction_id = cursor.lastrowid
        
        conn.commit()
        return prediction_id
        
    except Exception as e:
        print(f"Error saving prediction: {str(e)}")
        conn.rollback()
        return None
    
    finally:
        cursor.close()
        conn.close()

def save_feedback(prediction_id, satisfaction, comments):
    """
    Save user feedback to database
    """
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    try:
        if db_type == 'postgresql':
            cursor.execute("""
                INSERT INTO feedback (prediction_id, satisfaction, comments, timestamp)
                VALUES (%s, %s, %s, %s)
            """, (prediction_id, satisfaction, comments, datetime.now()))
        else:
            cursor.execute("""
                INSERT INTO feedback (prediction_id, satisfaction, comments, timestamp)
                VALUES (?, ?, ?, ?)
            """, (prediction_id, satisfaction, comments, datetime.now().isoformat()))
        
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Error saving feedback: {str(e)}")
        conn.rollback()
        return False
    
    finally:
        cursor.close()
        conn.close()

def get_all_predictions():
    """
    Retrieve all predictions for model retraining
    """
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT id, user_inputs, predicted_cluster, timestamp
            FROM predictions
            ORDER BY timestamp DESC
        """)
        
        results = cursor.fetchall()
        
        predictions = []
        for row in results:
            predictions.append({
                'id': row[0],
                'user_inputs': json.loads(row[1]) if isinstance(row[1], str) else row[1],
                'predicted_cluster': row[2],
                'timestamp': row[3]
            })
        
        return predictions
        
    except Exception as e:
        print(f"Error retrieving predictions: {str(e)}")
        return []
    
    finally:
        cursor.close()
        conn.close()

def get_predictions_with_feedback():
    """
    Retrieve predictions with feedback for analysis
    """
    conn, db_type = get_connection()
    cursor = conn.cursor()
    
    try:
        cursor.execute("""
            SELECT 
                p.id,
                p.user_inputs,
                p.predicted_cluster,
                p.timestamp,
                f.satisfaction,
                f.comments
            FROM predictions p
            LEFT JOIN feedback f ON p.id = f.prediction_id
            ORDER BY p.timestamp DESC
        """)
        
        results = cursor.fetchall()
        
        data = []
        for row in results:
            data.append({
                'prediction_id': row[0],
                'user_inputs': json.loads(row[1]) if isinstance(row[1], str) else row[1],
                'predicted_cluster': row[2],
                'prediction_timestamp': row[3],
                'satisfaction': row[4],
                'comments': row[5]
            })
        
        return data
        
    except Exception as e:
        print(f"Error retrieving predictions with feedback: {str(e)}")
        return []
    
    finally:
        cursor.close()
        conn.close()

# Initialize database on import
init_database()
