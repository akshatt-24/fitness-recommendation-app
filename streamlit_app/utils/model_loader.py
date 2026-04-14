"""
model_loader.py
─────────────────────────────────────────────────────────────────────────────
Runtime inference module. No dependency on fitness_model.py.

Flow:
    predict_cluster(user_data)
        -> preprocess_inputs()     : form keys -> numeric feature vector
        -> pkl bundle predict()    : if bundle loaded and functional
        -> calculate_fitness_cluster() : rule-based fallback otherwise
        -> build_result()          : unified output dict for results.py

Output dict shape (stored in st.session_state.prediction_result):
    {
        "cluster"        : int,          # 0=Very Low ... 4=High Fitness
        "cluster_label"  : str,
        "tagline"        : str,
        "description"    : str,
        "recommendations": {
            "diet"      : {"priority": str, "targets": list[str]},
            "exercise"  : {"priority": str, "targets": list[str]},
            "lifestyle" : {"priority": str, "targets": list[str]},
        },
    }
─────────────────────────────────────────────────────────────────────────────
"""

import warnings
import numpy as np
from pathlib import Path

warnings.filterwarnings("ignore")

# ── Cached bundle (None until first successful load) ─────────────────────────
_bundle = None


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 1 — PKL LOADER
# ═════════════════════════════════════════════════════════════════════════════

def load_model():
    """
    Attempt to load the joblib bundle from known filesystem locations.
    Returns the bundle dict on success, or None if unavailable / broken.
    The pkl requires fitness_model.py's custom classes on sys.path to unpickle;
    if that import fails, the rule-based fallback is used instead.
    """
    global _bundle
    if _bundle is not None:
        return _bundle

    search_paths = [
        Path(__file__).parent.parent / "fitness_model_bundle.pkl",           # app/
        Path(__file__).parent.parent.parent / "fitness_model_bundle.pkl",    # project root
        Path(__file__).parent / "fitness_model_bundle.pkl",                  # same dir
    ]

    for path in search_paths:
        if not path.exists():
            continue
        try:
            import joblib
            import sys
            # fitness_model.py must be importable so joblib can resolve custom classes
            streamlit_root = Path(__file__).parent.parent
            if str(streamlit_root) not in sys.path:
                sys.path.insert(0, str(streamlit_root))
            _bundle = joblib.load(path)
            return _bundle
        except Exception:
            # Version mismatch or missing fitness_model — fall through to fallback
            _bundle = None

    return None


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 2 — INPUT PREPROCESSING
# Keys must match exactly what input_form.py stores in user_data.
# ═════════════════════════════════════════════════════════════════════════════

def preprocess_inputs(user_data: dict) -> np.ndarray:
    """
    Convert form bucket strings to a numeric feature vector.
    Order matches the feature vector the pkl bundle was trained on.
    """
    f = []

    # Gender
    f.append({"Male": 1, "Female": 0, "Other": 2}.get(user_data["gender"], 1))

    # Height / weight — form stores numeric midpoints directly
    height = float(user_data["height"])
    weight = float(user_data["weight"])
    f.append(height)
    f.append(weight)
    f.append(round(weight / (height / 100) ** 2, 2))   # BMI

    # Steps
    f.append({
        "Less than 3000": 1500,
        "3000 - 6000":    4500,
        "6000-10000":     8000,
        "10000+":         11000,
    }.get(user_data["step_count"], 4500))

    # Exercise days
    f.append({
        "0 days":  0.0,
        "1-2":     1.5,
        "3-4":     3.5,
        "5+":      5.5,
    }.get(user_data["exercise_days"], 1.5))

    # Workout duration
    f.append({
        "0":    0.0,
        "15-30": 22.5,
        "30-60": 45.0,
        "60+":   75.0,
    }.get(user_data["workout_duration"], 22.5))

    # Workout type intensity score (multi-label joined string)
    wt = user_data.get("workout_type", "")
    wt_score = 0
    if "Gym" in wt or "Strength" in wt:      wt_score += 2
    if "Cardio" in wt or "Running" in wt:    wt_score += 2
    if "Sports" in wt:                        wt_score += 2
    if "Yoga" in wt or "Stretching" in wt:   wt_score += 1
    if wt.strip().lower() == "none":          wt_score  = 0
    f.append(round(wt_score / 7, 4))

    # Sleep
    f.append({
        "Less than 5 hours": 4.0,
        "5-6 hours":         5.5,
        "6-8 hours":         7.0,
        "8+ hours":          8.5,
    }.get(user_data["sleep_hours"], 7.0))

    # Screen time
    f.append({
        "Less than 3 hours": 1.5,
        "3-5 hours":         4.0,
        "5-7 hours":         6.0,
        "7+ hours":          8.0,
    }.get(user_data["screen_time"], 4.0))

    # Sitting time
    f.append({
        "Less than 4 hours": 2.0,
        "4-6 hours":         5.0,
        "6-8 hours":         7.0,
        "8+ hours":          9.0,
    }.get(user_data["sitting_time"], 5.0))

    # Alcohol
    f.append({"Never": 0, "Occasionally": 1, "Regularly": 2}.get(user_data["alcohol"], 0))

    # Smoke
    f.append(1 if user_data["smoke"] == "Yes" else 0)

    # Stress
    f.append({
        "Very low": 1, "Moderate": 2, "High": 3, "Very High": 4,
    }.get(user_data["stress_level"], 2))

    # Junk food
    f.append({
        "Rarely (once a month or less)": 4,
        "1-2 times a week":              3,
        "3-4 times a week":              2,
        "Almost daily":                  1,
    }.get(user_data["junk_food"], 3))

    # Water intake
    f.append({
        "1-2 liters":         1,
        "2-3 liters":         2,
        "more than 3 liters": 3,
    }.get(user_data["water_intake"], 2))

    # Fruit / veg
    f.append({
        "0 servings":  1,
        "1 serving":   2,
        "2-3 servings": 3,
        "3+ servings": 5,
    }.get(user_data["fruit_veg"], 3))

    # Calories
    f.append({
        "less than 1800 kcal": 3,
        "1800 - 2200 kcal":    5,
        "2200 - 2600 kcal":    2,
        "2600+ kcal":          1,
        "not sure":            3,
    }.get(user_data["calories"], 3))

    # Protein
    f.append({"Low": 1, "Moderate": 3, "High": 5}.get(user_data["protein_level"], 3))

    # Food order frequency
    f.append({
        "rarely (once a month or less)": 5,
        "1-2 times a week":              3,
        "3-4 times a week":              2,
        "5+ times a week":               1,
    }.get(user_data["food_order_freq"], 3))

    # Energetic
    f.append({
        "never": 1, "occasionally": 3, "frequently": 4, "always": 5,
    }.get(user_data["energetic"], 3))

    # Fatigue (inverted: less fatigue = higher score)
    f.append({
        "always": 1, "frequently": 2, "occasionally": 3, "never": 5,
    }.get(user_data["fatigue"], 3))

    # Self-rated fitness
    f.append({
        "Poor (1-2)":       1,
        "Average (3-5)":    3,
        "Good (6-7)":       4,
        "Excellent (8-10)": 5,
    }.get(user_data["fitness_rating"], 3))

    return np.array(f).reshape(1, -1)


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 3 — RULE-BASED FALLBACK CLUSTER ASSIGNMENT
# Used when the pkl bundle is unavailable or broken.
# ═════════════════════════════════════════════════════════════════════════════

def _rule_based_cluster(user_data: dict) -> int:
    """
    Score-based fitness cluster assignment.
    Returns int 0–4 where 0 = Very Low Fitness, 4 = High Fitness.
    """
    score = 0

    # Exercise (0-30 pts)
    ex_days = {
        "0 days": 0.0, "1-2": 1.5, "3-4": 3.5, "5+": 5.5,
    }.get(user_data["exercise_days"], 0.0)
    score += ex_days * 3  # max ~16.5

    duration = {
        "0": 0, "15-30": 22.5, "30-60": 45.0, "60+": 75.0,
    }.get(user_data["workout_duration"], 0)
    score += min(duration / 10, 10)  # cap 10 pts

    # Nutrition (0-25 pts)
    bmi = float(user_data["weight"]) / (float(user_data["height"]) / 100) ** 2
    if 18.5 <= bmi <= 24.9:    score += 10
    elif 17 <= bmi < 18.5 or 25 <= bmi <= 29.9: score += 5

    fv = {
        "0 servings": 0, "1 serving": 1, "2-3 servings": 2.5, "3+ servings": 4,
    }.get(user_data["fruit_veg"], 0)
    if fv >= 3:    score += 10
    elif fv >= 2:  score += 5

    # Lifestyle (0-25 pts)
    sleep = {
        "Less than 5 hours": 4.0, "5-6 hours": 5.5,
        "6-8 hours": 7.0,         "8+ hours":  8.5,
    }.get(user_data["sleep_hours"], 6.0)
    if 7 <= sleep <= 9: score += 10
    elif sleep >= 6:    score += 5

    if user_data["alcohol"] == "Never":        score += 5
    if user_data["smoke"] == "No":             score += 10

    # Activity (0-20 pts)
    steps = {
        "Less than 3000": 1500, "3000 - 6000": 4500,
        "6000-10000": 8000,     "10000+":      11000,
    }.get(user_data["step_count"], 1500)
    if steps >= 10000:  score += 10
    elif steps >= 5000: score += 5

    sitting = {
        "Less than 4 hours": 2, "4-6 hours": 5,
        "6-8 hours": 7,         "8+ hours":  9,
    }.get(user_data["sitting_time"], 7)
    if sitting <= 6:    score += 10
    elif sitting <= 8:  score += 5

    if score >= 80:   return 4   # High Fitness
    if score >= 60:   return 3   # Active but Imperfect
    if score >= 40:   return 2   # Moderate Fitness
    if score >= 20:   return 1   # Low Fitness
    return 0                     # Very Low Fitness


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 4 — CLUSTER DEFINITIONS
# Unified for both the pkl path and the rule-based path.
# ═════════════════════════════════════════════════════════════════════════════

_CLUSTER_INFO = {
    0: {
        "label"  : "Very Low Fitness",
        "tagline": "Immediate lifestyle change needed",
        "description": (
            "Extremely sedentary with almost no structured exercise. "
            "Very low daily steps and poor dietary habits — high junk food, "
            "low hydration, minimal fruit and vegetables. Sleep is irregular "
            "and stress is elevated. BMI is likely outside the healthy range."
        ),
        "recommendations": {
            "diet": {
                "priority": "High",
                "targets": [
                    "Eliminate or drastically reduce junk food — target Rarely (1x/week or less)",
                    "Drink at least 2-3 litres of water daily; carry a bottle as a reminder",
                    "Add one fruit or vegetable serving per meal as a starting point",
                    "Stop online food ordering on weekdays; cook simple home meals",
                    "Eat regular meals at fixed times — do not skip breakfast",
                    "Replace cold drinks and packaged juice with water or coconut water",
                    "Target 1800-2200 kcal/day; add a protein source to every meal",
                ],
            },
            "exercise": {
                "priority": "High — build habit before intensity",
                "targets": [
                    "Start with 20-minute walks 3x per week — consistency before intensity",
                    "Target 4000-5000 steps/day in week 1, increase by 500 steps weekly",
                    "Do 5-10 minutes of basic stretching every morning",
                    "Avoid all-day sitting: stand or walk for 5 minutes every hour",
                    "After 4 weeks of consistent walking, add bodyweight exercises",
                    "Aim for 3 active days per week before increasing to 4-5",
                ],
            },
            "lifestyle": {
                "priority": "High",
                "targets": [
                    "Reduce screen time to under 5 hours/day — set phone usage limits",
                    "Fix a consistent sleep schedule: same bedtime and wake time daily",
                    "Target 6-8 hours of sleep; avoid screens 30 minutes before bed",
                    "If smoking or drinking regularly: reduce frequency week by week",
                    "Use a 5-minute breathing exercise (box breathing) to manage stress",
                ],
            },
        },
    },
    1: {
        "label"  : "Low Fitness",
        "tagline": "Below average — focused effort will show quick results",
        "description": (
            "Low to occasional activity with inconsistent exercise. "
            "Diet quality is below average with frequent unhealthy food choices. "
            "Sleep and stress management need improvement. "
            "Some awareness of healthy habits exists but discipline is lacking."
        ),
        "recommendations": {
            "diet": {
                "priority": "Medium-High",
                "targets": [
                    "Reduce junk food to 1-2 times per week maximum",
                    "Increase daily water intake to at least 2 litres",
                    "Add 2-3 fruit/veg servings per day — include one with every main meal",
                    "Reduce online food orders to 1-2 times per week; plan meals in advance",
                    "Increase protein: add eggs, curd, or sprouts to at least 2 meals per day",
                    "Avoid eating within 2 hours of bedtime",
                    "Replace one processed snack per day with a healthier option",
                ],
            },
            "exercise": {
                "priority": "Medium-High",
                "targets": [
                    "Exercise at least 3 days per week — even 30-minute walks count",
                    "Build daily steps to 6000-7000; use stairs instead of the lift",
                    "Introduce one structured workout session per week",
                    "Increase session duration to 30-45 minutes as stamina improves",
                    "Add a 10-minute morning routine: light stretching and sun exposure",
                ],
            },
            "lifestyle": {
                "priority": "Medium",
                "targets": [
                    "Aim for 6.5-8 hours of sleep consistently; fix your wake-up time first",
                    "Limit screen time to 5 hours/day; avoid phone use in bed",
                    "Reduce sitting time to under 7 hours/day; take movement breaks hourly",
                    "Practice 10 minutes of relaxation daily: meditation or a walk",
                    "If consuming alcohol, limit to occasional and avoid binge episodes",
                ],
            },
        },
    },
    2: {
        "label"  : "Moderate Fitness",
        "tagline": "Average — consistency will unlock the next level",
        "description": (
            "Moderately active with 2-4 exercise days per week and average step count. "
            "Dietary habits are mixed — some healthy choices but inconsistency remains. "
            "Sleep and stress are reasonably managed. "
            "A strong foundation exists; needs better consistency and diet discipline to progress."
        ),
        "recommendations": {
            "diet": {
                "priority": "Medium",
                "targets": [
                    "Hit 3+ fruit/veg servings daily — add a salad or vegetable side to every dinner",
                    "Drink 2.5-3 litres of water daily; set reminders if needed",
                    "Keep junk food to Rarely or 1-2 times per week only",
                    "Prioritise high-protein meals: target 0.8-1g protein per kg bodyweight per day",
                    "Meal prep 2-3 days in advance to avoid impulsive ordering",
                    "Calibrate calorie intake: track for one week to confirm you are in range",
                ],
            },
            "exercise": {
                "priority": "Medium — focus on consistency and progression",
                "targets": [
                    "Increase exercise frequency to 4-5 days per week",
                    "Build daily steps to 8000-10000; aim for at least one 30-minute walk per day",
                    "Add one strength training session per week",
                    "Extend workout sessions to 45-60 minutes for better cardiovascular benefit",
                    "Introduce progressive overload: increase reps or duration every 2 weeks",
                ],
            },
            "lifestyle": {
                "priority": "Low-Medium",
                "targets": [
                    "Maintain 7-8 hours of sleep; use a consistent wind-down routine",
                    "Keep screen time under 5 hours/day; avoid doom-scrolling before sleep",
                    "Manage daily sitting to under 6 hours; use a standing or walking break schedule",
                    "Practice stress management: 10-15 min daily walk, journaling, or yoga",
                    "Limit alcohol to occasional or social; avoid mixing with high-calorie food",
                ],
            },
        },
    },
    3: {
        "label"  : "Active but Imperfect",
        "tagline": "Close to optimal — fix weak spots to reach High Fitness",
        "description": (
            "Regular physical activity (4-5 days/week) with good step count and workout consistency. "
            "Activity levels are strong but overall fitness is held back by one or more of: "
            "inconsistent diet, suboptimal sleep, high stress, or elevated lifestyle risk factors. "
            "Targeted improvements in weaker areas will unlock High Fitness quickly."
        ),
        "recommendations": {
            "diet": {
                "priority": "Medium — fine-tune rather than overhaul",
                "targets": [
                    "Optimise protein intake to support training: 1-1.2g per kg bodyweight per day",
                    "Eat 4-5 fruit/veg servings daily for micronutrient support and recovery",
                    "Time carbohydrates around workouts: higher carbs pre/post training",
                    "Eliminate remaining junk food and online order habits",
                    "Stay consistently hydrated: 3+ litres on training days, 2.5 on rest days",
                    "Avoid late-night eating after 9 PM — it disrupts sleep quality",
                ],
            },
            "exercise": {
                "priority": "Low — maintain and diversify",
                "targets": [
                    "Maintain 5+ days/week of activity; add one recovery/mobility day",
                    "Keep step count above 8000-10000 daily; rest days should not be sedentary",
                    "Add variety: if gym-focused, add a sport or swim session",
                    "Include progressive overload every 2-3 weeks to continue adaptation",
                    "Prioritise warm-up and cool-down to prevent injury at your training frequency",
                ],
            },
            "lifestyle": {
                "priority": "High — this is your limiting factor",
                "targets": [
                    "Fix sleep immediately: 7-9 hours non-negotiable at your activity level",
                    "If stress is High or Very High: add a structured stress-management practice",
                    "Completely eliminate smoking if present — it undermines cardiovascular capacity",
                    "Reduce alcohol to Occasionally or Never — it suppresses muscle protein synthesis",
                    "Limit screen time to 4-5 hours/day; avoid blue light 1 hour before bed",
                ],
            },
        },
    },
    4: {
        "label"  : "High Fitness",
        "tagline": "Optimal — maintain, refine, and prevent regression",
        "description": (
            "Highly active and disciplined lifestyle with consistent workouts (5+ days/week). "
            "Excellent diet, hydration, and recovery practices. "
            "Healthy BMI, low lifestyle risk, and high subjective energy. "
            "Represents optimal fitness and sustainable long-term habits."
        ),
        "recommendations": {
            "diet": {
                "priority": "Low — maintain quality, optimise periodically",
                "targets": [
                    "Continue 5+ fruit/veg servings daily — maintain micronutrient density",
                    "Keep protein at 1-1.2g/kg bodyweight; increase to 1.4g on heavy training weeks",
                    "Cycle calories if strength training: surplus on training days, maintenance on rest",
                    "Stay above 3 litres of water daily; increase on hot days or intense sessions",
                    "Maintain your low junk food and ordering frequency — protect this habit",
                ],
            },
            "exercise": {
                "priority": "Low — sustain and protect from injury",
                "targets": [
                    "Maintain 5-7 active days per week; include 1-2 active recovery sessions",
                    "Keep daily steps above 8000-10000 even on rest days",
                    "Prioritise mobility work to prevent injury at high training volumes",
                    "Include periodisation: plan de-load weeks every 4-6 weeks",
                    "Track performance metrics to detect early decline",
                ],
            },
            "lifestyle": {
                "priority": "Low — protect habits from regression",
                "targets": [
                    "Protect your sleep schedule as non-negotiable: 7-9 hours every night",
                    "Continue your low-risk lifestyle: maintain no or rare smoking and alcohol status",
                    "Monitor stress proactively — high achievers often ignore it until burnout",
                    "Keep screen time managed even when busy periods arise",
                    "Schedule annual health check-ups",
                ],
            },
        },
    },
}


# ═════════════════════════════════════════════════════════════════════════════
# SECTION 5 — MAIN INFERENCE ENTRY POINT
# ═════════════════════════════════════════════════════════════════════════════

def predict_cluster(user_data: dict) -> dict:
    """
    Primary entry point called from input_form.py.

    Args:
        user_data: dict with short form keys as stored by input_form.py

    Returns:
        Unified result dict consumed by results.py.
    """
    cluster_int = None

    # Attempt pkl-based prediction
    bundle = load_model()
    if bundle is not None:
        try:
            features = preprocess_inputs(user_data)
            # Bundle uses centroid_predictor, not a direct sklearn model
            predictor = bundle.get("centroid_predictor")
            scaler    = bundle.get("scaler")
            imputer   = bundle.get("imputer")
            if predictor and scaler and imputer:
                X_imp    = imputer.transform(features)
                X_scaled = scaler.transform(X_imp)
                raw_rank = int(predictor.predict(X_scaled)[0])
                # rank_to_label maps int rank -> label string; invert to get 0-4 index
                rank_to_label = bundle.get("rank_to_label", {})
                label_to_index = {
                    "Very Low Fitness":    0,
                    "Low Fitness":         1,
                    "Moderate Fitness":    2,
                    "Active but Imperfect": 3,
                    "High Fitness":        4,
                }
                label = rank_to_label.get(raw_rank, "Moderate Fitness")
                cluster_int = label_to_index.get(label, 2)
        except Exception:
            cluster_int = None   # fall through to rule-based

    # Rule-based fallback
    if cluster_int is None:
        cluster_int = _rule_based_cluster(user_data)

    info = _CLUSTER_INFO[cluster_int]
    return {
        "cluster"        : cluster_int,
        "cluster_label"  : info["label"],
        "tagline"        : info["tagline"],
        "description"    : info["description"],
        "recommendations": info["recommendations"],
    }