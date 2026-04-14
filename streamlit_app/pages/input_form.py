"""
input_form.py
─────────────────────────────────────────────────────────────────────────────
User input form. Collects all survey fields and passes them to
model_loader.predict_cluster() using short form keys.

Key contract (must match model_loader.py section 2 and 3):
    gender, height (int cm), weight (int kg), step_count, exercise_days,
    workout_duration, workout_type (joined str), sleep_hours, screen_time,
    sitting_time, alcohol, smoke, stress_level, junk_food, water_intake,
    fruit_veg, calories, protein_level, food_order_freq, energetic,
    fatigue, fitness_rating

Multi-select workout_type is joined to a comma-separated string so that
model_loader's substring checks ("Gym", "Cardio", "Sports", etc.) work
on combined selections.
─────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st
from utils.styles import inject_global_css
from utils.model_loader import predict_cluster


# ── Option sets ───────────────────────────────────────────────────────────────
# Every option string must contain the substring that model_loader's maps expect.

GENDER_OPTS = ["Male", "Female", "Other"]

HEIGHT_OPTS = [
    "Less than 150 cm",
    "150 - 160 cm",
    "160 - 170 cm",
    "170 - 180 cm",
    "180 - 190 cm",
    "190 cm or above",
]
HEIGHT_MID = {
    "Less than 150 cm" : 145,
    "150 - 160 cm"     : 155,
    "160 - 170 cm"     : 165,
    "170 - 180 cm"     : 175,
    "180 - 190 cm"     : 185,
    "190 cm or above"  : 193,
}

WEIGHT_OPTS = [
    "Less than 50 kg",
    "50 - 65 kg",
    "65 - 80 kg",
    "80 - 95 kg",
    "95 - 110 kg",
    "More than 110 kg",
]
WEIGHT_MID = {
    "Less than 50 kg"  : 45,
    "50 - 65 kg"       : 57,
    "65 - 80 kg"       : 72,
    "80 - 95 kg"       : 87,
    "95 - 110 kg"      : 102,
    "More than 110 kg" : 115,
}

# Step options — values contain substrings matched by model_loader step map keys.
STEP_OPTS = ["Less than 3000", "3000 - 6000", "6000-10000", "10000+"]

# Exercise days — values must match model_loader exercise_days map keys exactly.
EXERCISE_DAY_OPTS = ["0 days", "1-2", "3-4", "5+"]

# Duration — values must match model_loader duration map keys exactly.
DURATION_OPTS = ["0", "15-30", "30-60", "60+"]

# Workout options — values must contain substrings model_loader checks:
# "Gym", "Cardio" or "Running", "Sports", "Yoga" or "Stretching", "none".
WORKOUT_OPTS = [
    "Gym",
    "Cardio / Running",
    "Sports",
    "Yoga / Stretching",
    "none",
]

# Sleep — values must match model_loader sleep_map keys exactly.
SLEEP_OPTS = [
    "Less than 5 hours",
    "5-6 hours",
    "6-8 hours",
    "8+ hours",
]

# Screen time — must match model_loader screen_map keys exactly.
SCREEN_OPTS = [
    "Less than 3 hours",
    "3-5 hours",
    "5-7 hours",
    "7+ hours",
]

# Sitting — must match model_loader sitting_map keys exactly.
SITTING_OPTS = [
    "Less than 4 hours",
    "4-6 hours",
    "6-8 hours",
    "8+ hours",
]

ALCOHOL_OPTS  = ["Never", "Occasionally", "Regularly"]
SMOKE_OPTS    = ["No", "Yes"]
STRESS_OPTS   = ["Very low", "Moderate", "High", "Very High"]

# Junk — must contain substrings: "Rarely", "1-2 times", "3-4 times", "Almost daily"
JUNK_OPTS = [
    "Rarely (once a month or less)",
    "1-2 times a week",
    "3-4 times a week",
    "Almost daily",
]

# Water — must match model_loader water_map keys exactly.
WATER_OPTS = ["1-2 liters", "2-3 liters", "more than 3 liters"]

# Fruit/veg — must match model_loader fv_map keys exactly.
FRUIT_VEG_OPTS = ["0 servings", "1 serving", "2-3 servings", "3+ servings"]

# Calories — must match model_loader cal_map keys exactly.
CALORIE_OPTS = [
    "less than 1800 kcal",
    "1800 - 2200 kcal",
    "2200 - 2600 kcal",
    "2600+ kcal",
    "not sure",
]

PROTEIN_OPTS = ["Low", "Moderate", "High"]

# Order — must contain substrings: "rarely", "1-2 times", "3-4 times", "5+ times"
ORDER_OPTS = [
    "rarely (once a month or less)",
    "1-2 times a week",
    "3-4 times a week",
    "5+ times a week",
]

# Energy / fatigue — must match model_loader maps exactly (lowercase).
ENERGY_OPTS  = ["never", "occasionally", "frequently", "always"]
FATIGUE_OPTS = ["never", "occasionally", "frequently", "always"]

# Fitness self-rating — must match model_loader fitness_map keys exactly.
FITNESS_OPTS = [
    "Poor (1-2)",
    "Average (3-5)",
    "Good (6-7)",
    "Excellent (8-10)",
]


# ── Rendering helpers ─────────────────────────────────────────────────────────

def _section(label: str) -> None:
    st.markdown(f'<div class="section-label">{label}</div>', unsafe_allow_html=True)


def _radio(label: str, options: list, key: str, horizontal: bool = False) -> str:
    return st.radio(label, options, key=key, horizontal=horizontal)


def _multiselect(label: str, options: list, key: str) -> list:
    return st.multiselect(label, options, key=key)


# ── Main page ─────────────────────────────────────────────────────────────────

def show() -> None:
    inject_global_css()

    st.markdown("""
    <div class="page-header">
        <h1>Your Fitness Profile</h1>
        <p>Answer each question accurately — results depend on honest input.</p>
    </div>
    """, unsafe_allow_html=True)

    with st.form("fitness_form"):

        # ── Section 1: Personal Information ──────────────────────────────────
        _section("Personal Information")
        c1, c2 = st.columns(2)
        with c1:
            gender = _radio("Gender", GENDER_OPTS, "gender", horizontal=True)
        with c2:
            height_bucket = _radio("Height", HEIGHT_OPTS, "height_bucket", horizontal=False)

        c1, c2 = st.columns(2)
        with c1:
            weight_bucket = _radio("Weight", WEIGHT_OPTS, "weight_bucket", horizontal=False)
        with c2:
            step_count = _radio("Average daily step count", STEP_OPTS, "step_count", horizontal=False)

        # ── Section 2: Exercise & Activity ────────────────────────────────────
        _section("Exercise & Activity")
        c1, c2 = st.columns(2)
        with c1:
            exercise_days = _radio("Exercise days per week", EXERCISE_DAY_OPTS, "exercise_days", horizontal=False)
        with c2:
            workout_duration = _radio("Average workout duration per session", DURATION_OPTS, "workout_duration", horizontal=False)

        # Multi-select: joined to a single string for substring-based scoring in model_loader.
        workout_types = _multiselect(
            "Workout type(s) — select all that apply",
            WORKOUT_OPTS,
            "workout_types",
        )

        # ── Section 3: Sleep & Sedentary Behaviour ────────────────────────────
        _section("Sleep & Sedentary Behaviour")
        c1, c2 = st.columns(2)
        with c1:
            sleep_hours = _radio("Average sleep per night", SLEEP_OPTS, "sleep_hours", horizontal=False)
        with c2:
            screen_time = _radio("Daily screen time (phone + laptop)", SCREEN_OPTS, "screen_time", horizontal=False)

        sitting_time = _radio("Daily sitting time", SITTING_OPTS, "sitting_time", horizontal=True)

        # ── Section 4: Lifestyle Habits ───────────────────────────────────────
        _section("Lifestyle Habits")
        c1, c2 = st.columns(2)
        with c1:
            alcohol = _radio("Alcohol consumption", ALCOHOL_OPTS, "alcohol", horizontal=True)
        with c2:
            smoke = _radio("Do you smoke?", SMOKE_OPTS, "smoke", horizontal=True)

        stress_level = _radio("Daily workload / stress level", STRESS_OPTS, "stress_level", horizontal=True)

        # ── Section 5: Nutrition ──────────────────────────────────────────────
        _section("Nutrition")
        junk_food = _radio(
            "Junk food / packaged snacks frequency",
            JUNK_OPTS, "junk_food", horizontal=True,
        )

        c1, c2 = st.columns(2)
        with c1:
            water_intake = _radio("Daily water intake", WATER_OPTS, "water_intake", horizontal=False)
        with c2:
            fruit_veg = _radio("Fruit / vegetable servings per day", FRUIT_VEG_OPTS, "fruit_veg", horizontal=False)

        c1, c2 = st.columns(2)
        with c1:
            calories = _radio("Average daily calorie intake", CALORIE_OPTS, "calories", horizontal=False)
        with c2:
            protein_level = _radio("Protein intake level", PROTEIN_OPTS, "protein_level", horizontal=False)

        food_order_freq = _radio(
            "Online food order frequency",
            ORDER_OPTS, "food_order_freq", horizontal=True,
        )

        # ── Section 6: Health & Energy ────────────────────────────────────────
        _section("Health & Energy")
        c1, c2 = st.columns(2)
        with c1:
            energetic = _radio("How often do you feel energetic during the day?", ENERGY_OPTS, "energetic", horizontal=False)
        with c2:
            fatigue = _radio("How often do you experience fatigue?", FATIGUE_OPTS, "fatigue", horizontal=False)

        fitness_rating = _radio(
            "Overall fitness level (self-rated)",
            FITNESS_OPTS, "fitness_rating", horizontal=True,
        )

        # ── Submit ────────────────────────────────────────────────────────────
        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        _, mid, _ = st.columns([1, 2, 1])
        with mid:
            submitted = st.form_submit_button("Get My Results", use_container_width=True)

        if submitted:
            if not workout_types:
                st.warning("Please select at least one workout type (choose 'none' if you do not exercise).")
                return

            # Join multi-select list to a single string for substring matching
            workout_str = ", ".join(workout_types)

            # Build user_data with short form keys expected by model_loader.py
            user_data = {
                "gender"          : gender,
                "height"          : HEIGHT_MID.get(height_bucket, 170),  # int cm midpoint
                "weight"          : WEIGHT_MID.get(weight_bucket, 70),   # int kg midpoint
                "step_count"      : step_count,
                "exercise_days"   : exercise_days,
                "workout_duration": workout_duration,
                "workout_type"    : workout_str,
                "sleep_hours"     : sleep_hours,
                "screen_time"     : screen_time,
                "sitting_time"    : sitting_time,
                "alcohol"         : alcohol,
                "smoke"           : smoke,
                "stress_level"    : stress_level,
                "junk_food"       : junk_food,
                "water_intake"    : water_intake,
                "fruit_veg"       : fruit_veg,
                "calories"        : calories,
                "protein_level"   : protein_level,
                "food_order_freq" : food_order_freq,
                "energetic"       : energetic,
                "fatigue"         : fatigue,
                "fitness_rating"  : fitness_rating,
            }

            st.session_state.user_inputs = user_data

            with st.spinner("Analysing your fitness profile..."):
                try:
                    result = predict_cluster(user_data)
                    st.session_state.prediction_result = result
                    st.session_state.page = "results"
                    st.rerun()
                except Exception as exc:
                    st.error(f"Prediction error: {exc}")
                    st.info("Ensure all fields are filled correctly and try again.")

    # Back navigation (outside form)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        if st.button("Back to Home", use_container_width=True):
            st.session_state.page = "home"
            st.rerun()

    st.markdown('<div class="footer">Developed by Akshat 🩵</div>', unsafe_allow_html=True)