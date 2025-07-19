import streamlit as st
import google.generativeai as genai
import json
import os
import uuid
from filelock import FileLock
import pandas as pd

# Load Google API key from secrets or environment variable
try:
    GOOGLE_API_KEY = st.secrets["api_keys"]["google_api_key"]
    FACULTY_PASSCODE = st.secrets["faculty_passcode"]
except KeyError:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    FACULTY_PASSCODE = os.getenv("FACULTY_PASSCODE", "faculty123")
    if not GOOGLE_API_KEY:
        st.error("Google API key not found. Please set it in Streamlit secrets or as an environment variable.")
        st.stop()

if GOOGLE_API_KEY:
    genai.configure(api_key=GOOGLE_API_KEY)

# System prompt for MCQ generation
SYSTEM_PROMPT = """You are a highly qualified MCQ generator for an engineering college lecture. Your task is to create exactly 3 multiple-choice questions (MCQs) based strictly on the list of topics provided from a lecture. These MCQs serve as exit ticket questions to assess students' understanding of core concepts.

Instructions:
- Only use concepts that were explicitly covered in the given topic list
- Do not include or infer content beyond the provided topics
- Focus on the most essential technical points, definitions, principles, or equations
- Each question must have one correct answer and three plausible distractors
- The correct answer must be factually accurate
- Write short, clear, and professional questions and answer choices
- Use standard engineering terminology and units
- Keep all technical details precise and concise
- You must strictly follow any additional instructions provided by the user below.
- The explanation for each question should be clear, educational, and consist of 2–5 sentences.

Output Format (JSON):
{
  "questions": [
    {
      "question": "Question text here?",
      "options": {
        "A": "Option A text",
        "B": "Option B text", 
        "C": "Option C text",
        "D": "Option D text"
      },
      "correct_answer": "C",
      "explanation": "Brief explanation of why this answer is correct (2-5 sentences)"
    }
  ]
}

Requirements:
- Return ONLY valid JSON format
- Ensure all questions are relevant to the provided topics
- Make explanations educational and clear (2-5 sentences)
- Use engineering-appropriate language and precision"""

def generate_mcqs(lecture_topics, ai_instructions):
    """Generate MCQs using Google AI Studio"""
    try:
        prompt = f"""{SYSTEM_PROMPT}

Lecture Topics:
{lecture_topics}

Additional Instructions:
{ai_instructions if ai_instructions.strip() else "No additional instructions provided."}

Please generate exactly 3 MCQs based on the above topics and instructions.
Return ONLY the JSON format as specified above."""
        
        model = genai.GenerativeModel('gemini-1.5-flash')  # Verify model name
        response = model.generate_content(prompt)
        
        response_text = response.text
        start_idx = response_text.find('{')
        end_idx = response_text.rfind('}') + 1
        json_str = response_text[start_idx:end_idx]
        mcqs = json.loads(json_str)
        return mcqs
    except json.JSONDecodeError as e:
        st.error(f"Error parsing AI response: {e}")
        st.text("Raw response:")
        st.text(response_text)
        return None
    except Exception as e:
        st.error(f"Error generating MCQs: {e}")
        return None

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

def save_ticket(ticket_id, ticket_data):
    """Save an exit ticket to JSON file"""
    data_file = os.path.join("data", "exit_tickets.json")
    lock_file = f"{data_file}.lock"
    
    with FileLock(lock_file):
        data = load_tickets()
        data["tickets"][ticket_id] = ticket_data
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)

# Initialize session state
if 'passcode_validated' not in st.session_state:
    st.session_state.passcode_validated = False
if 'ai_instructions_text' not in st.session_state:
    st.session_state.ai_instructions_text = ""

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
    .stSelectbox > div > div {
        background-color: #FFFFFF !important;
        border: 2px solid #E2E8F0 !important;
        border-radius: 8px !important;
        padding: 0.5rem !important;
        color: #22223B !important;
    }
    .stSelectbox > div > div:focus, .stSelectbox > div > div:hover {
        border-color: #43A363 !important;
        box-shadow: 0 0 0 3px rgba(67, 163, 99, 0.10) !important;
    }
    .stDataFrame, .stTable {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 8px !important;
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

st.title("🎓 Faculty Portal")

# Passcode validation
if not st.session_state.passcode_validated:
    st.header("🔐 Faculty Access")
    with st.form("passcode_form"):
        passcode = st.text_input("Enter Faculty Passcode", type="password")
        if st.form_submit_button("Submit"):
            if passcode == FACULTY_PASSCODE:
                st.session_state.passcode_validated = True
                st.rerun()
            else:
                st.error("Incorrect passcode. Please try again.")
    st.stop()

# Faculty interface
tab1, tab2 = st.tabs(["Create Exit Ticket", "View Results"])

with tab1:
    st.header("📝 Create Exit Ticket")
    with st.form("mcq_form"):
        ticket_name = st.text_input("Exit Ticket Name", placeholder="e.g., Lecture 1 Exit Ticket")
        lecture_topics = st.text_area(
            "📚 Lecture Topics & Summary",
            placeholder="Enter the main topics, concepts, and key points covered in your lecture...",
            height=200
        )
        st.caption("💡 Select a suggestion to append to the AI Instructions:")
        prompt_suggestions = [
            "(None)",
            "Focus on conceptual understanding",
            "Include at least one calculation-based question",
            "Emphasize real-world applications",
            "Ask about common misconceptions",
            "Include a question that requires critical thinking"
        ]
        selected_suggestion = st.selectbox(
            "Prompt Suggestions",
            prompt_suggestions,
            index=0,
            key="prompt_suggestion"
        )
        if selected_suggestion != "(None)":
            current = st.session_state.ai_instructions_text
            if selected_suggestion not in current:
                if current.strip():
                    st.session_state.ai_instructions_text = current.strip() + "\n" + selected_suggestion
                else:
                    st.session_state.ai_instructions_text = selected_suggestion
                st.session_state.prompt_suggestion = "(None)"
                st.rerun()
        
        ai_instructions = st.text_area(
            "🤖 AI Instructions (Optional)",
            value=st.session_state.ai_instructions_text,
            placeholder="Add specific instructions for question generation...",
            height=100
        )
        submitted = st.form_submit_button("🚀 Generate MCQs")
        
        if submitted:
            if not ticket_name.strip():
                st.error("Please enter an exit ticket name.")
            elif not lecture_topics.strip():
                st.error("Please enter lecture topics.")
            else:
                with st.spinner("Generating MCQs..."):
                    mcqs = generate_mcqs(lecture_topics, st.session_state.ai_instructions_text)
                    if mcqs and 'questions' in mcqs:
                        ticket_id = str(uuid.uuid4())
                        ticket_data = {
                            "name": ticket_name,
                            "questions": mcqs['questions'],
                            "submissions": []
                        }
                        save_ticket(ticket_id, ticket_data)
                        st.session_state.ai_instructions_text = ""
                        st.success("Exit ticket created!")
                        shareable_link = f"{st.secrets.get('app_url', 'http://localhost:8501')}/student?ticket_id={ticket_id}"
                        st.markdown(f"**Shareable Link for Students:** [{shareable_link}]({shareable_link})")
                        st.info("Copy this link and share it with students to take the exit ticket.")

with tab2:
    st.header("📊 View Results")
    data = load_tickets()
    ticket_ids = list(data["tickets"].keys())
    ticket_names = [data["tickets"][tid]["name"] for tid in ticket_ids]
    
    if not ticket_ids:
        st.info("No exit tickets available.")
    else:
        selected_ticket = st.selectbox("Select Exit Ticket", options=ticket_ids, format_func=lambda x: data["tickets"][x]["name"])
        submissions = data["tickets"][selected_ticket]["submissions"]
        
        if not submissions:
            st.info("No student submissions yet.")
        else:
            df_data = []
            for sub in submissions:
                row = {
                    "Student Name": sub["student_name"],
                    "Q1": f"{sub['answers']['0']} ({'Correct' if sub['correctness']['0'] else 'Incorrect'})",
                    "Q2": f"{sub['answers']['1']} ({'Correct' if sub['correctness']['1'] else 'Incorrect'})",
                    "Q3": f"{sub['answers']['2']} ({'Correct' if sub['correctness']['2'] else 'Incorrect'})",
                    "Score": f"{sub['score']}/3"
                }
                df_data.append(row)
            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)
