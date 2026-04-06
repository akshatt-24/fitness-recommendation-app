import streamlit as st
from database.db_handler import save_prediction, save_feedback
from datetime import datetime

def show():
    # Check if we have results
    if st.session_state.prediction_result is None:
        st.warning("No prediction results found. Please complete the form first.")
        if st.button("Go to Form"):
            st.session_state.page = 'input'
            st.rerun()
        return
    
    result = st.session_state.prediction_result
    
    st.markdown("""
    <div class="main-header">
        <h1>🎉 Your Fitness Category</h1>
        <p>Based on your comprehensive fitness profile analysis</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display Results
    col1, col2, col3 = st.columns([1, 3, 1])
    
    with col2:
        st.markdown(f"""
        <div class="result-card">
            <h2>📊 Your Category: Cluster {result['cluster']}</h2>
            <p>{result['interpretation']['description']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Recommendations Section
        st.markdown("### 💪 Personalized Recommendations")
        
        st.markdown("""
        <div class="feature-card">
            <h3>🥗 Diet Recommendations</h3>
        """, unsafe_allow_html=True)
        
        for rec in result['interpretation']['diet_recommendations']:
            st.markdown(f"<p>• {rec}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-card">
            <h3>🏋️ Workout Recommendations</h3>
        """, unsafe_allow_html=True)
        
        for rec in result['interpretation']['workout_recommendations']:
            st.markdown(f"<p>• {rec}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Key Insights
        if 'insights' in result['interpretation']:
            st.markdown("""
            <div class="feature-card">
                <h3>💡 Key Insights</h3>
            """, unsafe_allow_html=True)
            
            for insight in result['interpretation']['insights']:
                st.markdown(f"<p>• {insight}</p>", unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Feedback Section
        st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feedback-section">
            <h3 style="color: #00d4ff; text-align: center;">📝 Your Feedback Matters</h3>
            <p style="text-align: center; color: #b8b8d1;">Help us improve by sharing your experience</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
        
        # Feedback form
        feedback_col1, feedback_col2, feedback_col3 = st.columns([1, 2, 1])
        
        with feedback_col2:
            if 'feedback_submitted' not in st.session_state:
                st.session_state.feedback_submitted = False
            
            if not st.session_state.feedback_submitted:
                satisfaction = st.radio(
                    "How satisfied are you with the response?",
                    options=[
                        "😍 Very Satisfied",
                        "😊 Satisfied",
                        "😐 Neutral",
                        "😕 Not Satisfied"
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
        
        # Action buttons
        col_a, col_b = st.columns(2)
        
        with col_a:
            if st.button("🔄 Take Another Assessment", use_container_width=True):
                # Clear session state
                st.session_state.user_inputs = {}
                st.session_state.prediction_result = None
                st.session_state.feedback_submitted = False
                st.session_state.page = 'input'
                st.rerun()
        
        with col_b:
            if st.button("🏠 Back to Home", use_container_width=True):
                # Clear session state
                st.session_state.user_inputs = {}
                st.session_state.prediction_result = None
                st.session_state.feedback_submitted = False
                st.session_state.page = 'home'
                st.rerun()
    
    # Footer
    st.markdown("""
    <div class="footer">
        Developed by Akshat with <span>❤️</span>
    </div>
    """, unsafe_allow_html=True)
