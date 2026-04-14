"""
results.py
─────────────────────────────────────────────────────────────────────────────
Results page. Renders the output of model_loader.predict_cluster().

Expected session state shape (set by input_form.py):
    st.session_state.prediction_result = {
        "cluster"        : int,              # 0=Very Low ... 4=High Fitness
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

import streamlit as st
from database.db_handler import save_prediction, save_feedback
from utils.styles import inject_global_css

# Maps cluster int (0-4) to a visual level indicator label
_LEVEL_LABELS = {
    0: "Level 1 of 5",
    1: "Level 2 of 5",
    2: "Level 3 of 5",
    3: "Level 4 of 5",
    4: "Level 5 of 5",
}


def _priority_class(priority_str: str) -> str:
    """Map priority string to CSS badge class."""
    p = priority_str.lower()
    if "high" in p and "low" not in p:
        return "priority-high"
    if "low" in p:
        return "priority-low"
    return "priority-medium"


def _render_rec_card(title: str, rec: dict) -> None:
    """Render a titled recommendation card with priority badge and target list."""
    priority    = rec.get("priority", "Medium")
    targets     = rec.get("targets", [])
    badge_class = _priority_class(priority)

    items_html = "".join(
        f'<div class="rec-item"><span class="rec-bullet">-</span>{t}</div>'
        for t in targets
    )

    st.markdown(f"""
    <div class="card">
        <h3>{title}</h3>
        <span class="priority-badge {badge_class}">Priority: {priority}</span>
        {items_html}
    </div>
    """, unsafe_allow_html=True)


def _render_fitness_bar(cluster: int) -> None:
    """Render a simple 5-segment progress bar showing fitness level."""
    filled   = cluster + 1   # 1-5
    segments = ""
    for i in range(5):
        color = "#4f8ef7" if i < filled else "rgba(255,255,255,0.08)"
        segments += f'<div style="flex:1;height:8px;background:{color};border-radius:4px;margin:0 2px"></div>'

    st.markdown(f"""
    <div style="margin:0.75rem 0 1.5rem">
        <div style="font-size:0.75rem;color:#7a8099;margin-bottom:0.4rem">
            Fitness Level — {_LEVEL_LABELS.get(cluster, "")}
        </div>
        <div style="display:flex;gap:4px">{segments}</div>
    </div>
    """, unsafe_allow_html=True)


def show() -> None:
    inject_global_css()

    result = st.session_state.get("prediction_result")

    if result is None:
        st.warning("No prediction results found. Please complete the assessment first.")
        if st.button("Go to Assessment"):
            st.session_state.page = "input"
            st.rerun()
        return

    st.markdown("""
    <div class="page-header">
        <h1>Your Fitness Results</h1>
        <p>Category assignment and personalised recommendations</p>
    </div>
    """, unsafe_allow_html=True)

    _, col, _ = st.columns([1, 3, 1])
    with col:

        # ── Cluster summary card ──────────────────────────────────────────────
        label       = result.get("cluster_label", "Unknown")
        tagline     = result.get("tagline", "")
        description = result.get("description", "")
        cluster_int = result.get("cluster", 2)

        st.markdown(f"""
        <div class="result-card">
            <div class="cluster-label">{label}</div>
            <div class="tagline">{tagline}</div>
            <p class="description">{description}</p>
        </div>
        """, unsafe_allow_html=True)

        # Fitness level progress bar
        _render_fitness_bar(cluster_int)

        # ── Recommendations ───────────────────────────────────────────────────
        st.markdown('<div class="section-label">Personalised Recommendations</div>',
                    unsafe_allow_html=True)

        recs = result.get("recommendations", {})
        _render_rec_card("Diet",      recs.get("diet",      {}))
        _render_rec_card("Exercise",  recs.get("exercise",  {}))
        _render_rec_card("Lifestyle", recs.get("lifestyle", {}))

        st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
        
        
        
        # Feedback form
        feedback_col1, feedback_col2, feedback_col3 = st.columns([1, 2, 1])
        
        with feedback_col2:
            if 'feedback_submitted' not in st.session_state:
                st.session_state.feedback_submitted = False
            
            if not st.session_state.feedback_submitted:
                satisfaction = st.radio(
                    "How satisfied are you with the response?",
                    options=[
                        " Very Satisfied",
                        " Satisfied",
                        " Neutral",
                        " Not Satisfied"
                    ],
                    key="satisfaction",
                    horizontal=False
                )
                
                comments = st.text_area(
                    "Additional comments (optional)",
                    placeholder="Share your thoughts, suggestions, or questions...",
                    key="comments"
                )
                
                if st.button("✅ Submit Feedback", use_container_width=True):
                    # Save to database
                    try:
                        # First save the prediction
                        prediction_id = save_prediction(
                            st.session_state.user_inputs,
                            result['cluster']
                        )
                        
                        # Then save feedback
                        save_feedback(
                            prediction_id,
                            satisfaction,
                            comments
                        )
                        
                        st.session_state.feedback_submitted = True
                        st.success("✅ Thank you for your feedback!")
                        st.balloons()
                        
                    except Exception as e:
                        st.error(f"Error saving feedback: {str(e)}")
            else:
                st.success("✅ Feedback submitted successfully!")
                st.info("Your feedback helps us improve our recommendations.")
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

        # ── Navigation ────────────────────────────────────────────────────────
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Take Another Assessment", use_container_width=True):
                st.session_state.user_inputs       = {}
                st.session_state.prediction_result = None
                st.session_state.page              = "input"
                st.rerun()
        with c2:
            if st.button("Back to Home", use_container_width=True):
                st.session_state.user_inputs       = {}
                st.session_state.prediction_result = None
                st.session_state.page              = "home"
                st.rerun()

    st.markdown('<div class="footer"><strong>Developed by Akshat 🩵</strong></div>', unsafe_allow_html=True)