import os
import random
from faker import Faker
import google.generativeai as genai
from sqlalchemy.orm import Session
from .models import Employee
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

fake = Faker()
departments = ["Engineering", "Sales", "Marketing", "HR", "Operations"]
themes = ["compensation", "burnout", "management", "growth", "culture"]

def analyze_feedback(feedback: str):
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt = f"""
        Analyze this employee feedback: "{feedback}"
        Return exactly two values separated by a comma:
        1. A sentiment score between 0.0 (extremely negative) and 1.0 (extremely positive).
        2. The primary theme (choose one: compensation, burnout, management, growth, culture, other).
        Example output: 0.2, burnout
        """
        response = model.generate_content(prompt)
        parts = response.text.strip().split(',')
        if len(parts) == 2:
            return float(parts[0].strip()), parts[1].strip().lower()
    except Exception as e:
        print(f"Gemini API error: {e}")
    
    return random.uniform(0.1, 0.9), random.choice(themes)

def generate_synthetic_data(db: Session, num_records: int = 50000):
    if db.query(Employee).count() > 0:
        return {"message": "Data already exists. Clear DB to regenerate."}

    for _ in range(num_records):
        feedback = fake.paragraph(nb_sentences=3)
        sentiment, theme = analyze_feedback(feedback)
        
        risk = "Low"
        if sentiment < 0.4:
            risk = "High" if random.random() > 0.3 else "Medium"
        elif sentiment < 0.7:
            risk = "Medium"

        emp = Employee(
            employee_id=f"EMP-{fake.unique.random_number(digits=5)}",
            department=random.choice(departments),
            tenure_years=round(random.uniform(0.5, 10.0), 1),
            salary=random.randint(50000, 150000),
            performance_score=round(random.uniform(1.0, 5.0), 1),
            survey_feedback=feedback,
            sentiment_score=sentiment,
            key_theme=theme,
            flight_risk=risk
        )
        db.add(emp)
        db.commit()
    return {"message": f"Successfully generated {num_records} employee records."}
