import streamlit as st
# from app.streamlit_app.utils.model_loader import load_model, predict_cluster
from utils.model_loader import load_model, predict_cluster

from datetime import datetime

def show():
    st.markdown("""
    <div class="main-header">
        <h1>📝 Your Fitness Profile</h1>
        <p>Please fill in your details accurately for best results</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Create form
    with st.form("fitness_form"):
        st.markdown("### Personal Information")
        col1, col2 = st.columns(2)
        
        with col1:
            gender = st.selectbox(
                "What is your gender?",
                options=["Male", "Female", "Other"],
                key="gender"
            )
        
        with col2:
            height = st.number_input(
                "What is your height (in cm)?",
                min_value=100,
                max_value=250,
                value=170,
                step=1,
                key="height"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            weight = st.number_input(
                "What is your weight (in kg)?",
                min_value=30,
                max_value=200,
                value=70,
                step=1,
                key="weight"
            )
        
        with col2:
            step_count = st.number_input(
                "Average daily step count (approx)",
                min_value=0,
                max_value=50000,
                value=5000,
                step=100,
                key="step_count"
            )
        
        st.markdown("### Exercise & Activity")
        
        col1, col2 = st.columns(2)
        
        with col1:
            exercise_days = st.slider(
                "How many days per week do you exercise?",
                min_value=0,
                max_value=7,
                value=3,
                key="exercise_days"
            )
        
        with col2:
            workout_duration = st.number_input(
                "Average workout duration per day (in minutes)",
                min_value=0,
                max_value=300,
                value=30,
                step=5,
                key="workout_duration"
            )
        
        workout_type = st.selectbox(
            "What type of workout you usually do?",
            options=[
                "Cardio",
                "Strength Training",
                "Yoga/Pilates",
                "Sports",
                "Mixed/Combination",
                "None"
            ],
            key="workout_type"
        )
        
        st.markdown("### Sleep & Screen Time")
        
        col1, col2 = st.columns(2)
        
        with col1:
            sleep_hours = st.slider(
                "Average sleep hours per day",
                min_value=0.0,
                max_value=12.0,
                value=7.0,
                step=0.5,
                key="sleep_hours"
            )
        
        with col2:
            screen_time = st.number_input(
                "Daily screen time (phone + laptop) in hours",
                min_value=0.0,
                max_value=24.0,
                value=6.0,
                step=0.5,
                key="screen_time"
            )
        
        sitting_time = st.number_input(
            "Daily sitting time (hours)",
            min_value=0.0,
            max_value=24.0,
            value=8.0,
            step=0.5,
            key="sitting_time"
        )
        
        st.markdown("### Lifestyle Habits")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alcohol = st.radio(
                "Do you consume alcohol?",
                options=["Yes", "No"],
                key="alcohol",
                horizontal=True
            )
        
        with col2:
            smoke = st.radio(
                "Do you smoke?",
                options=["Yes", "No"],
                key="smoke",
                horizontal=True
            )
        
        stress_level = st.select_slider(
            "Daily workload/stress level",
            options=["Very Low", "Low", "Moderate", "High", "Very High"],
            value="Moderate",
            key="stress_level"
        )
        
        st.markdown("### Nutrition")
        
        junk_food = st.selectbox(
            "Junk food consumption frequency (including packaged items like chips and cold drinks)",
            options=[
                "Rarely (once a month or less)",
                "Occasionally (2-3 times a month)",
                "Sometimes (once a week)",
                "Often (2-3 times a week)",
                "Very Often (daily or almost daily)"
            ],
            key="junk_food"
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            water_intake = st.selectbox(
                "Average water intake per day",
                options=[
                    "Less than 1 liter",
                    "1-2 liters",
                    "2-3 liters",
                    "3-4 liters",
                    "More than 4 liters"
                ],
                key="water_intake"
            )
        
        with col2:
            fruit_veg = st.number_input(
                "Fruit/Vegetable servings per day",
                min_value=0,
                max_value=20,
                value=3,
                step=1,
                key="fruit_veg"
            )
        
        col1, col2 = st.columns(2)
        
        with col1:
            calories = st.number_input(
                "Average daily calories intake in kcal (approx)",
                min_value=500,
                max_value=6000,
                value=2000,
                step=50,
                key="calories"
            )
        
        with col2:
            protein_level = st.selectbox(
                "Protein intake level",
                options=["Low", "Moderate", "High", "Very High"],
                key="protein_level"
            )
        
        food_order_freq = st.selectbox(
            "Frequency of online food order (Swiggy, Zomato etc.)",
            options=[
                "Never",
                "Rarely (once a month)",
                "Sometimes (2-3 times a month)",
                "Often (once a week)",
                "Very Often (multiple times a week)"
            ],
            key="food_order_freq"
        )
        
        st.markdown("### Health Assessment")
        
        col1, col2 = st.columns(2)
        
        with col1:
            energetic = st.radio(
                "Do you feel energetic during the day?",
                options=["Yes", "Sometimes", "No"],
                key="energetic",
                horizontal=True
            )
        
        with col2:
            fatigue = st.radio(
                "Do you experience frequent fatigue?",
                options=["Yes", "Sometimes", "No"],
                key="fatigue",
                horizontal=True
            )
        
        fitness_rating = st.slider(
            "How would you rate your overall fitness level?",
            min_value=1,
            max_value=10,
            value=5,
            key="fitness_rating",
            help="1 = Very Poor, 10 = Excellent"
        )
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            submitted = st.form_submit_button(
                "🎯 Get My Results",
                use_container_width=True
            )
        
        if submitted:
            # Collect all inputs
            user_data = {
                'gender': gender,
                'height': height,
                'weight': weight,
                'step_count': step_count,
                'exercise_days': exercise_days,
                'workout_duration': workout_duration,
                'workout_type': workout_type,
                'sleep_hours': sleep_hours,
                'screen_time': screen_time,
                'sitting_time': sitting_time,
                'alcohol': alcohol,
                'smoke': smoke,
                'stress_level': stress_level,
                'junk_food': junk_food,
                'water_intake': water_intake,
                'fruit_veg': fruit_veg,
                'calories': calories,
                'protein_level': protein_level,
                'food_order_freq': food_order_freq,
                'energetic': energetic,
                'fatigue': fatigue,
                'fitness_rating': fitness_rating,
                'timestamp': datetime.now().isoformat()
            }
            
            # Store in session state
            st.session_state.user_inputs = user_data
            
            # Make prediction
            with st.spinner('🔄 Analyzing your fitness profile...'):
                try:
                    cluster, interpretation = predict_cluster(user_data)
                    
                    st.session_state.prediction_result = {
                        'cluster': cluster,
                        'interpretation': interpretation
                    }
                    
                    # Navigate to results
                    st.session_state.page = 'results'
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"⚠️ Error making prediction: {str(e)}")
                    st.info("Please check that all inputs are valid and try again.")
    
    # Back button
    st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("⬅️ Back to Home", use_container_width=True):
            st.session_state.page = 'home'
            st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        Developed by Akshat with <span>❤️</span>
    </div>
    """, unsafe_allow_html=True)
