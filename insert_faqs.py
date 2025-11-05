from pymongo import MongoClient
import certifi
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()
MONGO_URL = os.getenv("MONGO_URL")

# Connect to MongoDB
client = MongoClient(MONGO_URL, tlsCAFile=certifi.where())
db = client["chatbot_db"]
faqs = db["faqs"]

# Clear old FAQs (optional)
faqs.delete_many({})

# -----------------------------
# GAT FAQs Dataset
# -----------------------------
faq_data = [
    {"question": "When was GAT established?", "answer": "Global Academy of Technology (GAT) was established in 2001 under the National Education Foundation (NEF)."},
    {"question": "Where is GAT located?", "answer": "GAT is located at Aditya Layout, Rajarajeshwari Nagar, Bengaluru, Karnataka – 560098."},
    {"question": "What kind of institution is GAT?", "answer": "GAT is an autonomous private engineering and management college affiliated with VTU, Belagavi."},
    {"question": "Is GAT NAAC accredited?", "answer": "Yes, GAT is NAAC accredited with Grade 'A'."},
    {"question": "Which entrance exams are accepted for admission?", "answer": "GAT accepts KCET, COMEDK UGET, and management quota admissions."},

    {"question": "What is the minimum attendance required?", "answer": "Students must have at least 85% attendance in each subject to appear for semester exams."},
    {"question": "Are there bridge courses for new students?", "answer": "Yes, departments conduct bridge and induction programs for first-year students."},
    {"question": "How is the teaching quality at GAT?", "answer": "GAT faculty are supportive, approachable, and focus on conceptual understanding."},
    {"question": "Is there continuous assessment or only final exams?", "answer": "Grades are based on internal tests, lab work, and end-semester exams."},
    {"question": "Are there certification courses?", "answer": "Yes, each department offers short-term certification and value-added programs."},

    {"question": "What facilities are available on campus?", "answer": "The campus has smart classrooms, advanced labs, WiFi, library, and research centers."},
    {"question": "Is there a gym or sports facility?", "answer": "Yes, there’s a gym, cricket & football grounds, volleyball & basketball courts, and indoor games."},
    {"question": "Is the campus WiFi enabled?", "answer": "Yes, high-speed WiFi is available throughout the campus and hostels."},
    {"question": "How is the library at GAT?", "answer": "The library houses thousands of books, e-resources, and a large reading hall."},
    {"question": "Is there a canteen on campus?", "answer": "Yes, the canteen serves hygienic vegetarian meals, snacks, and beverages."},

    {"question": "Are hostels available for both boys and girls?", "answer": "Yes, separate hostels for boys and girls are available within the campus."},
    {"question": "What are the hostel facilities?", "answer": "Hostels provide WiFi, mess, laundry, study tables, and 24x7 security."},
    {"question": "What is the hostel fee?", "answer": "Hostel fees are around ₹80,000 per year depending on sharing and facilities."},
    {"question": "How to apply for hostel accommodation?", "answer": "Hostel registration can be done online or during the admission process."},
    {"question": "Is outside food delivery allowed in hostels?", "answer": "Yes, within permitted hours and under campus rules."},

    {"question": "What are the main student clubs at GAT?", "answer": "Each department has clubs — CSE has IT Virtuoso, ECE has E-Spectrum, etc."},
    {"question": "Does GAT organize fests?", "answer": "Yes, annual events like GAT Utsav, Techno-Cultural Fest, and Innovation Day are organized."},
    {"question": "Are there entrepreneurship or innovation cells?", "answer": "Yes, GAT has an IEDC and Startup Incubation support system."},
    {"question": "How to join clubs or activities?", "answer": "Students can join clubs at the beginning of each semester via department announcements."},
    {"question": "Are there volunteering opportunities?", "answer": "Yes, through NSS, NCC, and social outreach programs."},

    {"question": "When do students start internships?", "answer": "Usually from 3rd year onwards, depending on the department."},
    {"question": "Are internships mandatory?", "answer": "Yes, one internship is mandatory before final year."},
    {"question": "Does the college help with placements?", "answer": "Yes, the Placement Cell conducts drives and provides training sessions."},
    {"question": "Which companies visit GAT for recruitment?", "answer": "Infosys, TCS, Wipro, Accenture, Amazon, and others."},
    {"question": "What are the highest and average packages?", "answer": "Highest: ₹22 LPA; Average: ₹5 LPA."},

    {"question": "Is there a student counselling system?", "answer": "Yes, each student is assigned a faculty mentor for guidance."},
    {"question": "Is there an anti-ragging cell?", "answer": "Yes, GAT has an Anti-Ragging Committee and Grievance Cell."},
    {"question": "Is medical help available on campus?", "answer": "Yes, a medical room with a doctor-on-call facility is available."},
    {"question": "Are scholarships available?", "answer": "Yes, both government and private scholarships are available."},
    {"question": "Is transport available for students?", "answer": "Yes, buses operate across major routes in Bengaluru."},

    {"question": "How are internal marks calculated?", "answer": "Through class tests, assignments, and attendance."},
    {"question": "What is the passing grade?", "answer": "Students need at least 40% overall (internal + external)."},
    {"question": "When are semester exams held?", "answer": "Odd semester in December and even semester in June."},
    {"question": "How to check results?", "answer": "Results are available on the college or VTU website."},
    {"question": "Are supplementary exams conducted?", "answer": "Yes, for students with backlogs."},

    {"question": "Does GAT have an alumni association?", "answer": "Yes, alumni actively support mentoring and placements."},
    {"question": "Are alumni involved in mentoring?", "answer": "Yes, alumni deliver lectures and help with career guidance."},
    {"question": "What are typical career paths?", "answer": "Students work in IT, core industries, startups, or pursue higher studies."},
    {"question": "Does GAT support GATE or GRE preparation?", "answer": "Yes, training sessions and workshops are organized."},
    {"question": "What percentage of students get placed?", "answer": "Around 85–90% of eligible students get placed every year."},

    {"question": "How is the induction program for first-year students?", "answer": "A week-long orientation helps students adapt to college culture."},
    {"question": "Can first-year students join clubs?", "answer": "Yes, they are encouraged to join and participate."},
    {"question": "Are mobile phones allowed in class?", "answer": "No, unless used for academic purposes."},
    {"question": "Is there ragging on campus?", "answer": "Strictly no. The campus is ragging-free and CCTV monitored."},
    {"question": "Who to contact for academic issues?", "answer": "Students can contact their HOD or faculty advisor."},

    {"question": "Who is the HOD of Computer Science Engineering?", "answer": "Dr. Kumaraswamy S. is the HOD of the CSE Department."},
    {"question": "Who is the HOD of CSE AI and ML?", "answer": "Dr. R. Chandramma is the HOD of the CSE (AI & ML) Department."},
    {"question": "Who is the HOD of Information Science?", "answer": "Dr. Kiran Y. C. is the HOD of the ISE Department."},
    {"question": "Who is the HOD of Electronics and Communication?", "answer": "Dr. Madhavi Mallam is the HOD of the ECE Department."},
    {"question": "Who is the HOD of Electrical Engineering?", "answer": "Dr. Deepika Masand is the HOD of the EEE Department."},
    {"question": "Who is the HOD of Mechanical Engineering?", "answer": "Dr. Bharat Vinjamuri is the HOD of the Mechanical Department."},
    {"question": "Who is the HOD of Civil Engineering?", "answer": "Dr. Allamaprabhu Kamatagi is the HOD of the Civil Engineering Department."},
    {"question": "Who is the HOD of Mathematics?", "answer": "Dr. Rupa K is the HOD of the Department of Mathematics."},
    {"question": "Who is the HOD of MBA Department?", "answer": "Dr. Sanjeev Kumar Thalari is the HOD of Management Studies (MBA)."},
]

# Insert all FAQs
faqs.insert_many(faq_data)
print("GAT FAQs inserted successfully!")
