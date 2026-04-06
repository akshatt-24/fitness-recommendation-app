import streamlit as st

def show():
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>💪 Fitness Categorization</h1>
        <p>Diet and Workout Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)
    
    
    # Introduction
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("""
        ### Welcome to Your Personalized Fitness Journey
        
        Our advanced machine learning system analyzes your lifestyle, habits, and fitness metrics to categorize your current fitness level and provide tailored recommendations.
        """)
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # What We Do Section
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 What We Do</h3>
            <p>
                This application uses <strong>Agglomerative Hierarchical Clustering</strong> to analyze your fitness profile 
                and place you into a specific fitness category. Based on your category, you'll receive personalized 
                diet and workout recommendations designed to help you achieve your health goals.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Features Grid
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="feature-card">
            <h3>📊 Comprehensive Analysis</h3>
            <p>
                We evaluate 20+ lifestyle and fitness parameters including exercise habits, 
                nutrition, sleep patterns, and daily activity levels.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🤖 ML-Powered Insights</h3>
            <p>
                Our trained clustering algorithm identifies patterns in your data to provide 
                accurate fitness categorization and actionable recommendations.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="feature-card">
            <h3>💡 Personalized Results</h3>
            <p>
                Get customized diet plans and workout routines based on your unique fitness 
                profile and category assignment.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 3rem;'></div>", unsafe_allow_html=True)
    
    # Objectives
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="feature-card">
            <h3>🎯 Our Objective</h3>
            <p>
                ✅ Accurately categorize your fitness level<br>
                ✅ Provide data-driven health insights<br>
                ✅ Recommend personalized diet and workout plans<br>
                ✅ Help you make informed decisions about your health journey<br>
                ✅ Continuously improve recommendations based on user feedback
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        # Get Started Button
        if st.button("🚀 Get Started", key="get_started_btn", use_container_width=True):
            st.session_state.page = 'input'
            st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        Developed by Akshat with <span>❤️</span>
    </div>
    """, unsafe_allow_html=True)
