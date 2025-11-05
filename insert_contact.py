from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os

# -----------------------------
# Load environment variables
# -----------------------------
load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

# -----------------------------
# Connect to MongoDB
# -----------------------------
client = MongoClient(MONGO_URL, tlsCAFile=certifi.where())
db = client["chatbot_db"]
contacts = db["contacts"]

# -----------------------------
# Clear existing contacts
# -----------------------------
contacts.delete_many({})

# -----------------------------
# Admin Contact Data
# -----------------------------
admin_contact = {
    "name": "Mr. Rajesh Kumar",
    "email": "rajesh.kumar@gat.ac.in"
}

# -----------------------------
# Insert Admin Contact
# -----------------------------
contacts.insert_one(admin_contact)
print(" Admin contact inserted successfully!")
