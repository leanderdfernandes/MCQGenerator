import streamlit as st

st.set_page_config(page_title="MCQ Generator", page_icon="🎓", layout="wide")

st.title("🎓 Engineering MCQ Generator")
st.markdown("Choose your role to get started:")

col1, col2 = st.columns(2)
with col1:
    st.markdown("[**Faculty Portal**](./faculty)", unsafe_allow_html=True)
with col2:
    st.markdown("[**Student Portal**](./student)", unsafe_allow_html=True)

st.markdown(
    """
    <style>
    body, .stApp, .main .block-container {
        background-color: #F7FAFC !important;
    }
    .stMarkdown, .stText, p, div, span, label {
        color: #22223B !important;
    }
    h1, h2, h3 {
        color: #22223B !important;
        font-weight: 600;
    }
    a {
        color: #43A363 !important;
        text-decoration: underline !important;
        font-weight: 500;
    }
    a:hover {
        color: #388752 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
