from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from dotenv import load_dotenv
import google.generativeai as genai
import os
from difflib import SequenceMatcher
from insert_contact import admin_contact

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# -----------------------------
# Connect to MongoDB
# -----------------------------
client = MongoClient(MONGO_URL)
db = client["chatbot_db"]
faqs = db["faqs"]
contacts = db["contacts"]

# -----------------------------
# Configure Gemini
# -----------------------------
genai.configure(api_key=GEMINI_API_KEY)

# -----------------------------
# Ask Gemini (AI)
# -----------------------------
def ask_gemini(message):
    """Ask Gemini, but force it to stay within Global Academy of Technology context."""
    try:
        print("💬 Sending to Gemini:", message)
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        # ✅ Strong contextual prompt
        context = (
            "You are the official AI assistant for Global Academy of Technology, Bangalore, Karnataka. "
            "Always assume the user is asking about this college, even if they don't mention its name. "
            "If the question is not related to the college, "
            "respond only with this exact message: "
            f"'Sorry, I can only answer queries related to Global Academy of Technology. "
            f"Please contact {admin_contact['name']} at {admin_contact['email']}.'\n\n"
            f"Question: {message}"
        )

        response = model.generate_content(context)
        return response.text.strip()
    except Exception as e:
        print("⚠️ Gemini API error:", e)
        return "Sorry, I'm unable to get an answer from AI right now."

# -----------------------------
# Detect college-related queries
# -----------------------------
def is_college_related(question: str):
    college_keywords = [
        "college", "admission", "fee", "course", "department", "faculty",
        "placement", "exam", "result", "principal", "library", "hostel",
        "hod", "infrastructure", "attendance", "student", "syllabus",
        "academic", "canteen", "transport", "scholarship", "campus",
        "mba", "b.e", "engineering", "gate", "mechanical", "computer science"
    ]
    q = question.lower()
    return any(word in q for word in college_keywords)

# -----------------------------
# Fuzzy FAQ Matching
# -----------------------------
def get_best_faq_match(user_question):
    """Finds the most similar FAQ from MongoDB based on text similarity."""
    user_q = user_question.lower()
    faqs_list = list(faqs.find({}))
    best_match = None
    highest_similarity = 0.0

    for faq in faqs_list:
        stored_q = faq["question"].lower()
        similarity = SequenceMatcher(None, user_q, stored_q).ratio()
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_match = faq

    if highest_similarity >= 0.75:  # adjust threshold if needed
        print(f"🧩 Matched FAQ with {round(highest_similarity * 100, 2)}% similarity")
        return best_match
    return None

# -----------------------------
# Chat Logic
# -----------------------------
def get_response(question):
    try:
        # ✅ Step 1: Check for close match in MongoDB
        faq = get_best_faq_match(question)
        if faq:
            return faq["answer"]

        # ✅ Step 2: If it’s college-related, ask Gemini
        if is_college_related(question):
            return ask_gemini(question)

        # ✅ Step 3: If not college-related → contact admin
        return (
            f"Sorry, I can only answer queries related to Global Academy of Technology. "
            f"Please contact {admin_contact['name']} at {admin_contact['email']}."
        )

    except Exception as e:
        print("⚠️ Error in get_response:", e)
        return (
            f"Sorry, something went wrong. Please contact "
            f"{admin_contact['name']} at {admin_contact['email']}."
        )

# -----------------------------
# FastAPI Setup
# -----------------------------
app = FastAPI(title="College Chatbot API")

# ✅ Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # replace "*" with "http://localhost:5173" for frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# API Input Model
# -----------------------------
class ChatInput(BaseModel):
    user_message: str

# -----------------------------
# Main Chat Endpoint
# -----------------------------
@app.post("/chat")
async def chat(input: ChatInput):
    """Main chat endpoint"""
    reply = get_response(input.user_message)
    return {"response": reply}
