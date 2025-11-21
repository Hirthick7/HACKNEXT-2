# 🎓 AI Learning Copilot — Adaptive 30-Day Personalized Study Planner

An intelligent learning web app built using *Flask, HTML, CSS, and JavaScript*.  
It analyzes a student's knowledge level and learning style, then automatically generates a *personalized 30-day curriculum* with topics, links, problems, and explanations.

The system also tracks progress and provides an interactive dashboard with a day-by-day checklist.

---

# 🚀 Features

## ✅ 1. Assessment Engine
- 10-question quiz  
- Calculates student score (/100)  
- Detects learning style (Visual, Reading, Hands-on, etc.)  
- Adjusts curriculum difficulty automatically  

## ✅ 2. AI-Generated 30-Day Curriculum
Each study day contains:
- 📌 Topic  
- 🔗 Learning link  
- 📝 Practice problem  
- 📘 Explanation  
- ✔ Progress tracking  

## ✅ 3. Dashboard & Progress Tracking
- Colorful 30-day grid  
- Completed days show ✓  
- “Mark Complete” button updates via AJAX  
- Auto reload after completion  

## ✅ 4. Beautiful UI
- Fully responsive  
- Clean card layout  
- No Jinja errors  
- Supports bright and animated themes  

---

# 🛠 Tech Stack

### *Backend*
- Python 3  
- Flask  

### *Frontend*
- HTML5  
- CSS3  
- JavaScript  

### *Template Engine*
- Jinja2  

### *Additional*
- AJAX (for progress updates)

---


# 📂 Folder Structure

learning_copilot/
│
├── app.py
├── requirements.txt
│
├── templates/
│ ├── base.html
│ ├── index.html
│ ├── assessment.html
│ ├── dashboard.html
│
└── static/
├── css/
│ └── styles.css
└── js/
└── script.js

---

## ▶ How to Run the Project

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt

requirements:
Flask==3.0.0
Jinja2==3.1.2
itsdangerous==2.1.2
Werkzeug==3.0.0
click==8.1.7
