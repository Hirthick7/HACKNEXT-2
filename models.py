# models.py - Data models for MongoDB
from datetime import datetime

# User Assessment Model
ASSESSMENT_MODEL = {
    "user_id": str,  # Generated UUID or session-based
    "subject": str,  # e.g., "Calculus"
    "prior_knowledge_score": int,  # 0-100
    "learning_style": str,  # "Visual", "Auditory", etc.
    "quiz_responses": list,  # List of answers
    "timestamp": datetime
}

# Curriculum Model (30-day plan)
CURRICULUM_MODEL = {
    "user_id": str,
    "subject": str,
    "days": list,  # List of 30 dicts: {"day": 1, "topics": [...], "links": [...], "problems": [...], "explanations": [...]}
    "generated_at": datetime,
    "progress": dict  # {"day": completed status}
}