import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# App Configuration
APP_TITLE = "🎓 Engineering MCQ Generator"
APP_ICON = "🎓"
PAGE_LAYOUT = "wide"

# Quiz Configuration
DEFAULT_QUESTIONS_COUNT = 3

# UI Configuration
QUESTION_HEIGHT = 200
INSTRUCTIONS_HEIGHT = 100 