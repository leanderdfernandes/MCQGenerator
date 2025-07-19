import streamlit as st
import json
import os
from filelock import FileLock

# CSS for consistent styling
st.markdown(
    """
    <style>
    body, .stApp, .main .block-container {
        background-color: #F7FAFC !important;
    }
    .stForm, .stExpander, .stMetric {
        background-color: #FFFFFF !important;
        border-radius: 12px !important;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06) !important;
        border: 1px solid #E2E8F0 !important;
    }
    .stMarkdown, .stText, p, div, span, label, .stCaption, .stMetricLabel {
        color: #22223B !important;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #22223B !important;
        font-weight: 600;
    }
    .stButton > button {
        background-color: #43A363 !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.2s cubic-bezier(.4,0,.2,1) !important;
        box-shadow: 0 2px 8px rgba(67, 163, 99, 0.10) !important;
    }
    .stButton > button:hover {
        background-color: #388752 !important;
    }
    .stButton > button:active {
        background-color: #2E6B4B !important;
    }
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
    .stTextInput input, .stTextArea textarea {
        background-color: #FFFFFF !important;
        color: #22223B !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 0.75rem !important;
    }
    .stTextInput input:focus, .stTextArea textarea:focus {
        border-color: #43A363 !important;
        box-shadow: 0 0 0 3px rgba(67, 163, 99, 0.10) !important;
    }
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
        accent-color: #B8EFC6 !important;
        background-color: #E9F7F0 !important;
    }
    .stRadio input[type="radio"]:checked {
        accent-color: #43A363 !important;
        background-color: #DFF3E8 !important;
    }
    .stProgress > div > div {
        background-color: #43A363 !important;
    }
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
    </style>
    """,
    unsafe_allow_html=True
)

def load_tickets():
    """Load exit tickets from JSON file"""
    data_dir = "data"
    data_file = os.path.join(data_dir, "exit_tickets.json")
    lock_file = f"{data_file}.lock"
    
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    
    if not os.path.exists(data_file):
        with FileLock(lock_file):
            with open(data_file, 'w') as f:
                json.dump({"tickets": {}}, f)
    
    with FileLock(lock_file):
        with open(data_file, 'r') as f:
            return json.load(f)

def save_submission(ticket_id, submission):
    """Save a student submission to JSON file"""
    data_file = os.path.join("data", "exit_tickets.json")
    lock_file = f"{data_file}.lock"
    
    with FileLock(lock_file):
        data = load_tickets()
        if ticket_id in data["tickets"]:
            # Overwrite existing submission for same student name
            submissions = data["tickets"][ticket_id]["submissions"]
            submissions = [s for s in submissions if s["student_name"] != submission["student_name"]]
            submissions.append(submission)
            data["tickets"][ticket_id]["submissions"] = submissions
            with open(data_file, 'w') as f:
                json.dump(data, f, indent=2)

st.title("🎓 Student Exit Ticket")

# Initialize session state
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
if 'student_name' not in st.session_state:
    st.session_state.student_name = ""

# Get ticket_id from query parameters
query_params = st.query_params
ticket_id = query_params.get("ticket_id", None)

if not ticket_id:
    st.error("No ticket ID provided. Please use a valid exit ticket link.")
    st.stop()

# Load ticket data
data = load_tickets()
if ticket_id not in data["tickets"]:
    st.error("Invalid ticket ID. Please check the link.")
    st.stop()

ticket = data["tickets"][ticket_id]
mcqs = ticket["questions"]
ticket_name = ticket["name"]

# Name input
if not st.session_state.student_name:
    st.header(f"📝 {ticket_name}")
    with st.form("name_form"):
        student_name = st.text_input("Enter Your Name", placeholder="e.g., John Doe")
        if st.form_submit_button("Start Test"):
            if not student_name.strip():
                st.error("Please enter your name.")
            else:
                st.session_state.student_name = student_name.strip()
                st.rerun()
    st.stop()

# Quiz interface
if not st.session_state.quiz_completed:
    st.header(f"📝 {ticket_name}")
    current_q = st.session_state.current_question
    
    if current_q >= len(mcqs):
        # Calculate score and save submission
        submission = {
            "student_name": st.session_state.student_name,
            "answers": st.session_state.user_answers,
            "correctness": {},
            "score": 0
        }
        for i, question_data in enumerate(mcqs):
            is_correct = st.session_state.user_answers.get(str(i)) == question_data["correct_answer"]
            submission["correctness"][str(i)] = is_correct
            if is_correct:
                submission["score"] += 1
        save_submission(ticket_id, submission)
        st.session_state.quiz_completed = True
        st.rerun()
    
    progress = (current_q + 1) / len(mcqs)
    st.progress(progress)
    st.caption(f"Question {current_q + 1} of {len(mcqs)}")
    
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
        submitted = st.form_submit_button("Submit Answer")
        if submitted:
            st.session_state.user_answers[str(current_q)] = user_answer
            st.session_state.last_user_answer = user_answer
            st.session_state.show_feedback = True
            st.rerun()
    
    if st.session_state.show_feedback:
        correct_answer = question_data['correct_answer']
        is_correct = st.session_state.last_user_answer == correct_answer
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
            if st.button("Next Question", key="next_btn"):
                st.session_state.current_question += 1
                st.session_state.show_feedback = False
                st.rerun()
        with col1:
            if st.button("Back to Question", key="back_btn"):
                st.session_state.show_feedback = False
                st.rerun()

else:
    st.header(f"📊 Results for {ticket_name}")
    correct_count = sum(1 for i, q in enumerate(mcqs) if st.session_state.user_answers.get(str(i)) == q["correct_answer"])
    score_percentage = (correct_count / len(mcqs)) * 100
    st.metric("Your Score", f"{correct_count}/{len(mcqs)} ({score_percentage:.1f}%)")
    
    st.markdown("---")
    st.subheader("📝 Question Review")
    for i, question_data in enumerate(mcqs):
        user_answer = st.session_state.user_answers.get(str(i), "Not answered")
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
    st.success("Your answers have been submitted. Thank you!")
