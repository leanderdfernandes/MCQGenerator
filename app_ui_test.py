import streamlit as st

# Dummy MCQ data for testing UI without API calls
DUMMY_MCQS = [
    {
        "question": "What is the capital of France?",
        "options": {
            "A": "Berlin",
            "B": "Madrid",
            "C": "Paris",
            "D": "Rome"
        },
        "correct_answer": "C",
        "explanation": "Paris is the capital and most populous city of France."
    },
    {
        "question": "Which element has the chemical symbol 'O'?",
        "options": {
            "A": "Gold",
            "B": "Oxygen",
            "C": "Silver",
            "D": "Iron"
        },
        "correct_answer": "B",
        "explanation": "'O' is the chemical symbol for Oxygen."
    },
    {
        "question": "What is 2 + 2?",
        "options": {
            "A": "3",
            "B": "4",
            "C": "5",
            "D": "22"
        },
        "correct_answer": "B",
        "explanation": "2 + 2 equals 4."
    }
]

def main():
    st.set_page_config(
        page_title="MCQ Generator UI Test",
        page_icon="🎓",
        layout="wide"
    )
    st.title("🎓 Engineering MCQ Generator (UI Test)")
    st.markdown("Generate multiple-choice questions from your lecture topics using AI (UI Test Mode, no API calls)")

    # Inject the same custom CSS as in app.py for consistent styling
    st.markdown(
        """
        <style>
        /* Aggressive light theme override for all buttons and inputs */
        body, .stApp, .main .block-container {
            background-color: #F7FAFC !important;
        }
        /* Card/form backgrounds */
        .stForm, .stExpander, .stMetric {
            background-color: #FFFFFF !important;
            border-radius: 12px !important;
            box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
            border: 1px solid #E2E8F0 !important;
        }
        /* Text colors */
        .stMarkdown, .stText, p, div, span, label, .stCaption, .stMetricLabel {
            color: #22223B !important;
        }
        h1, h2, h3, h4, h5, h6 {
            color: #22223B !important;
            font-weight: 600;
        }
        /* All buttons: primary, secondary, etc. */
        .stButton > button, .stForm button, button, input[type="button"], input[type="submit"] {
            background-color: #43A363 !important;
            color: #FFFFFF !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 1.5rem !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            transition: all 0.2s cubic-bezier(.4,0,.2,1) !important;
            box-shadow: 0 2px 8px rgba(67, 163, 99, 0.10) !important;
            outline: none !important;
        }
        .stButton > button:hover, .stForm button:hover, button:hover, input[type="button"]:hover, input[type="submit"]:hover {
            background-color: #388752 !important;
        }
        .stButton > button:active, .stForm button:active, button:active, input[type="button"]:active, input[type="submit"]:active {
            background-color: #2E6B4B !important;
        }
        /* Backward/secondary buttons (by key) - visually distinct */
        button#back_btn {
            background-color: #FFFFFF !important;
            color: #43A363 !important;
            border: 2px solid #43A363 !important;
            box-shadow: 0 2px 8px rgba(67, 163, 99, 0.05) !important;
        }
        button#back_btn:hover, button#back_btn:focus {
            background-color: #E9F7F0 !important;
            color: #388752 !important;
            border-color: #388752 !important;
        }
        /* Text inputs and textareas */
        .stTextInput input, .stTextArea textarea, input[type="text"], textarea {
            background-color: #FFFFFF !important;
            color: #22223B !important;
            border: 2px solid #E2E8F0 !important;
            border-radius: 8px !important;
            padding: 0.75rem !important;
            caret-color: #22223B !important;
        }
        .stTextInput input:focus, .stTextArea textarea:focus, input[type="text"]:focus, textarea:focus {
            border-color: #43A363 !important;
            box-shadow: 0 0 0 3px rgba(67, 163, 99, 0.10) !important;
        }
        /* Radio/toggle buttons - green accent and background */
        .stRadio > div {
            background-color: #FFFFFF !important;
            border-radius: 10px !important;
            padding: 1.25rem 2.5rem 1.25rem 1.5rem !important;
            border: 1.5px solid #E2E8F0 !important;
            margin-bottom: 1.1rem !important;
            min-width: 520px !important;
            max-width: 900px !important;
            width: 100% !important;
            box-shadow: 0 2px 8px rgba(0,0,0,0.04) !important;
            display: flex !important;
            flex-direction: column !important;
        }
        .stRadio label {
            color: #22223B !important;
            font-weight: 500 !important;
            font-size: 1.08rem !important;
            width: 100%;
        }
        .stRadio input[type="radio"] {
            accent-color: #B8EFC6 !important; /* light green */
            background-color: #E9F7F0 !important; /* very light green */
        }
        .stRadio input[type="radio"]:checked {
            accent-color: #43A363 !important; /* green when checked */
            background-color: #DFF3E8 !important;
        }
        /* Progress bar */
        .stProgress > div > div {
            background-color: #43A363 !important;
        }
        /* Success/Error/Info messages */
        .stSuccess {
            background-color: #DCFCE7 !important;
            color: #166534 !important;
            border-left: 4px solid #43A363 !important;
            padding: 1rem !important;
            border-radius: 8px !important;
        }
        .stError {
            background-color: #FEE2E2 !important;
            color: #B91C1C !important;
            border-left: 4px solid #EF4444 !important;
            padding: 1rem !important;
            border-radius: 8px !important;
        }
        .stInfo {
            background-color: #DBEAFE !important;
            color: #1E40AF !important;
            border-left: 4px solid #2563EB !important;
            padding: 1rem !important;
            border-radius: 8px !important;
        }
        /* Expander header */
        .stExpanderHeader {
            color: #22223B !important;
            background-color: #F1F5F9 !important;
            border-radius: 8px 8px 0 0 !important;
        }
        /* Links */
        a {
            color: #43A363 !important;
            text-decoration: underline !important;
        }
        /* Metrics */
        .stMetricValue {
            color: #43A363 !important;
            font-weight: bold !important;
        }
        /* Remove default Streamlit styling */
        * { color: inherit !important; }
        .stMarkdown p, .stMarkdown div, .stMarkdown span {
            color: #22223B !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Session state initialization
    if 'mcqs' not in st.session_state:
        st.session_state.mcqs = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'user_answers' not in st.session_state:
        st.session_state.user_answers = {}
    if 'quiz_completed' not in st.session_state:
        st.session_state.quiz_completed = False
    if 'show_feedback' not in st.session_state:
        st.session_state.show_feedback = False
    if 'last_user_answer' not in st.session_state:
        st.session_state.last_user_answer = None

    # Main application flow
    if st.session_state.mcqs is None:
        show_input_page()
    elif not st.session_state.quiz_completed:
        show_quiz_page()
    else:
        show_results_page()

def show_input_page():
    st.header("📝 Enter Lecture Information (Dummy)")
    with st.form("mcq_form"):
        lecture_topics = st.text_area(
            "📚 Lecture Topics & Summary",
            placeholder="Enter the main topics, concepts, and key points covered in your lecture...",
            height=200,
            help="Include all important topics, definitions, formulas, and concepts that were covered"
        )
        ai_instructions = st.text_area(
            "🤖 AI Instructions (Optional)",
            placeholder="Add any specific instructions for question generation (e.g., focus on practical applications, include calculations, etc.)",
            height=100,
            help="Optional: Provide additional guidance for the AI to generate better questions"
        )
        submitted = st.form_submit_button("🚀 Generate MCQs", type="primary")
        if submitted:
            st.session_state.mcqs = DUMMY_MCQS
            st.session_state.current_question = 0
            st.session_state.user_answers = {}
            st.session_state.quiz_completed = False
            st.session_state.show_feedback = False
            st.session_state.last_user_answer = None
            st.rerun()

def show_quiz_page():
    mcqs = st.session_state.mcqs
    current_q = st.session_state.current_question
    if current_q >= len(mcqs):
        st.session_state.quiz_completed = True
        st.rerun()
        return
    progress = (current_q + 1) / len(mcqs)
    st.progress(progress)
    st.caption(f"Question {current_q + 1} of {len(mcqs)}")
    if st.session_state.show_feedback:
        answered_question_data = mcqs[current_q]
        show_answer_feedback(answered_question_data, st.session_state.last_user_answer, current_q)
        return
    question_data = mcqs[current_q]
    st.header(f"Question {current_q + 1}")
    st.markdown(f"**{question_data['question']}**")
    with st.form(f"question_{current_q}"):
        user_answer = st.radio(
            "Select your answer:",
            options=list(question_data['options'].keys()),
            format_func=lambda x: f"{x}) {question_data['options'][x]}",
            key=f"radio_{current_q}"
        )
        submitted = st.form_submit_button("Submit Answer", type="primary")
        if submitted:
            st.session_state.user_answers[current_q] = user_answer
            st.session_state.last_user_answer = user_answer
            st.session_state.show_feedback = True
            st.rerun()

def show_answer_feedback(question_data, user_answer, question_index):
    correct_answer = question_data['correct_answer']
    is_correct = user_answer == correct_answer
    st.markdown("---")
    if is_correct:
        st.success("✅ **That's correct!**")
    else:
        st.error("❌ **That's incorrect.**")
    st.info(f"**Correct Answer:** {correct_answer}) {question_data['options'][correct_answer]}")
    st.markdown("**Explanation:**")
    st.markdown(question_data['explanation'])
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Next Question", type="primary", key="next_btn"):
            st.session_state.current_question += 1
            st.session_state.show_feedback = False
            st.rerun()
    with col1:
        if st.button("Back to Question", key="back_btn"):
            st.session_state.show_feedback = False
            st.rerun()

def show_results_page():
    st.header("📊 Quiz Results")
    mcqs = st.session_state.mcqs
    user_answers = st.session_state.user_answers
    correct_count = 0
    for i, question_data in enumerate(mcqs):
        if user_answers.get(i) == question_data['correct_answer']:
            correct_count += 1
    score_percentage = (correct_count / len(mcqs)) * 100
    st.metric("Final Score", f"{correct_count}/{len(mcqs)} ({score_percentage:.1f}%)")
    st.markdown("---")
    st.subheader("📝 Question Review")
    for i, question_data in enumerate(mcqs):
        user_answer = user_answers.get(i, "Not answered")
        correct_answer = question_data['correct_answer']
        is_correct = user_answer == correct_answer
        with st.expander(f"Question {i + 1}: {question_data['question'][:50]}..."):
            st.markdown(f"**Question:** {question_data['question']}")
            for option, text in question_data['options'].items():
                if option == user_answer and option == correct_answer:
                    st.markdown(f"✅ **{option}) {text}** (Your answer - Correct!)")
                elif option == user_answer:
                    st.markdown(f"❌ **{option}) {text}** (Your answer - Incorrect)")
                elif option == correct_answer:
                    st.markdown(f"✅ **{option}) {text}** (Correct answer)")
                else:
                    st.markdown(f"{option}) {text}")
            st.markdown(f"**Explanation:** {question_data['explanation']}")
    st.markdown("---")
    if st.button("🔄 Generate New Quiz", type="primary", key="newquiz_btn"):
        st.session_state.mcqs = None
        st.session_state.current_question = 0
        st.session_state.user_answers = {}
        st.session_state.quiz_completed = False
        st.session_state.show_feedback = False
        st.session_state.last_user_answer = None
        st.rerun()

if __name__ == "__main__":
    main() 