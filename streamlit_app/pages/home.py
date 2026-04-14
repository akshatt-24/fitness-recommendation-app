"""
home.py
─────────────────────────────────────────────────────────────────────────────
Landing page. Introduces the application and routes to the input form.
All styling is sourced from styles.py / config.toml.
─────────────────────────────────────────────────────────────────────────────
"""

import streamlit as st
from utils.styles import inject_global_css


def show() -> None:
    inject_global_css()

    # Page header
    st.markdown("""
    <div class="page-header">
        <h1>Fitness Categorization</h1>
        <p>Diet and Workout Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

    # Introduction
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="card">
            <h3>What This System Does</h3>
            <p>
                This application uses <strong>Agglomerative Hierarchical Clustering</strong> to
                analyse your fitness profile across 20+ lifestyle parameters and assign you to
                one of five fitness categories. Each category comes with targeted diet,
                exercise, and lifestyle recommendations derived directly from the model.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:0.5rem'></div>", unsafe_allow_html=True)

    # Feature highlights
    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
            <h3>Comprehensive Input</h3>
            <p>
                We evaluate exercise habits, nutrition, sleep patterns, sedentary behaviour,
                lifestyle risk factors, and subjective energy levels.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <h3>ML-Powered Analysis</h3>
            <p>
                A trained clustering model identifies your fitness profile and assigns you
                to the nearest centroid across seven composite health scores.
            </p>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
            <h3>Actionable Output</h3>
            <p>
                Recommendations are category-specific and prioritised so you know exactly
                which area to address first for the fastest improvement.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # Objectives
    _, col, _ = st.columns([1, 2, 1])
    with col:
        st.markdown("""
        <div class="card">
            <h3>Objectives</h3>
            <p>Accurately categorise your current fitness level</p>
            <p>Provide data-driven health insights from model scores</p>
            <p>Deliver prioritised diet, exercise, and lifestyle plans</p>
            <p>Support informed, evidence-based health decisions</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        if st.button("Get Started", key="get_started_btn", use_container_width=True):
            st.session_state.page = "input"
            st.rerun()

    # Footer
    st.markdown("""
    <div class="footer"><strong>Developed by Akshat 🩵</strong></div>
    """, unsafe_allow_html=True)