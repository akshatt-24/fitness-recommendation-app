import pickle
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

# Custom classes needed for unpickling
class RawEncoder:
    """Custom encoder class for the model"""
    pass

class ScoreAggregator:
    """Custom aggregator class for the model"""
    pass

# Global model variable
_model_bundle = None

def load_model():
    """Load the trained model bundle"""
    global _model_bundle
    
    if _model_bundle is not None:
        return _model_bundle
    
    try:
        
        #Try multiple possible locations
        possible_paths = [
            Path(__file__).parent.parent / 'fitness_model_bundle.pkl',  # Same dir as app.py
            Path(__file__).parent.parent.parent / 'fitness_model_bundle.pkl',  # Parent dir
            Path('/app/streamlit_app/fitness_model_bundle.pkl'),  # Absolute path
        ]
        
        model_path = None
        for path in possible_paths:
            if path.exists():
                model_path = path
                break
        
        if model_path is None:
            raise FileNotFoundError("\"Model file not found in any expected location\"")
                                    
                                    
        with open(model_path, 'rb') as f:
            _model_bundle = pickle.load(f)
        
        return _model_bundle
    
    except Exception as e:
        print(f"Error loading model: {str(e)}")
        # Return a mock bundle for development
        return {
            'model': None,
            'encoder': None,
            'scaler': None
        }

def preprocess_inputs(user_data):
    """
    Convert user inputs to model-ready format
    """
    # Create feature vector from user data
    features = []
    
    # Encode categorical variables
    gender_map = {'Male': 1, 'Female': 0, 'Other': 2}
    features.append(gender_map.get(user_data['gender'], 1))
    
    # Numerical features
    features.append(float(user_data['height']))
    features.append(float(user_data['weight']))
    
    # BMI calculation
    height_m = user_data['height'] / 100
    bmi = user_data['weight'] / (height_m ** 2)
    features.append(bmi)
    
    features.append(float(user_data['step_count']))
    features.append(float(user_data['exercise_days']))
    features.append(float(user_data['workout_duration']))
    
    # Workout type encoding
    workout_map = {
        'None': 0,
        'Cardio': 1,
        'Strength Training': 2,
        'Yoga/Pilates': 3,
        'Sports': 4,
        'Mixed/Combination': 5
    }
    features.append(workout_map.get(user_data['workout_type'], 0))
    
    features.append(float(user_data['sleep_hours']))
    features.append(float(user_data['screen_time']))
    features.append(float(user_data['sitting_time']))
    
    # Binary features
    features.append(1 if user_data['alcohol'] == 'Yes' else 0)
    features.append(1 if user_data['smoke'] == 'Yes' else 0)
    
    # Stress level encoding
    stress_map = {
        'Very Low': 1,
        'Low': 2,
        'Moderate': 3,
        'High': 4,
        'Very High': 5
    }
    features.append(stress_map.get(user_data['stress_level'], 3))
    
    # Junk food frequency
    junk_map = {
        'Rarely (once a month or less)': 1,
        'Occasionally (2-3 times a month)': 2,
        'Sometimes (once a week)': 3,
        'Often (2-3 times a week)': 4,
        'Very Often (daily or almost daily)': 5
    }
    features.append(junk_map.get(user_data['junk_food'], 3))
    
    # Water intake
    water_map = {
        'Less than 1 liter': 1,
        '1-2 liters': 2,
        '2-3 liters': 3,
        '3-4 liters': 4,
        'More than 4 liters': 5
    }
    features.append(water_map.get(user_data['water_intake'], 2))
    
    features.append(float(user_data['fruit_veg']))
    features.append(float(user_data['calories']))
    
    # Protein level
    protein_map = {'Low': 1, 'Moderate': 2, 'High': 3, 'Very High': 4}
    features.append(protein_map.get(user_data['protein_level'], 2))
    
    # Food order frequency
    food_order_map = {
        'Never': 0,
        'Rarely (once a month)': 1,
        'Sometimes (2-3 times a month)': 2,
        'Often (once a week)': 3,
        'Very Often (multiple times a week)': 4
    }
    features.append(food_order_map.get(user_data['food_order_freq'], 2))
    
    # Energetic feeling
    energetic_map = {'No': 0, 'Sometimes': 1, 'Yes': 2}
    features.append(energetic_map.get(user_data['energetic'], 1))
    
    # Fatigue
    fatigue_map = {'No': 0, 'Sometimes': 1, 'Yes': 2}
    features.append(fatigue_map.get(user_data['fatigue'], 1))
    
    features.append(float(user_data['fitness_rating']))
    
    return np.array(features).reshape(1, -1)

def predict_cluster(user_data):
    """
    Predict cluster and return interpretation
    """
    try:
        # Load model
        model_bundle = load_model()
        
        # Preprocess inputs
        features = preprocess_inputs(user_data)
        
        # Make prediction
        if model_bundle.get('model') is not None:
            cluster = model_bundle['model'].predict(features)[0]
        else:
            # Fallback: rule-based clustering for demo
            cluster = calculate_fitness_cluster(user_data)
        
        # Get interpretation
        interpretation = interpret_cluster(cluster, user_data)
        
        return int(cluster), interpretation
    
    except Exception as e:
        print(f"Prediction error: {str(e)}")
        # Fallback to rule-based
        cluster = calculate_fitness_cluster(user_data)
        interpretation = interpret_cluster(cluster, user_data)
        return int(cluster), interpretation

def calculate_fitness_cluster(user_data):
    """
    Rule-based clustering as fallback
    """
    # Calculate fitness score
    score = 0
    
    # Exercise contribution (0-30 points)
    score += user_data['exercise_days'] * 3
    score += min(user_data['workout_duration'] / 10, 10)
    
    # Nutrition contribution (0-25 points)
    height_m = user_data['height'] / 100
    bmi = user_data['weight'] / (height_m ** 2)
    if 18.5 <= bmi <= 24.9:
        score += 10
    elif 17 <= bmi < 18.5 or 25 <= bmi <= 29.9:
        score += 5
    
    if user_data['fruit_veg'] >= 5:
        score += 10
    elif user_data['fruit_veg'] >= 3:
        score += 5
    
    # Lifestyle contribution (0-25 points)
    if user_data['sleep_hours'] >= 7 and user_data['sleep_hours'] <= 9:
        score += 10
    elif user_data['sleep_hours'] >= 6:
        score += 5
    
    if user_data['alcohol'] == 'No':
        score += 5
    if user_data['smoke'] == 'No':
        score += 10
    
    # Activity contribution (0-20 points)
    if user_data['step_count'] >= 10000:
        score += 10
    elif user_data['step_count'] >= 5000:
        score += 5
    
    if user_data['sitting_time'] <= 6:
        score += 10
    elif user_data['sitting_time'] <= 8:
        score += 5
    
    # Determine cluster based on score
    if score >= 80:
        return 0  # Elite fitness
    elif score >= 60:
        return 1  # High fitness
    elif score >= 40:
        return 2  # Moderate fitness
    elif score >= 20:
        return 3  # Low fitness
    else:
        return 4  # Very low fitness

def interpret_cluster(cluster, user_data):
    """
    Provide detailed interpretation and recommendations for each cluster
    """
    interpretations = {
        0: {
            'description': '''You belong to the **Elite Fitness** category! Your lifestyle choices reflect 
            exceptional commitment to health and wellness. You maintain excellent exercise habits, 
            balanced nutrition, and healthy lifestyle practices.''',
            'diet_recommendations': [
                'Maintain your high protein intake to support muscle recovery',
                'Continue consuming 5+ servings of fruits and vegetables daily',
                'Stay hydrated with 3-4 liters of water per day',
                'Consider meal timing around workouts for optimal performance',
                'Include complex carbohydrates for sustained energy'
            ],
            'workout_recommendations': [
                'Continue your current workout routine with progressive overload',
                'Incorporate periodization to prevent plateaus',
                'Add mobility and flexibility work 2-3 times per week',
                'Ensure adequate recovery days (1-2 per week)',
                'Consider working with a coach for advanced techniques'
            ],
            'insights': [
                'Your BMI is in the healthy range',
                'Excellent exercise frequency and duration',
                'Great lifestyle habits with no smoking and minimal alcohol',
                'Keep monitoring your progress and adjusting as needed'
            ]
        },
        1: {
            'description': '''You fall into the **High Fitness** category. You have established good 
            fitness habits and maintain a relatively active lifestyle. With some adjustments, 
            you can reach elite fitness levels.''',
            'diet_recommendations': [
                'Increase protein intake to 1.6-2.2g per kg of body weight',
                'Aim for 4-5 servings of fruits and vegetables daily',
                'Drink at least 2-3 liters of water per day',
                'Reduce processed food and junk food consumption',
                'Plan meals ahead to maintain consistency'
            ],
            'workout_recommendations': [
                'Aim for 4-5 workout days per week',
                'Include both strength training and cardio',
                'Increase workout duration to 45-60 minutes',
                'Try high-intensity interval training (HIIT) 1-2 times per week',
                'Set specific, measurable fitness goals'
            ],
            'insights': [
                'You\'re on the right track with good habits',
                'Focus on consistency in both diet and exercise',
                'Small improvements can elevate you to elite fitness',
                'Monitor your sleep quality for better recovery'
            ]
        },
        2: {
            'description': '''You\'re in the **Moderate Fitness** category. You have a foundation to build upon, 
            but there\'s significant room for improvement in your exercise routine, nutrition, and lifestyle habits.''',
            'diet_recommendations': [
                'Start tracking your daily calorie and protein intake',
                'Increase fruit and vegetable consumption to at least 3 servings daily',
                'Reduce junk food to once per week maximum',
                'Aim for 2-2.5 liters of water daily',
                'Prepare more meals at home instead of ordering out',
                'Focus on whole foods: lean proteins, whole grains, and healthy fats'
            ],
            'workout_recommendations': [
                'Start with 3-4 workout days per week',
                'Begin with 30-minute sessions and gradually increase',
                'Mix cardio (walking, jogging, cycling) with basic strength training',
                'Aim for 7,000-8,000 steps daily',
                'Join a fitness class or find a workout buddy for motivation',
                'Set realistic short-term goals (e.g., exercise 3x/week for a month)'
            ],
            'insights': [
                'Your current habits show potential for improvement',
                'Focus on building consistency before intensity',
                'Improve sleep quality - aim for 7-8 hours nightly',
                'Reduce screen time and sitting hours for better health'
            ]
        },
        3: {
            'description': '''You\'re categorized as **Low Fitness**. Your current lifestyle habits need significant 
            improvement. Don\'t worry - small, sustainable changes can lead to remarkable improvements in your health and fitness.''',
            'diet_recommendations': [
                'Start by eliminating sugary drinks and replacing with water',
                'Add one fruit or vegetable to each meal',
                'Reduce junk food consumption by 50% immediately',
                'Avoid skipping meals - eat 3 balanced meals daily',
                'Drink at least 1.5-2 liters of water per day',
                'Limit processed foods and fast food orders',
                'Consider consulting a nutritionist for a personalized plan'
            ],
            'workout_recommendations': [
                'Start with 2-3 days of light exercise per week',
                'Begin with 15-20 minute walks daily',
                'Gradually increase to 30 minutes as you build stamina',
                'Try bodyweight exercises at home (squats, push-ups, planks)',
                'Take the stairs instead of elevator when possible',
                'Set a daily step goal (start with 5,000 steps)',
                'Find activities you enjoy to stay motivated'
            ],
            'insights': [
                'Small consistent changes are more important than drastic measures',
                'Prioritize sleep - aim for 7-8 hours per night',
                'If you smoke or drink alcohol, consider reducing or quitting',
                'Track your progress weekly to stay motivated',
                'Consider consulting a doctor before starting intense exercise'
            ]
        },
        4: {
            'description': '''Your fitness assessment indicates **Very Low Fitness** levels. This requires immediate 
            attention and lifestyle changes. Remember, every journey begins with a single step, and 
            with dedication, you can transform your health.''',
            'diet_recommendations': [
                'Consult a nutritionist or dietitian for a comprehensive plan',
                'Start with basic changes: drink water instead of sodas',
                'Add vegetables to at least 2 meals daily',
                'Completely avoid junk food and processed snacks for 30 days',
                'Eat smaller, more frequent meals (5-6 times daily)',
                'Focus on lean proteins, vegetables, and whole grains',
                'Prepare simple, healthy meals at home',
                'Keep a food diary to track what you eat'
            ],
            'workout_recommendations': [
                'Consult a doctor before starting any exercise program',
                'Start with 10-15 minute daily walks',
                'Focus on building the habit first, intensity later',
                'Try water-based exercises if available (low impact)',
                'Include stretching and light mobility exercises',
                'Set very small, achievable goals (e.g., walk 10 mins daily for a week)',
                'Consider working with a personal trainer familiar with beginners',
                'Celebrate small victories to stay motivated'
            ],
            'insights': [
                'Your health requires immediate attention and lifestyle changes',
                'Make sleep a priority - aim for 7-9 hours nightly',
                'If you smoke, quit immediately - seek support if needed',
                'Reduce alcohol consumption significantly or eliminate completely',
                'Reduce sitting time - stand and move every hour',
                'Consider medical check-up to rule out underlying conditions',
                'Be patient with yourself - progress takes time',
                'Build a support system (family, friends, or support groups)'
            ]
        }
    }
    
    return interpretations.get(cluster, interpretations[2])
